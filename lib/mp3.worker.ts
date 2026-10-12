/// <reference lib="webworker" />
import { Mp3Encoder } from '@breezystack/lamejs';

type Request =
  | { type: 'init'; channels: number; sampleRate: number; kbps: number }
  | { type: 'encode'; left: Float32Array; right?: Float32Array }
  | { type: 'flush' };

// lame works on frames of 1152 samples.
const BLOCK = 1152;

let encoder: Mp3Encoder | null = null;

function toInt16(input: Float32Array): Int16Array {
  const out = new Int16Array(input.length);
  for (let i = 0; i < input.length; i++) {
    const s = Math.max(-1, Math.min(1, input[i]));
    out[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
  }
  return out;
}

function concat(parts: Uint8Array[]): Uint8Array {
  const out = new Uint8Array(parts.reduce((n, p) => n + p.length, 0));
  let offset = 0;
  for (const p of parts) {
    out.set(p, offset);
    offset += p.length;
  }
  return out;
}

function reply(data?: Uint8Array) {
  if (data) self.postMessage({ type: 'ok', data }, [data.buffer]);
  else self.postMessage({ type: 'ok' });
}

self.onmessage = (event: MessageEvent<Request>) => {
  const msg = event.data;
  try {
    if (msg.type === 'init') {
      encoder = new Mp3Encoder(msg.channels, msg.sampleRate, msg.kbps);
      reply();
      return;
    }
    if (!encoder) throw new Error('Encoder ist nicht initialisiert.');

    if (msg.type === 'encode') {
      const left = toInt16(msg.left);
      const right = msg.right ? toInt16(msg.right) : undefined;
      const parts: Uint8Array[] = [];
      for (let i = 0; i < left.length; i += BLOCK) {
        const out = encoder.encodeBuffer(left.subarray(i, i + BLOCK), right?.subarray(i, i + BLOCK));
        if (out.length) parts.push(out);
      }
      reply(concat(parts));
    } else {
      const out = new Uint8Array(encoder.flush());
      encoder = null;
      reply(out);
    }
  } catch (err) {
    self.postMessage({ type: 'error', message: err instanceof Error ? err.message : String(err) });
  }
};
