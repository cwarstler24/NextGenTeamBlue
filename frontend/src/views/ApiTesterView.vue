<template>
  <div class="wrap" :data-theme="theme">
    <header>
      <div class="brand">
        <img src="../assets/SwaB_Logo.png" alt="Team Blue Logo" class="logo-img">
        <div>
          <h1>Team Blue — API Tester</h1>
          <p class="lead">Quick interface for your inventory API — local testing only</p>
        </div>
      </div>

      <div class="flex right">
        <div class="chip" :style="serverStatusStyle">{{ serverStatusText }}</div>
        <div class="theme-toggle">
          <button class="btn ghost small" @click="toggleTheme" title="Toggle light/dark mode">{{ themeButtonText }}</button>
        </div>
        <button class="btn ghost small" @click="pingRoot">Ping</button>
      </div>
    </header>

    <div class="grid">
      <!-- left: controls -->
      <div>
        <div class="panel">
          <div style="display:flex; gap:12px; align-items:center;">
            <div style="flex:1">
              <label for="bearer">Bearer token</label>
              <input id="bearer" v-model="bearer" type="text" placeholder="Paste token (without 'Bearer ')" />
            </div>
            <div style="width:120px;">
              <label>&nbsp;</label>
              <button class="btn small" @click="resetPage">Reset</button>
            </div>
          </div>
        </div>

        <div class="panel" style="margin-top:12px;">
          <h3 style="margin:0 0 10px 0;">Quick actions</h3>
          <div class="row">
            <div style="flex:1">
              <label>Show all resources</label>
              <div class="controls">
                <button class="btn" @click="callApi('/resources/')">Resources</button>
                <button class="btn" @click="callApi('/resources/types/')">Types</button>
              </div>
            </div>
          </div>

          <div class="row" style="margin-top:10px;">
            <div style="flex:1">
              <label>Get resource by ID</label>
              <div class="controls">
                <input v-model.number="getId" type="number" placeholder="ID" style="width:120px;" />
                <button class="btn small" @click="getById">Get</button>
              </div>
            </div>
          </div>

          <div class="row" style="margin-top:8px;">
            <div style="flex:1">
              <label>Search by location</label>
              <div class="controls">
                <input v-model.number="locId" type="number" placeholder="Location ID" style="width:120px;" />
                <button class="btn small" @click="searchByLocation">Search</button>
              </div>
            </div>
          </div>

          <div class="row" style="margin-top:8px;">
            <div style="flex:1">
              <label>Search by employee</label>
              <div class="controls">
                <input v-model.number="empId" type="number" placeholder="Employee ID" style="width:120px;" />
                <button class="btn small" @click="searchByEmployee">Search</button>
              </div>
            </div>
          </div>
        </div>

        <div class="panel" style="margin-top:12px;">
          <h3 style="margin:0 0 10px 0;">Create / Update</h3>

          <label for="postBody" style="font-size:13px;color:var(--muted)">POST body (JSON)</label>
          <textarea id="postBody" v-model="postBody" placeholder='{"type_id":4,"location_id":null,"employee_id":24,"notes":"HTML test","is_decommissioned":0}'></textarea>
          <div class="row" style="margin-top:10px;">
            <button class="btn" @click="postResource">POST</button>
            <button class="btn ghost" @click="validateJson('post')">Validate JSON</button>
          </div>

          <hr style="border:none;border-top:1px solid rgba(255,255,255,0.03); margin:12px 0;">

          <label for="putId" style="font-size:13px;color:var(--muted)">PUT id</label>
          <div class="row">
            <input v-model.number="putId" type="number" placeholder="Resource ID" style="width:120px;" />
          </div>
          <label for="putBody" style="font-size:13px;color:var(--muted); margin-top:8px;">PUT body (JSON)</label>
          <textarea id="putBody" v-model="putBody" placeholder='{"type_id":4,"location_id":null,"employee_id":24,"notes":"Update test","is_decommissioned":0}'></textarea>
          <div class="row" style="margin-top:8px;">
            <button class="btn" @click="putResource">PUT</button>
            <button class="btn ghost" @click="validateJson('put')">Validate JSON</button>
          </div>
        </div>

        <div class="panel" style="margin-top:12px;">
          <h3 style="margin:0 0 10px 0;">Delete</h3>
          <div class="row">
            <input v-model.number="delId" type="number" placeholder="Resource ID" style="width:120px;" />
            <button class="btn" @click="deleteResource">DELETE</button>
            <button class="btn ghost" @click="callApi('/resources/')">Refresh</button>
          </div>
          <p style="margin-top:10px;color:var(--muted);font-size:13px;">Delete routes require manager permissions.</p>
        </div>
      </div>

      <!-- right: outputs -->
      <div class="out-wrap">
        <div class="panel" style="padding:12px;">
          <div class="status">
            <div class="chip">{{ httpStatus }}</div>
            <div style="flex:1;color:var(--muted);font-size:13px">{{ statusText }}</div>
            <div style="display:flex;gap:8px;">
              <button class="btn small" @click="copyOutput">Copy</button>
              <button class="btn small ghost" @click="clearOutput">Clear</button>
            </div>
          </div>
          <pre class="output">{{ output }}</pre>
        </div>

        <div style="display:flex; gap:12px;">
          <div class="panel" style="flex:1; padding:12px;">
            <strong style="display:block;margin-bottom:6px">Recent activity</strong>
            <div id="logArea" style="font-family:ui-monospace,monospace; font-size:12px; color:var(--muted); max-height:120px; overflow:auto; white-space:pre-wrap;">{{ logText }}</div>
          </div>

          <div class="panel" style="width:240px; padding:12px;">
            <strong style="display:block;margin-bottom:6px">Hints</strong>
            <div style="color:var(--muted); font-size:13px;">
              • Make sure token is pasted without the leading "Bearer " prefix.<br><br>
              • Use Validate JSON before POST/PUT.<br><br>
              • If you see a 307, switch between trailing slash/no-slash on the URL.
            </div>
          </div>
        </div>

        <div class="footer">Local tester — not for production. Keep tokens private.</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const API_BASE = 'http://127.0.0.1:8000'

