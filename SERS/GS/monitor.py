"""
╔══════════════════════════════════════════════════════════╗
║   SPACE ENERGY MONITOR — FIAP Global Solution 2026       ║
║   Ciência da Computação · Energias Renováveis            ║
╚══════════════════════════════════════════════════════════╝

Sistema inteligente de monitoramento energético para missão
espacial experimental. Monitora temperatura, energia, potência,
sinal e captação solar em tempo real, com alertas automáticos
e tomada de decisão autônoma.
"""

import curses
import random
import time
import math
from dataclasses import dataclass, field
from collections import deque
from datetime import datetime
from typing import Optional

# ─── Constantes de limiar ────────────────────────────────────────────────────
TEMP_CRITICO   = 85.0
TEMP_ALERTA    = 70.0
ENERGIA_CRITICA = 15.0
ENERGIA_ALERTA  = 30.0
SINAL_CRITICO   = 20.0
SINAL_ALERTA    = 40.0

MAX_HISTORICO  = 30        # amostras mantidas por métrica
INTERVALO_SEG  = 1.5       # segundos entre cada ciclo de simulação

MODULOS = ["ALPHA", "BETA", "GAMMA", "DELTA"]

# ─── Paleta de cores (pares curses) ──────────────────────────────────────────
COR_TITULO    = 1
COR_NOMINAL   = 2
COR_ALERTA    = 3
COR_CRITICO   = 4
COR_INFO      = 5
COR_DESTAQUE  = 6
COR_APAGADO   = 7
COR_BORDA     = 8


# ─── Estruturas de dados ─────────────────────────────────────────────────────

@dataclass
class DadosModulo:
    nome: str
    temperatura: float = 45.0
    energia: float     = 70.0
    potencia: float    = 120.0
    sinal: float       = 90.0
    solar: float       = 60.0
    status: str        = "NOMINAL"
    hist_temp:    deque = field(default_factory=lambda: deque(maxlen=MAX_HISTORICO))
    hist_energia: deque = field(default_factory=lambda: deque(maxlen=MAX_HISTORICO))
    hist_potencia:deque = field(default_factory=lambda: deque(maxlen=MAX_HISTORICO))


@dataclass
class Alerta:
    nivel: str      # CRITICO | ALERTA | INFO
    modulo: str
    mensagem: str
    hora: str
    acao: Optional[str] = None


# ─── Lógica de simulação ─────────────────────────────────────────────────────

def _drift(valor: float, minv: float, maxv: float, passo: float) -> float:
    """Passeio aleatório suavizado."""
    return max(minv, min(maxv, valor + (random.random() - 0.5) * passo))


def calcular_status(temperatura, energia, sinal) -> str:
    if temperatura >= TEMP_CRITICO or energia <= ENERGIA_CRITICA or sinal <= SINAL_CRITICO:
        return "CRITICO"
    if temperatura >= TEMP_ALERTA or energia <= ENERGIA_ALERTA or sinal <= SINAL_ALERTA:
        return "ALERTA"
    return "NOMINAL"


def atualizar_modulo(mod: DadosModulo) -> DadosModulo:
    """Atualiza métricas do módulo com variação estocástica."""
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


# ─── Tomada de decisão autônoma ──────────────────────────────────────────────

def decisao_autonoma(mod: DadosModulo) -> Optional[str]:
    """
    Aplica regras de decisão baseadas nos parâmetros operacionais.
    Retorna a ação executada ou None se tudo estiver nominal.
    """
    if mod.energia <= ENERGIA_CRITICA:
        return ">> Modo emergência: subsistemas não-essenciais desligados."
    if mod.temperatura >= TEMP_CRITICO:
        return ">> Resfriamento emergencial acionado."
    if mod.sinal <= SINAL_CRITICO:
        return ">> Redirecionando para antena de backup."
    if mod.energia <= ENERGIA_ALERTA:
        return ">> Painéis solares adicionais ativados."
    if mod.temperatura >= TEMP_ALERTA:
        return ">> Ventilação aumentada para 80%."
    return None


