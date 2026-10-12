import { CHUNK_SIZE } from './constants';
import { buildId3 } from './id3';

export interface AudioFormat {
  itag: number;
  mimeType: string;
  bitrate: number;
  size: number;
}

export interface VideoInfo {
  id: string;
  title: string;
  author: string;
  duration: number;
  formats: AudioFormat[];
}

export type Stage = 'download' | 'decode' | 'encode';
export type ProgressFn = (stage: Stage, fraction: number | null) => void;

class HttpError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}

async function readError(res: Response): Promise<HttpError> {
  let message = `Serverfehler (${res.status})`;
  try {
    const body = await res.json();
    if (typeof body?.error === 'string') message = body.error;
  } catch {
    // keep the generic message
  }
  return new HttpError(message, res.status);
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/**
 * Picks the stream the browser can decode: AAC works almost everywhere
 * (Safari included), Opus covers Chromium builds without proprietary codecs.
 */
export function pickFormat(formats: AudioFormat[]): AudioFormat | undefined {
  const probe = typeof Audio === 'undefined' ? null : new Audio();
  const canPlay = (f: AudioFormat) => probe !== null && probe.canPlayType(f.mimeType) !== '';
  const aac = formats.find((f) => f.itag === 140) ?? formats.find((f) => f.mimeType.includes('mp4a.40.2'));
  if (aac && canPlay(aac)) return aac;
  const opus = formats.find((f) => f.itag === 251) ?? formats.find((f) => f.mimeType.includes('opus'));
  if (opus && canPlay(opus)) return opus;
  return aac ?? opus ?? formats[0];
}

export function originalExtension(format: AudioFormat): string {
  return format.mimeType.startsWith('audio/webm') ? 'webm' : 'm4a';
}

export async function fetchInfo(url: string, signal?: AbortSignal): Promise<VideoInfo> {
  const res = await fetch(`/api/info?url=${encodeURIComponent(url)}`, { signal });
  if (!res.ok) throw await readError(res);
  return res.json();
}

async function fetchChunk(
  id: string,
  format: AudioFormat,
  start: number,
  signal: AbortSignal,
  onBytes: (delta: number) => void,
): Promise<Uint8Array> {
  const expected = Math.min(start + CHUNK_SIZE, format.size) - start;
  let lastError: unknown;

  for (let attempt = 0; attempt < 3; attempt++) {
    let received = 0;
    try {
      const res = await fetch(`/api/chunk?v=${id}&itag=${format.itag}&start=${start}`, { signal });
      if (!res.ok || !res.body) throw await readError(res);

      const buffer = new Uint8Array(expected);
      const reader = res.body.getReader();
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        if (received + value.length > expected) throw new Error('Unerwartet viele Daten empfangen.');
        buffer.set(value, received);
        received += value.length;
        onBytes(value.length);
      }
      if (received !== expected) throw new Error('Download unvollständig.');
      return buffer;
    } catch (err) {
      onBytes(-received);
      if (signal.aborted) throw err;
      if (err instanceof HttpError && err.status >= 400 && err.status < 500) throw err;
      lastError = err;
      await sleep(1000 * 2 ** attempt);
    }
  }
  throw lastError;
}

/** Downloads the original audio stream (usually AAC in an M4A container). */
export async function downloadAudio(
  id: string,
  format: AudioFormat,
  onProgress: ProgressFn,
  signal: AbortSignal,
): Promise<Blob> {
  const starts: number[] = [];
  for (let s = 0; s < format.size; s += CHUNK_SIZE) starts.push(s);

  const parts: Uint8Array[] = new Array(starts.length);
  let received = 0;
  let next = 0;
  onProgress('download', 0);

  const run = async () => {
    while (next < starts.length) {
      const index = next++;
      parts[index] = await fetchChunk(id, format, starts[index], signal, (delta) => {
        received += delta;
        onProgress('download', received / format.size);
      });
    }
  };
  await Promise.all(Array.from({ length: Math.min(3, starts.length) }, run));

  return new Blob(parts as BlobPart[], { type: format.mimeType.split(';')[0] });
}

async function decode(blob: Blob): Promise<AudioBuffer> {
  const data = await blob.arrayBuffer();
  // Resample to 44.1 kHz, a rate every MP3 player handles.
  const ctx = new OfflineAudioContext(2, 1, 44100);
  try {
    return await ctx.decodeAudioData(data);
  } catch {
    throw new Error('Die Audiospur konnte in diesem Browser nicht dekodiert werden.');
  }
}

async function encodeMp3(
  audio: AudioBuffer,
  kbps: number,
  onProgress: ProgressFn,
  signal: AbortSignal,
): Promise<Uint8Array[]> {
  const worker = new Worker(new URL('./mp3.worker.ts', import.meta.url), { type: 'module' });
  const call = (message: unknown, transfer: Transferable[] = []) =>
    new Promise<Uint8Array | undefined>((resolve, reject) => {
      worker.onmessage = (e) => (e.data.type === 'error' ? reject(new Error(e.data.message)) : resolve(e.data.data));
      worker.onerror = (e) => reject(new Error(e.message || 'MP3-Encoder abgestürzt.'));
      worker.postMessage(message, transfer);
    });

  try {
    const channels = Math.min(audio.numberOfChannels, 2);
    const left = audio.getChannelData(0);
    const right = channels > 1 ? audio.getChannelData(1) : undefined;
    const slice = audio.sampleRate * 5;
    const parts: Uint8Array[] = [];

    await call({ type: 'init', channels, sampleRate: audio.sampleRate, kbps });
    for (let i = 0; i < left.length; i += slice) {
      if (signal.aborted) throw new DOMException('Abgebrochen', 'AbortError');
      const l = left.slice(i, i + slice);
      const r = right?.slice(i, i + slice);
      const out = await call({ type: 'encode', left: l, right: r }, r ? [l.buffer, r.buffer] : [l.buffer]);
      if (out?.length) parts.push(out);
      onProgress('encode', Math.min(1, (i + slice) / left.length));
    }
    const tail = await call({ type: 'flush' });
    if (tail?.length) parts.push(tail);
    return parts;
  } finally {
    worker.terminate();
  }
}

async function fetchCover(id: string): Promise<{ mime: string; data: Uint8Array } | undefined> {
  for (const name of ['maxresdefault', 'mqdefault']) {
    try {
      const res = await fetch(`https://i.ytimg.com/vi/${id}/${name}.jpg`);
      if (res.ok) return { mime: 'image/jpeg', data: new Uint8Array(await res.arrayBuffer()) };
    } catch {
      // cover art is optional
    }
  }
  return undefined;
}

export async function convertToMp3(
  info: VideoInfo,
  source: Blob,
  kbps: number,
  onProgress: ProgressFn,
  signal: AbortSignal,
): Promise<Blob> {
  const cover = fetchCover(info.id);
  onProgress('decode', null);
  const audio = await decode(source);
  if (signal.aborted) throw new DOMException('Abgebrochen', 'AbortError');
  const frames = await encodeMp3(audio, kbps, onProgress, signal);
  const tag = buildId3({ title: info.title, artist: info.author, cover: await cover });
  return new Blob([tag, ...frames] as BlobPart[], { type: 'audio/mpeg' });
}

export function fileName(title: string, ext: string): string {
  const clean = title
    .replace(/[\\/:*?"<>|\u0000-\u001f]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 150);
  return `${clean || 'audio'}.${ext}`;
}
