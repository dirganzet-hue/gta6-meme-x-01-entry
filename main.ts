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

// The gate only accepts an X post address, so fail loudly on a wrong
// host or scheme instead of handing the grader a typo. The placeholder
// still passes this shape check; the gate itself refuses it.
const postUrl = new URL(post.url);
if (postUrl.protocol !== 'https:' || !/(^|\.)(x\.com|twitter\.com)$/.test(postUrl.hostname)) {
  throw new Error(`POST.json url must be an https://x.com or twitter.com post address, got: ${post.url}`);
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, 'POST.json'), postText);
