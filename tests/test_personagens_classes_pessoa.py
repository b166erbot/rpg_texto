# import sys
# sys.path.append('.')

import curses

curses.initscr()
from collections import Counter
from unittest import TestCase, mock
from unittest.mock import MagicMock

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
from jogo.itens.pocoes import (
    ElixirDeVidaExtraGrande,
    ElixirDeVidaFraca,
    ElixirDeVidaGrande,
    ElixirDeVidaMedia,
)
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
)

# with mock.patch("jogo.personagens.classes.tela") as mocked_lib:
from jogo.personagens.classes import (
    Arqueiro,
    Assassino,
    Clerigo,
    Guerreiro,
    Mago,
    Monge,
)
from jogo.personagens.monstros import Tartaruga

curses.endwin()


# não necessita testar as outras classes pois esse método é da classe Humano
class TestElixir(TestCase):
    def setUp(self):
        self.mago = Mago("Nome", True)
        self.mago2 = Mago("nome", False)
        self.mago.status["vida"] = 30
        self.mago2.status["vida"] = 30

    def test_elixir_recuperando_20_porcento_da_vida(self):
        self.mago.inventario.append(ElixirDeVidaFraca())
        self.mago.consumir_pocoes()
        self.assertEqual(self.mago.status["vida"], 50)

    def test_elixir_recuperando_20_porcento_com_o_personagem_bot(self):
        self.mago2.inventario.append(ElixirDeVidaFraca())
        self.mago2.consumir_pocoes()
        self.assertEqual(self.mago2.status["vida"], 50)

    def test_elixir_recuperando_40_porcento_da_vida(self):
        self.mago.inventario.append(ElixirDeVidaMedia())
        self.mago.consumir_pocoes()
        self.assertEqual(self.mago.status["vida"], 70)

    def test_elixir_recuperando_40_porcento_com_o_personagem_bot(self):
        self.mago2.inventario.append(ElixirDeVidaMedia())
        self.mago2.consumir_pocoes()
        self.assertEqual(self.mago2.status["vida"], 70)

    def test_elixir_recuperando_60_porcento_da_vida(self):
        self.mago.inventario.append(ElixirDeVidaGrande())
        self.mago.consumir_pocoes()
        self.assertEqual(self.mago.status["vida"], 90)

    def test_elixir_recuperando_60_porcento_da_vida_com_personagem_bot(self):
        self.mago2.inventario.append(ElixirDeVidaGrande())
        self.mago2.consumir_pocoes()
        self.assertEqual(self.mago2.status["vida"], 90)

    def test_elixir_recuperando_80_porcento_da_vida(self):
        self.mago.inventario.append(ElixirDeVidaExtraGrande())
        self.mago.consumir_pocoes()
        self.assertEqual(self.mago.status["vida"], 100)

    def test_elixir_recuperando_80_porcento_da_vida_com_o_personagem_bot(self):
        self.mago2.inventario.append(ElixirDeVidaExtraGrande())
        self.mago2.consumir_pocoes()
        self.assertEqual(self.mago2.status["vida"], 100)


