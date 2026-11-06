#!/usr/bin/env node
/**
 * interview-skills installer
 *
 * Usage:
 *   npx github:lotsofmysteries-Lexi/interview-prep            # install all 6 skills
 *   npx github:lotsofmysteries-Lexi/interview-prep interview-prep   # install one skill
 *
 * Skills are copied to ~/.workbuddy/skills/<name>/
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const ROOT = __dirname;
const TARGET_BASE = path.join(os.homedir(), ".workbuddy", "skills");

const EXCLUDE = new Set([".DS_Store", "__MACOSX"]);

function log(msg) {
  process.stdout.write(msg + "\n");
}

function findSkillDirs() {
  return fs
    .readdirSync(ROOT, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .filter((d) => fs.existsSync(path.join(ROOT, d.name, "SKILL.md")))
    .map((d) => d.name)
    .sort();
}

function copyDir(src, dest) {
  fs.cpSync(src, dest, {
    recursive: true,
    filter: (s) => !EXCLUDE.has(path.basename(s)),
  });
}

function showHelp() {
  log(`
interview-skills — WorkBuddy interview skill suite

Usage:
  npx github:lotsofmysteries-Lexi/interview-prep [skill ...]

Skills:
${findSkillDirs()
  .map((s) => "  - " + s)
  .join("\n")}

Install all skills (default) or pass specific skill names.
Target directory: ${TARGET_BASE}
`);
}

function main() {
  const args = process.argv.slice(2);

  if (args.includes("-h") || args.includes("--help")) {
    showHelp();
    process.exit(0);
  }

  const available = findSkillDirs();
  if (available.length === 0) {
    log("Error: no skill directories (containing SKILL.md) found.");
    process.exit(1);
  }

  const requested = args.filter((a) => !a.startsWith("-"));
  const invalid = requested.filter((r) => !available.includes(r));
  if (invalid.length > 0) {
    log(`Unknown skill(s): ${invalid.join(", ")}`);
    log(`Available: ${available.join(", ")}`);
    process.exit(1);
  }

  const targets = requested.length > 0 ? requested : available;

  log(`Installing to ${TARGET_BASE}\n`);

  for (const name of targets) {
    const src = path.join(ROOT, name);
    const dest = path.join(TARGET_BASE, name);
    try {
      copyDir(src, dest);
      log(`  installed  ${name}  ->  ${dest}`);
    } catch (err) {
      log(`  FAILED     ${name}: ${err.message}`);
      process.exitCode = 1;
    }
  }

  log(`
Done. ${targets.length} skill(s) installed.
If WorkBuddy is running, restart it or rescan skills to activate.
`);
}

main();
