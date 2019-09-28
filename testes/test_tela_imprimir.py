from unittest import TestCase
from jogo.tela.imprimir import colorir  # , imprimir


class TestesColorir(TestCase):
    def test_retornando_uma_string(self):
        resposta = colorir('teste', 'verde')
        self.assertIsInstance(resposta, str)

    def test_retornando_texto_vermelho(self):
        resposta = colorir('teste', 'vermelho')
        self.assertEqual(resposta, '\x1b[38;5;1mteste\x1b[0m')

    def test_retornando_texto_verde(self):
        resposta = colorir('teste', 'verde')
        self.assertEqual(resposta, '\x1b[38;5;2mteste\x1b[0m')

    def test_retornando_texto_cyan(self):
        resposta = colorir('teste', 'cyan')
        self.assertEqual(resposta, '\x1b[38;5;6mteste\x1b[0m')

    def test_retornando_texto_azul(self):
        resposta = colorir('teste', 'azul')
        self.assertEqual(resposta, '\x1b[38;5;4mteste\x1b[0m')

    def test_retornando_texto_amarelo(self):
        resposta = colorir('teste', 'amarelo')
        self.assertEqual(resposta, '\x1b[38;5;3mteste\x1b[0m')

    def test_retornando_texto_roxo(self):
        resposta = colorir('teste', 'roxo')
        self.assertEqual(resposta, '\x1b[38;5;93mteste\x1b[0m')

    def test_retornando_texto_magenta(self):
        resposta = colorir('teste', 'magenta')
        self.assertEqual(resposta, '\x1b[38;5;5mteste\x1b[0m')

    def test_retornando_texto_cinza_escuro(self):
        resposta = colorir('teste', 'cinza_escuro')
        self.assertEqual(resposta, '\x1b[38;5;8mteste\x1b[0m')

    def test_retornando_texto_preto(self):
        resposta = colorir('teste', 'preto')
        self.assertEqual(resposta, '\x1b[38;5;16mteste\x1b[0m')

    def test_retornando_texto_turquesa(self):
        resposta = colorir('teste', 'turquesa')
        self.assertEqual(resposta, '\x1b[38;5;159mteste\x1b[0m')

    def test_retornando_texto_laranja_escuro(self):
        resposta = colorir('teste', 'laranja_escuro')
        self.assertEqual(resposta, '\x1b[38;5;208mteste\x1b[0m')

    def test_substituindo_um_o_valor_reset_pela_cor_passada(self):
        texto = colorir('teste', 'cyan')
        resposta = colorir(f"[{texto}]", 'amarelo')
        esperado = '\x1b[38;5;3m[\x1b[38;5;6mteste\x1b[38;5;3m]\x1b[0m'
        self.assertEqual(resposta, esperado)

    def test_substituindo_um_o_valor_reset_duas_vezes_pela_cor_passada(self):
        texto = colorir('teste', 'cyan')
        texto = colorir(f"[{texto}]", 'amarelo')
        resposta = colorir(f"({texto})", 'vermelho')
        esperado = ('\x1b[38;5;1m(\x1b[38;5;3m[\x1b[38;5;6mteste'
                    '\x1b[38;5;3m]\x1b[38;5;1m)\x1b[0m')
        self.assertEqual(resposta, esperado)

    def test_substituindo_um_o_valor_reset_tres_vezes_pela_cor_passada(self):
        texto = colorir('teste', 'cyan')
        texto = colorir(f"[{texto}]", 'amarelo')
        texto = colorir(f"({texto})", 'vermelho')
        resposta = colorir(f"-{texto}-", 'verde')
        esperado = ('\x1b[38;5;2m-\x1b[38;5;1m(\x1b[38;5;3m[\x1b[38;5;6mteste'
                    '\x1b[38;5;3m]\x1b[38;5;1m)\x1b[38;5;2m-\x1b[0m')
        self.assertEqual(resposta, esperado)


# class TestesImprimir(TestCase):
#     def setUp(self):
#         self.ciclo = cycle(range(2))
#         self.tela = Screen()
#
#     def test_texto_imprimindo_no_canto_esquerdo_na_primeira_linha_da_tela(self):
#         with patch('sys.stdout', new=StringIO()) as saida_falsa:
#             imprimir('teste', self.ciclo, self.tela)
#             resultado = saida_falsa.getvalue()
#         self.assertEqual(resultado, '\x1b[2J\x1b[1;1H\x1b[mteste\x1b[0m')
#
#     def test_dois_textos_imprimidos_um_apos_o_outro(self):
#         with patch('sys.stdout', new=StringIO()) as saida_falsa:
#             imprimir('teste', self.ciclo, self.tela)
#             imprimir('teste2', self.ciclo, self.tela)
#             resultado = saida_falsa.getvalue()
#             esperado = ('\x1b[2J\x1b[1;1H\x1b[mteste\x1b[0m\x1b[2;1H\x1b[m'
#                         'teste2\x1b[0m')
#             self.assertEqual(resultado, esperado)
#
#     def test_tres_textos_imprimidos_um_apos_o_outro(self):
#         with patch('sys.stdout', new=StringIO()) as saida_falsa:
#             imprimir('teste', self.ciclo, self.tela)
#             imprimir('teste2', self.ciclo, self.tela)
#             imprimir('teste3', self.ciclo, self.tela)
#             resultado = saida_falsa.getvalue()
#             esperado = ('\x1b[2J\x1b[1;1H\x1b[mteste\x1b[0m\x1b[2;1H\x1b[m'
#                         'teste2\x1b[0m\x1b[2J\x1b[1;1H\x1b[mteste3\x1b[0m')
#             self.assertEqual(resultado, esperado)
