// gta6-meme-x-01 entry: the post on X is the entry, and this program hands
// the grader its address. It reads POST.json from the repository root,
// checks it is a JSON object with a url string, and writes those exact
// bytes to the output directory. Nothing else is written, so the two runs
// the grader makes always produce identical output.
//
// Run locally the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const repoDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const postText = readFileSync(join(repoDir, 'POST.json'), 'utf8');
const post = JSON.parse(postText);
if (typeof post !== 'object' || post === null || typeof post.url !== 'string') {
  throw new Error('POST.json must be a JSON object with a string "url" field');
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, 'POST.json'), postText);
