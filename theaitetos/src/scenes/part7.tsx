import React from 'react';
import { AbsoluteFill, interpolate } from 'remotion';
import { Egg, Mouth, Profile, Stoa, Sun } from '../components/icons';
import { Arrow, At, Card, easeInOut, Formula, Gr, lerp, prog, Quote, Reveal, Strike, Svg, T, vis } from '../components/kit';
import { C, F } from '../theme';
import { SceneTiming } from '../timeline';
import { useScene } from './util';

type P = { t: SceneTiming };

/* ───────────── XXIII · Wahre Meinung mit Logos ───────────── */

export const Def3: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const letters = ['Σ', 'Ω', 'Κ', 'Ρ', 'Α', 'Τ', 'Η', 'Σ'];
  const weave = prog(f, s(2, 0.1), 50, easeInOut);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Formula f={f} at={s(0, 0.1)} left="ἐπιστήμη" right="δόξα ἀληθὴς μετὰ λόγου" leftDe="Erkenntnis" rightDe="wahre Meinung mit Erklärung" size={84} />
        <Reveal f={f} at={s(0, 0.6)}>
          <div style={{ ...T.serif(38, C.muted), marginTop: 70 }}>
            ohne Logos – <Gr>ἄλογον</Gr> – außerhalb der Erkenntnis · Tht. 201c–d
          </div>
        </Reveal>
      </AbsoluteFill>

      {/* dream: elements only named */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(127,163,201,0.12), rgba(0,0,0,0) 60%)', opacity: prog(f, s(1), 40) }} />
        {letters.slice(0, 7).map((l, i) => {
          const x = 300 + i * 220;
          const y = 470 + Math.sin(f / 25 + i * 1.7) * 30;
          return (
            <At key={i} x={x} y={y}>
              <Reveal f={f} at={s(1, 0.3 + i * 0.04)}>
                <div style={{ ...T.greek(120, C.ink), filter: `blur(${1.2 + Math.sin(f / 13 + i) * 0.8}px)` }}>{l}</div>
                <div style={{ ...T.label(16), marginTop: 6 }}>nur Name</div>
              </Reveal>
            </At>
          );
        })}
        <At x={960} y={200}>
          <Reveal f={f} at={s(1, 0.05)}>
            <div style={T.greek(56)}>ἄκουε δὴ ὄναρ ἀντὶ ὀνείρατος</div>
            <div style={T.italic(36, C.muted)}>„Höre also einen Traum für den andern“ · Tht. 201d</div>
          </Reveal>
        </At>
        <At x={960} y={800} w={1500}>
          <Reveal f={f} at={s(1, 0.75)}>
            <div style={{ position: 'relative', display: 'inline-block' }}>
              <div style={T.serif(44)}>„… es ist“</div>
              <Strike f={f} at={s(1, 0.85)} />
            </div>
            <div style={{ ...T.italic(34, C.muted), marginTop: 10 }}>nicht einmal „ist“ darf man ihnen zusprechen</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* weaving names into an account */}
      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          {letters.map((_, i) => {
            if (i === 0) return null;
            const x0 = lerp(300 + (i - 1) * 190, 640 + (i - 1) * 90, weave);
            const x1 = lerp(300 + i * 190, 640 + i * 90, weave);
            return <path key={i} d={`M ${x0 + 30} 470 Q ${(x0 + x1) / 2 + 30} ${400 + (i % 2) * 140} ${x1 + 30} 470`} stroke={C.gold} strokeWidth={2.5} fill="none" opacity={prog(f, s(2, 0.15) + i * 3, 14)} />;
          })}
        </Svg>
        {letters.map((l, i) => (
          <At key={i} x={lerp(300 + i * 190, 640 + i * 90, weave) + 30} y={470}>
            <div style={T.greek(110, weave > 0.95 ? C.gold : C.ink)}>{l}</div>
          </At>
        ))}
        <At x={960} y={200}>
          <Reveal f={f} at={s(2, 0.45)}>
            <div style={T.greek(54)}>ὀνομάτων γὰρ συμπλοκὴν εἶναι λόγου οὐσίαν</div>
            <div style={T.italic(36, C.muted)}>„Verflechtung von Namen sei das Wesen der Erklärung“ · Tht. 202b</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 680, left: 300, right: 300, display: 'flex', gap: 50 }}>
          <Reveal f={f} at={s(2, 0.7)} style={{ flex: 1 }}>
            <Card accent={C.blue}>
              <div style={T.label(22, C.blue)}>Urbestandteile</div>
              <div style={{ ...T.serif(36), marginTop: 8 }}>wahrnehmbar – nicht erklärbar, nicht erkennbar</div>
            </Card>
          </Reveal>
          <Reveal f={f} at={s(2, 0.8)} style={{ flex: 1 }}>
            <Card>
              <div style={T.label(22, C.gold)}>Verknüpfungen</div>
              <div style={{ ...T.serif(36), marginTop: 8 }}>erklärbar – erkennbar</div>
            </Card>
          </Reveal>
        </div>
      </AbsoluteFill>

      {/* Wittgenstein */}
      <AbsoluteFill style={{ opacity: vis(f, s(3)), justifyContent: 'center', alignItems: 'center' }}>
        <Quote
          f={f}
          at={s(3, 0.3)}
          de="Diese Urelemente waren auch Russell's ›individuals‹, und auch meine ›Gegenstände‹ (Log. Phil. Abh.)."
          src="Ludwig Wittgenstein, Philosophische Untersuchungen § 46 (1953)"
          width={1500}
          size={54}
        />
        <Reveal f={f} at={s(3, 0.05)}>
          <div style={{ ...T.label(24, C.gold), marginTop: 60 }}>logischer Atomismus · Russell · Tractatus</div>
        </Reveal>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XXIV · Buchstabe und Silbe ───────────── */

