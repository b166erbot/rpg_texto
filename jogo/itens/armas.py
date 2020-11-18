class Arma:
    def __init__(
        self, nome = '', dano = 1, velo_ataque = 1, critico = 0,
    ):
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
