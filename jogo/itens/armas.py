from jogo.itens.moedas import Pratas


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
    ):
        self.nome = nome
        self.dano = dano
        self.critico = critico
        self.aumento_critico = aumento_critico
        self.tipo_equipar = "Arma"
        self.classe = classe
        self.bonus = []
        self.preco = Pratas(
            (self.dano + self.aumento_critico + self.critico) * 8
        )
        self.conjunto = "item comum"

    def __repr__(self):
        retorno = (
            f"{self.nome}(dan: {self.dano}, "
            f"por_cri: {self.aumento_critico}, crit: {self.critico})"
        )
        return retorno


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
    def __init__(self, critico: int, aumento_critico: int):
        self.nome = "Adorno de arma"
        self.critico = critico
        self.aumento_critico = aumento_critico
        self.tipo_equipar = "Adorno de arma"
        self.classe = "Todos"
        self.bonus = []
        self.preco = Pratas(
            (self.aumento_critico + self.critico) * 8
        )
        self.conjunto = "item comum"

    def __repr__(self):
        retorno = (
            f"{self.nome}("
            f"aum_cri: {self.aumento_critico}, crit: {self.critico})"
        )
        return retorno


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
