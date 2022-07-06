from jogo.itens.moedas import Glifos, Pratas
from jogo.utils import Acumulador


class Arma:
    # tipo precisa ficar aqui em cima
    tipo = "Arma"

    def __init__(
        self,
        nome: str,
        dano: int,
        critico: int,
        aumento_critico: int,
        classe: str,
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
        self.classe = classe
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
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, nome="Espada longa", classe="Guerreiro", **kwargs
        )


class Machado(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Machado", classe="Guerreiro", **kwargs)


class Espada_curta(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, nome="Espada curta", classe="Guerreiro", **kwargs
        )


class Cajado(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado", classe="Mago", **kwargs)


class Cajado_negro(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Cajado negro", classe="Mago", **kwargs)


class Arco_longo(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Arco longo", classe="Arqueiro", **kwargs)


class Arco_curto(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Arco curto", classe="Arqueiro", **kwargs)


class Adaga(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Adaga", classe="Assassino", **kwargs)


class Luvas_de_ferro(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Luvas de ferro", classe="Monge", **kwargs)


class Botas_de_ferro(Arma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, nome="Botas de ferro", classe="Monge", **kwargs)


class AdornoDeArma:
    # tipo precisa ficar aqui em cima
    tipo = "Adorno de arma"

    def __init__(
        self,
        critico: int,
        aumento_critico: int,
        level: int = 1,
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
        self.classe = "Todos"
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


tudo = [
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
]
