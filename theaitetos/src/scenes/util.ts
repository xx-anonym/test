import { useCurrentFrame } from 'remotion';
import { SceneTiming } from '../timeline';

/**
 * Frame helpers for a scene:
 *  s(i, frac) – frame at `frac` of narration segment i
 *  e(i)       – end of segment i
 */
export const useScene = (t: SceneTiming) => {
  const f = useCurrentFrame();
  const s = (i: number, frac = 0) => Math.round(t.starts[Math.min(i, t.starts.length - 1)] + frac * t.durs[Math.min(i, t.durs.length - 1)]);
  const e = (i: number) => t.starts[i] + t.durs[i];
  return { f, s, e, end: t.duration };
};
