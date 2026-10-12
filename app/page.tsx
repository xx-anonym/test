'use client';

import { useEffect, useMemo, useRef, useState, type FormEvent } from 'react';
import { MP3_MAX_DURATION_SECONDS } from '@/lib/constants';
import {
  convertToMp3,
  downloadAudio,
  fetchInfo,
  fileName,
  originalExtension,
  pickFormat,
  type AudioFormat,
  type Stage,
  type VideoInfo,
} from '@/lib/convert';

type Format = '128' | '192' | '320' | 'original';

const MP3_FORMATS: { value: Format; label: string; hint: string }[] = [
  { value: '128', label: 'MP3 128', hint: 'klein' },
  { value: '192', label: 'MP3 192', hint: 'empfohlen' },
  { value: '320', label: 'MP3 320', hint: 'maximal' },
];

interface Job {
  stage: Stage | 'done';
  fraction: number | null;
}

interface Result {
  href: string;
  name: string;
  size: number;
}

function formatDuration(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const mm = h ? String(m).padStart(2, '0') : String(m);
  return `${h ? `${h}:` : ''}${mm}:${String(s).padStart(2, '0')}`;
}

function formatSize(bytes: number): string {
  return `${(bytes / 1024 / 1024).toLocaleString('de-DE', { maximumFractionDigits: 1 })} MB`;
}

function estimateSize(info: VideoInfo, source: AudioFormat, format: Format): number {
  return format === 'original' ? source.size : (info.duration * Number(format) * 1000) / 8;
}

function overallProgress(job: Job, format: Format): number {
  if (job.stage === 'done') return 1;
  if (format === 'original') return job.fraction ?? 0;
  if (job.stage === 'download') return (job.fraction ?? 0) * 0.55;
  if (job.stage === 'decode') return 0.6;
  return 0.6 + (job.fraction ?? 0) * 0.4;
}

function stageLabel(job: Job): string {
  const pct = job.fraction === null ? '' : ` ${Math.round(job.fraction * 100)} %`;
  switch (job.stage) {
    case 'download':
      return `Audio wird geladen …${pct}`;
    case 'decode':
      return 'Audio wird dekodiert …';
    case 'encode':
      return `MP3 wird erstellt …${pct}`;
    case 'done':
      return 'Fertig! Der Download wurde gestartet.';
  }
}

function saveFile(href: string, name: string) {
  const a = document.createElement('a');
  a.href = href;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
}

