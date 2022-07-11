import sys
from random import choice
from time import sleep
from unittest.mock import MagicMock

from jogo.locais.areas_abertas import Floresta
from jogo.locais.areas_fechadas import CovilDoArauto
from jogo.locais.habitaveis import Vilarejo
from jogo.pets import SemPet
from jogo.save import salvar_jogo
from jogo.tela.imprimir import Imprimir, formas
from jogo.utils import Artigo, Contador2, chunk

# Silenciar o pygame para não imprimir nada na tela
sys.stdout = MagicMock()
from pygame import mixer

sys.stdout = sys.__stdout__


mixer.init()
tela = Imprimir()


class Menu:
    def __init__(self, personagem, nome_jogo: str):
        self._nome_jogo = nome_jogo
        texto = ["O que deseja fazer?"]
        texto2 = [
            "explorar uma floresta",
            "visitar o vilarejo",
            "equipar equipamentos",
            "desequipar equipamentos",
            "mostrar equipamentos equipados",
            "equipar pets",
            "abrir caixas",
            "mostrar o status",
            "mostrar quests",
            "eventos especiais",
            "salvar jogo",
            "sair",
        ]
        self._texto = texto + [
            f"{numero} - {texto}" for numero, texto in enumerate(texto2, 1)
        ]
        self._personagem = personagem
        self._eventos_contador = Contador2(intervalo=4)
        self._evento_especial = False

    def ciclo(self):
        """Método onde é exibido o menu principal para o usuário."""
        musicas = ["musicas/musica1.ogg", "musicas/musica2.mp3"]
        musicas = [item for item in musicas]
        mixer.music.load(choice(musicas))
        mixer.music.play()
        forma = f"{formas[227]} {{}} {formas[228]}"
        while True:
            tela.limpar_tela()
            for texto in self._texto:
                condicoes = [
                    self._eventos_contador.usar,
                    "eventos especiais" in texto,
                ]
                if all(condicoes):
                    tela.imprimir(forma.format(texto) + "\n", "amarelo")
                else:
                    tela.imprimir(forma.format(texto) + "\n", "cyan")
            tela.imprimir(": ")
            caracter = tela.obter_string()
            if not caracter.isnumeric():
                continue
            caracter = int(caracter)
            match caracter:
                case 1:
                    mixer.music.stop()
                    continuar = self._primeira_vez()
                    if continuar:
                        self.floresta()
                        self._eventos_contador.acrescentar()
                    mixer.music.load(choice(musicas))
                    mixer.music.play()
                case 2:
                    try:
                        npcs = getattr(self, "_npcs")
                    except AttributeError:
                        raise Exception(
                            'Você esqueceu de chamar o metodo "obter_npcs" '
                            "com a lista de npcs."
                        )
                    vilarejo = Vilarejo(
                        "Vila dos hobbits", self._personagem, npcs
                    )
                    vilarejo.explorar()
                case 3:
                    self.equipar_equipamentos()
                case 4:
                    self.desequipar()
                case 5:
                    tela.limpar_tela()
                    equipamentos = self._personagem.equipamentos.items()
                    for nome, item in equipamentos:
                        if bool(item):
                            frase = f"{nome}: {item}\n"
                        else:
                            frase = str(item) + "\n"
                        tela.imprimir(frase)
                    tela.imprimir(
                        "aperte enter para retornar ao menu principal: "
                    )
                    tela.obter_string()
                case 6:
                    self.equipar_pets()
                case 7:
                    self.abrir_caixas()
                case 8:
                    tela.limpar_tela()
                    tela.imprimir(
                        self._arrumar_status(self._personagem),
                        "cyan",
                    )
                    tela.imprimir(
                        "aperte enter para retornar ao menu principal: ", "cyan"
                    )
                    tela.obter_string()
                case 9:
                    self._obter_numero_quests()
                case 10:
                    mixer.music.stop()
                    self.eventos_especiais()
                    mixer.music.load(choice(musicas))
                    mixer.music.play()
                case 11:
                    npcs = filter(lambda x: x.salvar, self._npcs)
                    salvar_jogo(self._personagem, npcs, self._nome_jogo)
                    tela.imprimir(f"jogo salvo {formas[959]}", "cyan")
                    sleep(3)
                case 12:
                    quit()

    def equipar_equipamentos(self):
        """Método que equipa equipamentos do inventário do personagem."""
        equipamentos = list(
            filter(lambda x: x, self._personagem.equipamentos.values())
        )
        numero = self._obter_numero_equipamentos(
            "deseja equipar qual equipamento?: ",
            equipamentos + self._personagem.inventario,
        )
        while bool(numero):
            inventario = dict(
                enumerate(equipamentos + self._personagem.inventario)
            )
            equipamento = inventario.get(int(numero))
            if bool(equipamento) and equipamento in self._personagem.inventario:
                self._personagem.equipar(equipamento)
            equipamentos = list(
                filter(lambda x: x, self._personagem.equipamentos.values())
            )
            numero = self._obter_numero_equipamentos(
                "deseja equipar qual equipamento?: ",
                equipamentos + self._personagem.inventario,
            )

    def desequipar(self):
        """Método que desequipa um equipamento do personagem."""
        numero = self._obter_numero_equipamentos(
            "deseja desequipar qual equipamento?: ",
            list(self._personagem.equipamentos.values()),
        )
        while bool(numero):
            inventario = dict(enumerate(self._personagem.equipamentos.values()))
            equipamento = inventario.get(int(numero))
            if equipamento is not None:
                self._personagem.desequipar(equipamento)
            numero = self._obter_numero_equipamentos(
                "deseja desequipar qual equipamento?: ",
                list(self._personagem.equipamentos.values()),
            )

    def floresta(self):
        """Método que conduz o personagem à floresta."""
        tela.limpar_tela()
        nomes_florestas = [
            "floresta rio preto",
            "floresta do caçador",
            "floresta mata grande",
            "floresta passo fundo",
            "floresta nublada",
            "floresta negra",
            "amazonia",
        ]
        nomes_florestas_dict = dict(enumerate(nomes_florestas, 1))
        for numero, floresta in enumerate(nomes_florestas, 1):
            tela.imprimir(
                f"{numero} - {floresta} [nível da floresta: {numero}]\n",
                "amarelo",
            )
        tela.imprimir(": ")
        numero = tela.obter_string()
        if numero.isnumeric() and int(numero) in nomes_florestas_dict:
            musica = "musicas/som_da_floresta.ogg"
            mixer.music.load(musica)
            mixer.music.play()
            numero = int(numero)
            floresta = nomes_florestas_dict[int(numero)]
            floresta = Floresta(floresta, self._personagem, numero)
            floresta.explorar()
            self._personagem.recuperar_magia_stamina_cem_porcento()
            self._personagem.ressucitar()
            mixer.music.stop()

    def _obter_numero_equipamentos(self, mensagem: str, itens: list):
        """Método que organiza as páginas para o usuário e retorna um número."""
        itens = list(enumerate(itens))
        if len(itens) == 0:
            tela.imprimir("você não tem itens no inventario.", "cyan")
            sleep(2)
            return ""
        itens = chunk(itens, 17)
        numeros_paginas = {f":{n}": n for n in range(1, len(itens) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            tela.imprimir(
                "itens coloridos de amarelo estão equipados\n", "cyan"
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens[n - 1]:
                mensagem2 = (
                    f"{numero} - {item} [classe: {item.classe}]"
                    if item.tipo
                    in [
                        "Elmo",
                        "Peitoral",
                        "Calça",
                        "Botas",
                        "Luvas",
                        "Anel",
                        "Amuleto",
                        "Arma",
                        "Escudo",
                        "Item secundário",
                        "Adorno de arma",
                    ]
                    else f"{numero} - {item}"
                )
                equipamento_equipado = map(
                    lambda x: x is item, self._personagem.equipamentos.values()
                )
                if any(equipamento_equipado):
                    tela.imprimir(mensagem2 + "\n", "amarelo")
                else:
                    tela.imprimir(mensagem2 + "\n")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        return numero

    def _obter_numero_quests(self):
        quests = list(enumerate(self._personagem.quests))
        if len(quests) == 0:
            tela.imprimir("você não tem quests.", "cyan")
            sleep(2)
            return
        quests = chunk(quests, 17)
        numeros_paginas = {f":{n}": n for n in range(1, len(quests) + 1)}
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(quests)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in quests[n - 1]:
                tela.imprimir(f"{numero} - {item}\n")
            tela.imprimir("aperte enter para retornar ao menu: ", "cyan")
            numero = tela.obter_string()

    def obter_npcs(self, npcs: list):
        self._npcs = npcs

    def _primeira_vez(self):
        tela.limpar_tela()
        pocoes = list(
            filter(
                lambda x: x.nome in "poção de vida média",
                self._personagem.inventario,
            )
        )
        condicoes = [
            self._personagem.level == 1,
            int(self._personagem.experiencia) == 0,
            sum([pocao.numero_de_pocoes for pocao in pocoes]) < 15,
        ]
        if all(condicoes):
            tela.imprimir(
                "Como é a sua primeira vez, certifique-se de comprar de "
                "15 a 20 poções de vida média no comerciante do vilarejo.\n"
            )
            tela.imprimir("Deseja continuar mesmo assim?: ")
            caracter = tela.obter_string().lower()
            if caracter in ["s", "sim"]:
                return True
            else:
                return False
        # retorna True caso personagem tenha mais de 10 poções
        return True

    def _obter_numero(self, itens, mensagem):
        itens_enumeradas = list(enumerate(itens))
        caixas_dict = {str(n): item for n, item in itens_enumeradas}
        itens_enumeradas = chunk(itens_enumeradas, 17)
        numeros_paginas = {
            f":{n}": n for n in range(1, len(itens_enumeradas) + 1)
        }
        numero = ":1"
        while bool(numero) and not numero.isnumeric():
            tela.limpar_tela()
            tela.imprimir(
                f"páginas: {len(itens_enumeradas)}"
                " - Para passar de página digite :numero exemplo-> :2\n",
                "cyan",
            )
            n = numeros_paginas.get(numero, 1)
            for numero, item in itens_enumeradas[n - 1]:
                tela.imprimir(f"{numero} - {item}\n")
            tela.imprimir(mensagem, "cyan")
            numero = tela.obter_string()
        return caixas_dict.get(numero)

    def abrir_caixas(self):
        tela.limpar_tela()
        caixas = list(
            filter(lambda x: x.tipo == "Caixa", self._personagem.inventario)
        )
        if len(caixas) == 0:
            tela.imprimir(
                "você não tem caixas no inventario para abrir", "cyan"
            )
            sleep(3)
            return
        caixa = self._obter_numero(caixas, "deseja escolher qual caixa: ")
        while len(caixas) > 0 and bool(caixa):
            tela.limpar_tela()
            tela.imprimir(f"caixa: {caixa.nome}, deseja abrir? [sim/não]: ")
            resposta = tela.obter_string().lower()
            if resposta in ["s", "sim"]:
                item = caixa.consumir()
                tela.imprimir(f"item adquirido: {item}\n")
                sleep(3)
                if item.nome == "Draconica":
                    self._personagem.moedas["Draconica"] += item
                else:
                    self._personagem.inventario.append(item)
                index = self._personagem.inventario.index(caixa)
                self._personagem.inventario.pop(index)
            caixas = list(
                filter(lambda x: x.tipo == "Caixa", self._personagem.inventario)
            )
            if len(caixas) == 0:
                tela.imprimir("você não tem mais caixas\n")
                sleep(3)
                return
            caixa = self._obter_numero(caixas, "deseja escolher qual caixa: ")

    def equipar_pets(self):
        tela.limpar_tela()
        pets = [
            item for item in self._personagem.inventario if item.tipo == "Pet"
        ]
        if len(pets) == 0:
            tela.imprimir("você não tem pets no inventario.\n", "cyan")
            sleep(3)
            return
        pet = self._obter_numero(pets, "deseja escolher qual pet: ")
        if bool(pet):
            self._personagem.pet_equipado = pet
            self._personagem.atualizar_status()
            tela.imprimir(f"Pet equipado: {pet}")
            sleep(3)
        else:
            self._personagem.pet_equipado = SemPet()
            self._personagem.atualizar_status()
            tela.imprimir("Pet desequipado.")
            sleep(3)

    def _arrumar_status(self, personagem):
        p = personagem
        armadura = f"armadura - {p.status['armadura']}"
        resistencia = f"resistencia - {p.status['resistencia']}"
        arm_porc = f"defesa da armadura % - {p.porcentagem_armadura}%"
        resi_porc = f"defesa da resistencia % - {p.porcentagem_resistencia}%"
        experiencia = f"xp - {p.experiencia}"
        pratas = f"{str(p.moedas['Pratas'])}"
        por_cri = f"porcentagem de dano critico - {p.porcentagem_critico}"
        critico = f"critico - {p.status['critico']}"
        aum_cri = f"aumento de dano critico % - {p.aumento_dano_critico}%"
        pet = f"pet: {p.pet_equipado}"
        tamanhos = (
            len(x)
            for x in (
                armadura,
                resistencia,
                experiencia,
                pratas,
                critico,
                aum_cri,
                pet,
            )
        )
        len_max = max(tamanhos) + 2
        textos = [
            f"{p.nome_completo[:67]} [{p.classe}]:",
            f"vida - {p.status['vida']}",
            f"{armadura: <{len_max}}{arm_porc}",
            f"{resistencia: <{len_max}}{resi_porc}",
            f"dano - {p.status['dano']}",
            f"{critico: <{len_max}}{por_cri}%",
            aum_cri,
            f"{pratas: <{len_max}}{str(p.moedas['Draconica'])}",
            f"{p.moedas['Glifos']}",
            f"{experiencia: <{len_max}}level - {p.level}",
            pet,
        ]
        return "\n".join(textos) + "\n"

    def eventos_especiais(self):
        if self._eventos_contador.usar and not bool(self._evento_especial):
            self._evento_especial = choice(["arauto"])
        elif not self._eventos_contador.usar and bool(self._evento_especial):
            self._evento_especial = False
        tela.limpar_tela()
        if bool(self._evento_especial):
            artigo = Artigo(self._evento_especial)
            tela.imprimir(f"evento d{artigo} {self._evento_especial}\n")
            tela.imprimir("deseja entrar no evento? [s/n]: ")
            resposta = tela.obter_string()
            if resposta in ["s", "sim"]:
                musica = "musicas/musica_combate1.ogg"
                mixer.music.load(musica)
                mixer.music.play()
                covil = CovilDoArauto(self._personagem, self._personagem.level)
                covil.explorar()
                self._eventos_contador.acrescentar()
                mixer.music.stop()


# TODO: colocar mais npcs com quests.
# TODO: poções, venenos.
# TODO: combate entre personagens bots.
# TODO: colocar o nome dos ataques tanto dos inimigos tanto do personagem na tela.
# TODO: com o level, colocar subclasses aos personagens.
# TODO: fazer uma função que imprime a história do jogo.
# TODO: histórias tem botão de skip (não sei se tem como fazer)
# TODO: obsessão por primitivos na classe Humano (não tem como)
# TODO: elixir deve ter um preço diferente para cada level.
# TODO: implementar stun?
# TODO: interagir com cenários e destruílos?
# TODO: fazer quests onde o personagem precise interagir com 2 ou mais npcs.
# TODO: implementar baús que dropam itens?
# TODO: ter um companheiro na campanha? (não sei se tem como implementar isso)
# TODO: trols, cavaleiros negros, esqueletos, catatumbas[areas abertas, ala a direita, tunel]
# TODO: implementar durabilidade nas armas?
# TODO: sangramento por dano de armas ou mobs
