// gta6-meme-x-01 (revision 3): the entry is a post on X, and this program
// is the courier that hands its address to the grader.
//
// It reads POST.json from the repository root, insists the url field is
// a real https://x.com (or twitter.com) post address, and writes the
// file's exact bytes to the output directory, together with a copy of
// the meme picture (meme-v3.png) the post carries. Nothing else is
// written, no network and no clock are touched, so the grader's two
// runs always land on identical bytes. The output folder itself is
// never removed, only created if it is missing.
//
// Run it exactly the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

function loadPost(repoDir: string): { text: string; url: string } {
  // The exact bytes are preserved: the file is written out untouched,
  // so the grader's two runs always produce identical output.
  const text = readFileSync(join(repoDir, 'POST.json'), 'utf8');
  const post: unknown = JSON.parse(text);
  if (
    typeof post !== 'object' ||
    post === null ||
    typeof (post as { url?: unknown }).url !== 'string'
  ) {
    throw new Error('POST.json must be a JSON object with a string "url" field');
  }
  return { text, url: (post as { url: string }).url };
}

function assertXPost(url: string): void {
  const parsed = new URL(url);
  const hostOk = /(^|\.)(x\.com|twitter\.com)$/.test(parsed.hostname);
  if (parsed.protocol !== 'https:' || !hostOk) {
    throw new Error(
      `POST.json url must be an https://x.com or twitter.com post address, got: ${url}`,
    );
  }
}

const repoDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const post = loadPost(repoDir);
assertXPost(post.url);

mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, 'POST.json'), post.text);
copyFileSync(join(repoDir, 'meme-v3.png'), join(outputDir, 'meme-v3.png'));
