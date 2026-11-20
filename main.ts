import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const source = join(scriptDir, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ? resolve(process.env.MAKEFUN_OUTPUT_DIR) : "/output";
const dest = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`entry.png missing: ${source}`);
}
const size = statSync(source).size;
if (size > 1048576) {
  throw new Error(`entry.png too large: ${size} bytes exceeds 1048576 bytes`);
}
const bytes = readFileSync(source);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(pngMagic)) {
  throw new Error("entry.png is not a valid PNG (bad magic bytes)");
}
if (bytes.subarray(12, 16).toString("ascii") !== "IHDR") {
  throw new Error("entry.png is not a valid PNG (missing IHDR chunk)");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png dimensions too large: ${width}x${height} exceeds 1024x1024`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);
console.log(`Validated OK and copied entry.png (${width}x${height}, ${size} bytes) to ${dest}`);
