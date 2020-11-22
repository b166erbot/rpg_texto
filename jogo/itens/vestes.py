class Roupa:
    def __init__(
        self, nome = '', vida = 0, resistencias = 0,
        armadura = 0, velo_movi = 0
    ):
        self.nome = nome
        self.vida = vida
        self.resistencias = resistencias
        self.armadura = armadura

    def __repr__(self):
        return (
            f"{self.nome} - vida: {self.vida},"
            f" resistencias: {self.resistencias}, armadura: {self.armadura}"
        )


class Peitoral(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Peitoral', **kwargs)

class Elmo(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Elmo', **kwargs)

class Calca(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Calca', **kwargs)

class Botas(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome = 'Botas', **kwargs)

tudo = [Peitoral, Elmo, Calca, Botas]