const bearer = ref('')
const getId = ref<number | null>(null)
const locId = ref<number | null>(null)
const empId = ref<number | null>(null)
const putId = ref<number | null>(null)
const postBody = ref('{"type_id":4,"location_id":null,"employee_id":24,"notes":"HTML test","is_decommissioned":0}')
const putBody = ref('{"type_id":4,"location_id":null,"employee_id":24,"notes":"Update test","is_decommissioned":0}')

const output = ref('{ "message": "Ready" }')
const httpStatus = ref('idle')
const statusText = ref('Responses and logs appear here')
const logText = ref('')

const theme = ref<'light' | 'dark'>('light')
const themeButtonText = ref('Dark')
const serverStatusText = ref('server: unknown')
const serverStatusStyle = ref<Record<string,string>>({})

function tokenHeader(): Record<string,string> {
  const t = bearer.value.trim()
  if(!t) return {}
  return { Authorization: 'Bearer ' + t }
}

function log(msg: string){
  logText.value = `${new Date().toLocaleTimeString()}  ${msg}\n` + logText.value
}

function setStatus(code: number | string, text: string){
  httpStatus.value = String(code)
  statusText.value = text
  log(`${code} — ${text}`)
}

async function callApi(endpoint: string, opts: { method?: string; headers?: Record<string,string>; body?: string } = {}){
  const url = API_BASE + endpoint
  output.value = 'Loading...'
  setStatus('loading', `Calling ${endpoint}`)
  try{
    const res = await fetch(url, { headers: { ...tokenHeader(), ...(opts.headers||{}) }, method: opts.method||'GET', body: opts.body||null })
    const text = await res.text()
    let parsed: unknown
    try{ parsed = JSON.parse(text) } catch { parsed = text }
    output.value = typeof parsed === 'string' ? String(parsed) : JSON.stringify(parsed, null, 2)
    setStatus(res.status, `${res.status} ${res.statusText}`)
  } catch(err: any){
    output.value = `Network error: ${err.message}`
    setStatus(0, 'Network error')
  }
}

