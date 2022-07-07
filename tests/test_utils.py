from unittest import TestCase

from jogo.utils import Acumulador, menor_numero


class TestAcumulador(TestCase):
    def setUp(self):
        self.acumulador = Acumulador(0, [1, 2, 3, 4, 5, 6], 1)

    def test_depositar_valor_retorna_level_3_caso_receba_3_de_valor(self):
        self.acumulador.depositar_valor(3)
        self.assertEqual(self.acumulador.level, 3)
        self.assertEqual(int(self.acumulador), 0)

    def test_valor_retorna_1_caso_receba_4_de_valor(self):
        self.acumulador.depositar_valor(4)
        self.assertEqual(self.acumulador.level, 3)
        self.assertEqual(int(self.acumulador), 1)

    def test_depositar_valor_retorna_level_maximo_caso_receba_21_de_valor(self):
        self.acumulador.depositar_valor(21)
        self.assertEqual(self.acumulador.level, 7)
        self.assertEqual(int(self.acumulador), 0)

    def test_depositar_valor_retorna_valor_0_caso_receba_22_de_valor(self):
        self.acumulador.depositar_valor(22)
        self.assertEqual(self.acumulador.level, 7)
        self.assertEqual(int(self.acumulador), 0)

    def test_valor_glifos_retorna_10_caso_level_seja_4(self):
        self.acumulador = Acumulador(0, [1, 2, 3, 4, 5, 6], 4)
        # 1 + 2 + 3 == 6
        self.assertEqual(self.acumulador.valor_glifos(), 6)

    def test_valor_glifos_retorna_21_caso_level_seja_7(self):
        self.acumulador = Acumulador(0, [1, 2, 3, 4, 5, 6], 7)
        self.assertEqual(self.acumulador.valor_glifos(), 21)

    def test_valor_retorna_0_caso_level_seja_7_e_valor_seja_1(self):
        self.acumulador = Acumulador(1, [1, 2, 3, 4, 5, 6], 7)
        self.assertEqual(self.acumulador.valor_glifos(), 21)
        self.assertEqual(int(self.acumulador), 0)

    def test_valor_glifos_retorna_21_caso_level_ultrapasse_o_limite_8(self):
        self.acumulador = Acumulador(1, [1, 2, 3, 4, 5, 6], 8)
        self.assertEqual(self.acumulador.valor_glifos(), 21)
        self.assertEqual(int(self.acumulador), 0)

    def test_valor_glifos_retorna_10_caso_depositar_valor_receba_10(self):
        self.acumulador.depositar_valor(10)
        self.assertEqual(self.acumulador.valor_glifos(), 10)

    def test_valor_glifos_retorna_11_caso_depositar_valor_receba_11(self):
        self.acumulador.depositar_valor(11)
        self.assertEqual(self.acumulador.valor_glifos(), 11)

    def test_valor_glifos_retorna_0_caso_acumular_level_8_e_depositar_valor_receba_10(
        self,
    ):
        self.acumulador = Acumulador(1, [1, 2, 3, 4, 5, 6], 8)
        self.acumulador.depositar_valor(10)
        self.assertEqual(self.acumulador.valor_glifos(), 21)

    def test_valor_glifos_retorna_1_caso_level_seja_1_e_depositar_valor_receba_1(
        self,
    ):
        self.acumulador.depositar_valor(1)
        self.assertEqual(self.acumulador.valor_glifos(), 1)

    def test_valor_faltando_retorna_0_caso_depositar_valor_receba_maximo_de_glifos(
        self,
    ):
        valor = self.acumulador.valor_total()
        self.acumulador.depositar_valor(valor)
        self.assertEqual(self.acumulador.valor_faltando(), 0)

    def test_valor_faltando_retorna_0_caso_acumular_esteja_no_level_maximo(
        self,
    ):
        self.acumulador = Acumulador(0, [1, 2, 3, 4, 5, 6], 7)
        self.assertEqual(self.acumulador.valor_faltando(), 0)

    def test_valor_faltando_retorna_6_caso_acumular_esteja_no_level_6(self):
        self.acumulador = Acumulador(0, [1, 2, 3, 4, 5, 6], 6)
        self.assertEqual(self.acumulador.valor_faltando(), 6)

    def test_valor_faltando_retorna_5_caso_acumular_esteja_no_level_6_e_com_1_de_valor(
        self,
    ):
        self.acumulador = Acumulador(1, [1, 2, 3, 4, 5, 6], 6)
        self.assertEqual(self.acumulador.valor_faltando(), 5)


class TestMenorNumero(TestCase):
    def setUp(self):
        self.lista = [5, 11, 17, 23, 29]

    def test_menor_numero_retornando_5_caso_numero_seja_menor_que_5(self):
        resultado = menor_numero(4, self.lista)
        self.assertEqual(5, resultado)

    def test_menor_numero_retornando_5_caso_numero_seja_igual_a_5(self):
        resultado = menor_numero(5, self.lista)
        self.assertEqual(5, resultado)

    def test_menor_numero_retornando_11_caso_numero_seja_igual_a_6(self):
        resultado = menor_numero(6, self.lista)
        self.assertEqual(11, resultado)

    def test_menor_numero_retornando_11_caso_numero_seja_igual_a_11(self):
        resultado = menor_numero(11, self.lista)
        self.assertEqual(11, resultado)

    def test_menor_numero_retornando_17_caso_numero_seja_igual_a_12(self):
        resultado = menor_numero(12, self.lista)
        self.assertEqual(17, resultado)

    def test_menor_numero_retornando_17_caso_numero_seja_igual_a_17(self):
        resultado = menor_numero(17, self.lista)
        self.assertEqual(17, resultado)

    def test_menor_numero_retornando_23_caso_numero_seja_igual_a_18(self):
        resultado = menor_numero(18, self.lista)
        self.assertEqual(23, resultado)

    def test_menor_numero_retornando_23_caso_numero_seja_igual_a_23(self):
        resultado = menor_numero(23, self.lista)
        self.assertEqual(23, resultado)

    def test_menor_numero_retornando_29_caso_numero_seja_igual_a_24(self):
        resultado = menor_numero(24, self.lista)
        self.assertEqual(29, resultado)

    def test_menor_numero_retornando_29_caso_numero_seja_igual_a_29(self):
        resultado = menor_numero(29, self.lista)
        self.assertEqual(29, resultado)

    def test_menor_numero_retornando_29_caso_numero_seja_maior_que_o_maximo(
        self,
    ):
        resultado = menor_numero(30, self.lista)
        self.assertEqual(29, resultado)
