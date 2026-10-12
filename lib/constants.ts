// Function responses on Vercel are capped at 4.5 MB, so audio is fetched
// from /api/chunk in ranges of this size and stitched together client-side.
export const CHUNK_SIZE = 4 * 1024 * 1024;

// Longer videos are offered as the original M4A only: decoding them to PCM
// for MP3 encoding would take more memory than a browser tab can spare.
export const MP3_MAX_DURATION_SECONDS = 30 * 60;
