from jogo.itens.itens import Atributo
from jogo.itens.moedas import Draconica, Pratas


class Roupa:
    # precisa colocar o tipo aqui.
    tipo: str = "Roupa"
    classe: str = "Todos"

    def __init__(
        self, nome: str, vida: int = 0, resistencia: int = 0, armadura: int = 0
    ):
        self.nome = nome
        self.vida = vida
        self.resistencia = resistencia
        self.armadura = armadura
        self.preco = Pratas((((vida // 2) + resistencia + armadura) * 8))
        self.bonus: list = []
        self.conjunto = "item comum"

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura})"
        )
        return retorno


class Peitoral(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Peitoral", **kwargs)
        self.tipo = "Peitoral"
        self.tipo_equipar = "Peitoral"


class Elmo(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Elmo", **kwargs)
        self.tipo = "Elmo"
        self.tipo_equipar = "Elmo"


class Calca(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Calça", **kwargs)
        self.tipo = "Calça"
        self.tipo_equipar = "Calça"


class Botas(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Botas", **kwargs)
        self.tipo = "Botas"
        self.tipo_equipar = "Botas"


class Luvas(Roupa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Luvas", **kwargs)
        self.tipo = "Luvas"
        self.tipo_equipar = "Luvas"


class Anel:
    tipo: str = "Anel"
    classe: str = "Todos"

    def __init__(
        self,
        nome: str = "Anel",
        dano: int = 0,
        vida: int = 0,
        resistencia: int = 0,
        armadura: int = 0,
    ):
        self.nome = nome
        self.dano = dano
        self.vida = vida
        self.resistencia = resistencia
        self.armadura = armadura
        self.preco = Pratas(
            (dano + (self.vida // 2) + resistencia + armadura) * 8
        )
        self.bonus = []
        self.conjunto = "item comum"
        self.tipo_equipar = "Anel"

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura}, dan: {self.dano})"
        )
        return retorno


class Amuleto:
    tipo: str = "Amuleto"
    classe: str = "Todos"

    def __init__(
        self,
        nome: str = "Amuleto",
        dano: int = 0,
        vida: int = 0,
        resistencia: int = 0,
        armadura: int = 0,
    ):
        self.nome = nome
        self.dano = dano
        self.vida = vida
        self.resistencia = resistencia
        self.armadura = armadura
        self.preco = Pratas(
            (dano + (self.vida // 2) + resistencia + armadura) * 8
        )
        self.bonus = []
        self.conjunto = "item comum"
        self.tipo_equipar = "Amuleto"

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura}, dan: {self.dano})"
        )
        return retorno


tudo = [Peitoral, Elmo, Calca, Botas, Luvas, Anel, Amuleto]


class RoupaDraconica:
    # precisa colocar o tipo aqui.
    tipo: str = "Roupa"
    classe: str = "Todos"

    def __init__(
        self, nome: str, vida: int = 0, resistencia: int = 0, armadura: int = 0
    ):
        self.nome = nome
        self.vida = vida
        self.resistencia = resistencia
        self.armadura = armadura
        self.preco = Draconica((((vida // 2) + resistencia + armadura) * 8))
        self.bonus = [
            Atributo("vida", 50, "valor real", 2),
            Atributo("resistencia", 10, "porcentagem", 3),
        ]
        self.conjunto = "item Draconico"

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura})"
        )
        return retorno


class PeitoralDraconico(RoupaDraconica):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Pei Draconico", **kwargs)
        self.tipo = "Peitoral"
        self.tipo_equipar = "Peitoral"


class ElmoDraconico(RoupaDraconica):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Elm Draconico", **kwargs)
        self.tipo = "Elmo"
        self.tipo_equipar = "Elmo"


class CalcaDraconio(RoupaDraconica):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cal Draconico", **kwargs)
        self.tipo = "Calça"
        self.tipo_equipar = "Calça"


roupas_draconicas = [PeitoralDraconico, ElmoDraconico, CalcaDraconio]
