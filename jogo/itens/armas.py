class Arma:
    def __init__(
        self, nome = '', dano = 1, velo_ataque = 1, critico = 0,
    ):
        self.nome = nome
        self.dano = dano
        self.velo_ataque = velo_ataque
        self.critico = critico

    def __repr__(self):
        return (
            f"{self.nome} - dano: {self.dano} velo_ataque: {self.velo_ataque}"
            f" critico: {self.critico}"
        )


class Espada_longa(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'espada longa', **kwargs)


class Machado(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Machado', **kwargs)


class Espada_curta(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'espada curta', **kwargs)


class Cajado(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'cajado', **kwargs)


class Cajado_negro(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'cajado negro', **kwargs)


class Arco_longo(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'arco longo', **kwargs)


class Arco_curto(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'arco curto', **kwargs)


class Adaga(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'adaga', **kwargs)


tudo = [
    Espada_longa, Machado, Espada_curta, Cajado, Cajado_negro, Arco_longo,
    Arco_curto, Adaga
]