export const Silben: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const join = prog(f, s(0, 0.5), 24, easeInOut);
  const nodes = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Σ', 'Ω'];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 20 * (1 - join) }}>
          <div style={{ ...T.greek(240, C.ink), transform: `translateX(${(1 - join) * -80}px)`, opacity: prog(f, s(0, 0.2), 20) }}>Σ</div>
          <div style={{ ...T.display(120, C.muted), opacity: (1 - join) * prog(f, s(0, 0.3), 20), width: 120 * (1 - join), overflow: 'hidden' }}>+</div>
          <div style={{ ...T.greek(240, C.ink), transform: `translateX(${(1 - join) * 80}px)`, opacity: prog(f, s(0, 0.35), 20) }}>Ω</div>
        </div>
        <Reveal f={f} at={s(0, 0.7)}>
          <div style={T.display(64)}>
            <span style={{ color: C.gold }}>So</span>krates · <span style={{ fontFamily: F.greek, color: C.gold }}>ΣΩ</span>ΚΡΑΤΗΣ
          </div>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <path
            d={Array.from({ length: 80 }, (_, i) => `${i === 0 ? 'M' : 'L'} ${380 + i * 6} ${560 + Math.sin(i * 1.7 + f / 2) * (10 + ((i * 37) % 13))}`).join(' ')}
            stroke={C.ink}
            strokeWidth={2}
            fill="none"
            opacity={prog(f, s(1, 0.2), 20)}
          />
          <line x1={1260} y1={560} x2={1720} y2={560} stroke={C.muted} strokeWidth={2} strokeDasharray="4 10" opacity={prog(f, s(1, 0.6), 20)} />
        </Svg>
        <At x={620} y={380}>
          <Reveal f={f} at={s(1, 0.05)}>
            <div style={T.greek(180)}>Σ</div>
          </Reveal>
        </At>
        <At x={1490} y={380}>
          <Reveal f={f} at={s(1, 0.55)}>
            <div style={T.greek(180)}>Β</div>
          </Reveal>
        </At>
        <At x={620} y={700}>
          <Reveal f={f} at={s(1, 0.25)}>
            <div style={T.serif(38)}>stimmlos – ein Zischen der Zunge</div>
          </Reveal>
        </At>
        <At x={1490} y={700}>
          <Reveal f={f} at={s(1, 0.6)}>
            <div style={T.serif(38)}>weder Stimme noch Geräusch</div>
          </Reveal>
        </At>
        <At x={960} y={870}>
          <Reveal f={f} at={s(1, 0.85)}>
            <div style={T.label(24, C.gold)}>Elemente ohne Erklärung · Tht. 203b</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6) }}>
        <Svg>
          <Arrow f={f} at={s(2, 0.1)} x1={960} y1={250} x2={560} y2={400} color={C.gold} />
          <Arrow f={f} at={s(2, 0.45)} x1={960} y1={250} x2={1360} y2={400} color={C.blue} />
        </Svg>
        <At x={960} y={190}>
          <Reveal f={f} at={s(2, 0.02)}>
            <div style={T.display(70)}>
              die Silbe <span style={{ fontFamily: F.greek, color: C.gold }}>ΣΩ</span>
            </div>
          </Reveal>
        </At>
        <At x={560} y={590} w={640}>
          <Reveal f={f} at={s(2, 0.15)}>
            <Card>
              <div style={T.display(50, C.gold)}>= Σ + Ω</div>
              <div style={{ ...T.serif(34), marginTop: 10 }}>Wer die Silbe kennt, kennt auch die Buchstaben.</div>
              <div style={{ ...T.serif(34, C.red), marginTop: 10, opacity: prog(f, s(2, 0.35), 16) }}>→ Elemente doch erkennbar</div>
            </Card>
          </Reveal>
        </At>
        <At x={1360} y={590} w={640}>
          <Reveal f={f} at={s(2, 0.5)}>
            <Card accent={C.blue}>
              <div style={T.display(50, C.blue)}>= eine neue Einheit</div>
              <div style={{ ...T.serif(34), marginTop: 10 }}>ohne Teile, aus den Buchstaben entstanden</div>
              <div style={{ ...T.serif(34, C.red), marginTop: 10, opacity: prog(f, s(2, 0.75), 16) }}>→ einfach, also unerklärbar</div>
            </Card>
          </Reveal>
        </At>
        <At x={960} y={880}>
          <Reveal f={f} at={s(2, 0.88)}>
            <div style={T.italic(42)}>So oder so: Der Traum hält nicht. · Tht. 203c–205e</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(3), s(4) - 6) }}>
        <Svg>
          {Array.from({ length: 7 }, (_, i) => (
            <line key={i} x1={1180 + i * 70} y1={330} x2={1180 + i * 70} y2={330 + 260 * prog(f, s(3, 0.4) + i * 2, 14)} stroke={C.gold} strokeWidth={3} opacity={0.8} />
          ))}
          <path d="M 1150 320 C 1150 260 1640 260 1640 320" stroke={C.gold} strokeWidth={4} fill="none" opacity={prog(f, s(3, 0.4), 20)} />
        </Svg>
        <div style={{ position: 'absolute', left: 220, top: 340, display: 'flex', gap: 22, flexWrap: 'wrap', width: 760 }}>
          {['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ'].map((l, i) => (
            <Reveal key={l} f={f} at={s(3, 0.05) + i * 2}>
              <div style={T.greek(80, C.ink)}>{l}</div>
            </Reveal>
          ))}
        </div>
        <At x={600} y={700}>
          <Reveal f={f} at={s(3, 0.1)}>
            <div style={T.label(22)}>Lesenlernen</div>
          </Reveal>
        </At>
        <At x={1400} y={700}>
          <Reveal f={f} at={s(3, 0.45)}>
            <div style={T.label(22)}>Musik: die einzelnen Töne</div>
          </Reveal>
        </At>
        <At x={960} y={860}>
          <Reveal f={f} at={s(3, 0.7)}>
            <div style={T.italic(44, C.gold)}>Die Elemente kennen wir zuerst – und am deutlichsten. · Tht. 206a–b</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(4)) }}>
        <Svg>
          {nodes.map((_, i) =>
            nodes.map((__, j) => {
              if (j <= i || (i * 3 + j) % 4 === 0) return null;
              const a1 = (i / nodes.length) * Math.PI * 2;
              const a2 = (j / nodes.length) * Math.PI * 2;
              return (
                <line
                  key={`${i}-${j}`}
                  x1={960 + Math.cos(a1) * 230}
                  y1={480 + Math.sin(a1) * 230}
                  x2={960 + Math.cos(a2) * 230}
                  y2={480 + Math.sin(a2) * 230}
                  stroke={C.gold}
                  strokeWidth={1.8}
                  opacity={prog(f, s(4, 0.3) + (i + j) * 2, 16) * 0.6}
                />
              );
            }),
          )}
        </Svg>
        {nodes.map((l, i) => {
          const a = (i / nodes.length) * Math.PI * 2;
          return (
            <At key={l} x={960 + Math.cos(a) * 230} y={480 + Math.sin(a) * 230}>
              <Reveal f={f} at={s(4, 0.05) + i * 3}>
                <div style={{ ...T.greek(64, C.ink), background: C.bg, borderRadius: 40, padding: '0 14px' }}>{l}</div>
              </Reveal>
            </At>
          );
        })}
        <At x={960} y={130}>
          <Reveal f={f} at={s(4, 0.05)}>
            <div style={T.label(24, C.gold)}>Gail Fine 1979 · „interrelation model of knowledge“</div>
          </Reveal>
        </At>
        <At x={960} y={860} w={1500}>
          <Reveal f={f} at={s(4, 0.55)}>
            <div style={T.italic(44)}>Wissen durch Zusammenhänge – nicht aus isolierten Elementen</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XXV · Drei Bedeutungen von Logos ───────────── */

