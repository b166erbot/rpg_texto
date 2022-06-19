import curses
from time import sleep

formas = (
    "▲▼◀▶◢◣◥◤△▽◿◺◹◸▴▾◂▸▵▿◃▹◁▷◅▻◬⟁⧋⧊⊿∆∇◭◮⧩⧨⌔⟐◇◆◈⬖⬗⬘⬙⬠⬡⎔⋄◊⧫⬢⬣▰▪◼▮◾▗▖■∎▃▄▅▆▇"
    "█▌▐▍▎▉▊▋❘❙❚▀▘▝▙▚▛▜▟▞░▒▓▂▁▬▔▫▯▭▱◽□◻▢⊞⊡⊟⊠▣▤▥▦⬚▧▨▩⬓◧⬒◨◩◪⬔⬕❏❐❑❒⧈◰◱◳◲◫⧇⧅⧄⍁⍂⟡⧉"
    "⚬○⚪◌◍◎◯❍◉⦾⊙⦿⊜⊖⊘⊚⊛⊝●⚫⦁◐◑◒◓◔◕⦶⦸◵◴◶◷⊕⊗⦇⦈⦉⦊❨❩⸨⸩◖◗❪❫❮❯❬❭❰❱⊏⊐⊑⊒◘◙◚◛◜◝◞◟◠◡⋒⋓⋐⋑"
    "⥰╰╮╭╯⌒⥿⥾⥽⥼⥊⥋⥌⥍⥎⥐⥑⥏╳✕⤫⤬╱╲⧸⧹⌓◦❖✖✚✜⧓⧗⧑⧒⧖_⚊╴╼╾‐⁃‑‒-–⎯—―╶╺╸─━┄┅┈┉╌╍═≣≡"
    "☰☱☲☳☴☵☶☷╵╷╹╻│▕▏┃┆┇┊╎┋╿╽⌞⌟⌜⌝⌊⌋⌈⌉⌋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┳"
    "┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╏║╔╒╓╕╖╗╚╘╙╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬"
)


def formatar_status(personagem):
    """Função que arruma os caracters para a magia, vida e stamina."""
    nome, vida = personagem.nome, personagem.status["vida"]
    magia, stamina = personagem.status["magia"], personagem.status["stamina"]
    texto = f"{nome} [{personagem.classe}]: "
    porcentagem = magia  # caso a magia aumentar, fazer o calculo da porcentagem
    blocos_com_barras = _formatar_barras(magia, 100)
    texto += f"{blocos_com_barras} {porcentagem:3d}% "
    porcentagem = int((vida * 100) / personagem.vida_maxima)
    blocos_com_barras = _formatar_barras(vida, personagem.vida_maxima, True)
    texto += f"{blocos_com_barras} {porcentagem:3d}%  "
    blocos_com_barras = _formatar_barras(stamina, 100)
    porcentagem = (
        stamina  # caso a stamina aumentar, fazer o calculo da porcentagem
    )
    return texto + f"{blocos_com_barras} {porcentagem:3d}%"


def _formatar_barras(atributo, vida_maxima, vida=False):
    """Função que cria as barras de magia, vida e stamina."""
    quantidade_blocos = 10 if vida else 5
    porcentagem = int(atributo / vida_maxima * quantidade_blocos)
    blocos = formas[53] * porcentagem
    blocos += (quantidade_blocos - len(blocos)) * formas[48]
    return f"{formas[191]}{blocos}{formas[192]}"


curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)


cores = {
    x: y
    for y, x in enumerate(
        ["verde", "cyan", "vermelho", "magenta", "amarelo"], 1
    )
}


def colorir(cor: str) -> int:
    """Função que retorna um número da cor correspondente."""
    return cores[cor]


class Imprimir:
    _tela = curses.newwin(20, 80, 4, 0)
    _tela2 = curses.newwin(4, 80)
    _tela2.nodelay(True)
    _tela2.box()
    _tela2.refresh()

    def imprimir(self, texto: str, cor: str = False):
        """Método que digita o texto na tela debaixo."""
        if bool(cor):
            self._tela.addstr(texto, curses.color_pair(colorir(cor)))
        else:
            self._tela.addstr(texto)
        self._tela.refresh()

    def imprimir_combate(self, texto, local):
        """Método que imprime o texto na tela de cima com uma caixa quadrada."""
        self._tela2.addstr(local, 2, texto)  # linhas, colunas
        self._tela2.box()
        self._tela2.refresh()

    def limpar_tela(self):
        """Método que limpa a tela de baixo."""
        self._tela.erase()
        self._tela.refresh()

    def limpar_tela2(self):
        """Método que limpa a tela de cima com uma caixa quadrada em volta."""
        self._tela2.erase()
        self._tela2.box()
        self._tela2.refresh()

    def obter_caracter(self):
        """Método que obtem um caracter do usuário."""
        return self._tela2.getch()

    def obter_string(self):
        """Método que obtem uma frase do usuário."""
        return self._tela.getstr().decode()

    def sem_delay(self):
        """Método que tira o delay."""
        self._tela2.nodelay(True)

    def com_delay(self):
        """Método que poim o delay."""
        self._tela2.nodelay(False)


tela = Imprimir()


def efeito_digitando(texto: str, dormir: float = 0.04):
    """Função que imprime na tela uma mensagem parecendo que está digitando."""
    for a in texto:
        tela.imprimir(a)
        sleep(dormir)
    tela.imprimir("\n")
