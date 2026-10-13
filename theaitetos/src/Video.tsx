import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { Background, SceneShell } from './components/chrome';
import { SCENES } from './scenes';
import { Credits } from './scenes/credits';
import { C } from './theme';
import { CREDITS_FROM, SceneTiming, TIMELINE, TOTAL_FRAMES } from './timeline';

const SceneAudio: React.FC<{ t: SceneTiming }> = ({ t }) => (
  <>
    {t.starts.map((s, i) => (
      <Sequence key={i} from={s} durationInFrames={t.durs[i] + 3} name={`${t.scene.id}-${i}`}>
        <Audio src={staticFile(`audio/${t.scene.id}-${i}.wav`)} />
      </Sequence>
    ))}
  </>
);

export const SceneView: React.FC<{ t: SceneTiming; audio?: boolean }> = ({ t, audio = true }) => {
  const Comp = SCENES[t.scene.id];
  return (
    <>
      <SceneShell timing={t}>{Comp ? <Comp t={t} /> : null}</SceneShell>
      {audio && <SceneAudio t={t} />}
    </>
  );
};

const ProgressLine: React.FC<{ frame: number }> = ({ frame }) => (
  <div
    style={{
      position: 'absolute',
      left: 0,
      bottom: 0,
      height: 3,
      width: `${(frame / TOTAL_FRAMES) * 100}%`,
      background: `linear-gradient(90deg, rgba(217,181,107,0.15), ${C.gold})`,
      opacity: 0.55,
    }}
  />
);

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      <Background frame={frame} />
      {TIMELINE.map((t) => (
        <Sequence key={t.scene.id} from={t.from} durationInFrames={t.duration} name={t.scene.id}>
          <SceneView t={t} />
        </Sequence>
      ))}
      <Sequence from={CREDITS_FROM} durationInFrames={TOTAL_FRAMES - CREDITS_FROM} name="credits">
        <Credits />
      </Sequence>
      <ProgressLine frame={frame} />
    </AbsoluteFill>
  );
};

/** Single scene on its own background, for previews and stills. */
export const ScenePreview: React.FC<{ id: string }> = ({ id }) => {
  const frame = useCurrentFrame();
  const t = TIMELINE.find((s) => s.scene.id === id)!;
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      <Background frame={frame} />
      <SceneView t={t} />
    </AbsoluteFill>
  );
};
