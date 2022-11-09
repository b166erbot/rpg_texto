from jogo.itens.moedas import Draconica, Glifos, Pratas
from jogo.utils import Acumulador

from .itens import Atributo


# a classe precisa ficar em cima pois na hora de dropar o item do monstro ele faz a verificação.
class Arma:
    # tipo precisa ficar aqui em cima
    tipo = "Arma"

    def __init__(
        self,
        nome: str,
        dano: int,
        critico: int,
        aumento_critico: int,
        level: int = 1,
    ):
        self.nome = nome
        self.dano = dano * level
        self.critico = critico * level
        self.aumento_critico = aumento_critico * level
        self._valores_base = {
            "dano": dano,
            "critico": critico,
            "aumento_critico": aumento_critico,
            "level": level,
        }
        self.tipo_equipar = "Arma"
        self.bonus = []
        self.conjunto = "item comum"
        self.preco = Pratas(
            (self.dano + self.aumento_critico + self.critico) * 8
        )
        self.glifos = Glifos(12 * level)
        self.level = level
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(dan: {self.dano}, "
            f"por_cri: {self.aumento_critico}, crit: {self.critico}, "
            f"lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )
        return glifos


class Espada_longa(Arma):
    classe = "Guerreiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Espada longa", **kwargs)


class Machado(Arma):
    classe = "Guerreiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Machado", **kwargs)


class Espada_curta(Arma):
    classe = "Guerreiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Espada curta", **kwargs)


class Cajado(Arma):
    classe = "Mago"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado", **kwargs)


class Cajado_negro(Arma):
    classe = "Mago"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado negro", **kwargs)


class Arco_longo(Arma):
    classe = "Arqueiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Arco longo", **kwargs)


class Arco_curto(Arma):
    classe = "Arqueiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Arco curto", **kwargs)


class Adaga(Arma):
    classe = "Assassino"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Adaga", **kwargs)


class CajadoDaFloresta(Arma):
    classe = "Druida"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado da Floresta", **kwargs)


class ArmaMonge:
    # tipo precisa ficar aqui em cima
    tipo = "Arma"

    def __init__(
        self,
        nome: str,
        dano: int,
        critico: int,
        aumento_critico: int,
        armadura: int,
        resistencia: int,
        tipo_equipar: str,
        level: int = 1,
    ):
        self.nome = nome
        self.dano = dano * level
        self.critico = critico * level
        self.aumento_critico = aumento_critico * level
        self.armadura = armadura * level
        self.resistencia = resistencia * level
        self._valores_base = {
            "dano": dano,
            "critico": critico,
            "aumento_critico": aumento_critico,
            "armadura": armadura,
            "resistencia": resistencia,
            "level": level,
        }
        self.tipo_equipar = tipo_equipar
        self.bonus = []
        self.conjunto = "item comum"
        self.preco = Pratas(
            (
                self.dano
                + self.aumento_critico
                + self.critico
                + self.armadura
                + self.resistencia
            )
            * 8
        )
        self.glifos = Glifos(12 * level)
        self.level = level
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(dan: {self.dano}, "
            f"por_cri: {self.aumento_critico}, crit: {self.critico}, "
            f"lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level
        return glifos


class Luvas_de_ferro(ArmaMonge):
    classe = "Monge"

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, nome="Luvas de ferro", tipo_equipar="Luvas", **kwargs
        )


class Botas_de_ferro(ArmaMonge):
    classe = "Monge"

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, nome="Botas de ferro", tipo_equipar="Botas", **kwargs
        )


