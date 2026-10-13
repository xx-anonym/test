import '@fontsource/cormorant-garamond/500.css';
import '@fontsource/cormorant-garamond/500-italic.css';
import '@fontsource/cormorant-garamond/600.css';
import '@fontsource/eb-garamond/400.css';
import '@fontsource/eb-garamond/400-italic.css';
import '@fontsource/eb-garamond/500.css';
import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import React from 'react';
import { Composition } from 'remotion';
import { FPS, H, W } from './theme';
import { TIMELINE, TOTAL_FRAMES, CREDITS_FROM } from './timeline';
import { ScenePreview, Video } from './Video';
import { Credits } from './scenes/credits';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Theaitetos" component={Video} durationInFrames={TOTAL_FRAMES} fps={FPS} width={W} height={H} />
    {TIMELINE.map((t) => (
      <Composition
        key={t.scene.id}
        id={`S-${t.scene.id}`}
        component={ScenePreview}
        defaultProps={{ id: t.scene.id }}
        durationInFrames={t.duration}
        fps={FPS}
        width={W}
        height={H}
      />
    ))}
    <Composition id="S-credits" component={Credits} durationInFrames={TOTAL_FRAMES - CREDITS_FROM} fps={FPS} width={W} height={H} />
  </>
);
