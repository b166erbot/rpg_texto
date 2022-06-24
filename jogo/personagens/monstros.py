from asyncio import sleep
from collections import Counter
from random import choice, randint

from jogo.itens.armas import tudo as armas
from jogo.itens.quest import ItemQuest
from jogo.itens.vestes import tudo as vestes
from jogo.tela.imprimir import Imprimir, efeito_digitando, formatar_status
from jogo.utils import Contador, arrumar_porcentagem, regra_3

tela = Imprimir()


class Monstro:
    def __init__(self, level=1, status={}):
        self.experiencia = 50 * level
        self.status = Counter(
            status
            or {
                "vida": 100,
                "dano": 3,
                "resistencia": 5,
                "velo-ataque": 1,
                "critico": 5,
                "armadura": 5,
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
        porcentagem = enumerate([25, 50, 75, 100, 125, 150, 175, 200], 1)
        self._porcentagem_arm_res_total = dict(porcentagem)
        self.porcentagem_armadura = 0
        self.porcentagem_resistencia = 0
        self.atualizar_status()
        self._contador = Contador(4)

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
            Item = choice(vestes + armas)
            if Item.tipo == 'Arma':
                status = [randint(1, 5), randint(1, 2), randint(1, 3)]
                status = map(lambda x: x * self.level, status)
                status_nomes = ["dano", "velo_ataque", "critico"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            elif Item.tipo == 'Roupa': # a classe tem tipo -> Roupa
                status = [
                    randint(1, 6),
                    randint(5, 20),
                    randint(1, 6),
                ]
                status = map(lambda x: x * self.level, status)
                status_nomes = ["armadura", "vida", "resistencia"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(**status_dict)
            elif Item.tipo in ['Anel', 'Amuleto']:
                status = [
                    randint(1, 3),
                    randint(3, 20),
                    randint(1, 6),
                    randint(1, 6),
                ]
                status = map(lambda x: x * self.level, status)
                status_nomes = ["dano", "vida", "resistencia", "armadura"]
                status_dict = dict(zip(status_nomes, status))
                item = Item(nome="Anel", **status_dict)
            personagem.moedas["Pratas"] += randint(
                30 * self.level, 50 * self.level
            )
            if personagem.e_possivel_guardar(item):
                personagem.guardar_item(item)
            else:
                tela.imprimir(
                    "não foi possível adicionar item ao inventario, "
                    "inventario cheio."
                )
                sleep(3)

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
                quest.monstro == self.nome,
            ]
            if all(condicoes):
                tela.imprimir(f"Item {quest.item.nome} adiquirido\n")
                if personagem.e_possivel_gardar(quest.item):
                    personagem.guardar_item(quest.item)

    def __str__(self):
        status = (
            f"{self.nome}(vida={self.status['vida']}, level={self.level},"
            f"dano={self.status['dano']})"
        )
        return status

    def dar_experiencia(self, personagem):
        personagem.experiencia.depositar_experiencia(self.experiencia)

    def atualizar_status(self):
        self.atualizar_porcentagem()

    def atualizar_porcentagem(self):
        self.porcentagem_armadura = arrumar_porcentagem(
            regra_3(
                self._porcentagem_arm_res_total[self.level],
                100,
                self.status["armadura"],
            )
        )
        self.porcentagem_resistencia = arrumar_porcentagem(
            regra_3(
                self._porcentagem_arm_res_total[self.level],
                100,
                self.status["resistencia"],
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


class Boss(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experiencia *= 2

    def sortear_drops(self, personagem):
        """Método que dá item e pratas ao personagem."""
        efeito_digitando("Loot encontrado.")
        Item = choice(vestes + armas)
        if Item.tipo == 'Arma':
            status = [randint(3, 5), randint(2, 2), randint(2, 3)]
            status = map(lambda x: x * self.level, status)
            status_nomes = ["dano", "velo_ataque", "critico"]
            status_dict = dict(zip(status_nomes, status))
            item = Item(**status_dict)
        elif Item.tipo == 'Roupa': # a classe tem tipo -> Roupa
            status = [
                randint(3, 6),
                randint(12, 20),
                randint(3, 6),
            ]
            status = map(lambda x: x * self.level, status)
            status_nomes = ["armadura", "vida", "resistencia"]
            status_dict = dict(zip(status_nomes, status))
            item = Item(**status_dict)
        elif Item.tipo in ['Anel', 'Amuleto']:
            status = [
                randint(2, 3),
                randint(12, 20),
                randint(2, 3),
                randint(2, 3),
            ]
            status = map(lambda x: x * self.level, status)
            status_nomes = ["dano", "vida", "resistencia", "armadura"]
            status_dict = dict(zip(status_nomes, status))
            item = Item(nome="Anel", **status_dict)
        personagem.moedas["Pratas"] += randint(30 * self.level, 50 * self.level)
        if personagem.e_possivel_guardar(item):
            personagem.guardar_item(item)
        else:
            tela.imprimir(
                    "não foi possível adicionar item ao inventario, "
                    "inventario cheio."
                )
            sleep(3)


class Tartaruga(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.investida, self.garras_afiadas]
        self.nome = "Tartaruga"
        self.classe = "Monstro comum"
        self.tipo = "Tatu bola"

    def investida(self, other):
        """Método que ataca o personagem."""
        dano = 4 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def garras_afiadas(self, other):
        """Método que ataca o personagem."""
        dano = 6 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano


class Camaleao(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.trapasseiro, self.roubo]
        self.nome = "Camaleão"
        self.classe = "Monstro comum"
        self.tipo = "trolador"

    def trapasseiro(self, other):
        """Método que ataca o personagem."""
        dano = 4 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def roubo(self, other):
        """Método que ataca o personagem."""
        dano = 5 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano


class Tamandua(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.abraco, self.linguada]
        self.nome = "Tamandua"
        self.classe = "Monstro comum"
        self.tipo = "trolador"

    def abraco(self, other):
        """Método que ataca o personagem."""
        dano = 5 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def linguada(self, other):
        """Método que ataca o personagem."""
        dano = 3 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano


class Sapo(Monstro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.salto, self.linguada]
        self.nome = "Sapo"
        self.classe = "Monstro comum"
        self.tipo = "trolador"

    def salto(self, other):
        """Método que ataca o personagem."""
        dano = 5 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano

    def linguada(self, other):
        """Método que ataca o personagem."""
        dano = 3 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano


class Topera(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.pulo_fatal, self.terremoto]
        self.nome = "Topera"
        self.classe = "Monstro chefe"
        self.tipo = "boss"

    def pulo_fatal(self, other):
        """Método que ataca o personagem."""
        dano = 7 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def terremoto(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano


class Mico(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.tacar_banana, self.esmagar]
        self.nome = "Mico"
        self.classe = "Monstro chefe"
        self.tipo = "boss"

    def tacar_banana(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano

    def esmagar(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano


class Sucuri(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.lancamento_de_calda, self.bote]
        self.nome = "Sucuri"
        self.classe = "Monstro chefe"
        self.tipo = "boss"

    def lancamento_de_calda(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def bote(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano


class ArvoreDeku(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.braçada, self.outono]
        self.nome = "Arvore Deku"
        self.classe = "Monstro chefe"
        self.tipo = "boss"

    def braçada(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def outono(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano


class Dragao(Boss):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.habilidades = [self.patada, self.fogo]
        self.nome = "Dragão ancião"
        self.classe = "Monstro chefe"
        self.tipo = "boss"

    def patada(self, other):
        """Método que ataca o personagem."""
        dano = 10 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
        other.status["vida"] -= dano - subtrair_dano

    def fogo(self, other):
        """Método que ataca o personagem."""
        dano = 15 * self.level
        subtrair_dano = regra_3(100, dano, other.porcentagem_resistencia)
        other.status["vida"] -= dano - subtrair_dano

    def sortear_drops(self, personagem):
        super().sortear_drops(personagem)
        personagem.inventario.append(ItemQuest("Coração de Dragão"))


monstros_comuns = [Tartaruga, Camaleao, Tamandua, Sapo]
bosses_comuns = [Topera, Mico, Sucuri, ArvoreDeku]
