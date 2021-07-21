class Roupa:
    def __init__(
        self, nome = '', vida = 0, resistencias = 0,
        armadura = 0, velo_movi = 0
    ):
        self.nome = nome
        self.vida = vida
        self.resistencias = resistencias
        self.armadura = armadura
        self.preco = (vida + resistencias + armadura) * 8

    def __repr__(self):
        return (
            f"{self.nome} - vida: {self.vida},"
            f" resistencias: {self.resistencias}, armadura: {self.armadura}"
        )


class Peitoral(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Peitoral', **kwargs)
        self.tipo = 'Peitoral'


class Elmo(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Elmo', **kwargs)
        self.tipo = 'Elmo'


class Calca(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Calca', **kwargs)
        self.tipo = 'Calca'


class Botas(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Botas', **kwargs)
        self.tipo = 'Botas'


class Luvas(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Luvas', **kwargs)
        self.tipo = 'Luvas'


class Anel:
    def __init__(
        self, nome = '', dano = 0, vida = 0, resistencias = 0, armadura = 0
    ):
        self.nome = nome
        self.dano = dano
        self.vida = vida
        self.resistencias = resistencias
        self.armadura = armadura
        self.tipo = "Anel"

    def __repr__(self):
        return (
            f"{self.nome} - vida: {self.vida}, dano: {self.dano}"
            f" resistencias: {self.resistencias}, armadura: {self.armadura}"
        )

tudo = [Peitoral, Elmo, Calca, Botas, Luvas, Anel]
