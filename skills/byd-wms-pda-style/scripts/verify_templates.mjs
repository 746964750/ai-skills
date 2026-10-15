// node <skill>/scripts/verify_templates.mjs <Vue project root>
import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'

const project = path.resolve(process.argv[2] || '.')
const require = createRequire(path.join(project, 'package.json'))
const { parse, compileScript, compileTemplate } = require('@vue/compiler-sfc')
const skill = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const files = ['assets/runtime/PdaPage.vue', ...fs.readdirSync(path.join(skill, 'assets/templates')).filter(name => name.endsWith('.vue')).map(name => 'assets/templates/' + name)]
const failures = []
for (const name of files) {
  const { descriptor, errors } = parse(fs.readFileSync(path.join(skill, name), 'utf8'), { filename: name })
  failures.push(...errors.map(error => ({ file: name, error: String(error) })))
  try { compileScript(descriptor, { id: 'pda-style-template' }) } catch (error) { failures.push({ file: name, error: String(error) }) }
  const result = compileTemplate({ source: descriptor.template.content, filename: name, id: 'pda-style-template' })
  failures.push(...result.errors.map(error => ({ file: name, error: String(error) })))
}
console.log(JSON.stringify({ status: failures.length ? 'failed' : 'passed', compiled: files.length, failures }, null, 2))
if (failures.length) process.exitCode = 1
