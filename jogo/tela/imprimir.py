from re import sub
from itertools import cycle
from time import sleep

from colored import fg, attr
import curses


formas = (
    '▲▼◀▶◢◣◥◤△▽◿◺◹◸▴▾◂▸▵▿◃▹◁▷◅▻◬⟁⧋⧊⊿∆∇◭◮⧩⧨⌔⟐◇◆◈⬖⬗⬘⬙⬠⬡⎔⋄◊⧫⬢⬣▰▪◼▮◾▗▖■∎▃▄▅▆▇'
    '█▌▐▍▎▉▊▋❘❙❚▀▘▝▙▚▛▜▟▞░▒▓▂▁▬▔▫▯▭▱◽□◻▢⊞⊡⊟⊠▣▤▥▦⬚▧▨▩⬓◧⬒◨◩◪⬔⬕❏❐❑❒⧈◰◱◳◲◫⧇⧅⧄⍁⍂⟡⧉'
    '⚬○⚪◌◍◎◯❍◉⦾⊙⦿⊜⊖⊘⊚⊛⊝●⚫⦁◐◑◒◓◔◕⦶⦸◵◴◶◷⊕⊗⦇⦈⦉⦊❨❩⸨⸩◖◗❪❫❮❯❬❭❰❱⊏⊐⊑⊒◘◙◚◛◜◝◞◟◠◡⋒⋓⋐⋑'
    '⥰╰╮╭╯⌒⥿⥾⥽⥼⥊⥋⥌⥍⥎⥐⥑⥏╳✕⤫⤬╱╲⧸⧹⌓◦❖✖✚✜⧓⧗⧑⧒⧖_⚊╴╼╾‐⁃‑‒-–⎯—―╶╺╸─━┄┅┈┉╌╍═≣≡'
    '☰☱☲☳☴☵☶☷╵╷╹╻│▕▏┃┆┇┊╎┋╿╽⌞⌟⌜⌝⌊⌋⌈⌉⌋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┳'
    '┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╏║╔╒╓╕╖╗╚╘╙╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬'
)


def formatar_status(personagem):
    nome, vida = personagem.nome, personagem.status['vida']
    magia, stamina = personagem.status['magia'], personagem.status['stamina']
    texto = f"{nome} [{personagem.classe}]: "
    blocos_com_barras = _formatar(magia, personagem.vida_maxima)
    texto += f"{blocos_com_barras} {magia:3d}% "
    blocos_com_barras = _formatar(vida, personagem.vida_maxima, True)
    texto += f"{blocos_com_barras} {vida:3d}%  "
    blocos_com_barras = _formatar(stamina, personagem.vida_maxima)
    return texto + f"{blocos_com_barras} {stamina:3d}%"


def _formatar(atributo, vida_maxima, vida=False):
    quantidade_blocos = 10 if vida else 5
    p = int(atributo / vida_maxima * quantidade_blocos)
    porcentagem = p + 1 if p < p else p
    blocos = formas[53] * porcentagem
    blocos += (quantidade_blocos - len(blocos)) * formas[48]
    return f"{formas[191]}{blocos}{formas[192]}"


class Imprimir:
    _tela = curses.newwin(20, 80, 4, 0)
    _tela2 = curses.newwin(4, 80)
    _tela2.nodelay(True)
    _tela2.box()
    _tela2.refresh()

    def imprimir(self, texto: str):
        self._tela.addstr(texto)
        self._tela.refresh()

    def imprimir_combate(self, texto, local):
        self._tela2.addstr(local, 0, texto)  # linhas, colunas
        self._tela2.box()
        self._tela2.refresh()

    def limpar_tela(self):
        self._tela.erase()
        self._tela.refresh()

    def limpar_tela2(self):
        self._tela2.erase()
        self._tela2.box()
        self._tela2.refresh()

    def obter_caracter(self):
        return self._tela2.getch()

    def obter_string(self):
        return self._tela.getstr()

    def sem_delay(self):
        self._tela2.nodelay(True)

    def com_delay(self):
        self._tela2.nodelay(False)


def efeito_digitando(texto: str, dormir: float = 0.04):
    tela = Imprimir()
    for a in texto:
        tela.imprimir(a)
        sleep(dormir)
    tela.imprimir('\n')
