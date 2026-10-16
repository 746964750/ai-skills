/* AST-backed JS/TS/Vue adapter. Dependencies resolved from the target project. */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const {createRequire} = require("node:module");
const {createHash} = require("node:crypto");
const input = JSON.parse(fs.readFileSync(0, "utf8"));
const root = path.resolve(input.root);
const settings = input.config.frontend || {};
const req = createRequire(path.join(root, "package.json"));
const output = {schema: 1, files: input.files, edges: [], findings: []};
function add(kind, rule, message, file, line=0) {
  output.findings.push({kind, rule, message, path: file, line});
}
function dependency(name) {
  if (process.env.HARNESS_NODE_MODULES) return require(require.resolve(name, {paths:[process.env.HARNESS_NODE_MODULES]}));
  return req(name);
}
function rel(p) { return path.relative(root, p).split(path.sep).join("/"); }
function resolveImport(spec, file, line) {
  let value = spec;
  const aliases = settings.aliases || {};
  const alias = Object.keys(aliases).sort((a,b)=>b.length-a.length).find(a=>value.startsWith(a));
  let target;
  if (alias) target = path.resolve(root, aliases[alias] + value.slice(alias.length));
  else if (value.startsWith(".")) target = path.resolve(root, path.dirname(file), value);
  else if (value.startsWith("/")) {
    add("gap", "JS-RESOLVE", "Absolute/root import requires explicit resolver: " + value, file, line); return;
  } else { output.edges.push({from:file, to:"external:"+value, line}); return; }
  const candidates = [target, ...[".js",".jsx",".ts",".tsx",".mjs",".cjs",".vue"].map(e=>target+e),
    ...[".js",".jsx",".ts",".tsx",".vue"].map(e=>path.join(target,"index"+e))];
  const found = candidates.find(p=>fs.existsSync(p) && fs.statSync(p).isFile());
  if (!found) { add("gap","JS-RESOLVE","Unresolved import: "+spec,file,line); return; }
  const actual = rel(fs.realpathSync(found));
  if (actual.startsWith("../") || path.isAbsolute(actual)) {
    add("gap","JS-SCOPE","Import escapes root: "+spec,file,line); return;
  }
  if (!/\.(?:[cm]?js|jsx|ts|tsx|vue)$/.test(actual)) return;
  if (!input.files.includes(actual)) {
    add("gap","JS-SCOPE","Imported code omitted from scan: "+actual,file,line); return;
  }
  output.edges.push({from:file,to:actual,line});
}
function analyze(parser, code, file, language, offset) {
  if (!["js","jsx","ts","tsx"].includes(language)) {
    add("gap","JS-LANG","Unsupported script language "+language,file); return;
  }
  const plugins = ["decorators-legacy", "dynamicImport"];
  if (language.includes("ts")) plugins.push("typescript");
  if (language.endsWith("x")) plugins.push("jsx");
  const ast = parser.parse(code, {sourceType:"unambiguous", plugins, errorRecovery:false});
  const seen = new WeakSet();
  function walk(node) {
    if (!node || typeof node !== "object" || seen.has(node)) return;
    seen.add(node);
    if (Array.isArray(node)) {node.forEach(walk); return;}
    const line = (node.loc?.start.line || 1) + offset;
    if (["ImportDeclaration","ExportNamedDeclaration","ExportAllDeclaration"].includes(node.type) && node.source)
      resolveImport(node.source.value,file,line);
    if (node.type === "TSImportType") {
      if (node.argument?.type === "StringLiteral") resolveImport(node.argument.value,file,line);
      else add("gap","JS-DYNAMIC","Unsupported type import",file,line);
    }
    if (node.type === "TSImportEqualsDeclaration") {
      const exp = node.moduleReference?.expression;
      if (exp?.type === "StringLiteral") resolveImport(exp.value,file,line);
      else add("gap","JS-DYNAMIC","Unsupported TS import assignment",file,line);
    }
    if (node.type === "ImportExpression") {
      if (node.source?.type === "StringLiteral") resolveImport(node.source.value,file,line);
      else add("gap","JS-DYNAMIC","Nonliteral dynamic import",file,line);
    }
    if (node.type === "CallExpression" &&
        (node.callee?.type === "Import" || (node.callee?.type === "Identifier" && node.callee.name === "require"))) {
      if (node.arguments?.[0]?.type === "StringLiteral") resolveImport(node.arguments[0].value,file,line);
      else add("gap","JS-DYNAMIC","Nonliteral import/require",file,line);
    }
    if (node.type === "DebuggerStatement") add("violation","ENT-DEBUGGER","Debugger statement",file,line);
    if (node.type === "CallExpression" || node.type === "OptionalCallExpression") {
      const callee=node.callee;
      if (["MemberExpression","OptionalMemberExpression"].includes(callee?.type) && callee.object?.name === "console") {
        const method=callee.computed ? callee.property?.value : callee.property?.name;
        if ((settings.console_methods || []).includes(method))
          add("violation","ENT-CONSOLE","Forbidden console."+method,file,line);
        else if (callee.computed && typeof method !== "string")
          add("review","ENT-CONSOLE-DYNAMIC","Computed console access needs review",file,line);
      }
    }
    if (/Function|Method/.test(node.type || "") && node.body && node.loc) {
      const count=node.loc.end.line-node.loc.start.line+1;
      if (count>settings.max_function_lines)
        add("violation","ENT-FUNCTION","Function lines "+count+" > "+settings.max_function_lines,file,line);
    }
    for (const [key,value] of Object.entries(node))
      if (!["loc","start","end","extra","tokens","comments","leadingComments","trailingComments","innerComments"].includes(key)) walk(value);
  }
  walk(ast);
  for (const comment of ast.comments || []) {
    const line=(comment.loc?.start.line || 1)+offset;
    if (/\b(?:TODO|FIXME)\b/.test(comment.value) && !(new RegExp(input.config.entropy.issue_pattern)).test(comment.value))
      add("violation","ENT-TODO","TODO/FIXME without issue reference",file,line);
    if (/(?:\b(?:return|import|function|const|let|var)\b.+[;{}]|\w+\s*\([^)]*\)\s*;)/.test(comment.value)) {
      const fingerprint = createHash("sha256").update(comment.value).digest("hex");
      const reviewed = (input.config.entropy.reviewed_comments || []).some(
        r => r.path === file && r.sha256 === fingerprint && r.reason && r.reviewer);
      if (!reviewed) add("review","ENT-OLD-CODE",
        "Possible commented-out code; review exact comment SHA256="+fingerprint,file,line);
    }
  }
}
try {
  if (settings.resolution_reviewed !== true) throw new Error("Alias/workspace/module resolution has not been reviewed");
  if (!Number.isInteger(settings.max_function_lines) || settings.max_function_lines < 1 ||
      !Array.isArray(settings.console_methods)) throw new Error("Explicit function limit and console method policy required");
  if (!input.config.entropy?.issue_pattern) throw new Error("Explicit issue pattern required");
  const parser=dependency("@babel/parser");
  for (const file of input.files) {
    const code=fs.readFileSync(path.join(root,file),"utf8");
    if (file.endsWith(".vue")) {
      let descriptor;
      let compiler;
      if (settings.vue_parser !== "vue2") {
        try {compiler=dependency("@vue/compiler-sfc");} catch (_) {}
      }
      if (compiler) {
        const parsed=compiler.parse(code,{filename:file});
        if (parsed.errors.length) throw new Error(file+": "+parsed.errors.join("; "));
        descriptor=parsed.descriptor;
      } else {
        const vue2=dependency("vue-template-compiler");
        descriptor=vue2.parseComponent(code,{pad:false});
      }
      for (const script of [descriptor.script,descriptor.scriptSetup].filter(Boolean)) {
        if (script.src || script.attrs?.src) {add("gap","VUE-SRC","External script src needs project resolver",file);continue;}
        const language=script.lang || script.attrs?.lang || "js";
        const start=script.loc?.start.offset ?? script.start ?? 0;
        const offset=code.slice(0,start).split("\n").length-1;
        analyze(parser,script.content,file,language,offset);
      }
    } else {
      const extension=path.extname(file).slice(1);
      analyze(parser,code,file,["mjs","cjs"].includes(extension) ? "js" : extension,0);
    }
  }
} catch (error) { add("gap","FRONTEND-ERROR",error.message,""); }
process.stdout.write(JSON.stringify(output));
