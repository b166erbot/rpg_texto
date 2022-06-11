from dataclasses import dataclass, field


@dataclass
class Roupa:
    nome: str = field(repr=False, default="")
    vida: int = 0
    resistencias: int = 0
    armadura: int = 0
    velo_movi: int = 0
    tipo: str = field(repr=False, default="Roupa", init=False)

    def __post_init__(self):
        self.preco = (
            int(self.vida / 2) + self.resistencias + self.armadura
        ) * 8


class Peitoral(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Peitoral", **kwargs)
        self.tipo = "Peitoral"


class Elmo(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Elmo", **kwargs)
        self.tipo = "Elmo"


class Calca(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Calça", **kwargs)
        self.tipo = "Calça"


class Botas(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Botas", **kwargs)
        self.tipo = "Botas"


class Luvas(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Luvas", **kwargs)
        self.tipo = "Luvas"


@dataclass
class Anel:
    nome: str = field(repr=False, default="")
    dano: int = 0
    vida: int = 0
    resistencias: int = 0
    armadura: int = 0
    tipo: str = field(repr=False, default="Anel", init=False)

    def __post_init__(self):
        self.preco = (
            self.dano + int(self.vida / 2) + self.resistencias + self.armadura
        ) * 8


tudo = [Peitoral, Elmo, Calca, Botas, Luvas, Anel]
