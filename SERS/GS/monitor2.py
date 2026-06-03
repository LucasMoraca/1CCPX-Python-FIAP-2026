"""
╔══════════════════════════════════════════════════════════╗
║   SPACE ENERGY MONITOR — FIAP Global Solution 2026       ║
║   Ciência da Computação · Energias Renováveis            ║
╚══════════════════════════════════════════════════════════╝

Abre um dashboard HTML no navegador com atualização em tempo real
via Server-Sent Events (SSE). Zero dependências externas.

Uso:
    python3 monitor.py
"""

import json
import math
import random
import threading
import time
import webbrowser
from dataclasses import dataclass, field
from collections import deque
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

# ─── Configurações ───────────────────────────────────────────────────────────
PORT            = 8765
INTERVALO_SEG   = 1.5
MAX_HISTORICO   = 30
MODULOS         = ["ALPHA", "BETA", "GAMMA", "DELTA"]

TEMP_CRITICO    = 85.0
TEMP_ALERTA     = 70.0
ENERGIA_CRITICA = 15.0
ENERGIA_ALERTA  = 30.0
SINAL_CRITICO   = 20.0
SINAL_ALERTA    = 40.0

# ─── Estado global compartilhado ─────────────────────────────────────────────
estado = {
    "modulos": [],
    "alertas": [],
    "ciclo": 0,
    "tempo_missao": 0,
    "pausado": False,
}
estado_lock = threading.Lock()
sse_clients = []
sse_lock = threading.Lock()

# ─── Dataclasses ─────────────────────────────────────────────────────────────
@dataclass
class DadosModulo:
    nome: str
    temperatura: float = 45.0
    energia: float     = 70.0
    potencia: float    = 120.0
    sinal: float       = 90.0
    solar: float       = 60.0
    status: str        = "NOMINAL"
    hist_temp:     deque = field(default_factory=lambda: deque(maxlen=MAX_HISTORICO))
    hist_energia:  deque = field(default_factory=lambda: deque(maxlen=MAX_HISTORICO))
    hist_potencia: deque = field(default_factory=lambda: deque(maxlen=MAX_HISTORICO))

    def to_dict(self):
        return {
            "nome": self.nome,
            "temperatura": round(self.temperatura, 1),
            "energia":     round(self.energia, 1),
            "potencia":    round(self.potencia, 1),
            "sinal":       round(self.sinal, 1),
            "solar":       round(self.solar, 1),
            "status":      self.status,
            "hist_temp":     list(self.hist_temp),
            "hist_energia":  list(self.hist_energia),
            "hist_potencia": list(self.hist_potencia),
        }

@dataclass
class Alerta:
    nivel: str
    modulo: str
    mensagem: str
    hora: str
    acao: Optional[str] = None

    def to_dict(self):
        return {"nivel": self.nivel, "modulo": self.modulo,
                "mensagem": self.mensagem, "hora": self.hora, "acao": self.acao}

# ─── Simulação ────────────────────────────────────────────────────────────────
def _drift(v, mn, mx, passo):
    return max(mn, min(mx, v + (random.random() - 0.5) * passo))

def calcular_status(temp, energia, sinal):
    if temp >= TEMP_CRITICO or energia <= ENERGIA_CRITICA or sinal <= SINAL_CRITICO:
        return "CRITICO"
    if temp >= TEMP_ALERTA or energia <= ENERGIA_ALERTA or sinal <= SINAL_ALERTA:
        return "ALERTA"
    return "NOMINAL"

def decisao_autonoma(mod: DadosModulo) -> Optional[str]:
    if mod.energia <= ENERGIA_CRITICA:
        return "Modo emergência: subsistemas não-essenciais desligados."
    if mod.temperatura >= TEMP_CRITICO:
        return "Resfriamento emergencial acionado."
    if mod.sinal <= SINAL_CRITICO:
        return "Redirecionando para antena de backup."
    if mod.energia <= ENERGIA_ALERTA:
        return "Painéis solares adicionais ativados."
    if mod.temperatura >= TEMP_ALERTA:
        return "Ventilação aumentada para 80%."
    return None