def gerar_alerta(mod_ant: DadosModulo, mod_nov: DadosModulo) -> Optional[Alerta]:
    """Gera alerta quando há transição de status."""
    hora = datetime.now().strftime("%H:%M:%S")

    if mod_nov.status == "CRITICO" and mod_ant.status != "CRITICO":
        acao = decisao_autonoma(mod_nov)
        return Alerta(
            nivel="CRITICO", modulo=mod_nov.nome,
            mensagem=(f"FALHA CRÍTICA | Temp:{mod_nov.temperatura:.1f}°C "
                      f"Energia:{mod_nov.energia:.1f}% Sinal:{mod_nov.sinal:.1f}%"),
            hora=hora, acao=acao
        )
    if mod_nov.status == "ALERTA" and mod_ant.status == "NOMINAL":
        return Alerta(
            nivel="ALERTA", modulo=mod_nov.nome,
            mensagem=f"Parâmetros em zona de atenção — monitoramento intensificado.",
            hora=hora
        )
    if mod_nov.status == "NOMINAL" and mod_ant.status != "NOMINAL":
        return Alerta(
            nivel="INFO", modulo=mod_nov.nome,
            mensagem="Módulo retornou ao estado NOMINAL.",
            hora=hora
        )
    return None


# ─── Helpers de desenho ──────────────────────────────────────────────────────

def cor_status(status: str) -> int:
    return {
        "NOMINAL": curses.color_pair(COR_NOMINAL),
        "ALERTA":  curses.color_pair(COR_ALERTA),
        "CRITICO": curses.color_pair(COR_CRITICO),
    }.get(status, curses.color_pair(COR_INFO))


def cor_nivel(nivel: str) -> int:
    return {
        "CRITICO": curses.color_pair(COR_CRITICO),
        "ALERTA":  curses.color_pair(COR_ALERTA),
        "INFO":    curses.color_pair(COR_INFO),
    }.get(nivel, curses.color_pair(COR_INFO))


def barra(valor: float, maximo: float = 100.0, largura: int = 16) -> str:
    preenchido = int((valor / maximo) * largura)
    return "█" * preenchido + "░" * (largura - preenchido)


def sparkline(historico: deque, largura: int = 12) -> str:
    """Gera minigrágico de tendência usando blocos Unicode."""
    blocos = "  ▂▃▄▅▆▇█"
    dados = list(historico)[-largura:]
    if len(dados) < 2:
        return " " * largura
    mn, mx = min(dados), max(dados)
    rang = mx - mn or 1
    return "".join(blocos[int((v - mn) / rang * (len(blocos) - 1))] for v in dados)


def safe_addstr(win, y: int, x: int, texto: str, attr: int = 0):
    """Escreve no curses sem lançar exceção em bordas."""
    try:
        max_y, max_x = win.getmaxyx()
        if 0 <= y < max_y and 0 <= x < max_x:
            espaco = max_x - x - 1
            win.addstr(y, x, texto[:espaco], attr)
    except curses.error:
        pass


# ─── Renderização do dashboard ───────────────────────────────────────────────

def desenhar_cabecalho(win, tempo_missao: int, ciclo: int, modulos: list[DadosModulo]):
    max_y, max_x = win.getmaxyx()
    win.attron(curses.color_pair(COR_BORDA))
    win.hline(0, 0, "═", max_x)
    win.attroff(curses.color_pair(COR_BORDA))

    titulo = "⟁  SPACE ENERGY MONITOR  ·  FIAP Global Solution 2026"
    safe_addstr(win, 0, (max_x - len(titulo)) // 2, titulo,
                curses.color_pair(COR_TITULO) | curses.A_BOLD)

    h = tempo_missao // 3600
    m = (tempo_missao % 3600) // 60
    s = tempo_missao % 60
    met = f"MET {h:02d}:{m:02d}:{s:02d}  CIC #{ciclo:04d}"
    safe_addstr(win, 0, max_x - len(met) - 2, met, curses.color_pair(COR_APAGADO))

    # linha de métricas globais
    avg_e = sum(m.energia for m in modulos) / len(modulos)
    avg_t = sum(m.temperatura for m in modulos) / len(modulos)
    tot_p = sum(m.potencia for m in modulos)
    avg_s = sum(m.solar for m in modulos) / len(modulos)

    resumo = (f"  ENERGIA MÉDIA: {avg_e:5.1f}%   "
              f"TEMP MÉDIA: {avg_t:5.1f}°C   "
              f"POT. TOTAL: {tot_p:6.1f}W   "
              f"SOLAR MÉDIO: {avg_s:5.1f}%  ")
    safe_addstr(win, 1, 0, resumo, curses.color_pair(COR_INFO))

    win.attron(curses.color_pair(COR_BORDA))
    win.hline(2, 0, "─", max_x)
    win.attroff(curses.color_pair(COR_BORDA))


