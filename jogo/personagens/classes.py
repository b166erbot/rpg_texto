from asyncio import sleep
from collections import Counter
from random import randint
from time import sleep as sleep2

from jogo.experiencia import Experiencia
from jogo.itens.armas import (
    Adaga,
    Arco_curto,
    Arco_longo,
    Botas_de_ferro,
    Cajado,
    Cajado_negro,
    Espada_curta,
    Espada_longa,
    Luvas_de_ferro,
    Machado,
)
from jogo.itens.itens import CalcularBonus, SemItemEquipado
from jogo.itens.moedas import Draconica, Pratas
from jogo.itens.pocoes import curas
from jogo.itens.quest import ItemQuest
from jogo.itens.vestes import roupas_draconicas
from jogo.itens.vestes import tudo as roupas
from jogo.tela.imprimir import Imprimir, formatar_status
from jogo.utils import Contador, arrumar_porcentagem, regra_3

tela = Imprimir()


class Humano:
    """
    Classe geral para cada classe de personagem no jogo.

    o que os atributos aumentão?
    vitalidade - vida
    fortividade - dano físico
    resistência - resistência a magia[
        fogo, gelo, raio, veneno, magia do submundo
    ]
    inteligência - dano mágico
    crítico - dano crítico
    destreza - velocidade ataque, habilidade com armas
    movimentação - velocidade movimentação
    """

    def __init__(
        self,
        nome,
        jogador=False,
        level=1,
        status={},
        experiencia=0,
        moedas={"Pratas": 1500, "Draconica": 0},
        peitoral=SemItemEquipado("Peitoral"),
        elmo=SemItemEquipado("Elmo"),
        calca=SemItemEquipado("Calça"),
        botas=SemItemEquipado("Botas"),
        luvas=SemItemEquipado("Luvas"),
        arma=SemItemEquipado("Arma"),
        Anel=SemItemEquipado("Anel"),
    ):
        self.nome = nome
        self.level = level
        leveis = [499, 999, 1999, 3499, 5499, 7999, 10999, 14499]
        self.experiencia = Experiencia(experiencia, leveis)
        self.status = Counter(
            status
            or {
                "vida": 100,
                "dano": 5,
                "resistencia": 0,
                "velo-ataque": 1,
                "criti": 0,
                "armadura": 0,
                "magia": 100,
                "stamina": 100,
                "velo-movi": 1,
            }
        )
        self.habilidades = {}
        self.inventario = []
        self.moedas = moedas
        self.moedas["Pratas"] = Pratas(self.moedas["Pratas"])
        self.moedas["Draconica"] = Draconica(self.moedas["Draconica"])
        self.jogador = jogador
        self.equipamentos = {
            "Peitoral": peitoral,
            "Elmo": elmo,
            "Calça": calca,
            "Botas": botas,
            "Luvas": luvas,
            "Arma": arma,
            "Anel": Anel,
        }
        self.quests = []
        porcentagem = enumerate([27, 54, 81, 108, 135, 162, 189, 216], 1)
        self._porcentagem_arm_res_total = dict(porcentagem)
        self.porcentagem_armadura = 0
        self.porcentagem_resistencia = 0
        self._calcular_bonus = CalcularBonus(self)
        self.atualizar_status()
        self._contador = Contador(4)

    @property
    def vida_maxima(self):
        """Método que retorna a vida máxima."""
        equipamentos = filter(lambda x: x, self.equipamentos.values())
        equipamentos = filter(
            lambda x: x.tipo in ["Elmo", "Peitoral", "Calça", "Botas", "Anel"],
            equipamentos,
        )
        vida = map(lambda x: x.vida, equipamentos)
        vida = 100 + (15 * (self.level - 1)) + sum(vida)
        return vida

    def atacar(self, other):
        """Método que escolhe se ataca como bot ou não."""
        if self.jogador:
            return self._atacar_como_jogador(other)
        return self._atacar_como_bot(other)

    async def _atacar_como_bot(self, other):
        """Método que ataca como bot."""
        while all([other.status["vida"] > 0, self.status["vida"] > 0]):
            self.consumir_pocoes()
            if randint(0, 2) == 2:
                habilidade = self.habilidades[randint(1, 2)]
                if self.consumir_magia_stamina():
                    habilidade(other)
                    self._contador.resetar()
            else:
                dano = self.status["dano"]
                subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
                other.status["vida"] -= dano - subtrair_dano
                other.arrumar_vida()
                self._contador.acrescentar()
            if self._contador.usar:
                self._recuperar_magia_stamina()
            tela.imprimir_combate(formatar_status(self), self)
            await sleep(0.2)
        tela.imprimir_combate(formatar_status(self), self)
        await sleep(1)

    async def _atacar_como_jogador(self, other):
        """Método que ataca como jogador."""
        while all([other.status["vida"] > 0, self.status["vida"] > 0]):
            self.consumir_pocoes()
            dano = self.status["dano"]
            subtrair_dano = regra_3(100, dano, other.porcentagem_armadura)
            other.status["vida"] -= dano - subtrair_dano
            caracter = tela.obter_caracter()
            if caracter != -1 and chr(caracter).isnumeric():
                caracter = int(chr(caracter))
                if caracter in [1, 2]:
                    habilidade = self.habilidades[caracter]
                    if self.consumir_magia_stamina():
                        habilidade(other)
                        self._contador.resetar()
                else:
                    self._contador.acrescentar()
            else:
                self._contador.acrescentar()
            if self._contador.usar:
                self._recuperar_magia_stamina()
            other.arrumar_vida()
            tela.imprimir_combate(formatar_status(self), 1)
            await sleep(0.5)
        tela.imprimir_combate(formatar_status(self), 1)
        await sleep(0.5)

    def arrumar_vida(self):
        """Método que arruma a vida para não sair do limite permitido."""
        if self.status["vida"] < 0:
            self.status["vida"] = 0
        if self.status["vida"] > self.vida_maxima:
            self.status["vida"] = self.vida_maxima

    def ressucitar(self):
        """Método que ressucita o personagem."""
        self.status["vida"] = self.vida_maxima

    def consumir_pocoes(self):
        """Método que consome a poção caso você tenha."""
        if self.status["vida"] <= 30:
            pocao = self._dropar_pocoes()
            if bool(pocao):
                self.status["vida"] += pocao.consumir(self.vida_maxima)
                self.arrumar_vida()

    def _dropar_pocoes(self) -> list:
        """Método que retorna uma poção caso você tenha."""
        nome_pocoes = list(map(lambda x: x.nome, curas))
        poções = [x for x in self.inventario if x.nome in nome_pocoes]
        if bool(poções):
            index = self.inventario.index(poções[0])
            poção = self.inventario.pop(index)
            return poção
        return False

    def recuperar_magia_stamina_cem_porcento(self):
        """Método que recupera a magia e stamina para máximo."""
        self.status["magia"] = 100
        self.status["stamina"] = 100

    # é melhor deixar que a instância desequipe.
    def vender(self, equipamento):
        """Método que vende um item no inventário."""
        if isinstance(equipamento.preco, Pratas):
            self.moedas["Pratas"] += equipamento.preco
        elif isinstance(equipamento.preco, Draconica):
            self.moedas["Draconica"] += equipamento.preco
        index = self.inventario.index(equipamento)
        self.inventario.pop(index)

    def desequipar(self, equipamento):
        """Método que desequipa um item no inventário."""
        equipamento2 = self.equipamentos.get(equipamento.tipo)
        if equipamento2 and equipamento2 is equipamento:
            guardado = self.guardar_item(equipamento)
            if guardado:
                self.equipamentos[equipamento.tipo] = SemItemEquipado(
                    equipamento.tipo
                )
                self.atualizar_status()

    def equipar(self, equipamento):
        raise NotImplementedError("Método não implementado.")

    def atualizar_status(self):
        """Método que atualiza o status."""
        self.level = self.experiencia.level
        equipamentos = [
            equipamento
            for equipamento in self.equipamentos.values()
            if bool(equipamento)
        ]
        vestes = list(
            filter(
                lambda x: x.tipo
                in ["Elmo", "Peitoral", "Calça", "Botas", "Anel"],
                equipamentos,
            )
        )
        equipamentos_dano = filter(
            lambda x: x.tipo in ["Anel", "Arma"], equipamentos
        )
        dano = map(lambda x: x.dano, equipamentos_dano)
        dano = 5 + sum(dano)
        vida = self.vida_maxima
        resistencia = sum(map(lambda x: x.resistencia, vestes))
        armadura = sum(map(lambda x: x.armadura, vestes))
        self.status["vida"] = vida
        self.status["resistencia"] = resistencia
        self.status["armadura"] = armadura
        self.status["dano"] = dano
        self.atualizar_porcentagem()
        self._calcular_bonus.calcular(self.equipamentos.values())

    def atualizar_porcentagem(self):
        self.porcentagem_armadura = arrumar_porcentagem(
            regra_3(
                self._porcentagem_arm_res_total[self.level], 100, self._armadura
            )
        )
        self.porcentagem_resistencia = arrumar_porcentagem(
            regra_3(
                self._porcentagem_arm_res_total[self.level],
                100,
                self._resistencia,
            )
        )

    def guardar_item(self, item):
        """Método que guarda um item no inventario se possível."""
        itens = list(
            filter(lambda x: not isinstance(x, ItemQuest), self.inventario)
        )
        if isinstance(item, ItemQuest):
            self.inventario.append(item)
            return True
        elif len(itens) < 30:
            self.inventario.append(item)
            return True
        else:
            tela.imprimir("não foi possível adicionar item ao inventario")
            sleep2(3)
            return False

    @property
    def _armadura(self):
        """Método que retorna a armadura dos equipamentos."""
        equipamentos = [
            equipamento
            for equipamento in self.equipamentos.values()
            if bool(equipamento)
        ]
        vestes = filter(
            lambda x: x.tipo in ["Elmo", "Peitoral", "Calça", "Botas", "Anel"],
            equipamentos,
        )
        armadura = sum(map(lambda x: x.armadura, vestes))
        return armadura

    @property
    def _resistencia(self):
        """Método que retorna a resistencia dos equipamentos."""
        equipamentos = [
            equipamento
            for equipamento in self.equipamentos.values()
            if bool(equipamento)
        ]
        vestes = filter(
            lambda x: x.tipo in ["Elmo", "Peitoral", "Calça", "Botas", "Anel"],
            equipamentos,
        )
        resistencia = sum(map(lambda x: x.resistencia, vestes))
        return resistencia

    def _recuperar_magia_stamina(self):
        if self.status["magia"] <= 80:
            self.status["magia"] += 20
        elif self.status["stamina"] <= 80:
            self.status["stamina"] += 20

    def atualizar_porcentagem_por_level(self, level):
        """Método que atualiza a porcentagem dependendo do level do inimigo."""
        self.porcentagem_armadura -= 8 * level
        self.porcentagem_resistencia -= 8 * level
        if self.porcentagem_armadura < 0:
            self.porcentagem_armadura = 0
        if self.porcentagem_resistencia < 0:
            self.porcentagem_resistencia = 0