class TestCriticoArqueiro(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.personagem2 = Arqueiro("nome", False)
        self.personagem.porcentagem_critico = 100
        self.personagem2.porcentagem_critico = 100

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_tres_flechas(self, mocked):
        self.personagem.tres_flechas(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_tres_flechas_como_bot(self, mocked):
        self.personagem2.tres_flechas(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_tres_flechas(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.tres_flechas(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_tres_flechas_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.tres_flechas(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_flecha_de_fogo(self, mocked):
        self.personagem.flecha_de_fogo(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_flecha_de_fogo_como_bot(
        self, mocked
    ):
        self.personagem2.flecha_de_fogo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_flecha_de_fogo(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.flecha_de_fogo(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 85)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_flecha_de_fogo_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.flecha_de_fogo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


class TestCriticoGuerreiro(TestCase):
    def setUp(self):
        self.personagem = Guerreiro("nome", True)
        self.personagem2 = Guerreiro("nome", False)
        self.personagem.porcentagem_critico = 100
        self.personagem2.porcentagem_critico = 100

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_investida(self, mocked):
        self.personagem.investida(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_investida_como_bot(self, mocked):
        self.personagem2.investida(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_investida(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.investida(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_investida_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.investida(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_esmagar(self, mocked):
        self.personagem.esmagar(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_esmagar_como_bot(self, mocked):
        self.personagem2.esmagar(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_esmagar(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.esmagar(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 85)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_esmagar_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.esmagar(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


class TestCriticoMago(TestCase):
    def setUp(self):
        self.personagem = Mago("nome", True)
        self.personagem2 = Mago("nome", False)
        self.personagem.porcentagem_critico = 100
        self.personagem2.porcentagem_critico = 100

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_lanca_de_gelo(self, mocked):
        self.personagem.lanca_de_gelo(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_lanca_de_gelo_como_bot(self, mocked):
        self.personagem2.lanca_de_gelo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_lanca_de_gelo(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.lanca_de_gelo(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_lanca_de_gelo_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.lanca_de_gelo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_bola_de_fogo(self, mocked):
        self.personagem.bola_de_fogo(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_bola_de_fogo_como_bot(self, mocked):
        self.personagem2.bola_de_fogo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_bola_de_fogo(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.bola_de_fogo(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 85)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_bola_de_fogo_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.bola_de_fogo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


class TestCriticoAssassino(TestCase):
    def setUp(self):
        self.personagem = Assassino("nome", True)
        self.personagem2 = Assassino("nome", False)
        self.personagem.porcentagem_critico = 100
        self.personagem2.porcentagem_critico = 100

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_lancar_faca(self, mocked):
        self.personagem.lancar_faca(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_lancar_faca_como_bot(self, mocked):
        self.personagem2.lancar_faca(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_lancar_faca(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.lancar_faca(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_lancar_faca_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.lancar_faca(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_ataque_furtivo(self, mocked):
        self.personagem.ataque_furtivo(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_ataque_furtivo_como_bot(
        self, mocked
    ):
        self.personagem2.ataque_furtivo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_ataque_furtivo(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.ataque_furtivo(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 85)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_ataque_furtivo_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.ataque_furtivo(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


class TestCriticoClerigo(TestCase):
    def setUp(self):
        self.personagem = Clerigo("nome", True)
        self.personagem2 = Clerigo("nome", False)
        self.personagem.porcentagem_critico = 100
        self.personagem2.porcentagem_critico = 100

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_curar(self, mocked):
        self.personagem.status["vida"] = 0
        self.personagem.curar(self.personagem2)
        self.assertEqual(self.personagem.status["vida"], 50)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_curar_como_bot(self, mocked):
        self.personagem2.status["vida"] = 0
        self.personagem2.curar(self.personagem)
        self.assertEqual(self.personagem2.status["vida"], 50)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_curar(
        self, mocked
    ):
        self.personagem.status["vida"] = 0
        self.personagem.porcentagem_critico = 80
        self.personagem.curar(self.personagem2)
        self.assertEqual(self.personagem.status["vida"], 25)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_curar_como_bot(
        self, mocked
    ):
        self.personagem2.status["vida"] = 0
        self.personagem2.porcentagem_critico = 80
        self.personagem2.curar(self.personagem)
        self.assertEqual(self.personagem2.status["vida"], 25)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_luz(self, mocked):
        self.personagem.luz(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_luz_como_bot(self, mocked):
        self.personagem2.luz(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_luz(self, mocked):
        self.personagem.porcentagem_critico = 80
        self.personagem.luz(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_luz_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.luz(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)


class TestCriticoMonge(TestCase):
    def setUp(self):
        self.personagem = Monge("nome", True)
        self.personagem2 = Monge("nome", False)
        self.personagem.porcentagem_critico = 100
        self.personagem2.porcentagem_critico = 100

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_multiplos_socos(self, mocked):
        self.personagem.multiplos_socos(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_multiplos_socos_como_bot(
        self, mocked
    ):
        self.personagem2.multiplos_socos(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 80)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_multiplos_socos(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.multiplos_socos(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_multiplos_socos_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.multiplos_socos(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 90)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_combo_de_chutes(self, mocked):
        self.personagem.combo_de_chutes(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=100)
    def test_critico_dando_o_dobro_de_dano_combo_de_chutes_como_bot(
        self, mocked
    ):
        self.personagem2.combo_de_chutes(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 70)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_combo_de_chutes(
        self, mocked
    ):
        self.personagem.porcentagem_critico = 80
        self.personagem.combo_de_chutes(self.personagem2)
        self.assertEqual(self.personagem2.status["vida"], 85)

    @mock.patch("jogo.personagens.classes.randint", return_value=81)
    def test_critico_nao_funcionando_caso_valor_menor_que_80_combo_de_chutes_como_bot(
        self, mocked
    ):
        self.personagem2.porcentagem_critico = 80
        self.personagem2.combo_de_chutes(self.personagem)
        self.assertEqual(self.personagem.status["vida"], 85)


# eu fiz essa bizarrice nos testes mas funciona, então vai ficar assim.
class TestPorcentagemArmaduraResistencia(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        self.personagem2 = Arqueiro("nome", False)
        self.personagem3 = Guerreiro("nome", True)
        self.personagem4 = Guerreiro("nome", False)
        self.personagem5 = Mago("nome", True)
        self.personagem6 = Mago("nome", False)
        self.personagem7 = Assassino("nome", True)
        self.personagem8 = Assassino("nome", False)
        self.personagem9 = Clerigo("nome", True)
        self.personagem10 = Clerigo("nome", False)
        self.personagem11 = Monge("nome", True)
        self.personagem12 = Monge("nome", False)
        self.personagem.porcentagem_resistencia = 80
        self.personagem2.porcentagem_resistencia = 80
        self.personagem.porcentagem_armadura = 80
        self.personagem2.porcentagem_armadura = 80
        self.personagem3.porcentagem_resistencia = 80
        self.personagem4.porcentagem_resistencia = 80
        self.personagem3.porcentagem_armadura = 80
        self.personagem4.porcentagem_armadura = 80
        self.personagem5.porcentagem_resistencia = 80
        self.personagem6.porcentagem_resistencia = 80
        self.personagem5.porcentagem_armadura = 80
        self.personagem6.porcentagem_armadura = 80
        self.personagem7.porcentagem_resistencia = 80
        self.personagem8.porcentagem_resistencia = 80
        self.personagem7.porcentagem_armadura = 80
        self.personagem8.porcentagem_armadura = 80
        self.personagem9.porcentagem_resistencia = 80
        self.personagem10.porcentagem_resistencia = 80
        self.personagem9.porcentagem_armadura = 80
        self.personagem10.porcentagem_armadura = 80
        self.personagem11.porcentagem_resistencia = 80
        self.personagem12.porcentagem_resistencia = 80
        self.personagem11.porcentagem_armadura = 80
        self.personagem12.porcentagem_armadura = 80

    def test_personagem_deve_receber_dano_menos_80_porcento_na_armadura_tres_flechas(
        self,
    ):
        self.personagem2.tres_flechas(self.personagem)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem2_deve_receber_dano_menos_80_porcento_na_armadura_tres_flechas(
        self,
    ):
        self.personagem.tres_flechas(self.personagem2)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem2.status["vida"], esperado)

    def test_personagem_deve_receber_dano_menos_80_porcento_na_resistencia_flecha_de_fogo(
        self,
    ):
        self.personagem2.flecha_de_fogo(self.personagem)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem.status["vida"], esperado)

    def test_personagem2_deve_receber_dano_menos_80_porcento_na_resistencia_flecha_de_fogo(
        self,
    ):
        self.personagem.flecha_de_fogo(self.personagem2)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem2.status["vida"], esperado)

    def test_personagem4_deve_receber_dano_menos_80_porcento_na_armadura_investida(
        self,
    ):
        self.personagem3.investida(self.personagem4)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem4.status["vida"], esperado)

    def test_personagem3_deve_receber_dano_menos_80_porcento_na_armadura_investida(
        self,
    ):
        self.personagem4.investida(self.personagem3)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem3.status["vida"], esperado)

    def test_personagem4_deve_receber_dano_menos_80_porcento_na_armadura_esmagar(
        self,
    ):
        self.personagem3.esmagar(self.personagem4)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem4.status["vida"], esperado)

    def test_personagem3_deve_receber_dano_menos_80_porcento_na_armadura_esmagar(
        self,
    ):
        self.personagem4.esmagar(self.personagem3)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem3.status["vida"], esperado)

    def test_personagem5_deve_receber_dano_menos_80_porcento_na_resistencia_lanca_de_gelo(
        self,
    ):
        self.personagem6.lanca_de_gelo(self.personagem5)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem5.status["vida"], esperado)

    def test_personagem6_deve_receber_dano_menos_80_porcento_na_resistencia_lanca_de_gelo(
        self,
    ):
        self.personagem5.lanca_de_gelo(self.personagem6)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem6.status["vida"], esperado)

    def test_personagem5_deve_receber_dano_menos_80_porcento_na_resistencia_bola_de_fogo(
        self,
    ):
        self.personagem6.bola_de_fogo(self.personagem5)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem5.status["vida"], esperado)

    def test_personagem6_deve_receber_dano_menos_80_porcento_na_resistencia_bola_de_fogo(
        self,
    ):
        self.personagem5.bola_de_fogo(self.personagem6)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem6.status["vida"], esperado)

    def test_personagem7_deve_receber_dano_menos_80_porcento_na_armadura_lancar_faca(
        self,
    ):
        self.personagem8.lancar_faca(self.personagem7)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem7.status["vida"], esperado)

    def test_personagem8_deve_receber_dano_menos_80_porcento_na_armadura_lancar_faca(
        self,
    ):
        self.personagem7.lancar_faca(self.personagem8)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem8.status["vida"], esperado)

    def test_personagem7_deve_receber_dano_menos_80_porcento_na_armadura_ataque_furtivo(
        self,
    ):
        self.personagem8.ataque_furtivo(self.personagem7)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem7.status["vida"], esperado)

    def test_personagem8_deve_receber_dano_menos_80_porcento_na_armadura_ataque_furtivo(
        self,
    ):
        self.personagem7.ataque_furtivo(self.personagem8)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem8.status["vida"], esperado)

    def test_personagem9_deve_receber_dano_menos_80_porcento_na_resistencia_luz(
        self,
    ):
        self.personagem10.luz(self.personagem9)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem9.status["vida"], esperado)

    def test_personagem10_deve_receber_dano_menos_80_porcento_na_resistencia_luz(
        self,
    ):
        self.personagem9.luz(self.personagem10)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem10.status["vida"], esperado)

    def test_personagem11_deve_receber_dano_menos_80_porcento_na_armadura_multiplos_socos(
        self,
    ):
        self.personagem12.multiplos_socos(self.personagem11)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem11.status["vida"], esperado)

    def test_personagem12_deve_receber_dano_menos_80_porcento_na_armadura_multiplos_socos(
        self,
    ):
        self.personagem11.multiplos_socos(self.personagem12)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem12.status["vida"], esperado)

    def test_personagem11_deve_receber_dano_menos_80_porcento_na_armadura_combo_de_chutes(
        self,
    ):
        self.personagem12.combo_de_chutes(self.personagem11)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem11.status["vida"], esperado)

    def test_personagem12_deve_receber_dano_menos_80_porcento_na_armadura_combo_de_chutes(
        self,
    ):
        self.personagem11.combo_de_chutes(self.personagem12)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem12.status["vida"], esperado)


class TestStatus(TestCase):
    def setUp(self):
        self.status = Counter(
            {
                "vida": 110,
                "dano": 10,
                "resistencia": 10,
                "velo-ataque": 1,
                "criti": 10,
                "armadura": 10,
                "magia": 100,
                "stamina": 100,
                "velo-movi": 1,
            }
        )
        self.personagem = Arqueiro("nome", True, status=self.status)

    def test_personagem_mantem_o_status_mesmo_depois_de_atualizar(self):
        self.personagem.atualizar_status()
        self.assertEqual(self.personagem.status, self.status)


class TestEquipandoEquipamentosOuNaoEmArqueiroArmas(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)

    def test_equipando_arco_curto(self):
        item = Arco_curto(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_arco_longo(self):
        item = Arco_longo(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_adorno_de_arma(self):
        item = AdornoDeArma(critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga(self):
        item = Adaga(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_botas_de_ferro(self):
        item = Botas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_cajado(self):
        item = Cajado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_cajado_negro(self):
        item = Cajado_negro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_curta(self):
        item = Espada_curta(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_longa(self):
        item = Espada_longa(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_luvas_de_ferro(self):
        item = Luvas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_machado(self):
        item = Machado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmArqueiroItemSecundario(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)

    def test_equipando_aljava(self):
        item = Aljava(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_buckler(self):
        item = Buckler(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga_secundaria(self):
        item = AdagaSecundaria(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_bola_de_cristal(self):
        item = BolaDeCristal(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_escudo(self):
        item = Escudo(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_livro(self):
        item = Livro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmArqueiroVestes(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)

    def test_equipando_amuleto(self):
        item = Amuleto(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_anel(self):
        item = Anel(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_botas(self):
        item = Botas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca(self):
        item = Calca(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo(self):
        item = Elmo(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_luvas(self):
        item = Luvas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral(self):
        item = Peitoral(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral_draconico(self):
        item = PeitoralDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca_draconico(self):
        item = CalcaDraconica(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo_draconico(self):
        item = ElmoDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmGuerreiroArmas(TestCase):
    def setUp(self):
        self.personagem = Guerreiro("nome", True)

    def test_nao_equipando_arco_curto(self):
        item = Arco_curto(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_arco_longo(self):
        item = Arco_longo(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_adorno_de_arma(self):
        item = AdornoDeArma(critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga(self):
        item = Adaga(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_botas_de_ferro(self):
        item = Botas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_cajado(self):
        item = Cajado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_cajado_negro(self):
        item = Cajado_negro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_espada_curta(self):
        item = Espada_curta(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_espada_longa(self):
        item = Espada_longa(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_luvas_de_ferro(self):
        item = Luvas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_machado(self):
        item = Machado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmGuerreiroItemSecundario(TestCase):
    def setUp(self):
        self.personagem = Guerreiro("nome", True)

    def test_nao_equipando_aljava(self):
        item = Aljava(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_not_equipando_buckler(self):
        item = Buckler(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga_secundaria(self):
        item = AdagaSecundaria(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_bola_de_cristal(self):
        item = BolaDeCristal(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_escudo(self):
        item = Escudo(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_livro(self):
        item = Livro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmGuerreiroVestes(TestCase):
    def setUp(self):
        self.personagem = Guerreiro("nome", True)

    def test_equipando_amuleto(self):
        item = Amuleto(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_anel(self):
        item = Anel(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_botas(self):
        item = Botas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca(self):
        item = Calca(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo(self):
        item = Elmo(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_luvas(self):
        item = Luvas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral(self):
        item = Peitoral(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral_draconico(self):
        item = PeitoralDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca_draconico(self):
        item = CalcaDraconica(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo_draconico(self):
        item = ElmoDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmMagoArmas(TestCase):
    def setUp(self):
        self.personagem = Mago("nome", True)

    def test_nao_equipando_arco_curto(self):
        item = Arco_curto(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_arco_longo(self):
        item = Arco_longo(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_adorno_de_arma(self):
        item = AdornoDeArma(critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga(self):
        item = Adaga(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_botas_de_ferro(self):
        item = Botas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_cajado(self):
        item = Cajado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_cajado_negro(self):
        item = Cajado_negro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_curta(self):
        item = Espada_curta(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_longa(self):
        item = Espada_longa(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_luvas_de_ferro(self):
        item = Luvas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_machado(self):
        item = Machado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmMagoItemSecundario(TestCase):
    def setUp(self):
        self.personagem = Mago("nome", True)

    def test_nao_equipando_aljava(self):
        item = Aljava(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_buckler(self):
        item = Buckler(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga_secundaria(self):
        item = AdagaSecundaria(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_bola_de_cristal(self):
        item = BolaDeCristal(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_escudo(self):
        item = Escudo(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_livro(self):
        item = Livro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmMagoVestes(TestCase):
    def setUp(self):
        self.personagem = Mago("nome", True)

    def test_equipando_amuleto(self):
        item = Amuleto(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_anel(self):
        item = Anel(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_botas(self):
        item = Botas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca(self):
        item = Calca(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo(self):
        item = Elmo(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_luvas(self):
        item = Luvas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral(self):
        item = Peitoral(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral_draconico(self):
        item = PeitoralDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca_draconico(self):
        item = CalcaDraconica(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo_draconico(self):
        item = ElmoDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmAssassinoArmas(TestCase):
    def setUp(self):
        self.personagem = Assassino("nome", True)

    def test_nao_equipando_arco_curto(self):
        item = Arco_curto(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_arco_longo(self):
        item = Arco_longo(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_adorno_de_arma(self):
        item = AdornoDeArma(critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_adaga(self):
        item = Adaga(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_botas_de_ferro(self):
        item = Botas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_cajado(self):
        item = Cajado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_cajado_negro(self):
        item = Cajado_negro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_curta(self):
        item = Espada_curta(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_longa(self):
        item = Espada_longa(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_luvas_de_ferro(self):
        item = Luvas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_machado(self):
        item = Machado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmAssassinoItemSecundario(TestCase):
    def setUp(self):
        self.personagem = Assassino("nome", True)

    def test_nao_equipando_aljava(self):
        item = Aljava(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_buckler(self):
        item = Buckler(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_adaga_secundaria(self):
        item = AdagaSecundaria(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_bola_de_cristal(self):
        item = BolaDeCristal(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_escudo(self):
        item = Escudo(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_livro(self):
        item = Livro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmAssassinoVestes(TestCase):
    def setUp(self):
        self.personagem = Assassino("nome", True)

    def test_equipando_amuleto(self):
        item = Amuleto(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_anel(self):
        item = Anel(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_botas(self):
        item = Botas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca(self):
        item = Calca(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo(self):
        item = Elmo(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_luvas(self):
        item = Luvas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral(self):
        item = Peitoral(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral_draconico(self):
        item = PeitoralDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca_draconico(self):
        item = CalcaDraconica(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo_draconico(self):
        item = ElmoDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmClerigoArmas(TestCase):
    def setUp(self):
        self.personagem = Clerigo("nome", True)

    def test_nao_equipando_arco_curto(self):
        item = Arco_curto(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_arco_longo(self):
        item = Arco_longo(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_adorno_de_arma(self):
        item = AdornoDeArma(critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga(self):
        item = Adaga(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_botas_de_ferro(self):
        item = Botas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_cajado(self):
        item = Cajado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_cajado_negro(self):
        item = Cajado_negro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_curta(self):
        item = Espada_curta(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_longa(self):
        item = Espada_longa(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_luvas_de_ferro(self):
        item = Luvas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_machado(self):
        item = Machado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmClerigoItemSecundario(TestCase):
    def setUp(self):
        self.personagem = Clerigo("nome", True)

    def test_nao_equipando_aljava(self):
        item = Aljava(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_buckler(self):
        item = Buckler(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga_secundaria(self):
        item = AdagaSecundaria(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_bola_de_cristal(self):
        item = BolaDeCristal(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_escudo(self):
        item = Escudo(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_livro(self):
        item = Livro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmClerigoVestes(TestCase):
    def setUp(self):
        self.personagem = Clerigo("nome", True)

    def test_equipando_amuleto(self):
        item = Amuleto(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_anel(self):
        item = Anel(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_botas(self):
        item = Botas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca(self):
        item = Calca(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo(self):
        item = Elmo(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_luvas(self):
        item = Luvas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral(self):
        item = Peitoral(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral_draconico(self):
        item = PeitoralDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca_draconico(self):
        item = CalcaDraconica(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo_draconico(self):
        item = ElmoDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmMongeArmas(TestCase):
    def setUp(self):
        self.personagem = Monge("nome", True)

    def test_nao_equipando_arco_curto(self):
        item = Arco_curto(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_arco_longo(self):
        item = Arco_longo(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_adorno_de_arma(self):
        item = AdornoDeArma(critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_adaga(self):
        item = Adaga(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    # esse teste tem que ser alterado pois equipamento não equipa no tipo_equipar
    def test_equipando_botas_de_ferro(self):
        item = Botas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos["Botas"], item)

    def test_nao_equipando_cajado(self):
        item = Cajado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_cajado_negro(self):
        item = Cajado_negro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_curta(self):
        item = Espada_curta(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_espada_longa(self):
        item = Espada_longa(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    # esse teste tem que ser alterado pois equipamento não equipa no tipo_equipar
    def test_equipando_luvas_de_ferro(self):
        item = Luvas_de_ferro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos["Luvas"], item)

    def test_nao_equipando_machado(self):
        item = Machado(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmMongeItemSecundario(TestCase):
    def setUp(self):
        self.personagem = Monge("nome", True)

    def test_nao_equipando_aljava(self):
        item = Aljava(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_buckler(self):
        item = Buckler(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_not_equipando_adaga_secundaria(self):
        item = AdagaSecundaria(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_bola_de_cristal(self):
        item = BolaDeCristal(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_escudo(self):
        item = Escudo(vida=5, armadura=5, resistencia=5, bloqueio=80)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_nao_equipando_livro(self):
        item = Livro(dano=5, critico=5, aumento_critico=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIsNot(self.personagem.equipamentos[item.tipo_equipar], item)


class TestEquipandoEquipamentosOuNaoEmMongeVestes(TestCase):
    def setUp(self):
        self.personagem = Monge("nome", True)

    def test_equipando_amuleto(self):
        item = Amuleto(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_anel(self):
        item = Anel(dano=5, vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_botas(self):
        item = Botas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca(self):
        item = Calca(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo(self):
        item = Elmo(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_luvas(self):
        item = Luvas(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral(self):
        item = Peitoral(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_peitoral_draconico(self):
        item = PeitoralDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_calca_draconico(self):
        item = CalcaDraconica(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)

    def test_equipando_elmo_draconico(self):
        item = ElmoDraconico(vida=5, resistencia=5, armadura=5)
        self.personagem.inventario.append(item)
        self.personagem.equipar(item)
        self.assertIs(self.personagem.equipamentos[item.tipo_equipar], item)


@mock.patch("jogo.personagens.classes.randint", return_value=42)
class TestPersonagemDaMaisDanoComAumentoDeCriticoArqueiro(TestCase):
    def setUp(self):
        self.personagem = Arqueiro("nome", True)
        item = AdornoDeArma(critico=6, aumento_critico=16)
        self.personagem.inventario.append(item)
        item2 = Arco_longo(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item2)
        item3 = Aljava(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item3)
        self.monstro = Tartaruga()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80
        self.personagem.equipar(item)
        self.personagem.equipar(item2)
        self.personagem.equipar(item3)

    def test_dando_mais_dano_com_aumento_critico_tres_flechas(self, *_):
        self.personagem.tres_flechas(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 10
        # esperado = valor - valor da porcentagem da armadura do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_dando_mais_dano_com_aumento_critico_flecha_de_fogo(self, *_):
        self.personagem.flecha_de_fogo(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 15
        # esperado = valor - valor da porcentagem da resistencia do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)


@mock.patch("jogo.personagens.classes.randint", return_value=28)
class TestPersonagemDaMaisDanoComAumentoDeCriticoGuerreiro(TestCase):
    def setUp(self):
        self.personagem = Guerreiro("nome", True)
        item = AdornoDeArma(critico=6, aumento_critico=16)
        self.personagem.inventario.append(item)
        item2 = Espada_longa(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item2)
        self.monstro = Tartaruga()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80
        self.personagem.equipar(item)
        self.personagem.equipar(item2)

    def test_dando_mais_dano_com_aumento_critico_investida(self, *_):
        self.personagem.investida(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (2 * 16) / 100) * 10
        # esperado = valor - valor da porcentagem da armadura do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_dando_mais_dano_com_aumento_critico_esmagar(self, *_):
        self.personagem.esmagar(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (2 * 16) / 100) * 15
        # esperado = valor - valor da porcentagem da armadura do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)


@mock.patch("jogo.personagens.classes.randint", return_value=42)
class TestPersonagemDaMaisDanoComAumentoDeCriticoMago(TestCase):
    def setUp(self):
        self.personagem = Mago("nome", True)
        item = AdornoDeArma(critico=6, aumento_critico=16)
        self.personagem.inventario.append(item)
        item2 = Cajado(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item2)
        item3 = Livro(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item3)
        self.monstro = Tartaruga()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80
        self.personagem.equipar(item)
        self.personagem.equipar(item2)
        self.personagem.equipar(item3)

    def test_dando_mais_dano_com_aumento_critico_lanca_de_gelo(self, *_):
        self.personagem.lanca_de_gelo(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 10
        # esperado = valor - valor da porcentagem da resistencia do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_dando_mais_dano_com_aumento_critico_bola_de_fogo(self, *_):
        self.personagem.bola_de_fogo(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 15
        # esperado = valor - valor da porcentagem da resistencia do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)


@mock.patch("jogo.personagens.classes.randint", return_value=42)
class TestPersonagemDaMaisDanoComAumentoDeCriticoAssassino(TestCase):
    def setUp(self):
        self.personagem = Assassino("nome", True)
        item = AdornoDeArma(critico=6, aumento_critico=16)
        self.personagem.inventario.append(item)
        item2 = Adaga(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item2)
        item3 = AdagaSecundaria(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item3)
        self.monstro = Tartaruga()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80
        self.personagem.equipar(item)
        self.personagem.equipar(item2)
        self.personagem.equipar(item3)

    def test_dando_mais_dano_com_aumento_critico_lancar_faca(self, *_):
        self.personagem.lancar_faca(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 10
        # esperado = valor - valor da porcentagem da armadura do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_dando_mais_dano_com_aumento_critico_ataque_furtivo(self, *_):
        self.personagem.ataque_furtivo(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 15
        # esperado = valor - valor da porcentagem da armadura do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)


@mock.patch("jogo.personagens.classes.randint", return_value=42)
class TestPersonagemDaMaisDanoComAumentoDeCriticoClerigo(TestCase):
    def setUp(self):
        self.personagem = Clerigo("nome", True)
        item = AdornoDeArma(critico=6, aumento_critico=16)
        self.personagem.inventario.append(item)
        item2 = Cajado(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item2)
        item3 = Livro(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item3)
        self.monstro = Tartaruga()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80
        self.personagem.equipar(item)
        self.personagem.equipar(item2)
        self.personagem.equipar(item3)

    def test_dando_mais_dano_com_aumento_critico_luz(self, *_):
        self.personagem.luz(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 10
        # esperado = valor - valor da porcentagem da resistencia do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)


@mock.patch("jogo.personagens.classes.randint", return_value=42)
class TestPersonagemDaMaisDanoComAumentoDeCriticoMonge(TestCase):
    def setUp(self):
        self.personagem = Monge("nome", True)
        item = AdornoDeArma(critico=6, aumento_critico=16)
        self.personagem.inventario.append(item)
        item2 = Luvas_de_ferro(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item2)
        item3 = Botas_de_ferro(dano=6, critico=6, aumento_critico=16)
        self.personagem.inventario.append(item3)
        self.monstro = Tartaruga()
        self.monstro.porcentagem_armadura = 80
        self.monstro.porcentagem_resistencia = 80
        self.personagem.equipar(item)
        self.personagem.equipar(item2)
        self.personagem.equipar(item3)

    def test_dando_mais_dano_com_aumento_critico_multiplos_socos(self, *_):
        self.personagem.multiplos_socos(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 10
        # esperado = valor - valor da porcentagem da armadura do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)

    def test_dando_mais_dano_com_aumento_critico_combo_de_chutes(self, *_):
        self.personagem.combo_de_chutes(self.monstro)
        # esperado = valor do aumento critico * dano
        esperado = (2 + (3 * 16) / 100) * 15
        # esperado = valor - valor da porcentagem da resistencia do monstro
        esperado = esperado - int((esperado * 80) // 100)
        # esperado = vida do monstro - esperado
        esperado = 100 - esperado
        self.assertEqual(self.monstro.status["vida"], esperado)
