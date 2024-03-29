from asyncio import sleep
from collections import Counter
from random import choice, randint
from time import sleep as sleep2

from jogo.itens.armas import CajadoArauto, armas_arauto, armas_comuns
from jogo.itens.caixas import CaixaDraconica
from jogo.itens.item_secundario import itens_comuns
from jogo.itens.quest import ItemQuest
from jogo.itens.vestes import AnelDoCeifador, roupas_comuns
from jogo.tela.imprimir import Imprimir, efeito_digitando, formatar_status
from jogo.utils import Contador, arrumar_porcentagem, menor_numero, regra_3

tela = Imprimir()


class Monstro:
    def __init__(self, level=1, status={}):
        self.experiencia = 50 * level
        self.status = Counter(
            status
            or {
                "vida": 100,
                "dano": 3,
                "resistencia": 8,
                "velo-ataque": 1,
                "critico": 8,
                "armadura": 8,
                "magia": 100,
                "stamina": 100,
                "velo-movi": 1,
            }
        )
        for item in self.status:
            if item in ["magia", "stamina"]:
                continue
            self.status[item] *= level
        self.habilidades = []
        self.vida_ = self.status["vida"]
        self.level = level
        porcentagem = enumerate([42, 84, 126, 168, 210, 252, 294, 336], 1)
        self._porcentagem_total = dict(porcentagem)
        self.porcentagem_armadura = 0
        self.porcentagem_resistencia = 0
        self.porcentagem_critico = 0
        self._contador = Contador(4)
        self._porcentagem_total_dano_lista = [5, 11, 17, 23, 29]
        self.atualizar_status()

    async def atacar(self, other):
        """Método que ataca como bot o personagem."""
        while all([other.status["vida"] > 0, self.status["vida"] > 0]):
            if randint(0, 2) == 2:
                habilidade = choice(self.habilidades)
                if self.status["stamina"] >= 20:
                    self.status["stamina"] -= 20
                    habilidade(other)
                    self._contador.resetar()
            else:
                dano = self.status["dano"]
                subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
                other.status["vida"] -= dano - subtrair_dano
                self._contador.acrescentar()
            if self._contador.usar:
                self._recuperar_stamina()
            other.arrumar_vida()
            tela.imprimir_combate(formatar_status(self), 2)
            await sleep(0.5)
        tela.imprimir_combate(formatar_status(self), 2)
        await sleep(0.5)

    def ressucitar(self):
        """Método que ressucita."""
        self.status["vida"] = self.vida_

    @property
    def vida_maxima(self):
        """Método que retorna a vida máxima."""
        return self.vida_

    def arrumar_vida(self):
        """Método que arruma a vida."""
        if self.status["vida"] < 0:
            self.status["vida"] = 0
        if self.status["vida"] > self.vida_maxima:
            self.status["vida"] = self.vida_maxima

    def sortear_drops(self, personagem):
        """Método que dá item e pratas ao personagem."""
        if randint(0, 2) == 1:
            efeito_digitando("Loot encontrado.")
            Item = choice(roupas_comuns + armas_comuns + itens_comuns)
            match (Item.tipo, Item.classe):
                case ("Arma", "Monge"):
                    status = [
                        randint(1, 6),
                        randint(1, 16),
                        randint(1, 6),
                        randint(1, 6),
                        randint(1, 6),
                        self.level,
                    ]
                    status_nomes = [
                        "dano",
                        "aumento_critico",
                        "critico",
                        "armadura",
                        "resistencia",
                        "level",
                    ]
                    status_dict = dict(zip(status_nomes, status))
                    item = Item(**status_dict)
                case ("Arma", _):
                    status = [
                        randint(1, 6),
                        randint(1, 16),
                        randint(1, 6),
                        self.level,
                    ]
                    status_nomes = [
                        "dano",
                        "aumento_critico",
                        "critico",
                        "level",
                    ]
                    status_dict = dict(zip(status_nomes, status))
                    item = Item(**status_dict)
                case ("Roupa", _):  # a classe tem tipo -> Roupa
                    status = [
                        randint(1, 6),
                        randint(3, 20),
                        randint(1, 6),
                        self.level,
                    ]
                    status_nomes = ["armadura", "vida", "resistencia", "level"]
                    status_dict = dict(zip(status_nomes, status))
                    item = Item(**status_dict)
                case ("Anel" | "Amuleto", _):
                    status = [
                        randint(1, 6),
                        randint(3, 20),
                        randint(1, 6),
                        randint(1, 6),
                        self.level,
                    ]
                    status_nomes = [
                        "dano",
                        "vida",
                        "resistencia",
                        "armadura",
                        "level",
                    ]
                    status_dict = dict(zip(status_nomes, status))
                    item = Item(**status_dict)
                case ("Escudo", _):
                    status = [
                        randint(3, 20),
                        randint(1, 6),
                        randint(1, 6),
                        randint(10, 80),
                        self.level,
                    ]
                    status_nomes = [
                        "vida",
                        "armadura",
                        "resistencia",
                        "bloqueio",
                        "level",
                    ]
                    status_dict = dict(zip(status_nomes, status))
                    item = Item(**status_dict)
                case ("Adorno de arma", _):
                    status = [
                        randint(1, 6),
                        randint(1, 16),
                        self.level,
                    ]
                    status_nomes = ["critico", "aumento_critico", "level"]
                    status_dict = dict(zip(status_nomes, status))
                    item = Item(**status_dict)
            if personagem.e_possivel_guardar(item):
                personagem.guardar_item(item)
            else:
                tela.imprimir(
                    "Não foi possível adicionar item ao inventario. "
                    "Inventario cheio.\n"
                )
                sleep2(3)
        personagem.moedas["Pratas"] += randint(30 * self.level, 50 * self.level)

    def sortear_drops_quest(self, personagem):
        """Método que dá itens de quests para o personagem."""
        quests = filter(
            lambda quest: quest.tipo == "monstro", personagem.quests
        )
        for quest in quests:
            condicoes = [
                quest.sorte_de_drop(),
                (
                    personagem.inventario.count(quest.item)
                    < quest.numero_de_itens_requeridos
                ),
                self.nome in quest.monstro_drop,
            ]
            if all(condicoes):
                tela.imprimir(f"Item {quest.item.nome} adiquirido\n")
                if personagem.e_possivel_guardar(quest.item):
                    personagem.guardar_item(quest.item)

    def __str__(self):
        status = (
            f"{self.nome}(level={self.level}, vida={self.status['vida']}, "
            f"dano={self.status['dano']}, resis={self.status['resistencia']}, "
            f"armad={self.status['armadura']})"
        )
        return status

    def dar_experiencia(self, personagem):
        personagem.experiencia.depositar_valor(self.experiencia)

    def atualizar_status(self):
        self.atualizar_porcentagem()

    def atualizar_porcentagem(self):
        self.porcentagem_armadura = arrumar_porcentagem(
            regra_3(
                self._porcentagem_total[self.level],
                100,
                self.status["armadura"],
            )
        )
        self.porcentagem_resistencia = arrumar_porcentagem(
            regra_3(
                self._porcentagem_total[self.level],
                100,
                self.status["resistencia"],
            )
        )
        self.porcentagem_critico = arrumar_porcentagem(
            regra_3(
                self._porcentagem_total[self.level],
                100,
                self.status["critico"],
            )
        )

    def _recuperar_stamina(self):
        if self.status["stamina"] <= 80:
            self.status["stamina"] += 20

    def atualizar_porcentagem_por_level(self, level: int):
        """Método que atualiza a porcentagem dependendo do level do inimigo."""
        diferenca = self.level - level
        if diferenca > 0:
            self.porcentagem_armadura -= 8 * diferenca
            self.porcentagem_resistencia -= 8 * diferenca
            if self.porcentagem_armadura < 0:
                self.porcentagem_armadura = 0
            if self.porcentagem_resistencia < 0:
                self.porcentagem_resistencia = 0

    def atualizar_porcentagem_por_dano(self, dano: int):
        valor = menor_numero(dano, list(self._porcentagem_total_dano))
        porcentagens = self._porcentagem_total_dano
        aumentar_porcentagem = porcentagens[valor]
        # divisão normal abaixo, favor manter.
        valor_armadura_resistencia = (
            aumentar_porcentagem * self._porcentagem_total[self.level]
        ) / 100
        self.status["armadura"] = valor_armadura_resistencia
        self.status["resistencia"] = valor_armadura_resistencia
        self.atualizar_status()

    @property
    def _porcentagem_total_dano(self):
        danos = [x * self.level for x in self._porcentagem_total_dano_lista]
        porcentagens = [11, 28, 45, 61, 78]
        return dict(zip(danos, porcentagens))


