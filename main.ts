// News-image entry: the image is entry.png beside this file, drawn by draw.py
// (a Python + PIL script, run once to produce the PNG), and this program
// copies it to /output/entry.png. The gate takes a whole PNG or JPEG of at
// most 1 MiB and 1024 by 1024 pixels; the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(out, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(out, 'entry.png'));
