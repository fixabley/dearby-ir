import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

// Explicit paths keep this check isolated from other Documents/repository files.
const config = fileURLToPath(new URL('./dearby-ir.htmlhint.json', import.meta.url));
const html = fileURLToPath(new URL('./dearby-ir-2026-09-08.html', import.meta.url));
const result = spawnSync('npx', [
  '--yes', 'htmlhint@1.9.2', '--config', config, html,
], { stdio: 'inherit', cwd: fileURLToPath(new URL('.', import.meta.url)) });

if (result.error) console.error(result.error.message);
process.exitCode = result.status ?? 1;
