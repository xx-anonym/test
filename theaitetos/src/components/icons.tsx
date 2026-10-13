import React from 'react';
import { C } from '../theme';

type G = { x?: number; y?: number; s?: number; color?: string; opacity?: number; rot?: number; sw?: number };

const tf = ({ x = 0, y = 0, s = 1, rot = 0 }: G) => `translate(${x} ${y}) rotate(${rot}) scale(${s})`;

export const Eye: React.FC<G & { look?: number; open?: number }> = ({ color = C.ink, opacity = 1, look = 0, open = 1, sw = 3, ...g }) => (
  <g transform={tf(g)} opacity={opacity}>
    <path d={`M -55 0 Q 0 ${-40 * open} 55 0 Q 0 ${40 * open} -55 0 Z`} fill="rgba(236,230,217,0.06)" stroke={color} strokeWidth={sw} />
    <g transform={`scale(1 ${Math.max(open, 0.05)})`}>
      <circle cx={look * 14} cy={0} r={18} fill="none" stroke={color} strokeWidth={sw} />
      <circle cx={look * 14} cy={0} r={8} fill={color} />
      <circle cx={look * 14 + 5} cy={-6} r={3} fill={C.bg} />
    </g>
  </g>
);

export const Ear: React.FC<G> = ({ color = C.ink, opacity = 1, sw = 3, ...g }) => (
  <g transform={tf(g)} opacity={opacity} fill="none" stroke={color} strokeWidth={sw} strokeLinecap="round">
    <path d="M -12 -42 C 30 -50 44 -6 20 12 C 8 21 12 40 -8 42 C -20 43 -24 34 -20 28" />
    <path d="M -2 -24 C 20 -26 22 -2 8 6 C 2 10 0 16 2 20" />
  </g>
);

export const Nose: React.FC<G> = ({ color = C.ink, opacity = 1, sw = 3, ...g }) => (
  <g transform={tf(g)} opacity={opacity} fill="none" stroke={color} strokeWidth={sw} strokeLinecap="round">
    <path d="M -6 -44 C -4 -14 18 8 22 22 C 25 33 10 36 0 31" />
    <path d="M -22 30 C -16 24 -8 26 -4 31" />
  </g>
);

export const Mouth: React.FC<G> = ({ color = C.ink, opacity = 1, sw = 3, ...g }) => (
  <g transform={tf(g)} opacity={opacity} fill="none" stroke={color} strokeWidth={sw} strokeLinecap="round">
    <path d="M -44 -4 C -20 -18 -6 -10 0 -12 C 6 -10 20 -18 44 -4 C 24 22 -24 22 -44 -4 Z" />
    <path d="M -44 -4 C -10 4 10 4 44 -4" />
  </g>
);

export const Hand: React.FC<G & { fill?: string }> = ({ color = C.ink, opacity = 1, sw = 3, fill = 'rgba(236,230,217,0.05)', ...g }) => (
  <g transform={tf(g)} opacity={opacity} fill={fill} stroke={color} strokeWidth={sw} strokeLinejoin="round">
    <path d="M -30 50 L -34 0 C -36 -10 -24 -12 -22 -2 L -20 -44 C -20 -54 -8 -54 -8 -44 L -6 -8 L -4 -54 C -4 -64 8 -64 8 -54 L 8 -8 L 12 -48 C 12 -58 24 -58 24 -48 L 22 -4 L 30 -34 C 32 -44 44 -42 42 -32 L 34 20 C 30 40 22 50 10 50 Z" />
  </g>
);

export const Figure: React.FC<G & { fill?: string }> = ({ color = C.ink, opacity = 1, sw = 3, fill = 'rgba(236,230,217,0.06)', ...g }) => (
  <g transform={tf(g)} opacity={opacity} stroke={color} strokeWidth={sw} fill={fill}>
    <circle cx={0} cy={-62} r={18} />
    <path d="M -30 52 C -30 2 -22 -36 0 -36 C 22 -36 30 2 30 52 Z" strokeLinejoin="round" />
  </g>
);