class Arqueiro(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.tres_flechas, self.flecha_de_fogo]
        self.habilidades_nomes = ["três flexas", "flecha de fogo"]
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = "Arqueiro"

    def tres_flechas(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 10, other.porcentagem_armadura)
        other.status["vida"] -= 10 - subtrair_dano

    def flecha_de_fogo(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 15, other.porcentagem_resistencia)
        other.status["vida"] -= 15 - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["stamina"] >= 20:
            self.status["stamina"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        condicao = any(
            map(
                lambda x: isinstance(equipamento, x),
                roupas + roupas_draconicas + [Arco_longo, Arco_curto],
            )
        )
        if condicao:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo]):
                self.inventario.append(self.equipamentos[equipamento.tipo])
            self.equipamentos[equipamento.tipo] = equipamento
            self.atualizar_status()


class Guerreiro(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.investida, self.esmagar]
        self.habilidades_nomes = ["investida", "esmagar"]
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = "Guerreiro"

    def investida(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 10, other.porcentagem_armadura)
        other.status["vida"] -= 10 - subtrair_dano

    def esmagar(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 15, other.porcentagem_armadura)
        other.status["vida"] -= 15 - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["stamina"] >= 20:
            self.status["stamina"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        condicao = any(
            map(
                lambda x: isinstance(equipamento, x),
                roupas
                + roupas_draconicas
                + [Espada_longa, Espada_curta, Machado],
            )
        )
        if condicao:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo]):
                self.inventario.append(self.equipamentos[equipamento.tipo])
            self.equipamentos[equipamento.tipo] = equipamento
            self.atualizar_status()