export const Logos: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const explode = prog(f, s(1, 0.5), 40, easeInOut);
  const count = Math.round(interpolate(f, [s(1, 0.55), s(1, 0.95)], [5, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const parts = [
    { gr: 'τροχοί', de: 'Räder', dx: 0, dy: 150, lx: -150, ly: 330 },
    { gr: 'ἄξων', de: 'Achse', dx: 0, dy: 90, lx: 330, ly: 160 },
    { gr: 'ὑπερτερία', de: 'Wagenkasten', dx: 0, dy: -60, lx: 340, ly: -110 },
    { gr: 'ἄντυγες', de: 'Geländer', dx: 0, dy: -170, lx: 0, ly: -370 },
    { gr: 'ζυγόν', de: 'Joch', dx: 170, dy: 0, lx: 620, ly: -20 },
  ];
  const name = 'ΘΕΑΙΤΗΤΟΣ';
  const name2 = 'ΤΕΟΔΩΡΟΣ';
  return (
    <AbsoluteFill>
      {/* 1 · voicing */}
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          <g opacity={prog(f, s(0, 0.15), 20)}>
            <Mouth x={420} y={420} s={1.4} />
            {[0, 1, 2, 3].map((i) => {
              const r = ((f / 2 + i * 25) % 100) + 20;
              return <path key={i} d={`M ${520 + r} ${420 - r * 0.7} Q ${560 + r * 1.3} 420 ${520 + r} ${420 + r * 0.7}`} stroke={C.gold} strokeWidth={3} fill="none" opacity={1 - r / 120} />;
            })}
          </g>
          <g opacity={prog(f, s(0, 0.3), 24)}>
            <circle cx={1300} cy={360} r={70} fill="rgba(217,181,107,0.25)" stroke={C.gold} strokeWidth={3} />
            <line x1={1080} y1={500} x2={1520} y2={500} stroke={C.blue} strokeWidth={3} />
            <circle cx={1300} cy={640} r={70} fill="rgba(217,181,107,0.12)" stroke={C.gold} strokeWidth={2} opacity={0.6} transform={`scale(1 ${0.9 + Math.sin(f / 9) * 0.04})`} style={{ transformOrigin: '1300px 640px' }} />
            {[0, 1, 2].map((i) => (
              <path key={i} d={`M ${1160 + i * 40} ${560 + i * 30} Q 1300 ${575 + i * 30} ${1440 - i * 40} ${560 + i * 30}`} stroke={C.blue} strokeWidth={2} fill="none" opacity={0.5} />
            ))}
          </g>
        </Svg>
        <At x={420} y={600}>
          <Reveal f={f} at={s(0, 0.15)}>
            <div style={T.label(24, C.gold)}>1 · aussprechen</div>
          </Reveal>
        </At>
        <At x={1300} y={800}>
          <Reveal f={f} at={s(0, 0.35)}>
            <div style={T.label(20)}>wie ein Bild im Spiegel oder Wasser · Tht. 206d</div>
          </Reveal>
        </At>
        <At x={960} y={180} w={1500}>
          <Reveal f={f} at={s(0, 0.7)}>
            <div style={T.italic(42, C.red)}>Das kann jeder, der nicht taub oder stumm ist.</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 2 · enumerating elements: the wagon */}
      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          <g transform="translate(760 560)" opacity={prog(f, s(1, 0.15), 24)} stroke={C.terracotta} strokeWidth={3} fill="rgba(207,106,71,0.1)" strokeLinejoin="round">
            <g transform={`translate(${parts[2].dx * explode} ${parts[2].dy * explode})`}>
              <path d="M -230 -110 H 230 L 200 -10 H -200 Z" />
            </g>
            <g transform={`translate(${parts[3].dx * explode} ${parts[3].dy * explode})`}>
              <path d="M -220 -150 H 220 M -220 -150 V -110 M 220 -150 V -110 M -110 -150 V -110 M 0 -150 V -110 M 110 -150 V -110" fill="none" />
            </g>
            <g transform={`translate(${parts[1].dx * explode} ${parts[1].dy * explode})`}>
              <line x1={-260} y1={50} x2={260} y2={50} strokeWidth={8} />
            </g>
            <g transform={`translate(${parts[0].dx * explode} ${parts[0].dy * explode})`}>
              {[-150, 150].map((x) => (
                <g key={x} transform={`rotate(${f * 2} ${x} 50)`}>
                  <circle cx={x} cy={50} r={70} fill="none" />
                  {Array.from({ length: 8 }, (_, k) => (
                    <line key={k} x1={x} y1={50} x2={x + Math.cos((k * Math.PI) / 4) * 70} y2={50 + Math.sin((k * Math.PI) / 4) * 70} strokeWidth={2} />
                  ))}
                </g>
              ))}
            </g>
            <g transform={`translate(${parts[4].dx * explode} ${parts[4].dy * explode})`}>
              <path d="M 230 -40 L 420 -60 M 400 -90 C 420 -110 470 -110 480 -80" fill="none" />
            </g>
          </g>
        </Svg>
        {parts.map((p, i) => (
          <At key={p.gr} x={760 + p.lx} y={560 + p.ly}>
            <div style={{ opacity: prog(f, s(1, 0.6) + i * 4, 14), textAlign: 'center' }}>
              <div style={T.greek(38)}>{p.gr}</div>
              <div style={T.label(18)}>{p.de}</div>
            </div>
          </At>
        ))}
        <At x={1640} y={520} w={420}>
          <Reveal f={f} at={s(1, 0.55)}>
            <div style={T.display(110, C.gold)}>{count}</div>
            <div style={T.label(20)}>Hölzer eines Wagens</div>
            <div style={{ ...T.italic(28, C.muted), marginTop: 6 }}>Hesiod, Werke und Tage 456</div>
          </Reveal>
        </At>
        <At x={960} y={110}>
          <Reveal f={f} at={s(1, 0.02)}>
            <div style={T.label(24, C.gold)}>2 · durch die Elemente gehen · Tht. 207a–c</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      {/* 3 · Theaitetos / Theodoros */}
      <AbsoluteFill style={{ opacity: vis(f, s(2)) }}>
        <At x={960} y={140}>
          <Reveal f={f} at={s(2, 0.02)}>
            <div style={T.label(24, C.gold)}>Aufzählen reicht nicht · Tht. 207d–208b</div>
          </Reveal>
        </At>
        <div style={{ position: 'absolute', top: 300, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 70 }}>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 40 }}>
            <div style={{ display: 'flex' }}>
              {name.split('').map((ch, i) => (
                <div key={i} style={{ ...T.greek(110, i < 2 ? C.gold : C.ink), opacity: prog(f, s(2, 0.08) + i * 3, 10), textShadow: i < 2 ? '0 0 20px rgba(217,181,107,0.5)' : undefined }}>
                  {ch}
                </div>
              ))}
            </div>
            <div style={{ ...T.display(80, C.gold), opacity: prog(f, s(2, 0.3), 14) }}>✓</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 40 }}>
            <div style={{ display: 'flex' }}>
              {name2.split('').map((ch, i) => (
                <div key={i} style={{ ...T.greek(110, i < 2 ? C.red : C.ink), opacity: prog(f, s(2, 0.42) + i * 3, 10) }}>
                  {ch}
                </div>
              ))}
            </div>
            <div style={{ ...T.display(80, C.red), opacity: prog(f, s(2, 0.6), 14) }}>✗</div>
          </div>
        </div>
        <At x={960} y={760}>
          <Reveal f={f} at={s(2, 0.55)}>
            <div style={T.serif(38, C.muted)}>
              richtig wäre <span style={{ fontFamily: F.greek, color: C.gold }}>ΘΕΟΔΩΡΟΣ</span>
            </div>
          </Reveal>
        </At>
        <At x={960} y={880} w={1500}>
          <Reveal f={f} at={s(2, 0.78)}>
            <div style={T.italic(44)}>wahre Meinung + alle Buchstaben aufgezählt – und doch kein Wissen</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XXVI · Unterscheidungsmerkmal ───────────── */

