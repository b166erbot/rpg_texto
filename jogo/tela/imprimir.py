from re import sub
from itertools import cycle

from colored import fg, attr
from screen import Screen
from sys import stdout


# tela = Screen()
shapes = (
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
    blocos = shapes[53] * porcentagem
    blocos += (quantidade_blocos - len(blocos)) * shapes[48]
    blocos_coloridos = colorir(blocos, cor_blocos)
    return f"{shapes[191]}{blocos_coloridos}{shapes[192]}"


def imprimir(texto: str, ciclo: cycle, tela: Screen):
    """
    Função que imprime um texto em uma posição conforme a gerada pelo ciclo.
    """
    eixo_y = next(ciclo)
    if eixo_y == 0:
        tela.erase_display()
    tela.writexy(0, eixo_y, texto)


def texto_efeito_pausa(texto: str):
    for a in texto:
        print(a, end='')
        stdout.flush()
        sleep(0.04)
    print()
