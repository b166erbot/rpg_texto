from copy import copy
from time import sleep

from jogo.itens.moedas import Draconica
from jogo.itens.quest import ItemQuest
from jogo.tela.imprimir import Imprimir
from jogo.utils import Artigo, chunk

tela = Imprimir()


class Npc:
    def __init__(self, nome: str, tipo: str):
        self.nome = nome
        self.tipo = tipo

    def __str__(self):
        return f"{self.nome}[{self.tipo}]"

    def __repr__(self):
        return f"{self.nome}[{self.tipo}]"


class Comerciante(Npc):
    def __init__(self, nome: str, itens: list):
        super().__init__(nome, "Comerciante")
        self._itens = itens
        self.itens = dict()
        self.tabela_cortada = []
        self.itens_criados = []
        self.salvar = False

    def interagir(self, personagem):
        """Método que mostra os itens e obtem o número da compra."""
        textos = [
            "comprar",
            "vender",
        ]
        textos_enumerados = list(enumerate(textos, 1))
        numeros_texto = [str(n) for n, texto in textos_enumerados]
        numero = ":1"
        numeros_pagina = [":1", ":2"]
        while numero in numeros_pagina + numeros_texto:
            tela.limpar_tela()
            for numero, texto in textos_enumerados:
                tela.imprimir(f"{numero} - {texto}\n")
            tela.imprimir("O que deseja fazer?: ")
            numero = tela.obter_string()
            if numero == "1":
                self.interagir_comprar(personagem)
            if numero == "2":
                self.interagir_vender(personagem)

    def interagir_vender(self, personagem):
        """Método que interage com o usuário e vende itens."""
        itens = filter(_retornar_itens_equipaveis, personagem.inventario)
        itens = [
            f"{numero} - {item} {item.preco}"
            for numero, item in enumerate(itens)
        ]
        if len(itens) == 0:
            tela.imprimir("você não tem itens no inventario.")
            sleep(2)
            return
        itens = chunk(itens, 16)
        numero = self._obter_numero(
            "deseja vender qual equipamento?: ",
            personagem,
            itens,
        )
        while bool(numero):
            tela.limpar_tela()
            inventario = {
                str(n): item for n, item in enumerate(personagem.inventario)
            }
            if len(inventario) == 0:
                break
            equipamento = inventario.get(numero)
            if equipamento is not None:
                if not isinstance(equipamento, ItemQuest):
                    self.vender(personagem, equipamento, equipamento.preco.nome)
                    tela.imprimir(
                        f"item {equipamento} vendido. {equipamento.preco}"
                    )
            itens = [
                f"{numero} - {item}"
                for numero, item in enumerate(personagem.inventario)
            ]
            itens = chunk(itens, 16)
            numero = self._obter_numero(
                "deseja vender qual equipamento?: ",
                personagem,
                itens,
            )

    def interagir_comprar(self, personagem):
        """Método que interage com o usuário e compra itens."""
        self.itens = self._criar_itens(personagem.level)
        self.tabela_cortada = self._criar_tabela()
        tela.limpar_tela()
        numero = self._obter_numero(
            "O que deseja comprar?: ",
            personagem,
            self.tabela_cortada,
        )
        while numero in self.itens:
            tela.imprimir("Quantidade: ", "cyan")
            quantidade = tela.obter_string()
            if not bool(quantidade):
                break
            item = self.itens[numero]
            self.comprar(item, int(quantidade), personagem, item.preco.nome)
            tela.limpar_tela()
            numero = self._obter_numero(
                "Deseja mais alguma coisa?: ",
                personagem,
                self.tabela_cortada,
            )
        tela.limpar_tela()
        tela.imprimir("volte sempre!", "cyan")
        sleep(1)

    def comprar(self, item, quantidade: int, personagem, tipo_de_moeda: str):
        """Método que de fato, faz a compra dos itens."""
        preço = quantidade * int(item.preco)
        if int(personagem.moedas[tipo_de_moeda]) >= preço:
            personagem.moedas[tipo_de_moeda] -= preço
            # ao comprar, guarda o item de qualquer forma.
            for n in range(quantidade):
                personagem.inventario.append(copy(item))
        else:
            texto = "compra não realizada: dinheiro insuficiente"
            tela.imprimir(texto, "cyan")
            sleep(3)

    def vender(self, personagem, equipamento, tipo_de_moeda: str):
        personagem.moedas[tipo_de_moeda] += equipamento.preco
        index = personagem.inventario.index(equipamento)
        personagem.inventario.pop(index)

    def _obter_numero(self, mensagem: str, personagem, itens_cortados):
        """Método que organiza as páginas para o usuário e retorna um numero."""
        numeros_paginas = {
            f":{n}": n for n in range(1, len(itens_cortados) + 1)
        }
        numero = ":1"
        while numero in numeros_paginas:
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens_cortados)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            tela.imprimir(
                f"seu dinheiro: {personagem.moedas['Pratas']} "
                f"- {personagem.moedas['Draconica']} "
                f"- {personagem.moedas['Glifos']}\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for texto in itens_cortados[n - 1]:
                tela.imprimir(texto + "\n", "cyan")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        return numero

    def _criar_tabela(self):
        tabela = []
        for numero, item in self.itens.items():
            if item.tipo == "Poções":
                texto = (
                    f"{numero} - {item.nome}. "
                    f"{item.preco} quanto cura: {item.quanto_cura}"
                )
            else:
                texto = f"{numero} - {item.nome}. {item.preco}"
            tabela.append(texto)
        return chunk(tabela, 16)

    def _criar_itens(self, level):
        self.itens_criados = []
        for item in self._itens:
            if item.tipo == "Poções":
                self.itens_criados.append(item())
            elif item.tipo == "Roupa":
                atributos = [20, 6, 6, level]
                atributos_nomes = ["vida", "resistencia", "armadura", "level"]
                atributos_dict = dict(zip(atributos_nomes, atributos))
                self.itens_criados.append(item(**atributos_dict))
        return {
            str(numero): item
            for numero, item in enumerate(self.itens_criados, 1)
        }


class Pessoa(Npc):
    def __init__(self, nome: str):
        super().__init__(nome, "Pessoa do vilarejo")
        self.quest_atual = False
        self.salvar = True

    def missao(self, personagem):
        """Método que coloca a missão na tela para o personagem."""
        quests = [
            quest
            for quest in self.quests
            if all(
                [
                    not quest.finalizada,
                    not quest.iniciada,
                    quest.level <= personagem.level,
                ]
            )
        ]
        if len(quests) > 0:
            quest = quests[0]
            quest.historia()
            aceito = quest.aceitar()
            if aceito:
                personagem.quests.append(quest)
                quest.iniciada = True

    def entregar_quest(self, personagem):
        """
        Método que recebe a quest devolta, paga e da o xp para o personagem.
        """
        itens = list(
            filter(
                lambda x: self.quest_atual.item.nome == x.nome,
                personagem.inventario,
            )
        )
        quest = self.quest_atual
        if len(itens) == quest.numero_de_itens_requeridos:
            quest.pagar(personagem)
            quest.depositar_xp(personagem)
            quest.depositar_item(personagem)
            personagem.atualizar_status()
            quests = filter(lambda q: q == quest, personagem.quests)
            for q in quests:
                index = personagem.quests.index(q)
                personagem.quests.pop(index)
            for item in itens:
                index = personagem.inventario.index(item)
                personagem.inventario.pop(index)
            self.quest_atual.finalizada = True
            tela.imprimir(
                f"{self.nome}: Muito obrigad{Artigo(self.nome)}."
                f" aqui está seu dinheiro ${self.quest_atual.valor} "
                f"xp={self.quest_atual.xp}",
                "cyan",
            )
            sleep(3)
        else:
            tela.imprimir("complete a missão e depois volte aqui", "cyan")
            sleep(3)

    def interagir(self, personagem):
        """Método que dá a quest para o personagem."""
        tela.limpar_tela()
        if not self.quest_atual or self.quest_atual.finalizada:
            self.proxima_quest(personagem.level)
        if not self.quest_atual:
            tela.imprimir(f"{self.nome}: não tenho mais nada a pedir.", "cyan")
            if len(self._obter_quests_nao_iniciadas2(personagem.level)):
                tela.imprimir(" volte quando tiver mais level\n", "cyan")
            sleep(3)
            return
        if self.quest_atual.iniciada and not self.quest_atual.finalizada:
            self.entregar_quest(personagem)
        else:
            self.missao(personagem)

    def receber_quest(self, quests: list):
        """Método que recebe as quests."""
        quests = sorted(quests, key=lambda quest: quest.level)
        self.quests = quests
        self.proxima_quest(1)

    def proxima_quest(self, level):
        """Método que define a próxima quest."""
        if not self.quest_atual:
            self._definir_proxima_quest(level)
        else:
            if self.quest_atual.finalizada:
                self._definir_proxima_quest(level)

    def _definir_proxima_quest(self, level):
        """Método auxiliar que define a proxima quest."""
        quests = self._obter_quests_nao_iniciadas(level)
        if len(quests):
            self.quest_atual = quests[0]
        else:
            self.quest_atual = False

    def _obter_quests_nao_iniciadas(self, level):
        """Método que retorna as quests não iniciadas do level pra baixo."""
        return [
            quest
            for quest in self.quests
            if not quest.iniciada and quest.level <= level
        ]

    def _obter_quests_nao_iniciadas2(self, level):
        """Método que retorna as quests não iniciadas do level pra cima"""
        return [
            quest
            for quest in self.quests
            if not quest.iniciada and quest.level > level
        ]


class ComercianteItemQuest(Npc):
    def __init__(self, nome: str, itens: list, requisitos: list):
        super().__init__(nome, "Comerciante Item Quest")
        self.itens = {numero: item for numero, item in enumerate(itens, 1)}
        itens = zip(self.itens.items(), requisitos)
        self.tabela = [
            f"{numero} - {item.nome}. requerido -> {item_requerido}"
            for (numero, item), item_requerido in itens
        ]
        self.tabela_cortada = chunk(self.tabela, 16)
        self.salvar = False

    def distinguir_moeda(self, item, personagem):
        """Método que faz as compras pelo personagem."""
        if issubclass(item, Draconica):
            self.comprar_draconica(item, personagem)

    def comprar_draconica(self, item, personagem):
        tela.limpar_tela()
        item = ItemQuest("Coração de Dragão")
        condicoes = [personagem.inventario.count(item) > 0]
        if all(condicoes):
            coracoes = list(filter(lambda x: x == item, personagem.inventario))
            for coracao in coracoes:
                index = personagem.inventario.index(coracao)
                personagem.inventario.pop(index)
                personagem.moedas["Draconica"] += 15
            tela.imprimir(f"{len(coracoes)} coração(ões) vendido(s)")
        else:
            tela.imprimir("você não tem corações de dragão.")
        sleep(3)

    def interagir(self, personagem):
        """Método que mostra os itens e obtem o número da compra."""
        tela.limpar_tela()
        numero = self._obter_numero("O que deseja trocar?: ", personagem)
        while numero.isnumeric() and int(numero) in self.itens:
            self.distinguir_moeda(self.itens[int(numero)], personagem)
            tela.limpar_tela()
            numero = self._obter_numero(
                "Deseja mais alguma coisa?: ", personagem
            )
        tela.limpar_tela()
        tela.imprimir("volte sempre!", "cyan")
        sleep(1)

    def _obter_numero(self, mensagem: str, personagem):
        """Método que organiza as páginas para o usuário e retorna um numero."""
        numeros_paginas = {
            f":{n}": n for n in range(1, len(self.tabela_cortada) + 1)
        }
        numero = ":1"
        while numero in numeros_paginas:
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(self.tabela_cortada)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            tela.imprimir(
                f"seu dinheiro: {personagem.moedas['Pratas']} "
                f"- {personagem.moedas['Draconica']}\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for texto in self.tabela_cortada[n - 1]:
                tela.imprimir(texto + "\n", "cyan")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        return numero


class Banqueiro(Npc):
    def __init__(self, nome: str):
        super().__init__(nome, "Banqueiro")
        self.nome = nome
        self.salvar = True
        self.tamanho_do_inventario = 30
        self.inventario = []

    def e_possivel_guardar(self, item):
        """Método que verifica se é possível guardar item no inventario."""
        if len(self.inventario) < self.tamanho_do_inventario:
            return True
        else:
            return False

    def guardar_item(self, item, personagem):
        """Método que guarda um item no inventario do banqueiro."""
        # guardar o item no banqueiro
        self.inventario.append(item)
        # remover o item no inventario
        index = personagem.inventario.index(item)
        personagem.inventario.pop(index)

    def retirar(self, item, personagem):
        """Método que retira um item do inventario do banqueiro."""
        index = self.inventario.index(item)
        if personagem.e_possivel_guardar(item):
            personagem.inventario.append(item)
            self.inventario.pop(index)
        else:
            tela.imprimir(
                "não foi possível adicionar item ao inventario, "
                "inventario cheio.\n"
            )
            sleep(3)

    def interagir(self, personagem):
        """Método que interage com o personagem."""
        tela.limpar_tela()
        tela.imprimir("1 -> guardar, 2 -> retirar\n")
        tela.imprimir("deseja guardar ou retirar um item?: ")
        numero = tela.obter_string()
        while numero.isnumeric():
            if numero == "1":  # gardar
                item = self._obter_equipamentos_personagem(
                    "deseja guardar qual item?: ", personagem
                )
                if bool(item):
                    if self.e_possivel_guardar(item):
                        self.guardar_item(item, personagem)
                    else:
                        tela.imprimir("inventario do banqueiro cheio.")
                        sleep(2)
            elif numero == "2":  # retirar
                item = self._obter_equipamentos_banqueiro(
                    "deseja obter qual item?: ", personagem
                )
                if bool(item):
                    self.retirar(item, personagem)
            tela.limpar_tela()
            tela.imprimir("1 -> guardar, 2 -> adquirir\n")
            tela.imprimir("deseja guardar ou adquirir um item?: ")
            numero = tela.obter_string()

    def _obter_equipamentos_personagem(self, mensagem: str, personagem):
        """Método que organiza as páginas para o usuário e retorna um item."""
        itens = list(enumerate(personagem.inventario))
        itens_dict = {str(numero): item for numero, item in itens}
        if len(itens) == 0:
            tela.imprimir("você não tem itens no inventario.", "cyan")
            sleep(2)
            return ""
        itens = chunk(itens, 18)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n - 1]:
                mensagem2 = f"{numero} - {item}"
                tela.imprimir(mensagem2 + "\n")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        item = itens_dict.get(numero)
        return item

    def _obter_equipamentos_banqueiro(self, mensagem: str, personagem):
        """Método que organiza as páginas para o usuário e retorna um item."""
        itens = list(enumerate(self.inventario))
        itens_dict = {str(numero): item for numero, item in itens}
        if len(itens) == 0:
            tela.imprimir(
                "você não tem itens no inventario do banqueiro.", "cyan"
            )
            sleep(2)
            return ""
        itens = chunk(itens, 18)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n - 1]:
                mensagem2 = f"{numero} - {item}"
                tela.imprimir(mensagem2 + "\n")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        item = itens_dict.get(numero)
        return item


