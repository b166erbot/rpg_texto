class Arma:
    def __init__(
        self, nome = '', dano = 1, velo_ataque = 1, critico = 0,
    ):
        self.nome = nome
        self.dano = dano
        self.velo_ataque = velo_ataque
        self.critico = critico
        self.preco = (dano + velo_ataque + critico) * 8
        self.tipo = 'Arma'

    def __repr__(self):
        return (
            f"{self.nome} - dano: {self.dano} velo_ataque: {self.velo_ataque}"
            f" critico: {self.critico}"
        )


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