function validateJson(which: 'post'|'put'){
  const txt = which === 'post' ? postBody.value : putBody.value
  try{ JSON.parse(txt); setStatus('valid','JSON looks valid') }
  catch(e: any){ setStatus(400, 'Invalid JSON: ' + e.message) }
}

async function postResource(){
  try{
    const b = JSON.parse(postBody.value)
    await callApi('/resources/', { method:'POST', headers:{ 'Content-Type': 'application/json' }, body: JSON.stringify(b) })
  } catch {
    setStatus(400,'Invalid JSON body')
  }
}

async function putResource(){
  if(!putId.value){ setStatus(400,'Missing id'); return }
  try{
    const b = JSON.parse(putBody.value)
    await callApi(`/resources/${putId.value}`, { method:'PUT', headers:{ 'Content-Type': 'application/json' }, body: JSON.stringify(b) })
  } catch {
    setStatus(400, 'Invalid JSON body')
  }
}

async function deleteResource(){
  if(!delId.value){ setStatus(400,'Missing id'); return }
  if(!confirm(`Delete resource ${delId.value}?`)) return
  await callApi(`/resources/${delId.value}`, { method:'DELETE' })
}

async function getById(){
  if(!getId.value){ setStatus(400,'Missing id'); return }
  await callApi(`/resources/${getId.value}`)
}

async function searchByLocation(){
  if(!locId.value){ setStatus(400,'Missing location id'); return }
  await callApi(`/resources/location/${locId.value}`)
}

async function searchByEmployee(){
  if(!empId.value){ setStatus(400,'Missing employee id'); return }
  await callApi(`/resources/employee/${empId.value}`)
}

function clearOutput(){ output.value = ''; setStatus('idle','cleared') }
async function copyOutput(){ try{ await navigator.clipboard.writeText(output.value); setStatus('copied','Output copied to clipboard') } catch { setStatus(0,'Copy failed') } }

function resetPage(){
  bearer.value = ''
  postBody.value = '{"type_id":4,"location_id":null,"employee_id":24,"notes":"HTML test","is_decommissioned":0}'
  putBody.value = '{"type_id":4,"location_id":null,"employee_id":24,"notes":"Update test","is_decommissioned":0}'
  setStatus('ready','Page reset')
}

async function pingRoot(){
  try{
    const res = await fetch(API_BASE + '/', { method:'GET' })
    serverStatusText.value = res.ok ? 'server: online' : 'server: offline'
    serverStatusStyle.value = { background: res.ok ? 'linear-gradient(90deg,#16a34a,#10b981)' : 'linear-gradient(90deg,#ef4444,#fb7185)' }
    log(`ping ${res.status} ${res.statusText}`)
  } catch {
    serverStatusText.value = 'server: unreachable'
    serverStatusStyle.value = { background: 'linear-gradient(90deg,#ef4444,#fb7185)' }
    log('ping failed')
  }
}

function applyTheme(next: 'light'|'dark'){
  theme.value = next
  themeButtonText.value = next === 'dark' ? 'Light' : 'Dark'
  document.documentElement.setAttribute('data-theme', next)
  localStorage.setItem('themePref', next)
}
function toggleTheme(){ applyTheme(theme.value === 'light' ? 'dark' : 'light') }

onMounted(() => {
  const stored = localStorage.getItem('themePref')
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  const initial = (stored as 'light'|'dark') || (prefersDark ? 'dark' : 'light')
  applyTheme(initial)
  pingRoot()
})

const delId = ref<number | null>(null)
</script>

