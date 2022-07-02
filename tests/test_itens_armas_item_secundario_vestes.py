import curses

curses.initscr()

from unittest import TestCase, mock

from jogo.itens.armas import (
    Adaga,
    AdornoDeArma,
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
from jogo.itens.item_secundario import Adaga as AdagaSecundaria
from jogo.itens.item_secundario import (
    Aljava,
    BolaDeCristal,
    Buckler,
    Escudo,
    Livro,
)
from jogo.itens.pocoes import curas
from jogo.itens.vestes import (
    Amuleto,
    Anel,
    Botas,
    Calca,
    CalcaDraconica,
    Elmo,
    ElmoDraconico,
    Luvas,
    Peitoral,
    PeitoralDraconico,
    roupas_draconicas,
)
from jogo.personagens.classes import Arqueiro
from jogo.personagens.npc import Comerciante


@mock.patch("jogo.personagens.npc.sleep")
@mock.patch("jogo.personagens.npc.tela")
class TestVenderArmasDaoPratas(TestCase):
    def setUp(self):
        self.comerciante = Comerciante("nome", curas + roupas_draconicas)
        self.personagem = Arqueiro("nome", True)

    def test_vendendo_adaga_no_comerciante_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        adaga = Adaga(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(adaga)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_adorno_de_arma_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5) * 8
        adorno_de_arma = AdornoDeArma(critico=5, aumento_critico=5)
        self.personagem.inventario.append(adorno_de_arma)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_arco_curto_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        arco_curto = Arco_curto(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(arco_curto)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_arco_longo_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        arco_longo = Arco_longo(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(arco_longo)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_botas_de_ferro_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        botas_de_ferro = Botas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(botas_de_ferro)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_cajado_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        cajado = Cajado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(cajado)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_cajado_negro_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        cajado_negro = Cajado_negro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(cajado_negro)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_espada_curta_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        espada_curta = Espada_curta(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(espada_curta)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_espada_longa_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        espada_longa = Espada_longa(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(espada_longa)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_luvas_de_ferro_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        luvas_de_ferro = Luvas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(luvas_de_ferro)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_machado_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + 5 + 5) * 8
        machado = Machado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(machado)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)


@mock.patch("jogo.personagens.npc.sleep")
@mock.patch("jogo.personagens.npc.tela")
class TestVenderRoupasDaoPratasDraconica(TestCase):
    def setUp(self):
        self.comerciante = Comerciante("nome", curas + roupas_draconicas)
        self.personagem = Arqueiro("nome", True)

    def test_vendendo_amuleto_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + (5 // 2) + 5 + 5) * 8
        amuleto = Amuleto(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(amuleto)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_anel_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = (5 + (5 // 2) + 5 + 5) * 8
        anel = Anel(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(anel)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_elmo_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = ((5 // 2) + 5 + 5) * 8
        elmo = Elmo(vida=5, armadura=5, resistencia=5)
        self.personagem.inventario.append(elmo)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_peitoral_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        esperado = ((5 // 2) + 5 + 5) * 8
        peitoral = Peitoral(vida=5, armadura=5, resistencia=5)
        self.personagem.inventario.append(peitoral)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_luvas_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        luvas = Luvas(vida=5, armadura=5, resistencia=5)
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(luvas)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_botas_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        botas = Botas(vida=5, armadura=5, resistencia=5)
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(botas)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_calca_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        calca = Calca(vida=5, armadura=5, resistencia=5)
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(calca)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_elmo_draconico_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        elmo = ElmoDraconico(vida=5, armadura=5, resistencia=5)
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(elmo)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Draconica"]), esperado)

    def test_vendendo_peitoral_draconico_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        peitoral = PeitoralDraconico(vida=5, armadura=5, resistencia=5)
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(peitoral)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Draconica"]), esperado)

    def test_vendendo_calca_draconico_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        calca = CalcaDraconica(vida=5, armadura=5, resistencia=5)
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(calca)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Draconica"]), esperado)


@mock.patch("jogo.personagens.npc.sleep")
@mock.patch("jogo.personagens.npc.tela")
class TestVenderItemsSecundariosDaoPratas(TestCase):
    def setUp(self):
        self.comerciante = Comerciante("nome", curas + roupas_draconicas)
        self.personagem = Arqueiro("nome", True)

    def test_vendendo_adaga_secundaria_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        adaga = AdagaSecundaria(dano=5, critico=5, aumento_critico=5)
        esperado = (5 + 5 + (5 // 2)) * 8
        self.personagem.inventario.append(adaga)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_aljava_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        aljava = Aljava(dano=5, critico=5, aumento_critico=5)
        esperado = (5 + 5 + (5 // 2)) * 8
        self.personagem.inventario.append(aljava)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_bola_de_cristal_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        bola_de_cristal = BolaDeCristal(
            vida=5, armadura=5, resistencia=5, bloqueio=80
        )
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(bola_de_cristal)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_buckler_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        buckler = Buckler(vida=5, armadura=5, resistencia=5, bloqueio=80)
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(buckler)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_escudo_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        escudo = Escudo(vida=5, armadura=5, resistencia=5, bloqueio=80)
        esperado = ((5 // 2) + 5 + 5) * 8
        self.personagem.inventario.append(escudo)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)

    def test_vendendo_livro_e_recebendo_dinheiro(self, tela, *_):
        tela.obter_string.side_effect = ["2", "0", ""]
        livro = Livro(dano=5, critico=5, aumento_critico=5)
        esperado = (5 + 5 + (5 // 2)) * 8
        self.personagem.inventario.append(livro)
        self.comerciante.interagir(self.personagem)
        self.assertEqual(int(self.personagem.moedas["Pratas"]), 1500 + esperado)
