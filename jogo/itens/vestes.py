class Roupa:
    def __init__(
        self, vida = 0, dano = 0, resistencias = 0, velo_ataque = 0,
        critico = 0, armadura = 0, velo_movi = 0
    ):
        self.vida = vida
        self.dano = dano
        self.resistencias = resistencias
        self.velo_ataque = velo_ataque
        self.critico = critico
        self.armadura = armadura
        self.velo_movi = velo_movi


class Peitoral(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Elmo(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Calca(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Bota(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

tudo = [Peitoral, Elmo, Calca, Bota]
