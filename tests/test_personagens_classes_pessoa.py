# import sys
# sys.path.append('.')

import curses

curses.initscr()
from unittest import TestCase, mock
from collections import Counter

from jogo.itens.pocoes import (
    ElixirDeVidaExtraGrande,
    ElixirDeVidaFraca,
    ElixirDeVidaGrande,
    ElixirDeVidaMedia,
)

with mock.patch("jogo.personagens.classes.tela") as mocked_lib:
    from jogo.personagens.classes import (
        Arqueiro,
        Assassino,
        Clerigo,
        Guerreiro,
        Mago,
        Monge,
    )
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


class TestPorcentagemArmaduraResistencia(TestCase):
    def setUp(self):
        self.personagem = Arqueiro('nome', True)
        self.personagem2 = Arqueiro('nome', False)
        self.personagem3 = Guerreiro('nome', True)
        self.personagem4 = Guerreiro('nome', False)
        self.personagem5 = Mago('nome', True)
        self.personagem6 = Mago('nome', False)
        self.personagem7 = Assassino('nome', True)
        self.personagem8 = Assassino('nome', False)
        self.personagem9 = Clerigo('nome', True)
        self.personagem10 = Clerigo('nome', False)
        self.personagem11 = Monge('nome', True)
        self.personagem12 = Monge('nome', False)
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
    
    def test_personagem_deve_receber_dano_menos_80_porcento_na_armadura_tres_flechas(self):
        self.personagem2.tres_flechas(self.personagem)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem.status['vida'], esperado)

    def test_personagem2_deve_receber_dano_menos_80_porcento_na_armadura_tres_flechas(self):
        self.personagem.tres_flechas(self.personagem2)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem2.status['vida'], esperado)

    def test_personagem_deve_receber_dano_menos_80_porcento_na_resistencia_flecha_de_fogo(self):
        self.personagem2.flecha_de_fogo(self.personagem)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem.status['vida'], esperado)
    
    def test_personagem2_deve_receber_dano_menos_80_porcento_na_resistencia_flecha_de_fogo(self):
        self.personagem.flecha_de_fogo(self.personagem2)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem2.status['vida'], esperado)
    
    def test_personagem4_deve_receber_dano_menos_80_porcento_na_armadura_investida(self):
        self.personagem3.investida(self.personagem4)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem4.status['vida'], esperado)

    def test_personagem3_deve_receber_dano_menos_80_porcento_na_armadura_investida(self):
        self.personagem4.investida(self.personagem3)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem3.status['vida'], esperado)

    def test_personagem4_deve_receber_dano_menos_80_porcento_na_armadura_esmagar(self):
        self.personagem3.esmagar(self.personagem4)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem4.status['vida'], esperado)
    
    def test_personagem3_deve_receber_dano_menos_80_porcento_na_armadura_esmagar(self):
        self.personagem4.esmagar(self.personagem3)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem3.status['vida'], esperado)

    def test_personagem5_deve_receber_dano_menos_80_porcento_na_resistencia_lanca_de_gelo(self):
        self.personagem6.lanca_de_gelo(self.personagem5)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem5.status['vida'], esperado)
    
    def test_personagem6_deve_receber_dano_menos_80_porcento_na_resistencia_lanca_de_gelo(self):
        self.personagem5.lanca_de_gelo(self.personagem6)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem6.status['vida'], esperado)

    def test_personagem5_deve_receber_dano_menos_80_porcento_na_resistencia_bola_de_fogo(self):
        self.personagem6.bola_de_fogo(self.personagem5)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem5.status['vida'], esperado)

    def test_personagem6_deve_receber_dano_menos_80_porcento_na_resistencia_bola_de_fogo(self):
        self.personagem5.bola_de_fogo(self.personagem6)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem6.status['vida'], esperado)

    def test_personagem7_deve_receber_dano_menos_80_porcento_na_armadura_lancar_faca(self):
        self.personagem8.lancar_faca(self.personagem7)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem7.status['vida'], esperado)

    def test_personagem8_deve_receber_dano_menos_80_porcento_na_armadura_lancar_faca(self):
        self.personagem7.lancar_faca(self.personagem8)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem8.status['vida'], esperado)

    def test_personagem7_deve_receber_dano_menos_80_porcento_na_armadura_ataque_furtivo(self):
        self.personagem8.ataque_furtivo(self.personagem7)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem7.status['vida'], esperado)
    
    def test_personagem8_deve_receber_dano_menos_80_porcento_na_armadura_ataque_furtivo(self):
        self.personagem7.ataque_furtivo(self.personagem8)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem8.status['vida'], esperado)

    def test_personagem9_deve_receber_dano_menos_80_porcento_na_resistencia_luz(self):
        self.personagem10.luz(self.personagem9)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem9.status['vida'], esperado)

    def test_personagem10_deve_receber_dano_menos_80_porcento_na_resistencia_luz(self):
        self.personagem9.luz(self.personagem10)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem10.status['vida'], esperado)

    def test_personagem11_deve_receber_dano_menos_80_porcento_na_armadura_multiplos_socos(self):
        self.personagem12.multiplos_socos(self.personagem11)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem11.status['vida'], esperado)

    def test_personagem12_deve_receber_dano_menos_80_porcento_na_armadura_multiplos_socos(self):
        self.personagem11.multiplos_socos(self.personagem12)
        esperado = 100 - (10 - int((10 * 80) // 100))
        self.assertEqual(self.personagem12.status['vida'], esperado)

    def test_personagem11_deve_receber_dano_menos_80_porcento_na_armadura_combo_de_chutes(self):
        self.personagem12.combo_de_chutes(self.personagem11)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem11.status['vida'], esperado)
    
    def test_personagem12_deve_receber_dano_menos_80_porcento_na_armadura_combo_de_chutes(self):
        self.personagem11.combo_de_chutes(self.personagem12)
        esperado = 100 - (15 - int((15 * 80) // 100))
        self.assertEqual(self.personagem12.status['vida'], esperado)


class TestStatus(TestCase):
    def setUp(self):
        self.status = Counter({
            "vida": 110,
            "dano": 10,
            "resistencia": 10,
            "velo-ataque": 1,
            "criti": 10,
            "armadura": 10,
            "magia": 100,
            "stamina": 100,
            "velo-movi": 1,
        })
        self.personagem = Arqueiro('nome', True, status=self.status)

    def test_personagem_mantem_o_status_mesmo_depois_de_atualizar(self):
        self.personagem.atualizar_status()
        self.assertEqual(self.personagem.status, self.status)