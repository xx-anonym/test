import { NextResponse, type NextRequest } from 'next/server';
import { errorResponse } from '@/lib/http';
import { getVideoDetails, parseVideoId } from '@/lib/youtube';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 30;

export async function GET(req: NextRequest) {
  const id = parseVideoId(req.nextUrl.searchParams.get('url') ?? '');
  if (!id) {
    return NextResponse.json({ error: 'Bitte einen gültigen YouTube-Link eingeben.' }, { status: 400 });
  }

  try {
    const details = await getVideoDetails(id);
    return NextResponse.json(details, { headers: { 'Cache-Control': 'no-store' } });
  } catch (err) {
    return errorResponse(err);
  }
}