def atualizar_modulo(mod: DadosModulo) -> DadosModulo:
    mod.hist_temp.append(mod.temperatura)
    mod.hist_energia.append(mod.energia)
    mod.hist_potencia.append(mod.potencia)
    mod.temperatura = _drift(mod.temperatura, 10.0, 110.0, 3.5)
    mod.energia     = max(0.0, min(100.0, mod.energia + (random.random() - 0.52) * 2.5))
    mod.potencia    = _drift(mod.potencia, 40.0, 300.0, 12.0)
    mod.sinal       = _drift(mod.sinal, 0.0, 100.0, 4.0)
    mod.solar       = _drift(mod.solar, 0.0, 100.0, 5.0)
    mod.status      = calcular_status(mod.temperatura, mod.energia, mod.sinal)
    return mod

def gerar_alerta(ant: DadosModulo, nov: DadosModulo) -> Optional[Alerta]:
    hora = datetime.now().strftime("%H:%M:%S")
    if nov.status == "CRITICO" and ant.status != "CRITICO":
        return Alerta("CRITICO", nov.nome,
            f"Falha crítica | Temp:{nov.temperatura:.1f}°C Energia:{nov.energia:.1f}% Sinal:{nov.sinal:.1f}%",
            hora, decisao_autonoma(nov))
    if nov.status == "ALERTA" and ant.status == "NOMINAL":
        return Alerta("ALERTA", nov.nome,
            "Parâmetros em zona de atenção — monitoramento intensificado.", hora)
    if nov.status == "NOMINAL" and ant.status != "NOMINAL":
        return Alerta("INFO", nov.nome, "Módulo retornou ao estado NOMINAL.", hora)
    return None

# ─── Thread de simulação ──────────────────────────────────────────────────────
def loop_simulacao():
    import copy
    modulos = [
        DadosModulo(nome=n, temperatura=45+i*5, energia=70-i*4,
                    potencia=120+i*15, sinal=90-i*3, solar=60+i*8)
        for i, n in enumerate(MODULOS)
    ]
    while True:
        time.sleep(INTERVALO_SEG)
        with estado_lock:
            if estado["pausado"]:
                continue
            estado["ciclo"] += 1
            estado["tempo_missao"] += int(INTERVALO_SEG)
            novos = []
            for mod in modulos:
                ant = copy.copy(mod)
                mod = atualizar_modulo(mod)
                al  = gerar_alerta(ant, mod)
                if al:
                    estado["alertas"].insert(0, al.to_dict())
                    estado["alertas"] = estado["alertas"][:20]
                novos.append(mod)
            modulos = novos
            estado["modulos"] = [m.to_dict() for m in modulos]

        # Notifica todos os clientes SSE
        payload = json.dumps({
            "modulos":      estado["modulos"],
            "alertas":      estado["alertas"],
            "ciclo":        estado["ciclo"],
            "tempo_missao": estado["tempo_missao"],
            "pausado":      estado["pausado"],
        })
        with sse_lock:
            mortos = []
            for q in sse_clients:
                try:
                    q.append(payload)
                except Exception:
                    mortos.append(q)
            for q in mortos:
                sse_clients.remove(q)