class Mago(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.bola_de_fogo, self.lanca_de_gelo]
        self.habilidades_nomes = ["bola de fogo", "lanca de gelo"]
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = "Mago"

    def bola_de_fogo(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 15, other.porcentagem_resistencia)
        other.status["vida"] -= 15 - subtrair_dano

    def lanca_de_gelo(self, other):
        """Método que ataca o oponente."""
        other.status["vida"] -= 10

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["magia"] >= 20:
            self.status["magia"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        condicao = any(
            map(
                lambda x: isinstance(equipamento, x),
                roupas + roupas_draconicas + [Cajado, Cajado_negro],
            )
        )
        if condicao:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo]):
                self.inventario.append(self.equipamentos[equipamento.tipo])
            self.equipamentos[equipamento.tipo] = equipamento
            self.atualizar_status()


class Assassino(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.lancar_faca, self.ataque_furtivo]
        self.habilidades_nomes = ["lancar faca", "ataque furtivo"]
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = "Assassino"

    def lancar_faca(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 10, other.porcentagem_armadura)
        other.status["vida"] -= 10 - subtrair_dano

    def ataque_furtivo(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 15, other.porcentagem_armadura)
        other.status["vida"] -= 15 - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["stamina"] >= 20:
            self.status["stamina"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        condicao = any(
            map(
                lambda x: isinstance(equipamento, x),
                roupas + roupas_draconicas + [Adaga],
            )
        )
        if condicao:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo]):
                self.inventario.append(self.equipamentos[equipamento.tipo])
            self.equipamentos[equipamento.tipo] = equipamento
            self.atualizar_status()