export default function Home() {
  const [url, setUrl] = useState('');
  const [info, setInfo] = useState<VideoInfo | null>(null);
  const [loadingInfo, setLoadingInfo] = useState(false);
  const [format, setFormat] = useState<Format>('192');
  const [job, setJob] = useState<Job | null>(null);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const sourceRef = useRef<{ key: string; blob: Blob } | null>(null);

  const audioFormat = useMemo(() => (info ? pickFormat(info.formats) : undefined), [info]);
  const originalExt = audioFormat ? originalExtension(audioFormat) : 'm4a';
  const mp3Allowed = !info || info.duration <= MP3_MAX_DURATION_SECONDS;
  const busy = job !== null && job.stage !== 'done';

  useEffect(() => {
    const initial = new URLSearchParams(window.location.search).get('url');
    if (initial) {
      setUrl(initial);
      void load(initial);
    }
    return () => abortRef.current?.abort();
  }, []);

  useEffect(() => {
    return () => {
      if (result) URL.revokeObjectURL(result.href);
    };
  }, [result]);

  async function load(value: string) {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setError(null);
    setInfo(null);
    setJob(null);
    setResult(null);
    sourceRef.current = null;
    setLoadingInfo(true);
    try {
      const next = await fetchInfo(value, controller.signal);
      setInfo(next);
      if (next.duration > MP3_MAX_DURATION_SECONDS) setFormat('original');
      else setFormat((f) => (f === 'original' ? '192' : f));
    } catch (err) {
      if (!controller.signal.aborted) setError(err instanceof Error ? err.message : String(err));
    } finally {
      if (abortRef.current === controller) setLoadingInfo(false);
    }
  }

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (url.trim()) void load(url);
  }

  async function start() {
    if (!info || !audioFormat) return;
    const controller = new AbortController();
    abortRef.current = controller;
    setError(null);
    setResult(null);

    const onProgress = (stage: Stage, fraction: number | null) => setJob({ stage, fraction });
    try {
      const key = `${info.id}:${audioFormat.itag}`;
      let source = sourceRef.current?.key === key ? sourceRef.current.blob : null;
      if (!source) {
        source = await downloadAudio(info.id, audioFormat, onProgress, controller.signal);
        sourceRef.current = { key, blob: source };
      }

      const output =
        format === 'original'
          ? source
          : await convertToMp3(info, source, Number(format), onProgress, controller.signal);
      const name = fileName(info.title, format === 'original' ? originalExt : 'mp3');
      const href = URL.createObjectURL(output);
      setResult({ href, name, size: output.size });
      setJob({ stage: 'done', fraction: 1 });
      saveFile(href, name);
    } catch (err) {
      setJob(null);
      if (!controller.signal.aborted) setError(err instanceof Error ? err.message : String(err));
    }
  }

  function cancel() {
    abortRef.current?.abort();
    setJob(null);
  }

  return (
    <main className="shell">
      <header className="hero">
        <div className="badge" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M9 18V5l12-2v13" strokeLinecap="round" strokeLinejoin="round" />
            <circle cx="6" cy="18" r="3" />
            <circle cx="18" cy="16" r="3" />
          </svg>
        </div>
        <h1>YT2MP3</h1>
        <p>YouTube-Link einfügen und die Tonspur als MP3 speichern. Die Umwandlung läuft direkt in deinem Browser.</p>
      </header>

      <form className="search" onSubmit={onSubmit}>
        <input
          type="text"
          inputMode="url"
          autoComplete="off"
          spellCheck={false}
          placeholder="https://www.youtube.com/watch?v=…"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={busy}
          aria-label="YouTube-Link"
        />
        <button type="submit" disabled={busy || loadingInfo || !url.trim()}>
          {loadingInfo ? <span className="spinner" aria-label="Lädt" /> : 'Laden'}
        </button>
      </form>

      {error && (
        <div className="alert" role="alert">
          {error}
        </div>
      )}

      {info && audioFormat && (
        <section className="card">
          <div className="video">
            <img src={`https://i.ytimg.com/vi/${info.id}/mqdefault.jpg`} alt="" width={160} height={90} />
            <div className="meta">
              <h2 title={info.title}>{info.title}</h2>
              <p>
                {info.author}
                {info.author && ' · '}
                {formatDuration(info.duration)}
              </p>
            </div>
          </div>

          <fieldset className="formats" disabled={busy}>
            <legend>Format</legend>
            {[...MP3_FORMATS, { value: 'original' as Format, label: 'Original', hint: originalExt.toUpperCase() }].map((f) => {
              const disabled = f.value !== 'original' && !mp3Allowed;
              return (
                <label key={f.value} className={format === f.value ? 'active' : ''} data-disabled={disabled || undefined}>
                  <input
                    type="radio"
                    name="format"
                    value={f.value}
                    checked={format === f.value}
                    disabled={disabled}
                    onChange={() => {
                      setFormat(f.value);
                      setResult(null);
                      setJob(null);
                    }}
                  />
                  <strong>{f.label}</strong>
                  <span>{f.hint}</span>
                </label>
              );
            })}
          </fieldset>
          {!mp3Allowed && (
            <p className="note">
              MP3 ist für Videos bis {MP3_MAX_DURATION_SECONDS / 60} Minuten verfügbar. Längere Videos gibt es im
              Originalformat ({originalExt.toUpperCase()}).
            </p>
          )}

          {busy && job ? (
            <div className="progress">
              <div className="bar">
                <div
                  className={job.fraction === null ? 'fill pulse' : 'fill'}
                  style={{ width: `${Math.round(overallProgress(job, format) * 100)}%` }}
                />
              </div>
              <div className="progress-row">
                <span>{stageLabel(job)}</span>
                <button type="button" className="link" onClick={cancel}>
                  Abbrechen
                </button>
              </div>
            </div>
          ) : (
            <button type="button" className="primary" onClick={start}>
              {format === 'original' ? originalExt.toUpperCase() : 'MP3'} herunterladen
              <span>≈ {formatSize(estimateSize(info, audioFormat, format))}</span>
            </button>
          )}

          {job?.stage === 'done' && result && (
            <p className="done">
              {stageLabel(job)} Nichts passiert?{' '}
              <a href={result.href} download={result.name}>
                {result.name}
              </a>{' '}
              ({formatSize(result.size)}) speichern.
            </p>
          )}
        </section>
      )}

      <footer>
        Bitte nur Inhalte herunterladen, für die du die Rechte hast oder die frei lizenziert sind, und die
        Nutzungsbedingungen von YouTube beachten. Kein Angebot von oder Verbindung zu YouTube/Google.
      </footer>
    </main>
  );
}