class Ferreiro(Npc):
    def __init__(self, nome: str):
        super().__init__(nome, "Ferreiro")
        self.salvar = False

    def interagir(self, personagem):
        """Método que interage com o personagem."""
        textos = [
            "derreter arma",
            "acrescentar glifos",
            "remover glifos",
        ]
        textos_enumerados = list(enumerate(textos, 1))
        numeros_texto = [str(n) for n, texto in textos_enumerados]
        numero = ":1"
        numeros_pagina = [":1", ":2"]
        while numero in numeros_pagina + numeros_texto:
            tela.limpar_tela()
            for numero, texto in textos_enumerados:
                tela.imprimir(f"{numero} - {texto}\n")
            tela.imprimir("O que deseja fazer?: ")
            numero = tela.obter_string()
            if numero == "1":
                self.derreter_item(personagem)
            elif numero == "2":
                self.acrescentar_glifos(personagem)
            elif numero == "3":
                self.remover_glifos(personagem)

    def derreter_item(self, personagem):
        """Método que escolhe itens e os derretem."""
        equipamentos = list(
            filter(
                _retornar_itens_equipaveis,
                personagem.inventario,
            )
        )
        if len(equipamentos) == 0:
            tela.imprimir("você não tem itens no inventario.", "cyan")
            sleep(3)
            return
        item = self._obter_numero_equipamentos(
            equipamentos,
            "deseja derreter qual item?: ",
            personagem,
        )
        while bool(item):
            personagem.moedas["Glifos"] += item.glifos
            index = personagem.inventario.index(item)
            personagem.inventario.pop(index)
            equipamentos = list(
                filter(
                    _retornar_itens_equipaveis,
                    personagem.inventario,
                )
            )
            if len(equipamentos) == 0:
                break
            item = self._obter_numero_equipamentos(
                equipamentos,
                "deseja derreter qual item?: ",
                personagem,
            )

    def acrescentar_glifos(self, personagem):
        """Método que escolhe itens e os acrecentam glifos."""
        equipamentos = [
            equipamento
            for equipamento in personagem.equipamentos.values()
            if bool(equipamento)
        ]
        equipamentos += list(
            filter(
                _retornar_itens_equipaveis,
                personagem.inventario,
            )
        )
        if len(equipamentos) == 0:
            tela.imprimir(
                "você não tem itens no inventario e nem equipados.", "cyan"
            )
            sleep(3)
            return
        item = self._obter_numero_equipamentos(
            equipamentos,
            "deseja acrescentar em qual equipamento?: ",
            personagem,
        )
        while bool(item):
            tela.limpar_tela()
            tela.imprimir(f"seus glifos: {personagem.moedas['Glifos']}\n")
            maximo_glifos_acrescentar = item.glifos_level.valor_faltando()
            tela.imprimir(
                "Quantos glifos deseja acrescentar "
                f"[maximo {maximo_glifos_acrescentar}]: "
            )
            quantidade = tela.obter_string()
            if not quantidade.isnumeric():
                break
            if int(personagem.moedas["Glifos"]) < int(quantidade):
                tela.imprimir(f"você não tem {quantidade} glifo(s).")
                sleep(3)
            elif int(quantidade) > maximo_glifos_acrescentar:
                tela.imprimir(
                    "não é possível inserir mais que o máximo: "
                    f"{maximo_glifos_acrescentar}"
                )
                sleep(3)
            else:
                item.receber_glifos(int(quantidade))
                personagem.moedas["Glifos"] -= int(quantidade)
                tela.imprimir(f"item: {item}")
                sleep(3)
            equipamentos = [
                equipamento
                for equipamento in personagem.equipamentos.values()
                if bool(equipamento)
            ]
            equipamentos += list(
                filter(
                    _retornar_itens_equipaveis,
                    personagem.inventario,
                )
            )
            item = self._obter_numero_equipamentos(
                equipamentos,
                "deseja acrescentar em qual equipamento?: ",
                personagem,
            )

    def remover_glifos(self, personagem):
        """Método que escolhe um item e remove os glifos dele."""
        equipamentos = []
        for equipamento in personagem.equipamentos.values():
            if (
                bool(equipamento)
                and equipamento.glifos_level.valor_glifos() > 0
            ):
                equipamentos.append(equipamento)
        equipamentos_ = list(
            filter(
                _retornar_itens_equipaveis,
                personagem.inventario,
            )
        )
        equipamentos_ = filter(
            lambda x: x.glifos_level.valor_glifos() > 0, equipamentos_
        )
        equipamentos += equipamentos_
        if len(equipamentos) == 0:
            tela.imprimir(
                "você não tem itens no inventario e nem equipados "
                "que contenham glifos.",
                "cyan",
            )
            sleep(3)
            return
        item = self._obter_numero_equipamentos(
            equipamentos,
            "deseja retirar de qual equipamento?: ",
            personagem,
        )
        while bool(item):
            tela.limpar_tela()
            tela.imprimir(
                f"seus glifos: {personagem.moedas['Glifos']} "
                f"suas pratas: {personagem.moedas['Pratas']}\n"
            )
            valor = int(item.glifos_level.valor_glifos() * 0.30)
            tela.imprimir(
                "tem certeza que deseja remover os glifos? "
                f"Pratas {valor} [s/n]: "
            )
            resposta = tela.obter_string()
            if resposta in ["s", "sim"]:
                if int(personagem.moedas["Pratas"]) >= valor:
                    personagem.moedas["Pratas"] -= valor
                    glifos = item.remover_glifos()
                    personagem.moedas["Glifos"] += glifos
                    tela.imprimir(f"item: {item}")
                    sleep(3)
                else:
                    tela.imprimir("você não tem dinheiro suficiente.")
                    sleep(3)
            equipamentos = []
            for equipamento in personagem.equipamentos.values():
                if (
                    bool(equipamento)
                    and equipamento.glifos_level.valor_glifos() > 0
                ):
                    equipamentos.append(equipamento)
            equipamentos_ = list(
                filter(
                    _retornar_itens_equipaveis,
                    personagem.inventario,
                )
            )
            equipamentos_ = filter(
                lambda x: x.glifos_level.valor_glifos() > 0, equipamentos_
            )
            equipamentos += equipamentos_
            if len(equipamentos) == 0:
                break
            item = self._obter_numero_equipamentos(
                equipamentos,
                "deseja retirar em qual equipamento?: ",
                personagem,
            )

    def _obter_numero_equipamentos(self, equipamentos, mensagem, personagem):
        """Método que organiza as páginas para o usuário e retorna um item."""
        itens = list(enumerate(equipamentos))
        itens_dict = {str(n): item for n, item in itens}
        itens = chunk(itens, 18)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n - 1]:
                mensagem2 = f"{numero} - {item} level: {item.level}"
                equipamento_equipado = map(
                    lambda x: x is item, personagem.equipamentos.values()
                )
                if any(equipamento_equipado):
                    tela.imprimir(mensagem2 + "\n", "amarelo")
                else:
                    tela.imprimir(mensagem2 + "\n", "cyan")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        return itens_dict.get(numero)


def _retornar_itens_equipaveis(item):
    tipos = [
        "Peitoral",
        "Elmo",
        "Calça",
        "Botas",
        "Luvas",
        "Arma",
        "Anel",
        "Amuleto",
        "Adorno de arma",
        "Escudo",
    ]
    return item.tipo in tipos
