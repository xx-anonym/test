import React from 'react';
import { Easing, interpolate } from 'remotion';
import { C, F } from '../theme';

export const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
export const easeInOut = Easing.bezier(0.65, 0, 0.35, 1);

/** 0→1 between `start` and `start + dur` (clamped, eased). */
export const prog = (f: number, start: number, dur = 20, easing = easeOut) =>
  interpolate(f, [start, start + dur], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing,
  });

/** Fade in at `start`, fade out at `end` (if given). */
export const vis = (f: number, start: number, end?: number, dur = 18) =>
  prog(f, start, dur) * (end === undefined ? 1 : 1 - prog(f, end, dur, easeInOut));

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

type Div = React.CSSProperties;

/** Fades and lifts its children into place. */
export const Reveal: React.FC<{
  f: number;
  at: number;
  out?: number;
  dur?: number;
  y?: number;
  x?: number;
  blur?: boolean;
  style?: Div;
  children: React.ReactNode;
}> = ({ f, at, out, dur = 22, y = 24, x = 0, blur = true, style, children }) => {
  const p = prog(f, at, dur);
  const o = out === undefined ? 0 : prog(f, out, 16, easeInOut);
  return (
    <div
      style={{
        opacity: p * (1 - o),
        transform: `translate(${x * (1 - p)}px, ${y * (1 - p) - o * 10}px)`,
        filter: blur ? `blur(${(1 - p) * 8}px)` : undefined,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

/** Absolutely positioned box, centred on (x, y) unless `anchor` says otherwise. */
export const At: React.FC<{ x: number; y: number; w?: number; anchor?: 'center' | 'left' | 'right'; style?: Div; children: React.ReactNode }> = ({
  x,
  y,
  w,
  anchor = 'center',
  style,
  children,
}) => (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      width: w ?? 'max-content',
      maxWidth: w ? undefined : 1760,
      transform: anchor === 'center' ? 'translate(-50%, -50%)' : anchor === 'right' ? 'translate(-100%, -50%)' : 'translate(0, -50%)',
      textAlign: anchor === 'center' ? 'center' : anchor,
      ...style,
    }}
  >
    {children}
  </div>
);

export const T = {
  display: (size = 96, color = C.ink): Div => ({ fontFamily: F.display, fontWeight: 500, fontSize: size, color, lineHeight: 1.05, letterSpacing: '-0.01em' }),
  serif: (size = 44, color = C.ink): Div => ({ fontFamily: F.serif, fontSize: size, color, lineHeight: 1.35 }),
  italic: (size = 44, color = C.ink): Div => ({ fontFamily: F.serif, fontStyle: 'italic', fontSize: size, color, lineHeight: 1.35 }),
  greek: (size = 52, color = C.gold): Div => ({ fontFamily: F.greek, fontSize: size, color, lineHeight: 1.3 }),
  label: (size = 22, color = C.muted): Div => ({
    fontFamily: F.sans,
    fontSize: size,
    fontWeight: 500,
    color,
    letterSpacing: '0.16em',
    textTransform: 'uppercase',
  }),
  sans: (size = 30, color = C.ink): Div => ({ fontFamily: F.sans, fontSize: size, color, lineHeight: 1.35 }),
};

/** SVG path that draws itself between `at` and `at + dur`. */
export const Draw: React.FC<
  { f: number; at: number; dur?: number; d: string; out?: number } & React.SVGProps<SVGPathElement>
> = ({ f, at, dur = 30, d, out, ...rest }) => {
  const p = prog(f, at, dur, easeInOut);
  const o = out === undefined ? 1 : 1 - prog(f, out, 15);
  return (
    <path
      d={d}
      pathLength={1}
      strokeDasharray={1}
      strokeDashoffset={1 - p}
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
      opacity={p > 0 ? o : 0}
      {...rest}
    />
  );
};

/** A horizontal strike-through that sweeps across its parent. */
export const Strike: React.FC<{ f: number; at: number; color?: string; width?: number; top?: string }> = ({
  f,
  at,
  color = C.red,
  width = 5,
  top = '52%',
}) => {
  const p = prog(f, at, 16, easeInOut);
  return (
    <div
      style={{
        position: 'absolute',
        left: -12,
        top,
        height: width,
        width: `calc(${p * 100}% + ${p * 24}px)`,
        background: color,
        borderRadius: width,
        boxShadow: `0 0 18px ${color}`,
        transform: 'rotate(-3deg)',
        transformOrigin: 'left center',
      }}
    />
  );
};

/** Card with a thin golden border. */
export const Card: React.FC<{ style?: Div; children: React.ReactNode; accent?: string }> = ({ style, children, accent = C.gold }) => (
  <div
    style={{
      position: 'relative',
      padding: '26px 34px',
      borderRadius: 18,
      border: `1.5px solid ${accent}55`,
      background: `linear-gradient(160deg, rgba(255,255,255,0.055), rgba(255,255,255,0.015)), ${C.bg}`,
      boxShadow: '0 20px 60px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06)',
      ...style,
    }}
  >
    {children}
  </div>
);

/** Quotation with optional Greek original and source line. */
export const Quote: React.FC<{
  f: number;
  at: number;
  de: string;
  gr?: string;
  src?: string;
  width?: number;
  size?: number;
  out?: number;
}> = ({ f, at, de, gr, src, width = 1300, size = 50, out }) => {
  const words = de.split(' ');
  const per = Math.max(1.2, Math.min(3, 70 / words.length));
  return (
    <div style={{ width, opacity: out === undefined ? 1 : 1 - prog(f, out, 16) }}>
      <div style={{ ...T.display(150, C.gold), height: 70, opacity: prog(f, at, 20) * 0.7, marginBottom: 10 }}>„</div>
      <div style={{ ...T.italic(size), textWrap: 'balance' } as Div}>
        {words.map((w, i) => {
          const p = prog(f, at + 6 + i * per, 14);
          return (
            <span key={i} style={{ opacity: p, filter: `blur(${(1 - p) * 6}px)`, display: 'inline-block', marginRight: '0.26em' }}>
              {w}
            </span>
          );
        })}
      </div>
      {gr && (
        <div style={{ ...T.greek(size * 0.72), marginTop: 26, opacity: prog(f, at + 10 + words.length * per, 30) }}>{gr}</div>
      )}
      {src && <div style={{ ...T.label(22, C.muted), marginTop: 22, opacity: prog(f, at + 18 + words.length * per, 24) }}>{src}</div>}
    </div>
  );
};

/** Simple arrow between two points. */
export const Arrow: React.FC<{
  f: number;
  at: number;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  color?: string;
  width?: number;
  dur?: number;
  bend?: number;
  dashed?: boolean;
}> = ({ f, at, x1, y1, x2, y2, color = C.gold, width = 3, dur = 22, bend = 0, dashed }) => {
  const mx = (x1 + x2) / 2 - (y2 - y1) * bend;
  const my = (y1 + y2) / 2 + (x2 - x1) * bend;
  const p = prog(f, at, dur, easeInOut);
  const ang = Math.atan2(y2 - my, x2 - mx);
  const head = 16;
  return (
    <g opacity={p > 0 ? 1 : 0}>
      <path
        d={`M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`}
        pathLength={1}
        strokeDasharray={dashed ? undefined : 1}
        strokeDashoffset={dashed ? undefined : 1 - p}
        stroke={color}
        strokeWidth={width}
        fill="none"
        strokeLinecap="round"
        style={dashed ? { strokeDasharray: '8 10', opacity: p } : undefined}
      />
      <path
        d={`M ${x2} ${y2} L ${x2 - head * Math.cos(ang - 0.45)} ${y2 - head * Math.sin(ang - 0.45)} M ${x2} ${y2} L ${
          x2 - head * Math.cos(ang + 0.45)
        } ${y2 - head * Math.sin(ang + 0.45)}`}
        stroke={color}
        strokeWidth={width}
        strokeLinecap="round"
        opacity={prog(f, at + dur * 0.8, 8)}
      />
    </g>
  );
};

/** Full-frame SVG canvas in 1920×1080 coordinates. */
export const Svg: React.FC<{ children: React.ReactNode; style?: Div }> = ({ children, style }) => (
  <svg viewBox="0 0 1920 1080" width={1920} height={1080} style={{ position: 'absolute', inset: 0, overflow: 'visible', ...style }}>
    <defs>
      <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="6" result="b" />
        <feMerge>
          <feMergeNode in="b" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="14" />
      </filter>
      <radialGradient id="goldGlow">
        <stop offset="0%" stopColor={C.gold} stopOpacity="0.55" />
        <stop offset="100%" stopColor={C.gold} stopOpacity="0" />
      </radialGradient>
    </defs>
    {children}
  </svg>
);

/** Equation-style headline, e.g. ἐπιστήμη = αἴσθησις. */
export const Formula: React.FC<{ f: number; at: number; left: string; right: string; leftDe: string; rightDe: string; size?: number }> = ({
  f,
  at,
  left,
  right,
  leftDe,
  rightDe,
  size = 92,
}) => {
  const a = prog(f, at, 24);
  const b = prog(f, at + 14, 24);
  const c = prog(f, at + 28, 24);
  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', gap: 50, justifyContent: 'center' }}>
      <div style={{ textAlign: 'center', opacity: a, transform: `translateX(${(1 - a) * -40}px)` }}>
        <div style={T.greek(size, C.ink)}>{left}</div>
        <div style={{ ...T.label(24), marginTop: 10 }}>{leftDe}</div>
      </div>
      <div style={{ ...T.display(size, C.gold), opacity: b, transform: `scale(${0.6 + 0.4 * b})` }}>=</div>
      <div style={{ textAlign: 'center', opacity: c, transform: `translateX(${(1 - c) * 40}px)` }}>
        <div style={T.greek(size, C.gold)}>{right}</div>
        <div style={{ ...T.label(24), marginTop: 10 }}>{rightDe}</div>
      </div>
    </div>
  );
};

/** Greek words inside an uppercase label: keep lowercase with accents. */
export const Gr: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{ textTransform: 'none', fontFamily: F.greek, letterSpacing: 0, fontSize: '1.3em', fontWeight: 400 }}>{children}</span>
);