<style scoped>
/* Copy of styles from index_test.html */
:root {
  --bg:#f5f7fa;
  --bg-accent:#eef3f8;
  --panel:#ffffff;
  --panel-border:#e2e8f0;
  --panel-shadow:0 2px 4px rgba(0,0,0,0.04),0 4px 18px -4px rgba(0,0,0,0.06);
  --muted:#5b6474;
  --text:#1e293b;
  --accent:#0284c7;
  --accent-2:#0ea5e9;
  --success:#15803d;
  --danger:#dc2626;
  --chip-bg:#e2e8f0;
  --chip-fg:#334155;
  --log-bg:#f1f5f9;
  --log-border:#d8e3ed;
  --input-bg:#ffffff;
  --input-border:#cbd5e1;
  --output-bg:#ffffff;
  --output-border:#d5dbe3;
  --code-fg:#0f172a;
  --input-focus-bg:#f8fcff;
  --focus-ring:rgba(2,132,199,0.25);
  --ghost-bg:#ffffff;
  --ghost-bg-hover:#f1f5f9;
  --ghost-bg-active:#e2e8f0;
  --ghost-border:#cbd5e1;
  --divider:#e2e8f0;
  --scroll-thumb:#334155;
  --scroll-thumb-hover:#475569;
  --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", "Courier New", monospace;
  --radius:12px;
}
[data-theme="dark"] {
  --bg:#0b1220;
  --bg-accent:#101b2e;
  --panel:#0f1724;
  --panel-border:#1f2b3a;
  --panel-shadow:0 4px 20px -4px rgba(0,0,0,0.55),0 2px 4px rgba(0,0,0,0.4);
  --muted:#94a3b8;
  --text:#e6eef6;
  --accent:#0ea5b7;
  --accent-2:#0369a1;
  --success:#16a34a;
  --danger:#ef4444;
  --chip-bg:#1e293b;
  --chip-fg:#cbd5e1;
  --log-bg:#162232;
  --log-border:#223248;
  --input-bg:#1e293b;
  --input-border:#2f4154;
  --output-bg:#0b1626;
  --output-border:#1f2b3a;
  --code-fg:#f1f5f9;
  --input-focus-bg:#112031;
  --focus-ring:rgba(14,165,183,0.35);
  --ghost-bg:#1e293b;
  --ghost-bg-hover:#253242;
  --ghost-bg-active:#2d3b4d;
  --ghost-border:#2f4154;
  --divider:#1f2b3a;
  --scroll-thumb:#2f4154;
  --scroll-thumb-hover:#40566d;
}
html, body { height:100%; margin:0; background:linear-gradient(180deg,var(--bg) 0%, var(--bg-accent) 70%); color:var(--text); -webkit-font-smoothing:antialiased; }
body { font-size:14px; line-height:1.4; }
.wrap { max-width:1220px; margin:28px auto 48px; padding:0 28px; box-sizing:border-box; }
header { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:22px; }
.brand { display:flex; gap:14px; align-items:center; }
h1 { font-size:22px; margin:0 0 2px; letter-spacing:-0.4px; font-weight:600; }
p.lead { margin:0; color:var(--muted); font-size:13px; }
.grid { display:grid; grid-template-columns: 1fr 430px; gap:22px; align-items:start; }
.panel { background:var(--panel); border:1px solid var(--panel-border); border-radius:var(--radius); padding:18px 18px 20px; box-shadow:var(--panel-shadow); }
.panel h3 { font-size:15px; font-weight:600; letter-spacing:-0.2px; color:var(--text); }
.row { display:flex; gap:12px; align-items:center; margin-bottom:12px; flex-wrap:wrap; }
label { font-size:12px; text-transform:uppercase; letter-spacing:0.5px; color:var(--muted); font-weight:600; display:block; margin-bottom:4px; }
input[type="text"], input[type="number"], textarea, select { background:var(--input-bg); border:1px solid var(--input-border); color:var(--text); padding:10px 12px; border-radius:8px; outline:none; width:100%; box-sizing:border-box; font-size:14px; transition:border-color .15s, box-shadow .15s, background .15s, color .15s; }
input:focus, textarea:focus, select:focus { border-color:var(--accent); box-shadow:0 0 0 3px var(--focus-ring); background:var(--input-focus-bg); }
textarea { resize:vertical; min-height:96px; font-family:var(--mono); line-height:1.35; }
.controls { display:flex; gap:8px; flex-wrap:wrap; }
.btn { background:linear-gradient(90deg,var(--accent),var(--accent-2)); color:#ffffff; border:none; padding:10px 16px; border-radius:10px; cursor:pointer; font-weight:600; font-size:13px; letter-spacing:0.3px; box-shadow:0 2px 4px rgba(0,0,0,0.05), 0 4px 14px -6px rgba(2,132,199,0.55); display:inline-flex; align-items:center; gap:6px; transition:box-shadow .18s, transform .18s, filter .18s; }
.btn:hover { box-shadow:0 3px 6px rgba(0,0,0,0.08), 0 6px 18px -6px rgba(2,132,199,0.55); }
.btn:active { transform:translateY(1px); }
.btn:focus-visible { outline:2px solid var(--accent-2); outline-offset:2px; }
.btn.ghost { background:var(--ghost-bg); color:var(--accent); border:1px solid var(--ghost-border); box-shadow:none; }
.btn.ghost:hover { background:var(--ghost-bg-hover); }
.btn.ghost:active { background:var(--ghost-bg-active); }
.small { padding:7px 12px; font-size:12px; }
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button { -webkit-appearance: none; margin:0; }
input[type=number] { -moz-appearance: textfield; appearance:textfield; }
.out-wrap { display:flex; flex-direction:column; gap:16px; height:calc(100vh - 150px); }
.output { background:var(--output-bg); color:var(--code-fg); border-radius:10px; padding:14px 14px 16px; font-family:var(--mono); font-size:13px; line-height:1.4; overflow:auto; border:1px solid var(--output-border); flex:1; min-height:140px; max-height:400px; white-space:pre-wrap; }
.output:focus-visible { outline:2px solid var(--accent-2); outline-offset:2px; }
.output::-webkit-scrollbar { width:8px; }
.output::-webkit-scrollbar-thumb { background-color:var(--scroll-thumb); border-radius:8px; }
.output::-webkit-scrollbar-thumb:hover { background-color:var(--scroll-thumb-hover); }
.status { display:flex; align-items:center; gap:10px; color:var(--muted); font-size:12px; margin-bottom:10px; flex-wrap:wrap; }
.chip { padding:6px 10px; border-radius:999px; background:var(--chip-bg); color:var(--chip-fg); font-weight:600; font-size:12px; line-height:1; letter-spacing:0.5px; }
.logo-img { width:52px; height:52px; border-radius:14px; object-fit:cover; box-shadow:0 4px 14px rgba(0,0,0,0.15); }
.footer { margin-top:10px; color:var(--muted); font-size:12px; text-align:center; }
.flex { display:flex; gap:10px; align-items:center; }
.right { justify-content:flex-end; }
hr { border:none; border-top:1px solid var(--divider); margin:16px 0 14px; }
pre { margin:0; }
code { font-family:var(--mono); font-size:13px; }
#logArea { background:var(--log-bg); border:1px solid var(--log-border); border-radius:8px; padding:8px 10px; line-height:1.35; color:var(--muted); }
#logArea::-webkit-scrollbar { width:8px; }
#logArea::-webkit-scrollbar-thumb { background:#c3ccd6; border-radius:6px; }
#logArea::-webkit-scrollbar-thumb:hover { background:#9aa5b1; }
.panel strong { font-size:13px; font-weight:600; letter-spacing:0.3px; color:var(--text); }
.panel .hints { color:var(--muted); font-size:12.5px; line-height:1.45; }
@media (max-width:1080px) { .grid { grid-template-columns:1fr; } .out-wrap { height:auto; } }
@media (max-width:640px) { header { flex-direction:column; align-items:flex-start; } .brand { width:100%; } }
.theme-toggle { position:relative; }
.theme-toggle .btn { background:linear-gradient(90deg,var(--accent-2),var(--accent)); padding:8px 14px; }
.theme-toggle .btn.ghost { background:var(--ghost-bg); color:var(--accent); }
body, .panel, .output, #logArea, .chip { transition: background-color .35s, color .35s, border-color .35s, box-shadow .35s; }
</style>
