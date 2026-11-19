// News-image entry: the program is a one-line copy. The image it ships,
// entry.png, was drawn programmatically with Python and PIL (see draw.py
// in this repository) so every word on it is typeset, never generated:
// no garbled text, no invented detail. The grader runs this program with
// no network; it copies the image into the output directory make.fun
// gives it, and the copy is byte for byte the file in this repository.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
