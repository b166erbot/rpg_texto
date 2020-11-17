class Roupa:
    def __init__(
        self, vida = 0, dano = 0, resistencias = 0, velo_ataque = 0,
        critico = 0, armadura = 0, velo_movi = 0, nome = ''
    ):
        self.vida = vida
        self.dano = dano
        self.resistencias = resistencias
        self.velo_ataque = velo_ataque
        self.critico = critico
        self.armadura = armadura
        self.velo_movi = velo_movi
        self.nome = nome


class Peitoral(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Peitoral', **kwargs)

class Elmo(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Elmo', **kwargs)

class Calca(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Calca', **kwargs)

class Bota(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Bota', **kwargs)

tudo = [Peitoral, Elmo, Calca, Bota]