def desenhar_modulo(win, linha_ini: int, col_ini: int, mod: DadosModulo, largura: int = 38):
    """Desenha o painel de um único módulo."""
    cor = cor_status(mod.status)

    # cabeçalho do módulo
    titulo_mod = f" ▸ MÓDULO {mod.nome} "
    safe_addstr(win, linha_ini, col_ini, titulo_mod, cor | curses.A_BOLD)

    status_str = f"[{mod.status}]"
    safe_addstr(win, linha_ini, col_ini + largura - len(status_str) - 1,
                status_str, cor | curses.A_BOLD)

    win.attron(curses.color_pair(COR_BORDA))
    safe_addstr(win, linha_ini + 1, col_ini, "─" * largura, 0)
    win.attroff(curses.color_pair(COR_BORDA))

    # métricas
    dados = [
        ("TEMPERATURA", mod.temperatura, 110.0, "°C", mod.hist_temp,
         COR_CRITICO if mod.temperatura >= TEMP_CRITICO else
         COR_ALERTA  if mod.temperatura >= TEMP_ALERTA  else COR_NOMINAL),
        ("ENERGIA    ", mod.energia,     100.0, "% ",  mod.hist_energia,
         COR_CRITICO if mod.energia <= ENERGIA_CRITICA else
         COR_ALERTA  if mod.energia <= ENERGIA_ALERTA  else COR_NOMINAL),
        ("POTÊNCIA   ", mod.potencia,    300.0, "W ",  mod.hist_potencia,
         COR_DESTAQUE),
        ("SINAL COMM ", mod.sinal,       100.0, "% ",  deque(),
         COR_CRITICO if mod.sinal <= SINAL_CRITICO else
         COR_ALERTA  if mod.sinal <= SINAL_ALERTA  else COR_INFO),
        ("SOLAR      ", mod.solar,       100.0, "% ",  deque(),
         COR_ALERTA if mod.solar < 30 else COR_NOMINAL),
    ]

    for i, (label, valor, maximo, unid, hist, cor_id) in enumerate(dados):
        linha = linha_ini + 2 + i
        barra_str  = barra(valor, maximo, 14)
        spark_str  = sparkline(hist) if hist else " " * 12
        valor_str  = f"{valor:6.1f}{unid}"
        linha_txt  = f"  {label}: {valor_str} {barra_str}"
        safe_addstr(win, linha, col_ini, linha_txt, curses.color_pair(cor_id))
        safe_addstr(win, linha, col_ini + largura - 13, spark_str,
                    curses.color_pair(COR_APAGADO))

    # ação autônoma
    acao = decisao_autonoma(mod)
    if acao:
        safe_addstr(win, linha_ini + 7, col_ini,
                    f"  {acao[:largura - 2]}", curses.color_pair(COR_ALERTA))
    else:
        safe_addstr(win, linha_ini + 7, col_ini,
                    "  Sistema nominal — sem ações autônomas.",
                    curses.color_pair(COR_APAGADO))

    win.attron(curses.color_pair(COR_BORDA))
    safe_addstr(win, linha_ini + 8, col_ini, "─" * largura, 0)
    win.attroff(curses.color_pair(COR_BORDA))


def desenhar_alertas(win, linha_ini: int, max_x: int, alertas: list[Alerta]):
    safe_addstr(win, linha_ini, 0,
                " CENTRAL DE ALERTAS & DECISÕES AUTÔNOMAS ",
                curses.color_pair(COR_TITULO) | curses.A_BOLD)
    win.attron(curses.color_pair(COR_BORDA))
    win.hline(linha_ini + 1, 0, "─", max_x)
    win.attroff(curses.color_pair(COR_BORDA))

    if not alertas:
        safe_addstr(win, linha_ini + 2, 2,
                    "✓  Todos os sistemas nominais — nenhum alerta ativo.",
                    curses.color_pair(COR_NOMINAL))
        return

    icones = {"CRITICO": "⚠", "ALERTA": "△", "INFO": "ℹ"}
    max_y = win.getmaxyx()[0]
    for i, alerta in enumerate(alertas):
        if linha_ini + 2 + i * 2 + 1 >= max_y - 1:
            break
        icone = icones.get(alerta.nivel, "·")
        linha_a = f"  {icone} [{alerta.hora}] MOD {alerta.modulo:5s} | {alerta.mensagem}"
        safe_addstr(win, linha_ini + 2 + i * 2, 0,
                    linha_a[:max_x - 1], cor_nivel(alerta.nivel) | curses.A_BOLD)
        if alerta.acao:
            safe_addstr(win, linha_ini + 3 + i * 2, 4,
                        alerta.acao[:max_x - 5], curses.color_pair(COR_ALERTA))


