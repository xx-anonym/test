import { Innertube, Platform, type Misc, type Types } from 'youtubei.js';

// YouTube obfuscates stream URLs with functions from its player script.
// youtubei.js extracts those functions; we only have to run them.
Platform.shim.eval = (data: Types.BuildScriptResult, env: Record<string, Types.VMPrimative>) => {
  const args = [env.n, env.sp, env.sig].map((v) => JSON.stringify(typeof v === 'string' ? v : ''));
  return new Function(`${data.output}\nreturn process(${args.join(', ')});`)();
};

// Clients tried in order. WEB/ANDROID currently only return SABR streams
// without plain URLs, so start with the ones that still hand out direct links.
const CLIENTS: Types.InnerTubeClient[] = ['MWEB', 'IOS', 'TV', 'ANDROID_VR'];

// Videos longer than this are rejected outright.
const MAX_DURATION_SECONDS = 3 * 60 * 60;

export interface AudioFormat {
  itag: number;
  mimeType: string;
  bitrate: number;
  size: number;
}

export interface VideoDetails {
  id: string;
  title: string;
  author: string;
  duration: number;
  formats: AudioFormat[];
}

export class UserError extends Error {
  constructor(
    message: string,
    public status = 400,
  ) {
    super(message);
  }
}

const ID_PATTERN = /^[A-Za-z0-9_-]{11}$/;

export function isVideoId(value: string): boolean {
  return ID_PATTERN.test(value);
}

/** Accepts watch/shorts/embed/live/youtu.be/music links or a bare video ID. */
export function parseVideoId(input: string): string | null {
  const value = input.trim();
  if (isVideoId(value)) return value;

  let url: URL;
  try {
    url = new URL(/^https?:\/\//i.test(value) ? value : `https://${value}`);
  } catch {
    return null;
  }

  const host = url.hostname.toLowerCase().replace(/^www\./, '');
  let candidate: string | null = null;
  if (host === 'youtu.be') {
    candidate = url.pathname.split('/')[1] ?? null;
  } else if (host === 'youtube.com' || host.endsWith('.youtube.com') || host === 'youtube-nocookie.com') {
    candidate = url.searchParams.get('v');
    if (!candidate) {
      const match = url.pathname.match(/^\/(?:shorts|embed|live|v)\/([^/?#]+)/);
      candidate = match?.[1] ?? null;
    }
  }
  return candidate && isVideoId(candidate) ? candidate : null;
}

let innertube: Promise<Innertube> | null = null;

function getInnertube(): Promise<Innertube> {
  innertube ??= Innertube.create({ retrieve_player: true, generate_session_locally: true }).catch((err) => {
    innertube = null;
    throw err;
  });
  return innertube;
}

/** Audio-only formats of the original track, one per itag. */
function audioFormats(formats: Misc.Format[]): Misc.Format[] {
  const audio = formats.filter((f) => f.has_audio && !f.has_video && f.content_length && !f.is_drc && !f.is_type_otf);
  const original = audio.filter((f) => f.is_original);
  const plain = audio.filter((f) => !f.is_dubbed && !f.is_auto_dubbed && !f.is_descriptive && !f.is_secondary);
  const preferred = original.length ? original : plain.length ? plain : audio;

  const byItag = new Map<number, Misc.Format>();
  for (const f of preferred) if (!byItag.has(f.itag)) byItag.set(f.itag, f);
  return [...byItag.values()].sort((a, b) => b.bitrate - a.bitrate);
}

interface Entry {
  details: VideoDetails;
  formats: Map<number, Misc.Format>;
  urls: Map<number, string>;
  expiresAt: number;
}

// Stream URLs are bound to the IP that requested them, so they are only
// reused within the same (warm) function instance.
const cache = new Map<string, Entry>();
const CACHE_TTL_MS = 60 * 60 * 1000;

async function resolve(id: string): Promise<Entry> {
  const yt = await getInnertube();
  let lastReason = '';

  for (const client of CLIENTS) {
    let info;
    try {
      info = await yt.getBasicInfo(id, { client });
    } catch (err) {
      lastReason = err instanceof Error ? err.message : String(err);
      continue;
    }

    const status = info.playability_status?.status;
    if (status !== 'OK') {
      lastReason = info.playability_status?.reason || status || 'unbekannt';
      continue;
    }

    const duration = info.basic_info.duration ?? 0;
    if (info.basic_info.is_live) throw new UserError('Livestreams werden nicht unterstützt.');
    if (duration > MAX_DURATION_SECONDS) throw new UserError('Das Video ist zu lang (maximal 3 Stunden).');

    const formats = audioFormats(info.streaming_data?.adaptive_formats ?? []);
    // Formats without a direct URL (or cipher) are SABR-only; try the next client.
    if (!formats.some((f) => f.url || f.signature_cipher || f.cipher)) {
      lastReason = 'Keine direkt ladbare Audiospur gefunden';
      continue;
    }

    return {
      details: {
        id,
        title: info.basic_info.title ?? id,
        author: (info.basic_info.author ?? '').replace(/ - Topic$/, ''),
        duration,
        formats: formats.map((f) => ({
          itag: f.itag,
          mimeType: f.mime_type,
          bitrate: f.bitrate,
          size: Number(f.content_length),
        })),
      },
      formats: new Map(formats.map((f) => [f.itag, f])),
      urls: new Map(),
      expiresAt: Date.now() + CACHE_TTL_MS,
    };
  }

  if (/not a bot/i.test(lastReason)) {
    throw new UserError(
      'YouTube blockiert gerade Anfragen von diesem Server (Bot-Schutz). Bitte später erneut versuchen.',
      503,
    );
  }
  throw new UserError(`YouTube hat das Video nicht freigegeben: ${lastReason}`, 502);
}

async function getEntry(id: string, fresh = false): Promise<Entry> {
  const hit = cache.get(id);
  if (hit && !fresh && hit.expiresAt > Date.now()) return hit;

  const entry = await resolve(id);
  cache.set(id, entry);
  if (cache.size > 100) {
    for (const [key, value] of cache) if (value.expiresAt <= Date.now()) cache.delete(key);
  }
  return entry;
}

export async function getVideoDetails(id: string): Promise<VideoDetails> {
  return (await getEntry(id)).details;
}

export async function getStream(id: string, itag: number, fresh = false): Promise<{ url: string; size: number }> {
  const entry = await getEntry(id, fresh);
  const format = entry.formats.get(itag);
  if (!format) throw new UserError('Dieses Audioformat ist für das Video nicht verfügbar.', 404);

  let url = entry.urls.get(itag);
  if (!url) {
    const yt = await getInnertube();
    try {
      url = await format.decipher(yt.session.player);
    } catch {
      throw new UserError('Die Stream-Adresse konnte nicht entschlüsselt werden.', 502);
    }
    entry.urls.set(itag, url);
  }
  return { url, size: Number(format.content_length) };
}
