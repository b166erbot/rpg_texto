from re import sub
from itertools import cycle
from time import sleep

from colored import fg, attr
from screen import Screen


# tela = Screen()
formas = (
    '▲▼◀▶◢◣◥◤△▽◿◺◹◸▴▾◂▸▵▿◃▹◁▷◅▻◬⟁⧋⧊⊿∆∇◭◮⧩⧨⌔⟐◇◆◈⬖⬗⬘⬙⬠⬡⎔⋄◊⧫⬢⬣▰▪◼▮◾▗▖■∎▃▄▅▆▇'
    '█▌▐▍▎▉▊▋❘❙❚▀▘▝▙▚▛▜▟▞░▒▓▂▁▬▔▫▯▭▱◽□◻▢⊞⊡⊟⊠▣▤▥▦⬚▧▨▩⬓◧⬒◨◩◪⬔⬕❏❐❑❒⧈◰◱◳◲◫⧇⧅⧄⍁⍂⟡⧉'
    '⚬○⚪◌◍◎◯❍◉⦾⊙⦿⊜⊖⊘⊚⊛⊝●⚫⦁◐◑◒◓◔◕⦶⦸◵◴◶◷⊕⊗⦇⦈⦉⦊❨❩⸨⸩◖◗❪❫❮❯❬❭❰❱⊏⊐⊑⊒◘◙◚◛◜◝◞◟◠◡⋒⋓⋐⋑'
    '⥰╰╮╭╯⌒⥿⥾⥽⥼⥊⥋⥌⥍⥎⥐⥑⥏╳✕⤫⤬╱╲⧸⧹⌓◦❖✖✚✜⧓⧗⧑⧒⧖_⚊╴╼╾‐⁃‑‒-–⎯—―╶╺╸─━┄┅┈┉╌╍═≣≡'
    '☰☱☲☳☴☵☶☷╵╷╹╻│▕▏┃┆┇┊╎┋╿╽⌞⌟⌜⌝⌊⌋⌈⌉⌋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┳'
    '┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╏║╔╒╓╕╖╗╚╘╙╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬')
cores = {
    'vermelho': fg('red'), 'verde': fg('green'), 'amarelo': fg('yellow'),
    'roxo': fg('purple_1a'), 'azul': fg('blue'), 'magenta': fg('magenta'),
    'cyan': fg('cyan'), 'cinza_escuro': fg('dark_gray'), 'preto': fg('grey_0'),
    'turquesa': fg('pale_turquoise_1'), 'laranja_escuro': fg('dark_orange')}


def colorir(texto: str, cor: str) -> str:
    """
    Função que retorna um texto colorido.
    [args]
        - texto: texto à ser colorido.
        - cor:   cor que irá colorir o texto.

    cores: vermelho, verde, amarelo, roxo, azul, magenta, cyan, cinza_escuro,
           preto, turquesa, laranja_escuro.
    """

    texto = sub(r'\x1b\[0m', cores[cor], texto)
    return f"{cores[cor]}{texto}{attr(0)}"


def formatar_status(personagem) -> str:
    """
    Função que organiza e retorna os status para a imprimir na tela.
    """

    nome, vida = personagem.nome, personagem.status['vida']
    magia, stamina = personagem.status['magia'], personagem.status['stamina']
    cor_nome = 'turquesa' if vida else 'cinza_escuro'
    texto = colorir(f"{nome} [{personagem.classe}]: ", cor_nome)
    if personagem.classe in ('Mago', 'Clerigo', 'Assassino'):
        cores = ('azul', 'amarelo') + ('cinza_escuro',) * 2
    else:
        cores = ('cinza_escuro',) * 2 + ('verde', 'amarelo')
    blocos_com_barras = _formatar(magia, cores[0])
    texto += colorir(f"{blocos_com_barras} {magia:3d}%  ", cores[1])
    blocos_com_barras = _formatar(vida, 'vermelho')
    texto += colorir(f"{blocos_com_barras} {vida:3d}%  ", 'amarelo')
    blocos_com_barras = _formatar(stamina, cores[2])
    return texto + colorir(f"{blocos_com_barras} {stamina:3d}%", cores[3])


def _formatar(atributo: str, cor_blocos: str) -> str:
    """ Função auxiliar para a função formatar. """
    quantidade_blocos = 10 if cor_blocos == 'vermelho' else 5
    p = atributo / 100 * quantidade_blocos
    porcentagem = int(p) + 1 if int(p) < p else int(p)
    blocos = formas[53] * porcentagem
    blocos += (quantidade_blocos - len(blocos)) * formas[48]
    blocos_coloridos = colorir(blocos, cor_blocos)
    return f"{formas[191]}{blocos_coloridos}{formas[192]}"


class Imprimir:
    _tamanho = 0
    _tela = Screen()
    _ciclo = cycle((0,))
    _ids_textos = {}

    # botar o init novamente com classmethod?

    @classmethod
    def reiniciar_posicoes(cls):
        cls._ids_textos = {}

    @classmethod
    def gerar_ciclo(cls, tamanho):
        cls._tamanho = tamanho
        cls._ciclo = cycle(range(tamanho))

    @classmethod
    def reiniciar_ciclo_menos_1(cls):
        if cls._tamanho > 0:
            cls._tamanho -= 1
        cls._ciclo = cycle(range(cls._tamanho))

    def imprimir(self, texto: str):
        texto_id = self.remover_cores(texto).split()[0]
        if not self._ids_textos:
            self._ids_textos[texto_id] = 0
        elif texto_id not in self._ids_textos:
            ultimo_numero = self._ids_textos[list(self._ids_textos)[-1]]
            self._ids_textos[texto_id] = ultimo_numero + 1
        self._tela.writexy(0, self._ids_textos[texto_id], texto)
        # self._tela.write(texto)

    def limpar_tela(self):
        self.reiniciar_posicoes()
        self._tela.gotoxy(0, 0)
        self._tela.erase_display()

    def remover_cores(self, texto: str) -> str:
        """ Método que remove quaisquer cores em um texto. """
        return sub('\\x1b\[[\d;]+m', '', texto)


def efeito_digitando(texto: str, dormir: float = 0.04):
    for a in texto:
        print(a, end='', flush=True)
        sleep(dormir)
    print()  # end='\r'
