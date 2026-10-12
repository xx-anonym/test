import { NextResponse } from 'next/server';
import { UserError } from './youtube';

export function errorResponse(err: unknown): NextResponse {
  if (err instanceof UserError) {
    return NextResponse.json({ error: err.message }, { status: err.status });
  }
  console.error(err);
  return NextResponse.json({ error: 'Interner Fehler. Bitte später erneut versuchen.' }, { status: 500 });
}
