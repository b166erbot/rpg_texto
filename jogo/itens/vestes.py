from jogo.itens.itens import Atributo
from jogo.itens.moedas import Draconica, Glifos, Pratas
from jogo.utils import Acumulador


class Roupa:
    # precisa colocar o tipo aqui.
    tipo: str = "Roupa"
    classe: str = "Todos"

    def __init__(
        self,
        vida: int,
        resistencia: int,
        armadura: int,
        level: int = 1,
    ):
        self.vida = vida * level
        self.resistencia = resistencia * level
        self.armadura = armadura * level
        self._valores_base = {
            "vida": vida,
            "resistencia": resistencia,
            "armadura": armadura,
            "level": level,
        }
        self.bonus = []
        self.conjunto = "item comum"
        self.preco = Pratas((((vida // 2) + resistencia + armadura) * 8))
        self.glifos = Glifos(12 * level)
        self.level = level
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura}, lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.vida = self._valores_base["vida"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.vida = self._valores_base["vida"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        return glifos


class Peitoral(Roupa):
    nome = "Peitoral"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = "Peitoral"
        self.tipo_equipar = "Peitoral"


class Elmo(Roupa):
    nome = "Elmo"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = "Elmo"
        self.tipo_equipar = "Elmo"


class Calca(Roupa):
    nome = "Calça"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = "Calça"
        self.tipo_equipar = "Calça"


class Botas(Roupa):
    nome = "Botas"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = "Botas"
        self.tipo_equipar = "Botas"


class Luvas(Roupa):
    nome = "Luvas"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = "Luvas"
        self.tipo_equipar = "Luvas"


class Anel:
    tipo: str = "Anel"
    classe: str = "Todos"
    nome = "Anel"

    def __init__(
        self,
        dano: int,
        vida: int,
        resistencia: int,
        armadura: int,
        level: int = 1,
    ):
        self.dano = dano * level
        self.vida = vida * level
        self.resistencia = resistencia * level
        self.armadura = armadura * level
        self._valores_base = {
            "dano": dano,
            "vida": vida,
            "resistencia": resistencia,
            "armadura": armadura,
            "level": level,
        }
        self.bonus = []
        self.conjunto = "item comum"
        self.tipo_equipar = "Anel"
        self.preco = Pratas((dano + (vida // 2) + resistencia + armadura) * 8)
        self.glifos = Glifos(12 * level)
        self.level = level
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura}, dan: {self.dano}, lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.dano = self._valores_base["dano"] * self.level
        self.vida = self._valores_base["vida"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.dano = self._valores_base["dano"] * self.level
        self.vida = self._valores_base["vida"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level
        return glifos


class Amuleto:
    tipo: str = "Amuleto"
    classe: str = "Todos"
    nome = "Amuleto"

    def __init__(
        self,
        dano: int,
        vida: int,
        resistencia: int,
        armadura: int,
        level: int = 1,
    ):
        self.dano = dano * level
        self.vida = vida * level
        self.resistencia = resistencia * level
        self.armadura = armadura * level
        self._valores_base = {
            "dano": dano,
            "vida": vida,
            "resistencia": resistencia,
            "armadura": armadura,
            "level": level,
        }
        self.bonus = []
        self.conjunto = "item comum"
        self.tipo_equipar = "Amuleto"
        self.preco = Pratas((dano + (vida // 2) + resistencia + armadura) * 8)
        self.glifos = Glifos(12 * level)
        self.level = level
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura}, dan: {self.dano}, lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.dano = self._valores_base["dano"] * self.level
        self.vida = self._valores_base["vida"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.dano = self._valores_base["dano"] * self.level
        self.vida = self._valores_base["vida"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level
        return glifos


class RoupaDraconica:
    # precisa colocar o tipo aqui.
    tipo: str = "Roupa"
    classe: str = "Todos"

    def __init__(
        self,
        vida: int,
        resistencia: int,
        armadura: int,
        level: int = 1,
    ):
        self.vida = vida * level
        self.resistencia = resistencia * level
        self.armadura = armadura * level
        self._valores_base = {
            "vida": vida,
            "resistencia": resistencia,
            "armadura": armadura,
            "level": level,
        }
        self.bonus = [
            Atributo("vida", 50, "valor real", 2),
            Atributo("resistencia", 10, "porcentagem", 3),
        ]
        self.conjunto = "item Draconico"
        self.preco = Draconica((((vida // 2) + resistencia + armadura) * 8))
        self.glifos = Glifos(500 * level)
        self.level = level
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(vid: {self.vida}, resis: {self.resistencia}"
            f", arm: {self.armadura}, lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.vida = self._valores_base["vida"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.vida = self._valores_base["vida"] * self.level
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level
        return glifos


class PeitoralDraconico(RoupaDraconica):
    nome = "Pei Draconico"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = "Peitoral"
        self.tipo_equipar = "Peitoral"


class ElmoDraconico(RoupaDraconica):
    nome = "Elm Draconico"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = "Elmo"
        self.tipo_equipar = "Elmo"


class CalcaDraconica(RoupaDraconica):
    nome = "Cal Draconica"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = "Calça"
        self.tipo_equipar = "Calça"


tudo = [Peitoral, Elmo, Calca, Botas, Luvas, Anel, Amuleto]
roupas_draconicas = [PeitoralDraconico, ElmoDraconico, CalcaDraconica]
