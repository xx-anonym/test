// Minimal ID3v2.3 writer: title, artist and an optional cover image.

function utf16(text: string): Uint8Array {
  // Encoding byte 1 = UTF-16 with BOM (little endian).
  const out = new Uint8Array(3 + text.length * 2);
  out.set([1, 0xff, 0xfe]);
  for (let i = 0; i < text.length; i++) {
    const code = text.charCodeAt(i);
    out[3 + i * 2] = code & 0xff;
    out[4 + i * 2] = code >> 8;
  }
  return out;
}

function frame(id: string, body: Uint8Array): Uint8Array {
  const out = new Uint8Array(10 + body.length);
  for (let i = 0; i < 4; i++) out[i] = id.charCodeAt(i);
  new DataView(out.buffer).setUint32(4, body.length);
  out.set(body, 10);
  return out;
}

export interface Id3Fields {
  title: string;
  artist: string;
  cover?: { mime: string; data: Uint8Array };
}

export function buildId3({ title, artist, cover }: Id3Fields): Uint8Array {
  const frames = [frame('TIT2', utf16(title))];
  if (artist) frames.push(frame('TPE1', utf16(artist)));
  if (cover) {
    const mime = new TextEncoder().encode(cover.mime);
    // encoding (latin1), MIME, NUL, picture type 3 (front cover), empty description, data
    const body = new Uint8Array(mime.length + 4 + cover.data.length);
    body.set(mime, 1);
    body[mime.length + 2] = 3;
    body.set(cover.data, mime.length + 4);
    frames.push(frame('APIC', body));
  }

  const size = frames.reduce((n, f) => n + f.length, 0);
  const out = new Uint8Array(10 + size);
  out.set([0x49, 0x44, 0x33, 3, 0, 0]);
  // Tag size is "syncsafe": 7 bits per byte.
  out[6] = (size >> 21) & 0x7f;
  out[7] = (size >> 14) & 0x7f;
  out[8] = (size >> 7) & 0x7f;
  out[9] = size & 0x7f;
  let offset = 10;
  for (const f of frames) {
    out.set(f, offset);
    offset += f.length;
  }
  return out;
}