/** Line-art head in profile, facing right. `beard` for Socrates/Theodorus. */
export const Profile: React.FC<G & { beard?: boolean; bald?: boolean; snub?: boolean; noseColor?: string; eyeBulge?: boolean }> = ({
  color = C.ink,
  opacity = 1,
  sw = 3.2,
  beard,
  bald,
  snub = true,
  noseColor,
  eyeBulge,
  ...g
}) => {
  const nose = snub
    ? 'M 156 100 C 160 112 172 126 178 136 C 180 142 172 146 162 145'
    : 'M 156 100 C 164 116 180 132 186 142 C 186 148 172 148 162 146';
  return (
    <g transform={tf(g)} opacity={opacity} fill="none" stroke={color} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round">
      <g transform="translate(-110 -130)">
        {/* back of head, crown, forehead */}
        <path d="M 78 240 C 72 212 52 196 48 160 C 42 104 70 46 124 42 C 150 40 160 64 158 84 C 157 92 155 96 156 100" />
        {!bald && <path d="M 52 150 C 50 100 74 56 120 50 C 98 64 90 80 92 96 C 80 92 66 112 52 150 Z" fill={color} fillOpacity={0.15} />}
        {bald && <path d="M 52 152 C 46 128 54 112 62 104" opacity={0.6} />}
        <path d={nose} stroke={noseColor ?? color} strokeWidth={noseColor ? sw * 1.5 : sw} />
        {/* lips, chin, jaw, neck */}
        <path d="M 162 145 C 166 152 166 156 160 160 C 166 164 164 170 158 172 C 160 184 154 196 140 202 C 126 207 112 210 108 222 L 106 244" />
        {/* eye and brow */}
        <path d="M 128 92 C 136 86 146 86 152 90" />
        <circle cx={141} cy={101} r={eyeBulge ? 8 : 5} fill={color} stroke="none" />
        {eyeBulge && <circle cx={141} cy={101} r={13} strokeWidth={2} opacity={0.6} />}
        {/* ear */}
        <path d="M 92 104 C 84 102 80 116 84 128 C 88 138 96 136 98 128" />
        {beard && (
          <path
            d="M 108 150 C 104 176 114 214 136 236 C 146 246 160 232 164 216 C 168 200 164 184 160 174"
            fill={color}
            fillOpacity={0.12}
          />
        )}
      </g>
    </g>
  );
};

export const Egg: React.FC<G & { crack?: number; fill?: string }> = ({ color = C.ink, opacity = 1, sw = 3, crack = 0, fill = 'rgba(244,239,228,0.08)', ...g }) => (
  <g transform={tf(g)} opacity={opacity} stroke={color} strokeWidth={sw} fill={fill} strokeLinejoin="round">
    <g transform={`translate(${-crack * 10} 0) rotate(${-crack * 14} 0 10)`}>
      <path d="M 0 -52 C -28 -52 -40 4 -40 20 C -40 46 -22 58 0 58 L 0 16 L -10 6 L 4 -6 L -6 -18 L 0 -52 Z" />
    </g>
    <g transform={`translate(${crack * 10} 0) rotate(${crack * 14} 0 10)`}>
      <path d="M 0 -52 C 28 -52 40 4 40 20 C 40 46 22 58 0 58 L 0 16 L -10 6 L 4 -6 L -6 -18 L 0 -52 Z" />
    </g>
  </g>
);

export const Bird: React.FC<G & { flap?: number; fill?: string }> = ({ color = C.ink, opacity = 1, sw = 2.6, flap = 0, fill = 'rgba(236,230,217,0.08)', ...g }) => {
  const w = Math.sin(flap) * 18;
  return (
    <g transform={tf(g)} opacity={opacity} stroke={color} strokeWidth={sw} fill={fill} strokeLinejoin="round">
      <path d="M -42 6 C -24 -14 8 -16 28 -6 L 44 -12 L 40 2 C 30 18 0 22 -20 15 L -42 24 Z" />
      <path d={`M -8 0 C -2 ${-26 - w} 18 ${-34 - w} 26 ${-30 - w} C 16 -14 10 -6 6 2`} />
      <circle cx={30} cy={-6} r={2.2} fill={color} stroke="none" />
    </g>
  );
};

export const Coin: React.FC<G & { label?: string }> = ({ color = C.gold, opacity = 1, label, ...g }) => (
  <g transform={tf(g)} opacity={opacity}>
    <circle r={26} fill="rgba(217,181,107,0.18)" stroke={color} strokeWidth={3} />
    <circle r={19} fill="none" stroke={color} strokeWidth={1.5} opacity={0.6} />
    {label && (
      <text textAnchor="middle" dy={8} fontFamily="EB Garamond" fontSize={22} fill={color}>
        {label}
      </text>
    )}
  </g>
);

