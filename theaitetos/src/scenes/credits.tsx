import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { Meander } from '../components/chrome';
import { prog, T } from '../components/kit';
import { C } from '../theme';
import bibliography from '../data/bibliography.json';

/** Rolling bibliography at the end of the video. */
export const Credits: React.FC = () => {
  const f = useCurrentFrame();
  const groups = bibliography as { heading: string; items: string[] }[];
  const scroll = interpolate(f, [90, 26 * 30 - 30], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const height = 900 + groups.reduce((n, g) => n + 110 + g.items.length * 58, 0);
  return (
    <AbsoluteFill style={{ opacity: prog(f, 0, 30) }}>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 0, transform: `translateY(${300 - scroll * (height - 700)}px)`, textAlign: 'center' }}>
        <div style={T.label(28, C.gold)}>Quellen und Literatur</div>
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: 26 }}>
          <Meander f={f} at={6} width={520} />
        </div>
        {groups.map((g) => (
          <div key={g.heading} style={{ marginTop: 70 }}>
            <div style={{ ...T.label(24, C.gold), marginBottom: 26 }}>{g.heading}</div>
            {g.items.map((it) => (
              <div key={it} style={{ ...T.serif(31, C.ink), opacity: 0.9, margin: '0 auto 18px', maxWidth: 1500 }}>
                {it}
              </div>
            ))}
          </div>
        ))}
        <div style={{ marginTop: 140, ...T.italic(36, C.muted) }}>Animation: Remotion</div>
      </div>
    </AbsoluteFill>
  );
};