export const Merkmal: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const stage = f < s(1, 0.35) ? 0 : f < s(1, 0.65) ? 1 : 2;
  const faces = Array.from({ length: 12 }, (_, i) => ({ snub: i === 4 || i === 9, beard: i % 3 !== 1, bald: i === 9 }));
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          {[180, 280, 380].map((r, i) => (
            <ellipse key={r} cx={960} cy={500} rx={r * 1.6} ry={r * 0.6} fill="none" stroke={C.line} strokeWidth={1.5} opacity={prog(f, s(0, 0.1) + i * 5, 20)} />
          ))}
          {[0, 1, 2].map((i) => {
            const a = f / (60 + i * 30) + i * 2;
            const r = [180, 280, 380][i];
            return <circle key={i} cx={960 + Math.cos(a) * r * 1.6} cy={500 + Math.sin(a) * r * 0.6} r={10 - i * 2} fill={C.marble} opacity={0.7 * prog(f, s(0, 0.2), 20)} />;
          })}
          <g opacity={prog(f, s(0, 0.4), 30)}>
            <Sun x={960 + Math.cos(f / 80) * 290} y={500 + Math.sin(f / 80) * 110} s={1.1} />
          </g>
          <circle cx={960} cy={500} r={26} fill={C.blue} opacity={prog(f, s(0, 0.1), 20)} />
        </Svg>
        <At x={960} y={170}>
          <Reveal f={f} at={s(0, 0.05)}>
            <div style={T.label(24, C.gold)}>3 · das Unterscheidungsmerkmal</div>
          </Reveal>
        </At>
        <At x={960} y={880} w={1500}>
          <Reveal f={f} at={s(0, 0.55)}>
            <div style={T.italic(44)}>Die Sonne: das Hellste, was am Himmel um die Erde läuft · Tht. 208d</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6) }}>
        <Svg>
          {faces.map((fc, i) => {
            const x = 300 + (i % 6) * 264;
            const y = 330 + Math.floor(i / 6) * 300;
            const on = stage === 0 || (stage === 1 && fc.snub) || (stage === 2 && i === 4);
            return (
              <g key={i} opacity={prog(f, s(1, 0.05) + i * 2, 14) * (on ? 1 : 0.15)}>
                <circle cx={x} cy={y} r={110} fill="rgba(207,106,71,0.06)" stroke={on && stage > 0 ? C.gold : C.line} strokeWidth={on && stage > 0 ? 3 : 1.5} />
                <Profile x={x} y={y + 8} s={0.62} snub={fc.snub} beard={fc.beard} bald={fc.bald} eyeBulge={fc.snub} noseColor={fc.snub && stage > 0 ? C.gold : undefined} />
              </g>
            );
          })}
        </Svg>
        <At x={960} y={150} w={1600}>
          <div style={{ position: 'relative', height: 60 }}>
            {[
              'Nase, Mund und Augen – das haben alle',
              'stumpfe Nase, hervortretende Augen – auch Sokrates',
              'diese besondere Stumpfnasigkeit – nur Theaitetos',
            ].map((w, i) => (
              <div key={w} style={{ position: 'absolute', inset: 0, textAlign: 'center', opacity: stage === i ? prog(f, [s(1, 0.05), s(1, 0.35), s(1, 0.65)][i], 14) : 0, ...T.display(54, i === 2 ? C.gold : C.ink) }}>
                {w}
              </div>
            ))}
          </div>
        </At>
        <At x={960} y={940}>
          <Reveal f={f} at={s(1, 0.8)}>
            <div style={T.label(22)}>… sodass ich ihn morgen wiedererkenne · Tht. 209b–c</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2), s(3) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Reveal f={f} at={s(2, 0.1)}>
          <div style={T.display(64)}>
            Merkmal hinzufügen, <span style={{ color: C.muted }}>das man schon hat?</span>
          </div>
        </Reveal>
        <Reveal f={f} at={s(2, 0.55)}>
          <Card style={{ marginTop: 60 }}>
            <div style={T.italic(48, C.gold)}>„das Zureden eines Blinden“</div>
            <div style={{ ...T.label(20), marginTop: 10 }}>Tht. 209e</div>
          </Card>
        </Reveal>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(3)) }}>
        <Svg>
          <path
            d="M 1500 560 C 1600 760 1100 860 760 760 C 420 660 360 420 520 380"
            stroke={C.red}
            strokeWidth={4}
            fill="none"
            pathLength={1}
            strokeDasharray={1}
            strokeDashoffset={1 - prog(f, s(3, 0.65), 40, easeInOut)}
          />
          <Arrow f={f} at={s(3, 0.65) + 36} x1={500} y1={400} x2={540} y2={370} color={C.red} dur={6} />
        </Svg>
        <At x={960} y={460} w={1700}>
          <Reveal f={f} at={s(3, 0.3)}>
            <div style={T.display(66)}>
              <span style={{ color: C.gold }}>Erkenntnis</span> = richtige Meinung + <span style={{ color: C.red }}>Erkenntnis</span> des Unterschieds
            </div>
          </Reveal>
        </At>
        <At x={960} y={580}>
          <Reveal f={f} at={s(3, 0.45)}>
            <div style={T.greek(44)}>δόξα ὀρθὴ μετὰ ἐπιστήμης διαφορότητος</div>
            <div style={T.label(20)}>Tht. 210a</div>
          </Reveal>
        </At>
        <At x={960} y={900}>
          <Reveal f={f} at={s(3, 0.8)}>
            <div style={T.italic(46, C.red)}>Die Definition dreht sich im Kreis.</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ───────────── XXVII · Windeier ───────────── */

