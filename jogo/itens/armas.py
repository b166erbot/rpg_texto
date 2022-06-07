from dataclasses import dataclass, field


@dataclass
class Arma:
    nome: str = field(repr = False, default = '')
    dano: int = 1
    velo_ataque: int = 1
    critico: int = 0
    tipo: str = field(repr=False, default='Arma', init=False)

    def __post_init__(self):
        self.preco = (self.dano + self.velo_ataque + self.critico) * 8


class Espada_longa(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Espada longa', **kwargs)


class Machado(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Machado', **kwargs)


class Espada_curta(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Espada curta', **kwargs)


class Cajado(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Cajado', **kwargs)


class Cajado_negro(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Cajado negro', **kwargs)


class Arco_longo(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Arco longo', **kwargs)


class Arco_curto(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Arco curto', **kwargs)


class Adaga(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Adaga', **kwargs)


class Luvas_de_ferro(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Luvas de ferro', **kwargs)


tudo = [
    Espada_longa, Machado, Espada_curta, Cajado, Cajado_negro, Arco_longo,
    Arco_curto, Adaga, Luvas_de_ferro
]