export const Cup: React.FC<G & { fill?: string }> = ({ color = C.ink, opacity = 1, sw = 3, fill = 'rgba(207,106,71,0.25)', ...g }) => (
  <g transform={tf(g)} opacity={opacity} stroke={color} strokeWidth={sw} strokeLinejoin="round">
    <path d="M -64 -14 H 64 C 58 18 28 30 0 30 C -28 30 -58 18 -64 -14 Z" fill={fill} />
    <path d="M -64 -10 C -84 -12 -86 6 -70 10 M 64 -10 C 84 -12 86 6 70 10" fill="none" />
    <path d="M 0 30 V 52 M -26 56 H 26" fill="none" />
  </g>
);

export const Stoa: React.FC<G> = ({ color = C.ink, opacity = 1, sw = 2.5, ...g }) => (
  <g transform={tf(g)} opacity={opacity} stroke={color} strokeWidth={sw} fill="none">
    <path d="M -230 -110 L 0 -170 L 230 -110 Z" fill="rgba(236,230,217,0.05)" />
    <rect x={-240} y={-110} width={480} height={26} />
    {[-200, -120, -40, 40, 120, 200].map((cx) => (
      <g key={cx}>
        <rect x={cx - 16} y={-84} width={32} height={170} />
        <path d={`M ${cx - 6} -80 V 82 M ${cx + 6} -80 V 82`} opacity={0.5} />
      </g>
    ))}
    <rect x={-250} y={86} width={500} height={16} />
    <rect x={-270} y={102} width={540} height={14} />
  </g>
);

export const Stone: React.FC<G> = ({ color = C.ink, opacity = 1, sw = 3, ...g }) => (
  <g transform={tf(g)} opacity={opacity}>
    <path
      d="M -52 18 C -60 -10 -34 -40 -4 -42 C 26 -44 54 -24 56 2 C 58 28 30 44 0 44 C -26 44 -46 38 -52 18 Z"
      fill="rgba(236,230,217,0.07)"
      stroke={color}
      strokeWidth={sw}
    />
    <path d="M -20 -20 C -8 -26 8 -24 18 -16" stroke={color} strokeWidth={2} fill="none" opacity={0.5} />
  </g>
);

export const Die: React.FC<G & { n?: number; fill?: string }> = ({ color = C.ink, opacity = 1, n = 6, fill = 'rgba(244,239,228,0.1)', ...g }) => {
  const pips: Record<number, [number, number][]> = {
    1: [[0, 0]],
    2: [[-1, -1], [1, 1]],
    3: [[-1, -1], [0, 0], [1, 1]],
    4: [[-1, -1], [1, -1], [-1, 1], [1, 1]],
    5: [[-1, -1], [1, -1], [0, 0], [-1, 1], [1, 1]],
    6: [[-1, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [1, 1]],
  };
  return (
    <g transform={tf(g)} opacity={opacity}>
      <rect x={-30} y={-30} width={60} height={60} rx={12} fill={fill} stroke={color} strokeWidth={2.6} />
      {pips[n].map(([px, py], i) => (
        <circle key={i} cx={px * 15} cy={py * 15} r={5} fill={color} />
      ))}
    </g>
  );
};

export const Sun: React.FC<G & { glow?: number }> = ({ color = C.gold, opacity = 1, glow = 1, ...g }) => (
  <g transform={tf(g)} opacity={opacity}>
    <circle r={110} fill="url(#goldGlow)" opacity={glow} />
    <circle r={40} fill={color} />
    {Array.from({ length: 12 }, (_, i) => {
      const a = (i / 12) * Math.PI * 2;
      return (
        <line
          key={i}
          x1={Math.cos(a) * 52}
          y1={Math.sin(a) * 52}
          x2={Math.cos(a) * 72}
          y2={Math.sin(a) * 72}
          stroke={color}
          strokeWidth={4}
          strokeLinecap="round"
        />
      );
    })}
  </g>
);

export const Column: React.FC<G & { h?: number }> = ({ color = C.ink, opacity = 1, h = 300, sw = 2.5, ...g }) => (
  <g transform={tf(g)} opacity={opacity} stroke={color} strokeWidth={sw} fill="rgba(236,230,217,0.04)">
    <rect x={-40} y={-h / 2 - 20} width={80} height={20} />
    <rect x={-28} y={-h / 2} width={56} height={h} />
    {[-14, 0, 14].map((x) => (
      <line key={x} x1={x} y1={-h / 2 + 6} x2={x} y2={h / 2 - 6} opacity={0.4} />
    ))}
    <rect x={-40} y={h / 2} width={80} height={18} />
  </g>
);