export const Aporie: React.FC<P> = ({ t }) => {
  const { f, s } = useScene(t);
  const walk = interpolate(f, [s(2, 0.1), s(2) + t.durs[2] + 20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: vis(f, 0, s(1) - 6) }}>
        <Svg>
          {[0, 1, 2].map((i) => (
            <g key={i} opacity={prog(f, s(0, 0.05) + i * 6, 16)}>
              <Egg x={560 + i * 400} y={440} s={1.8} crack={prog(f, s(0, 0.55) + i * 8, 20)} color={C.muted} />
              {[0, 1].map((k) => {
                const p = prog(f, s(0, 0.6) + i * 8 + k * 4, 30);
                return <circle key={k} cx={560 + i * 400 + (k - 0.5) * 30} cy={410 - p * 160} r={14 + p * 26} fill="none" stroke={C.muted} strokeWidth={2} opacity={(1 - p) * 0.8} />;
              })}
            </g>
          ))}
        </Svg>
        {['Wahrnehmung', 'wahre Meinung', 'wahre Meinung mit Logos'].map((w, i) => (
          <At key={w} x={560 + i * 400} y={680} w={380}>
            <Reveal f={f} at={s(0, 0.1) + i * 6}>
              <div style={{ position: 'relative', display: 'inline-block' }}>
                <div style={T.serif(36)}>{w}</div>
                <Strike f={f} at={s(0, 0.35) + i * 6} />
              </div>
            </Reveal>
          </At>
        ))}
        <At x={960} y={860}>
          <Reveal f={f} at={s(0, 0.75)}>
            <div style={T.display(64, C.gold)}>Windeier</div>
          </Reveal>
        </At>
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(1), s(2) - 6), justifyContent: 'center', alignItems: 'center' }}>
        <Quote
          f={f}
          at={s(1, 0.3)}
          de="… weniger beschwerlich sein und sanftmütiger, und besonnenerweise nicht glauben zu wissen, was du nicht weißt."
          gr="σωφρόνως οὐκ οἰόμενος εἰδέναι ἃ μὴ οἶσθα"
          src="Tht. 210c · Übers. Schleiermacher"
          width={1500}
          size={52}
        />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: vis(f, s(2)) }}>
        <Svg>
          <g opacity={prog(f, s(2), 30)}>
            <Stoa x={1420} y={520} s={1.1} />
          </g>
          <g opacity={1 - prog(f, s(2) + t.durs[2] - 10, 30)}>
            <Profile x={lerp(380, 1180, walk)} y={540} s={0.7} beard bald snub />
          </g>
        </Svg>
        <At x={1420} y={810}>
          <Reveal f={f} at={s(2, 0.1)}>
            <div style={T.label(24, C.gold)}>Königshalle · Klage des Meletos</div>
          </Reveal>
        </At>
        <At x={960} y={170} w={1500}>
          <Reveal f={f} at={s(2, 0.2)}>
            <div style={T.italic(42)}>„Jetzt nun muß ich mich in der Königshalle einstellen …“</div>
            <div style={{ ...T.label(20), marginTop: 10 }}>Tht. 210d</div>
          </Reveal>
        </At>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

