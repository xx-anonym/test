import { NextResponse, type NextRequest } from 'next/server';
import { CHUNK_SIZE } from '@/lib/constants';
import { errorResponse } from '@/lib/http';
import { getStream, isVideoId } from '@/lib/youtube';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;

function fetchRange(url: string, start: number, end: number): Promise<Response> {
  return fetch(`${url}&range=${start}-${end}`, { signal: AbortSignal.timeout(45_000) });
}

export async function GET(req: NextRequest) {
  const params = req.nextUrl.searchParams;
  const id = params.get('v') ?? '';
  const itag = Number(params.get('itag'));
  const start = Number(params.get('start'));
  if (!isVideoId(id) || !Number.isInteger(itag) || !Number.isInteger(start) || start < 0) {
    return NextResponse.json({ error: 'Ungültige Anfrage.' }, { status: 400 });
  }

  try {
    let source = await getStream(id, itag);
    if (start >= source.size) {
      return NextResponse.json({ error: 'Bereich außerhalb der Datei.' }, { status: 416 });
    }
    const end = Math.min(start + CHUNK_SIZE, source.size) - 1;

    let upstream = await fetchRange(source.url, start, end);
    if (!upstream.ok) {
      // Cached URL expired or belongs to another instance's IP: resolve again.
      await upstream.body?.cancel();
      source = await getStream(id, itag, true);
      upstream = await fetchRange(source.url, start, end);
    }
    if (!upstream.ok || !upstream.body) {
      await upstream.body?.cancel();
      return NextResponse.json({ error: `YouTube-Server antwortete mit ${upstream.status}.` }, { status: 502 });
    }

    const headers = new Headers({
      'Content-Type': 'application/octet-stream',
      'Cache-Control': 'no-store',
      'X-Total-Size': String(source.size),
      'X-Range-End': String(end),
    });
    const length = upstream.headers.get('content-length');
    if (length) headers.set('Content-Length', length);
    return new Response(upstream.body, { headers });
  } catch (err) {
    return errorResponse(err);
  }
}