class Boss(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experiencia *= 2

    def sortear_drops(self, personagem):
        """Método que dá item e pratas ao personagem."""
        efeito_digitando("Loot encontrado.")
        Item = choice(roupas_comuns + armas_comuns)
        match (Item.tipo, Item.classe):
            case ("Arma", "Monge"):
                status = [
                    randint(3, 6),
                    randint(8, 16),
                    randint(3, 6),
                    randint(3, 6),
                    randint(3, 6),
                    self.level,
                ]
                status_nomes = [
                    "dano",
                    "aumento_critico",
                    "critico",
                    "armadura",
                    "resistencia",
                    "level",
                ]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            case ("Arma", _):
                status = [
                    randint(3, 6),
                    randint(8, 16),
                    randint(3, 6),
                    self.level,
                ]
                status_nomes = ["dano", "aumento_critico", "critico", "level"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            case ("Roupa", _):  # a classe tem tipo -> Roupa
                status = [
                    randint(3, 6),
                    randint(10, 20),
                    randint(3, 6),
                    self.level,
                ]
                status_nomes = ["armadura", "vida", "resistencia", "level"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            case ("Anel" | "Amuleto", _):
                status = [
                    randint(3, 6),
                    randint(10, 20),
                    randint(3, 6),
                    randint(3, 6),
                    self.level,
                ]
                status_nomes = [
                    "dano",
                    "vida",
                    "resistencia",
                    "armadura",
                    "level",
                ]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            case ("Escudo", _):
                status = [
                    randint(10, 20),
                    randint(3, 6),
                    randint(3, 6),
                    randint(40, 80),
                    self.level,
                ]
                status_nomes = [
                    "vida",
                    "armadura",
                    "resistencia",
                    "bloqueio",
                    "level",
                ]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            case ("Adorno de arma", _):
                status = [
                    randint(3, 6),
                    randint(8, 16),
                    self.level,
                ]
                status_nomes = ["critico", "aumento_critico", "level"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
        if personagem.e_possivel_guardar(item):
            personagem.guardar_item(item)
        else:
            tela.imprimir(
                "não foi possível adicionar item ao inventario, "
                "inventario cheio.\n"
            )
            sleep2(3)
        personagem.moedas["Pratas"] += randint(
            300 * self.level, 500 * self.level
        )


class Tartaruga(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.investida, self.garras_afiadas]
        self.nome = "Tartaruga"
        self.classe = "Monstro comum"

    def investida(self, other):
        """Método que ataca o personagem."""
        dano = 4 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def garras_afiadas(self, other):
        """Método que ataca o personagem."""
        dano = 6 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class Camaleao(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.trapasseiro, self.roubo]
        self.nome = "Camaleão"
        self.classe = "Monstro comum"

    def trapasseiro(self, other):
        """Método que ataca o personagem."""
        dano = 4 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def roubo(self, other):
        """Método que ataca o personagem."""
        dano = 6 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class Tamandua(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.linguada, self.abraco]
        self.nome = "Tamandua"
        self.classe = "Monstro comum"

    def linguada(self, other):
        """Método que ataca o personagem."""
        dano = 4 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def abraco(self, other):
        """Método que ataca o personagem."""
        dano = 6 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class Sapo(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.linguada, self.salto]
        self.nome = "Sapo"
        self.classe = "Monstro comum"

    def linguada(self, other):
        """Método que ataca o personagem."""
        dano = 4 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def salto(self, other):
        """Método que ataca o personagem."""
        dano = 6 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class DemonioDoCovil(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.cuspir_fogo, self.garras_afiadas]
        self.nome = "demônio do covil"
        self.classe = "Monstro comum"

    def cuspir_fogo(self, other):
        """Método que ataca o personagem"""
        dano = 4 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def garras_afiadas(self, other):
        """Método que ataca o personagem."""
        dano = 6 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class FilhoDoArauto(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.jato_de_fogo, self.explosao]
        self.nome = "Filho do Arauto"
        self.classe = "Monstro comum"

    def jato_de_fogo(self, other):
        """Método que ataca o personagem"""
        dano = 4 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def explosao(self, other):
        """Método que ataca o personagem."""
        dano = 6 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class Esqueleto(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.golpe_com_escudo, self.golpe_com_espada]
        self.nome = "Esqueleto"
        self.classe = "Monstro comum"

    def golpe_com_escudo(self, other):
        """Método que ataca o personagem"""
        dano = 4 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def golpe_com_espada(self, other):
        """Método que ataca o personagem."""
        dano = 6 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class Topera(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.pulo_fatal, self.terremoto]
        self.nome = "Topera"
        self.classe = "Monstro chefe"

    def pulo_fatal(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def terremoto(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class Mico(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.tacar_banana, self.esmagar]
        self.nome = "Mico"
        self.classe = "Monstro chefe"

    def tacar_banana(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def esmagar(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class Sucuri(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.lancamento_de_calda, self.bote]
        self.nome = "Sucuri"
        self.classe = "Monstro chefe"

    def lancamento_de_calda(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def bote(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class ArvoreDeku(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.braçada, self.outono]
        self.nome = "Arvore Deku"
        self.classe = "Monstro chefe"

    def braçada(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def outono(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2


class Dragao(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.patada, self.fogo]
        self.nome = "Dragão ancião"
        self.classe = "Monstro chefe"

    def patada(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano

        other.status["vida"] -= dano - subtrair_dano2

    def fogo(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def sortear_drops(self, personagem):
        # super().sortear_drops(personagem)
        personagem.inventario.append(ItemQuest("Coração de Dragão"))
        personagem.inventario.append(CaixaDraconica(personagem.level))


class Arauto(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.esmagar, self.explosao]
        self.nome = "Arauto"
        self.classe = "Monstro chefe"
        self.drops = {item.classe: [] for item in armas_arauto}
        for item in armas_arauto:
            self.drops[item.classe].append(item)
        self.drops["Clerigo"] = [CajadoArauto]

    def esmagar(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def explosao(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def sortear_drops(self, personagem):
        """Método que dá item e pratas ao personagem."""
        if randint(0, 100) in range(5):
            efeito_digitando("Loot encontrado.")
            Item = choice(self.drops[personagem.classe])
            if Item.classe == "Monge":
                status = [
                    randint(3, 6),
                    randint(8, 16),
                    randint(3, 6),
                    randint(3, 6),
                    randint(3, 6),
                    self.level,
                ]
                status_nomes = [
                    "dano",
                    "aumento_critico",
                    "critico",
                    "armadura",
                    "resistencia",
                    "level",
                ]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            else:
                status = [
                    randint(3, 6),
                    randint(8, 16),
                    randint(3, 6),
                    self.level,
                ]
                status_nomes = [
                    "dano",
                    "aumento_critico",
                    "critico",
                    "level",
                ]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            # guarda o item de qualquer maneira
            personagem.inventario.append(item)
        personagem.moedas["Pratas"] += randint(
            300 * self.level, 500 * self.level
        )


class Ceifador(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.corte_com_foice, self.invocando_fantasmas]
        self.nome = "Ceifador"
        self.classe = "Monstro chefe"

    def corte_com_foice(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def invocando_fantasmas(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        if randint(1, 100) <= self.porcentagem_critico:
            dano *= 2
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        dano -= subtrair_dano
        subtrair_dano2 = other.valor_de_bloqueio * dano
        other.status["vida"] -= dano - subtrair_dano2

    def sortear_drops(self, personagem):
        """Método que dá item e pratas ao personagem."""
        if randint(0, 100) in range(5):
            efeito_digitando("Loot encontrado.")
            status = [
                randint(3, 6),
                randint(10, 20),
                randint(3, 6),
                randint(3, 6),
                randint(3, 6),
                self.level,
            ]
            status_nomes = [
                "dano",
                "vida",
                "armadura",
                "resistencia",
                "level",
            ]
            status_dict = dict(zip(status_nomes, status))
            item = AnelDoCeifador(**status_dict)
            # guarda o item de qualquer maneira
            personagem.inventario.append(item)
        personagem.moedas["Pratas"] += randint(
            300 * self.level, 500 * self.level
        )


monstros_da_floresta = [Tartaruga, Camaleao, Tamandua, Sapo]
bosses_da_floresta = [Topera, Mico, Sucuri, ArvoreDeku]