class Clerigo(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.curar, self.luz]
        self.habilidades_nomes = ["curar", "luz"]
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = "Clerigo"

    def curar(self, other):
        """Método que cura o personagem."""
        self.status["vida"] += 25
        if self.status["vida"] >= self.vida_maxima:
            self.status["vida"] = self.vida_maxima

    def luz(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 10, other.porcentagem_resistencias)
        other.status["vida"] -= 10 - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["magia"] >= 20:
            self.status["magia"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        condicao = any(
            map(
                lambda x: isinstance(equipamento, x),
                roupas + roupas_draconicas + [Cajado, Cajado_negro],
            )
        )
        if condicao:
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            if bool(self.equipamentos[equipamento.tipo]):
                self.inventario.append(self.equipamentos[equipamento.tipo])
            self.equipamentos[equipamento.tipo] = equipamento
            self.atualizar_status()


class Monge(Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habilidades = [self.combo_de_chutes, self.multiplos_socos]
        self.habilidades_nomes = ["combo_de_chutes", "multiplos_socos"]
        self.habilidades = dict(enumerate(habilidades, 1))
        self.classe = "Monge"

    def combo_de_chutes(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 15, other.porcentagem_armadura)
        other.status["vida"] -= 15 - subtrair_dano

    def multiplos_socos(self, other):
        """Método que ataca o oponente."""
        subtrair_dano = regra_3(100, 10, other.porcentagem_armadura)
        other.status["vida"] -= 10 - subtrair_dano

    def consumir_magia_stamina(self):
        """Método que consome a magia ou stamina."""
        if self.status["stamina"] >= 20:
            self.status["stamina"] -= 20
            return True
        return False

    def equipar(self, equipamento):
        """Método que equipa um equipamento."""
        condicao = any(
            map(
                lambda x: isinstance(equipamento, x), roupas + roupas_draconicas
            )
        )
        if condicao:
            # tira o equipamento do inventario
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            # se tiver equipamento equipado, mova-o para o inventario
            if bool(self.equipamentos[equipamento.tipo]):
                self.inventario.append(self.equipamentos[equipamento.tipo])
            # equipa o equipamento
            self.equipamentos[equipamento.tipo] = equipamento
        if isinstance(equipamento, Luvas_de_ferro):
            # tira o equipamento do inventario
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            # desequipa o item
            self.desequipar(self.equipamentos["Luvas"])
            # equipa o item
            self.equipamentos["Luvas"] = equipamento
        elif isinstance(equipamento, Botas_de_ferro):
            # tira o equipamento do inventario
            index = self.inventario.index(equipamento)
            self.inventario.pop(index)
            # desequipa o item
            self.desequipar(self.equipamentos["Botas"])
            # equipa o item
            self.equipamentos["Botas"] = equipamento
        self.atualizar_status()


# druida?
# dual blade?