class AdornoDeArma:
    # tipo precisa ficar aqui em cima
    tipo = "Adorno de arma"
    classe = "Todos"

    def __init__(
        self, critico: int, aumento_critico: int, level: int = 1,
    ):
        self.nome = "Adorno de arma"
        self.critico = critico * level
        self.aumento_critico = aumento_critico * level
        self._valores_base = {
            "critico": critico,
            "aumento_critico": aumento_critico,
            "level": level,
        }
        self.tipo_equipar = "Adorno de arma"
        self.bonus = []
        self.conjunto = "item comum"
        self.preco = Pratas((self.aumento_critico + self.critico) * 8)
        self.glifos = Glifos(12 * level)
        self.level = level
        leveis = [100, 200, 300, 400, 500, 600, 700, 800]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}("
            f"aum_cri: {self.aumento_critico}, crit: {self.critico}, "
            f"lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )
        return glifos


class ArmaArauto:
    # tipo precisa ficar aqui em cima
    tipo = "Arma"

    def __init__(
        self,
        nome: str,
        dano: int,
        critico: int,
        aumento_critico: int,
        level: int = 1,
    ):
        self.nome = nome
        self.dano = dano * level
        self.critico = critico * level
        self.aumento_critico = aumento_critico * level
        self._valores_base = {
            "dano": dano,
            "critico": critico,
            "aumento_critico": aumento_critico,
            "level": level,
        }
        self.tipo_equipar = "Arma"
        self.bonus = [Atributo("dano", 10, "porcentagem", 1)]
        self.conjunto = "item do Submundo"
        self.preco = Draconica(
            (self.dano + self.aumento_critico + self.critico) * 8
        )
        self.glifos = Glifos(500 * level)
        self.level = level
        leveis = [300, 400, 500, 600, 700, 800, 900, 1000]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(dan: {self.dano}, "
            f"por_cri: {self.aumento_critico}, crit: {self.critico}, "
            f"lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )
        return glifos


class ArmaArautoMonge:
    # tipo precisa ficar aqui em cima
    tipo = "Arma"

    def __init__(
        self,
        nome: str,
        dano: int,
        critico: int,
        aumento_critico: int,
        armadura: int,
        resistencia: int,
        tipo_equipar: str,
        level: int = 1,
    ):
        self.nome = nome
        self.dano = dano * level
        self.critico = critico * level
        self.aumento_critico = aumento_critico * level
        self.armadura = armadura * level
        self.resistencia = resistencia * level
        self._valores_base = {
            "dano": dano,
            "critico": critico,
            "aumento_critico": aumento_critico,
            "armadura": armadura,
            "resistencia": resistencia,
            "level": level,
        }
        self.tipo_equipar = tipo_equipar
        self.bonus = [Atributo("dano", 10, "porcentagem", 1)]
        self.conjunto = "item do Submundo"
        self.preco = Draconica(
            (self.dano + self.aumento_critico + self.critico) * 8
        )
        self.glifos = Glifos(500 * level)
        self.level = level
        leveis = [300, 400, 500, 600, 700, 800, 900, 1000]
        self.glifos_level = Acumulador(0, leveis, level)

    def __repr__(self):
        retorno = (
            f"{self.nome}(dan: {self.dano}, "
            f"por_cri: {self.aumento_critico}, crit: {self.critico}, "
            f"lvl: {self.level})"
        )
        return retorno

    def receber_glifos(self, glifos):
        self.glifos_level.depositar_valor(int(glifos))
        self.level = self.glifos_level.level
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level

    def remover_glifos(self):
        glifos = Glifos(self.glifos_level.valor_glifos())
        self.glifos_level.resetar()
        self.level = self._valores_base["level"]
        self.dano = self._valores_base["dano"] * self.level
        self.critico = self._valores_base["critico"] * self.level
        self.aumento_critico = (
            self._valores_base["aumento_critico"] * self.level
        )
        self.armadura = self._valores_base["armadura"] * self.level
        self.resistencia = self._valores_base["resistencia"] * self.level
        return glifos


class MachadoArauto(ArmaArauto):
    classe = "Guerreiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Machado Arauto", **kwargs)
        self.tipo = "Arma"
        self.tipo_equipar = "Arma"


class CajadoArauto(ArmaArauto):
    classe = "Mago"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado Arauto", **kwargs)
        self.tipo = "Arma"
        self.tipo_equipar = "Arma"


class ArcoArauto(ArmaArauto):
    classe = "Arqueiro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Arco Arauto", **kwargs)
        self.tipo = "Arma"
        self.tipo_equipar = "Arma"


class AdagaArauto(ArmaArauto):
    classe = "Assassino"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Adaga Arauto", **kwargs)
        self.tipo = "Arma"
        self.tipo_equipar = "Arma"


class LuvasArauto(ArmaArautoMonge):
    classe = "Monge"

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, nome="Luvas Arauto", tipo_equipar="Luvas", **kwargs,
        )
        self.tipo = "Arma"


class BotasArauto(ArmaArautoMonge):
    classe = "Monge"

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, nome="Botas Arauto", tipo_equipar="Botas", **kwargs,
        )
        self.tipo = "Arma"


class CajadoVerdejanteArauto(ArmaArauto):
    classe = "Druida"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado V. Arauto", **kwargs)
        self.tipo = "Arma"
        self.tipo_equipar = "Arma"


armas_comuns = [
    Espada_longa,
    Machado,
    Espada_curta,
    Cajado,
    Cajado_negro,
    Arco_longo,
    Arco_curto,
    Adaga,
    Luvas_de_ferro,
    Botas_de_ferro,
    AdornoDeArma,
    CajadoDaFloresta,
]

armas_arauto = [
    MachadoArauto,
    CajadoArauto,
    ArcoArauto,
    AdagaArauto,
    LuvasArauto,
    BotasArauto,
    CajadoVerdejanteArauto,
]
