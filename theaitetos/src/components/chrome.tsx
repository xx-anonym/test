import React from 'react';
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { C, F } from '../theme';
import { CARD, SceneTiming } from '../timeline';
import { easeInOut, prog, T } from './kit';

/** Dark gradient, drifting warm light and film grain. Rendered once behind everything. */
export const Background: React.FC<{ frame: number }> = ({ frame }) => {
  const t = frame / 30;
  const lx = 50 + 18 * Math.sin(t / 23);
  const ly = 40 + 12 * Math.cos(t / 31);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 45%, ${C.bg2} 0%, ${C.bg} 70%)` }}>
      <AbsoluteFill
        style={{ background: `radial-gradient(circle at ${lx}% ${ly}%, rgba(217,181,107,0.07) 0%, rgba(217,181,107,0) 45%)` }}
      />
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)' }} />
      <Img
        src={staticFile('img/grain.png')}
        style={{
          position: 'absolute',
          inset: 0,
          width: 1920,
          height: 1080,
          objectFit: 'cover',
          opacity: 0.05,
          mixBlendMode: 'overlay',
          transform: `translate(${(frame * 37) % 7}px, ${(frame * 53) % 5}px) scale(1.02)`,
        }}
      />
    </AbsoluteFill>
  );
};

/** Greek key ornament that draws itself. */
export const Meander: React.FC<{ f: number; at: number; width: number; unit?: number; color?: string; dur?: number }> = ({
  f,
  at,
  width,
  unit = 40,
  color = C.gold,
  dur = 40,
}) => {
  const n = Math.floor(width / unit);
  let d = `M 0 38 H ${n * unit}`;
  for (let i = 0; i < n; i++) {
    const x = i * unit;
    d += ` M ${x + 4} 38 V 4 H ${x + 34} V 28 H ${x + 14} V 14 H ${x + 24} V 20`;
  }
  const p = prog(f, at, dur, easeInOut);
  return (
    <svg width={n * unit} height={42} viewBox={`0 0 ${n * unit} 42`} style={{ overflow: 'visible' }}>
      <defs>
        <clipPath id={`mclip-${at}-${width}`}>
          <rect x={0} y={-5} width={n * unit * p} height={52} />
        </clipPath>
      </defs>
      <path d={d} stroke={color} strokeWidth={2.2} fill="none" clipPath={`url(#mclip-${at}-${width})`} opacity={0.85} />
    </svg>
  );
};

export const ChapterCard: React.FC<{ f: number; chapter: string; title: string; steph?: string }> = ({ f, chapter, title, steph }) => {
  const out = prog(f, CARD - 16, 16, easeInOut);
  const a = prog(f, 0, 22);
  const b = prog(f, 6, 26);
  const c = prog(f, 16, 24);
  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', opacity: 1 - out, transform: `scale(${1 + out * 0.04})` }}>
      <div style={{ ...T.label(26, C.gold), opacity: a, letterSpacing: '0.4em' }}>Kapitel {chapter}</div>
      <div
        style={{
          ...T.display(118),
          marginTop: 26,
          opacity: b,
          filter: `blur(${(1 - b) * 10}px)`,
          transform: `translateY(${(1 - b) * 20}px)`,
          textAlign: 'center',
          maxWidth: 1500,
        }}
      >
        {title}
      </div>
      <div style={{ marginTop: 34 }}>
        <Meander f={f} at={10} width={560} />
      </div>
      {steph && (
        <div style={{ ...T.label(24, C.muted), marginTop: 26, opacity: c, letterSpacing: '0.22em' }}>
          {/^\d/.test(steph) ? `Theaitetos ${steph}` : steph}
        </div>
      )}
    </AbsoluteFill>
  );
};

/** Bottom line: source of the current statement (left) and chapter (right). */
export const CitationBar: React.FC<{ f: number; timing: SceneTiming }> = ({ f, timing }) => {
  const { scene, starts, durs } = timing;
  let idx = -1;
  starts.forEach((s, i) => {
    if (f >= s - 6) idx = i;
  });
  const cite = idx >= 0 ? scene.segments[idx].cite : '';
  const enter = idx >= 0 ? prog(f, starts[idx] - 6, 14) : 0;
  const nextStart = idx >= 0 && idx + 1 < starts.length ? starts[idx + 1] - 6 : Infinity;
  const leave = idx >= 0 ? prog(f, Math.min(nextStart - 10, starts[idx] + durs[idx] + 40), 10, easeInOut) : 0;
  const chapterOpacity = prog(f, timing.body - 10, 20);
  return (
    <>
      {cite && (
        <div
          style={{
            position: 'absolute',
            left: 110,
            bottom: 52,
            display: 'flex',
            alignItems: 'center',
            gap: 16,
            opacity: enter * (1 - leave),
            transform: `translateY(${(1 - enter) * 8}px)`,
          }}
        >
          <div style={{ width: 10, height: 10, background: C.gold, transform: 'rotate(45deg)', boxShadow: `0 0 12px ${C.gold}` }} />
          <div style={{ fontFamily: F.sans, fontSize: 25, color: C.ink, opacity: 0.86, letterSpacing: '0.02em' }}>{cite}</div>
        </div>
      )}
      {scene.chapter && (
        <div
          style={{
            position: 'absolute',
            right: 110,
            bottom: 54,
            fontFamily: F.sans,
            fontSize: 21,
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
            color: C.muted,
            opacity: chapterOpacity * 0.8,
          }}
        >
          {scene.chapter} · {scene.title}
        </div>
      )}
    </>
  );
};

/** Wraps a scene: chapter card, visual body (faded at the edges) and citation bar. */
export const SceneShell: React.FC<{ timing: SceneTiming; children: React.ReactNode }> = ({ timing, children }) => {
  const f = useCurrentFrame();
  const { scene, duration, body } = timing;
  const bodyIn = scene.chapter ? prog(f, body - 14, 18) : prog(f, 0, 18);
  const sceneOut = interpolate(f, [duration - 16, duration], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ opacity: sceneOut }}>
      {scene.chapter && f < body + 2 && <ChapterCard f={f} chapter={scene.chapter} title={scene.title} steph={scene.steph} />}
      <AbsoluteFill style={{ opacity: bodyIn }}>{children}</AbsoluteFill>
      <CitationBar f={f} timing={timing} />
    </AbsoluteFill>
  );
};
