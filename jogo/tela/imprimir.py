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

# cores = {
#     'vermelho': fg('red'), 'verde': fg('green'), 'amarelo': fg('yellow'),
#     'roxo': fg('purple_1a'), 'azul': fg('blue'), 'magenta': fg('magenta'),
#     'cyan': fg('cyan'), 'cinza_escuro': fg('dark_gray'), 'preto': fg('grey_0'),
#     'turquesa': fg('pale_turquoise_1'), 'laranja_escuro': fg('dark_orange')}


# def colorir(texto: str, cor: str) -> str:
#     """
#     Função que retorna um texto colorido.
#     [args]
#         - texto: texto à ser colorido.
#         - cor:   cor que irá colorir o texto.
#
#     cores: vermelho, verde, amarelo, roxo, azul, magenta, cyan, cinza_escuro,
#            preto, turquesa, laranja_escuro.
#     """
#
#     texto = sub(r'\x1b\[0m', cores[cor], texto)
#     return f"{cores[cor]}{texto}{attr(0)}"


def formatar_status(personagem):
    nome, vida = personagem.nome, personagem.status['vida']
    magia, stamina = personagem.status['magia'], personagem.status['stamina']
    texto = f"{nome} [{personagem.classe}]: "
    blocos_com_barras = _formatar(magia)
    texto += f"{blocos_com_barras} {magia:3d}% "
    blocos_com_barras = _formatar(vida, True)
    texto += f"{blocos_com_barras} {vida:3d}%  "
    blocos_com_barras = _formatar(stamina)
    return texto + f"{blocos_com_barras} {stamina:3d}%"


def _formatar(atributo, vida=False):
    quantidade_blocos = 10 if vida else 5
    p = int(atributo / 100 * quantidade_blocos)
    porcentagem = p + 1 if p < p else p
    blocos = formas[53] * porcentagem
    blocos += (quantidade_blocos - len(blocos)) * formas[48]
    return f"{formas[191]}{blocos}{formas[192]}"


class Imprimir:
    _tela = curses.newwin(22, 80, 2, 0)
    _tela2 = curses.newwin(2, 80)
    _tela2.nodelay(True)

    def imprimir(self, texto: str):
        self._tela.addstr(texto)
        self._tela.refresh()

    def imprimir_combate(self, texto, personagem):
        self._tela2.addstr(personagem.local_imprimir, 0, texto)
        self._tela2.refresh()

    def limpar_tela(self):
        self._tela.erase()
        self._tela.refresh()

    def limpar_tela2(self):
        self._tela2.erase()
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
