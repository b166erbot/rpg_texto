from dataclasses import dataclass, field


@dataclass
class Arma:
    nome: str = field(repr=False)
    dano: int
    velo_ataque: int
    critico: int
    tipo: str = field(repr=False, default="Arma", init=False)
    classe: str = field(repr=False)

    def __post_init__(self):
        self.preco = (self.dano + self.velo_ataque + self.critico) * 8


class Espada_longa(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, nome="Espada longa", classe="Guerreiro", **kwargs
        )


class Machado(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Machado", classe="Guerreiro", **kwargs)


class Espada_curta(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, nome="Espada curta", classe="Guerreiro", **kwargs
        )


class Cajado(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado", classe="Mago" ** kwargs)


class Cajado_negro(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado negro", classe="Mago", **kwargs)


class Arco_longo(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Arco longo", classe="Arqueiro", **kwargs)


class Arco_curto(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Arco curto", classe="Arqueiro", **kwargs)


class Adaga(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Adaga", classe="Assassino", **kwargs)


class Luvas_de_ferro(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Luvas de ferro", classe="Monge", **kwargs)


tudo = [
    Espada_longa,
    Machado,
    Espada_curta,
    Cajado,
    Cajado_negro,
    Arco_longo,
    Arco_curto,
    Adaga,
    Luvas_de_ferro,
]