# ─── HTML do dashboard ────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Space Energy Monitor</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:       #020c1b;
    --bg2:      #0a1628;
    --bg3:      #0d1f35;
    --border:   #1a3a5c;
    --cyan:     #00e5ff;
    --cyan-dim: #007a99;
    --green:    #00ff88;
    --yellow:   #ffcc00;
    --red:      #ff3c3c;
    --purple:   #c084fc;
    --text:     #cce0f5;
    --muted:    #3a5a7a;
    --font-mono:'Share Tech Mono', monospace;
    --font-hd:  'Orbitron', sans-serif;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:var(--font-mono);min-height:100vh;overflow-x:hidden}

  /* scanline overlay */
  body::after{content:'';position:fixed;inset:0;background:repeating-linear-gradient(
    0deg,transparent,transparent 2px,rgba(0,0,0,.07) 2px,rgba(0,0,0,.07) 4px);
    pointer-events:none;z-index:9999}

  /* TOP BAR */
  header{
    display:flex;align-items:center;justify-content:space-between;
    padding:14px 28px;
    background:linear-gradient(90deg,#020c1b,#061525,#020c1b);
    border-bottom:1px solid var(--border);
    position:sticky;top:0;z-index:100;
  }
  .logo{display:flex;align-items:center;gap:14px}
  .logo-dot{width:10px;height:10px;border-radius:50%;background:var(--cyan);
    box-shadow:0 0 10px var(--cyan);animation:blink 2s infinite}
  .logo-title{font-family:var(--font-hd);font-size:15px;font-weight:900;
    letter-spacing:.18em;color:var(--cyan);text-shadow:0 0 20px var(--cyan-dim)}
  .logo-sub{font-size:10px;color:var(--muted);letter-spacing:.15em;margin-top:2px}

  .header-stats{display:flex;gap:28px;align-items:center}
  .hstat{text-align:center}
  .hstat-label{font-size:9px;color:var(--muted);letter-spacing:.15em;text-transform:uppercase}
  .hstat-value{font-size:16px;font-weight:700;font-family:var(--font-hd);margin-top:2px}
  .met{color:var(--cyan)}
  .ev{color:var(--green)}
  .tv{color:var(--yellow)}
  .pv{color:var(--purple)}

  .header-controls{display:flex;gap:10px}
  .btn{
    font-family:var(--font-mono);font-size:11px;letter-spacing:.1em;
    padding:7px 18px;border-radius:4px;cursor:pointer;border:1px solid;
    transition:all .2s;text-transform:uppercase;
  }
  .btn-pause{background:#0d2b1a;border-color:#16a34a;color:#4ade80}
  .btn-pause:hover{background:#16a34a22}
  .btn-pause.paused{background:#2b0a0a;border-color:#dc2626;color:#f87171}
  .btn-clear{background:#0d1f35;border-color:var(--border);color:var(--muted)}
  .btn-clear:hover{border-color:var(--cyan);color:var(--cyan)}

  /* CRITICAL BANNER */
  #banner{
    display:none;padding:9px 28px;font-size:12px;font-weight:700;
    letter-spacing:.1em;text-align:center;animation:blink 1.2s infinite;
  }
  #banner.critico{background:#2b0a0a;border-bottom:1px solid var(--red);color:var(--red);display:block}
  #banner.alerta{background:#2b1e00;border-bottom:1px solid var(--yellow);color:var(--yellow);display:block}

  /* MAIN LAYOUT */
  .main{display:grid;grid-template-columns:1fr 320px;gap:0;height:calc(100vh - 65px)}

  /* MODULES GRID */
  .modules-area{padding:20px;overflow-y:auto;display:flex;flex-direction:column;gap:16px}
  .modules-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}

  /* MODULE CARD */
  .card{
    background:linear-gradient(135deg,var(--bg2) 0%,var(--bg) 100%);
    border:1px solid var(--border);border-radius:12px;padding:18px 20px;
    transition:border-color .4s,box-shadow .4s;position:relative;overflow:hidden;
  }
  .card::before{
    content:'';position:absolute;inset:0;border-radius:12px;
    background:radial-gradient(ellipse at top left,rgba(0,229,255,.04),transparent 60%);
    pointer-events:none;
  }
  .card.alerta{border-color:#d97706;box-shadow:0 0 20px #d9770622}
  .card.critico{border-color:var(--red);box-shadow:0 0 24px #ff3c3c33;animation:glowpulse 1.4s infinite}

  .card-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px}
  .card-name-label{font-size:9px;color:var(--muted);letter-spacing:.2em;margin-bottom:3px}
  .card-name{font-family:var(--font-hd);font-size:20px;font-weight:900;color:var(--text);letter-spacing:.1em}
  .badge{
    font-size:10px;font-weight:700;letter-spacing:.12em;padding:3px 12px;
    border-radius:99px;border:1px solid;
  }
  .badge.NOMINAL{background:#0d2b1a;border-color:#16a34a;color:#4ade80}
  .badge.ALERTA {background:#2b1e00;border-color:#d97706;color:#fbbf24}
  .badge.CRITICO{background:#2b0a0a;border-color:var(--red);color:var(--red);animation:blink 1s infinite}

  /* METRICS */
  .metrics{display:flex;flex-direction:column;gap:9px}
  .metric{display:flex;align-items:center;gap:10px}
  .metric-label{font-size:10px;color:var(--muted);letter-spacing:.1em;width:80px;flex-shrink:0}
  .metric-value{font-size:12px;font-weight:700;width:68px;flex-shrink:0;text-align:right}
  .bar-track{flex:1;height:6px;background:#0d1f35;border-radius:3px;overflow:hidden}
  .bar-fill{height:100%;border-radius:3px;transition:width .6s ease,background .4s}
  .spark-wrap{width:50px;flex-shrink:0}
  svg.spark{width:50px;height:20px;overflow:visible}

  /* ENERGY FLOW */
  .flow-panel{
    background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:16px 18px;
  }
  .section-label{font-size:9px;color:var(--muted);letter-spacing:.2em;text-transform:uppercase;margin-bottom:12px}
  .flow-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
  .flow-card{background:var(--bg);border-radius:8px;padding:10px 12px}
  .flow-name{font-size:9px;color:var(--muted);letter-spacing:.15em;margin-bottom:6px}
  .flow-bar-label{display:flex;justify-content:space-between;margin-bottom:3px}
  .flow-bar-label span:first-child{font-size:9px;color:var(--muted)}
  .flow-bar-label span:last-child{font-size:9px;font-weight:700}
  .flow-track{background:#0d1f35;border-radius:2px;height:5px;overflow:hidden;margin-bottom:6px}
  .flow-fill{height:100%;border-radius:2px;transition:width .6s ease}

  /* ALERTS PANEL */
  .alerts-panel{
    border-left:1px solid var(--border);background:#040e1a;
    display:flex;flex-direction:column;overflow:hidden;
  }
  .alerts-header{
    padding:14px 16px;border-bottom:1px solid var(--border);
    display:flex;justify-content:space-between;align-items:center;flex-shrink:0;
  }
  .alerts-title-label{font-size:9px;color:var(--muted);letter-spacing:.2em}
  .alerts-title{font-family:var(--font-hd);font-size:13px;font-weight:700;letter-spacing:.08em;color:var(--text)}
  .alerts-count{
    font-size:11px;padding:2px 10px;border-radius:99px;
    background:#2b0a0a;border:1px solid var(--red);color:var(--red);font-weight:700;
  }
  .alerts-list{flex:1;overflow-y:auto;padding:10px}
  .alerts-list::-webkit-scrollbar{width:3px;background:transparent}
  .alerts-list::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
  .alert-item{
    padding:9px 11px;border-radius:0 6px 6px 0;margin-bottom:7px;
    animation:slideIn .3s ease;
  }
  .alert-item.CRITICO{background:#1a0505;border-left:3px solid var(--red)}
  .alert-item.ALERTA {background:#1a1200;border-left:3px solid var(--yellow)}
  .alert-item.INFO   {background:#050f1f;border-left:3px solid #3b82f6}
  .alert-msg{font-size:11px;color:var(--text);line-height:1.4}
  .alert-acao{font-size:10px;color:var(--yellow);margin-top:4px;padding-top:4px;border-top:1px solid #2b1e00}
  .alert-meta{font-size:9px;color:var(--muted);margin-top:3px}

  .autonomous-panel{
    padding:12px 14px;border-top:1px solid var(--border);flex-shrink:0;
  }
  .autonomous-label{font-size:9px;color:var(--muted);letter-spacing:.2em;margin-bottom:8px}
  .autonomous-action{
    font-size:10px;color:var(--yellow);padding:6px 10px;
    background:#1a1200;border-radius:5px;border-left:2px solid var(--yellow);
    margin-bottom:5px;
  }
  .autonomous-ok{font-size:10px;color:var(--muted)}

  /* ANIMATIONS */
  @keyframes blink{0%,100%{opacity:1}50%{opacity:.4}}
  @keyframes glowpulse{0%,100%{box-shadow:0 0 24px #ff3c3c33}50%{box-shadow:0 0 40px #ff3c3c66}}
  @keyframes slideIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}

  .no-alerts{text-align:center;color:var(--muted);margin-top:50px;font-size:12px}
  .no-alerts-icon{font-size:32px;margin-bottom:10px}
</style>
</head>
<body>

<header>
  <div class="logo">
    <div class="logo-dot"></div>
    <div>
      <div class="logo-title">⟁ SPACE ENERGY MONITOR</div>
      <div class="logo-sub">FIAP · GLOBAL SOLUTION 2026 · ENERGIAS RENOVÁVEIS</div>
    </div>
  </div>
  <div class="header-stats">
    <div class="hstat"><div class="hstat-label">MET</div><div class="hstat-value met" id="h-met">00:00:00</div></div>
    <div class="hstat"><div class="hstat-label">Energia Média</div><div class="hstat-value ev" id="h-energia">--%</div></div>
    <div class="hstat"><div class="hstat-label">Temp Média</div><div class="hstat-value tv" id="h-temp">--°C</div></div>
    <div class="hstat"><div class="hstat-label">Pot. Total</div><div class="hstat-value pv" id="h-pot">-- W</div></div>
    <div class="hstat"><div class="hstat-label">Ciclo</div><div class="hstat-value met" id="h-ciclo">#0000</div></div>
  </div>
  <div class="header-controls">
    <button class="btn btn-pause" id="btn-pause" onclick="togglePause()">⏸ PAUSAR</button>
    <button class="btn btn-clear" onclick="clearAlerts()">✕ ALERTAS</button>
  </div>
</header>

<div id="banner"></div>

<div class="main">
  <div class="modules-area">
    <div class="modules-grid" id="modules-grid"></div>
    <div class="flow-panel">
      <div class="section-label">Fluxo Energético por Módulo</div>
      <div class="flow-grid" id="flow-grid"></div>
    </div>
  </div>

  <div class="alerts-panel">
    <div class="alerts-header">
      <div>
        <div class="alerts-title-label">CENTRAL DE</div>
        <div class="alerts-title">ALERTAS & DECISÕES</div>
      </div>
      <span class="alerts-count" id="alerts-count" style="display:none">0</span>
    </div>
    <div class="alerts-list" id="alerts-list">
      <div class="no-alerts"><div class="no-alerts-icon">✓</div>Todos os sistemas nominais</div>
    </div>
    <div class="autonomous-panel">
      <div class="autonomous-label">SISTEMA AUTÔNOMO · AÇÕES ATIVAS</div>
      <div id="autonomous-actions"><div class="autonomous-ok">Nenhuma ação necessária.</div></div>
    </div>
  </div>
</div>

<script>
const DECISIONS = {
  NOMINAL: null,
};

function fmtTime(s){
  const h=String(Math.floor(s/3600)).padStart(2,'0');
  const m=String(Math.floor((s%3600)/60)).padStart(2,'0');
  const sec=String(s%60).padStart(2,'0');
  return `${h}:${m}:${sec}`;
}

function barColor(label, value){
  if(label==='TEMPERATURA') return value>=85?'#ff3c3c':value>=70?'#ffcc00':'#00ff88';
  if(label==='ENERGIA')     return value<=15?'#ff3c3c':value<=30?'#ffcc00':'#00e5ff';
  if(label==='SINAL')       return value<=20?'#ff3c3c':value<=40?'#ffcc00':'#38bdf8';
  if(label==='SOLAR')       return value<30?'#ffcc00':'#fbbf24';
  return '#c084fc';
}

function makeSpark(data, color){
  if(!data||data.length<2) return '';
  const w=50,h=20;
  const mn=Math.min(...data), mx=Math.max(...data), rng=mx-mn||1;
  const pts=data.map((v,i)=>{
    const x=(i/(data.length-1))*w;
    const y=h-((v-mn)/rng)*h;
    return `${x},${y}`;
  }).join(' ');
  const last=data[data.length-1];
  const lx=w, ly=h-((last-mn)/rng)*h;
  return `<svg class="spark" viewBox="0 0 ${w} ${h}">
    <polyline points="${pts}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linejoin="round"/>
    <circle cx="${lx}" cy="${ly}" r="2.5" fill="${color}"/>
  </svg>`;
}

function renderModules(modulos){
  const grid = document.getElementById('modules-grid');
  const flow = document.getElementById('flow-grid');

  grid.innerHTML = modulos.map(mod => {
    const metrics = [
      {label:'TEMPERATURA', value:mod.temperatura, max:110, unit:'°C', hist:mod.hist_temp},
      {label:'ENERGIA',     value:mod.energia,     max:100, unit:'%',  hist:mod.hist_energia},
      {label:'POTÊNCIA',    value:mod.potencia,    max:300, unit:'W',  hist:mod.hist_potencia},
      {label:'SINAL',       value:mod.sinal,       max:100, unit:'%',  hist:[]},
      {label:'SOLAR',       value:mod.solar,       max:100, unit:'%',  hist:[]},
    ];
    const metricsHtml = metrics.map(m=>{
      const pct = Math.min(100,(m.value/m.max)*100);
      const col = barColor(m.label, m.value);
      const valColor = col;
      const spark = m.hist.length>1 ? makeSpark(m.hist, col) : '<span style="width:50px;display:inline-block"></span>';
      return `<div class="metric">
        <span class="metric-label">${m.label}</span>
        <span class="metric-value" style="color:${valColor}">${m.value.toFixed(1)}${m.unit}</span>
        <div class="bar-track"><div class="bar-fill" style="width:${pct}%;background:${col}"></div></div>
        <div class="spark-wrap">${spark}</div>
      </div>`;
    }).join('');

    return `<div class="card ${mod.status.toLowerCase()}">
      <div class="card-header">
        <div>
          <div class="card-name-label">MÓDULO</div>
          <div class="card-name">${mod.nome}</div>
        </div>
        <span class="badge ${mod.status}">${mod.status}</span>
      </div>
      <div class="metrics">${metricsHtml}</div>
    </div>`;
  }).join('');

  flow.innerHTML = modulos.map(mod => `
    <div class="flow-card">
      <div class="flow-name">MÓDULO ${mod.nome}</div>
      <div class="flow-bar-label"><span>Energia</span><span style="color:#00e5ff">${mod.energia.toFixed(0)}%</span></div>
      <div class="flow-track"><div class="flow-fill" style="width:${mod.energia}%;background:${barColor('ENERGIA',mod.energia)}"></div></div>
      <div class="flow-bar-label"><span>Solar</span><span style="color:#fbbf24">${mod.solar.toFixed(0)}%</span></div>
      <div class="flow-track"><div class="flow-fill" style="width:${mod.solar}%;background:#fbbf24"></div></div>
    </div>
  `).join('');
}

function renderAlerts(alertas){
  const list = document.getElementById('alerts-list');
  const count = document.getElementById('alerts-count');
  if(!alertas||alertas.length===0){
    list.innerHTML='<div class="no-alerts"><div class="no-alerts-icon">✓</div>Todos os sistemas nominais</div>';
    count.style.display='none';
    return;
  }
  count.style.display='inline';
  count.textContent=alertas.length;
  const icons={CRITICO:'⚠',ALERTA:'△',INFO:'ℹ'};
  list.innerHTML=alertas.map(a=>`
    <div class="alert-item ${a.nivel}">
      <div class="alert-msg">${icons[a.nivel]||'·'} <strong>MOD ${a.modulo}</strong> — ${a.mensagem}</div>
      ${a.acao?`<div class="alert-acao">→ ${a.acao}</div>`:''}
      <div class="alert-meta">${a.hora}</div>
    </div>
  `).join('');
}

function renderAutonomous(modulos){
  const el = document.getElementById('autonomous-actions');
  const actions = modulos.map(m=>{
    let acao=null;
    if(m.energia<=15) acao='Modo emergência: subsistemas não-essenciais desligados.';
    else if(m.temperatura>=85) acao='Resfriamento emergencial acionado.';
    else if(m.sinal<=20) acao='Redirecionando para antena de backup.';
    else if(m.energia<=30) acao='Painéis solares adicionais ativados.';
    else if(m.temperatura>=70) acao='Ventilação aumentada para 80%.';
    if(acao) return `<div class="autonomous-action"><span style="color:var(--muted)">${m.nome}: </span>${acao}</div>`;
    return '';
  }).filter(Boolean).join('');
  el.innerHTML = actions || '<div class="autonomous-ok">Nenhuma ação necessária.</div>';
}

function updateBanner(modulos){
  const banner = document.getElementById('banner');
  const crit = modulos.filter(m=>m.status==='CRITICO').length;
  const alert = modulos.filter(m=>m.status==='ALERTA').length;
  if(crit>0){
    banner.className='critico';
    banner.textContent=`⚠  ${crit} MÓDULO(S) EM ESTADO CRÍTICO — AÇÃO IMEDIATA NECESSÁRIA`;
  } else if(alert>0){
    banner.className='alerta';
    banner.textContent=`△  ${alert} MÓDULO(S) EM ALERTA — MONITORAMENTO INTENSIFICADO`;
  } else {
    banner.className='';
  }
}

function updateHeader(data){
  const mods = data.modulos;
  document.getElementById('h-met').textContent = fmtTime(data.tempo_missao);
  document.getElementById('h-ciclo').textContent = '#'+String(data.ciclo).padStart(4,'0');
  const avgE = mods.reduce((s,m)=>s+m.energia,0)/mods.length;
  const avgT = mods.reduce((s,m)=>s+m.temperatura,0)/mods.length;
  const totP = mods.reduce((s,m)=>s+m.potencia,0);
  document.getElementById('h-energia').textContent = avgE.toFixed(1)+'%';
  document.getElementById('h-temp').textContent    = avgT.toFixed(1)+'°C';
  document.getElementById('h-pot').textContent     = Math.round(totP)+' W';
  document.getElementById('h-energia').style.color = avgE<15?'#ff3c3c':avgE<30?'#ffcc00':'#00ff88';
  document.getElementById('h-temp').style.color    = avgT>=85?'#ff3c3c':avgT>=70?'#ffcc00':'#fbbf24';
}

// SSE
const evtSource = new EventSource('/events');
evtSource.onmessage = function(e){
  const data = JSON.parse(e.data);
  const btn = document.getElementById('btn-pause');
  if(data.pausado){
    btn.textContent='▶ RETOMAR'; btn.className='btn btn-pause paused';
  } else {
    btn.textContent='⏸ PAUSAR'; btn.className='btn btn-pause';
  }
  updateHeader(data);
  updateBanner(data.modulos);
  renderModules(data.modulos);
  renderAlerts(data.alertas);
  renderAutonomous(data.modulos);
};

function togglePause(){
  fetch('/pause',{method:'POST'});
}
function clearAlerts(){
  fetch('/clear',{method:'POST'});
}
</script>
</body>
</html>
"""

# ─── Servidor HTTP ────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # silencia logs do servidor

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode())

        elif self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            queue = []
            with sse_lock:
                sse_clients.append(queue)
            try:
                while True:
                    if queue:
                        msg = queue.pop(0)
                        self.wfile.write(f"data: {msg}\n\n".encode())
                        self.wfile.flush()
                    else:
                        time.sleep(0.05)
            except Exception:
                pass
            finally:
                with sse_lock:
                    if queue in sse_clients:
                        sse_clients.remove(queue)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/pause":
            with estado_lock:
                estado["pausado"] = not estado["pausado"]
            self.send_response(200)
            self.end_headers()
        elif self.path == "/clear":
            with estado_lock:
                estado["alertas"] = []
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


def iniciar_servidor():
    server = HTTPServer(("localhost", PORT), Handler)
    server.serve_forever()


# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n  ⟁  SPACE ENERGY MONITOR — FIAP Global Solution 2026")
    print(f"  {'─'*50}")
    print(f"  Iniciando servidor em http://localhost:{PORT}")
    print(f"  Abrindo dashboard no navegador...")
    print(f"  {'─'*50}")
    print(f"  Pressione Ctrl+C para encerrar.\n")

    t_sim = threading.Thread(target=loop_simulacao, daemon=True)
    t_sim.start()

    t_srv = threading.Thread(target=iniciar_servidor, daemon=True)
    t_srv.start()

    time.sleep(0.8)
    webbrowser.open(f"http://localhost:{PORT}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Sistema encerrado. Até a próxima missão! 🚀\n")