def desenhar_rodape(win):
    max_y, max_x = win.getmaxyx()
    win.attron(curses.color_pair(COR_BORDA))
    win.hline(max_y - 1, 0, "═", max_x)
    win.attroff(curses.color_pair(COR_BORDA))
    rodape = "  [Q] Sair   [P] Pausar/Retomar   [L] Limpar alertas  "
    safe_addstr(win, max_y - 1, 0, rodape, curses.color_pair(COR_APAGADO))


# ─── Loop principal ──────────────────────────────────────────────────────────

def main(stdscr):
    # Inicializa cores
    curses.start_color()
    
    # Define a cor de fundo padrão com fallback para o Windows/PowerShell
    bg_color = -1
    try:
        curses.use_default_colors()
    except curses.error:
        # Se falhar (retornar ERR), usa PRETO no lugar do fundo transparente (-1)
        bg_color = curses.COLOR_BLACK

    curses.init_pair(COR_TITULO,   curses.COLOR_CYAN,    bg_color)
    curses.init_pair(COR_NOMINAL,  curses.COLOR_GREEN,   bg_color)
    curses.init_pair(COR_ALERTA,   curses.COLOR_YELLOW,  bg_color)
    curses.init_pair(COR_CRITICO,  curses.COLOR_RED,     bg_color)
    curses.init_pair(COR_INFO,     curses.COLOR_BLUE,    bg_color)
    curses.init_pair(COR_DESTAQUE, curses.COLOR_MAGENTA, bg_color)
    curses.init_pair(COR_APAGADO,  curses.COLOR_WHITE,   bg_color)
    curses.init_pair(COR_BORDA,    curses.COLOR_CYAN,    bg_color)

    # ─── CORREÇÃO APLICADA AQUI ──────────────────────────────────────────────
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    # ─────────────────────────────────────────────────────────────────────────
    
    stdscr.nodelay(True)
    stdscr.keypad(True)

    # Estado inicial
    modulos = [
        DadosModulo(nome=nome, temperatura=45.0 + i * 5,
                    energia=70.0 - i * 4,
                    potencia=120.0 + i * 15,
                    sinal=90.0 - i * 3,
                    solar=60.0 + i * 8)
        for i, nome in enumerate(MODULOS)
    ]
    alertas: list[Alerta] = []
    ciclo = 0
    tempo_missao = 0
    pausado = False
    ultimo_tick = time.time()

    while True:
        # Input não-bloqueante
        tecla = stdscr.getch()
        if tecla in (ord("q"), ord("Q")):
            break
        elif tecla in (ord("p"), ord("P")):
            pausado = not pausado
        elif tecla in (ord("l"), ord("L")):
            alertas.clear()

        agora = time.time()
        if not pausado and (agora - ultimo_tick) >= INTERVALO_SEG:
            ultimo_tick = agora
            ciclo += 1
            tempo_missao += int(INTERVALO_SEG)

            novos_modulos = []
            for mod in modulos:
                import copy
                mod_ant = copy.copy(mod)
                mod = atualizar_modulo(mod)
                alerta = gerar_alerta(mod_ant, mod)
                if alerta:
                    alertas.insert(0, alerta)
                    if len(alertas) > 15:
                        alertas.pop()
                novos_modulos.append(mod)
            modulos = novos_modulos

        # Renderização
        stdscr.erase()
        max_y, max_x = stdscr.getmaxyx()

        desenhar_cabecalho(stdscr, tempo_missao, ciclo, modulos)

        # 4 módulos em grade 2×2
        col_l = 0
        col_r = max_x // 2
        larg  = max(36, max_x // 2 - 2)

        for i, mod in enumerate(modulos):
            col   = col_l if i % 2 == 0 else col_r
            linha = 3 + (i // 2) * 10
            desenhar_modulo(stdscr, linha, col, mod, larg)

        # Alertas abaixo dos módulos
        linha_alertas = 3 + 2 * 10 + 1
        if linha_alertas < max_y - 3:
            desenhar_alertas(stdscr, linha_alertas, max_x, alertas)

        if pausado:
            msg = "  ⏸  SIMULAÇÃO PAUSADA — pressione [P] para retomar  "
            safe_addstr(stdscr, max_y - 2, (max_x - len(msg)) // 2,
                        msg, curses.color_pair(COR_ALERTA) | curses.A_BOLD)

        desenhar_rodape(stdscr)
        stdscr.refresh()
        time.sleep(0.05)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    print("\nSistema encerrado. Até a próxima missão! 🚀")