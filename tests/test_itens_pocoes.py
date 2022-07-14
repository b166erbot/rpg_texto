from unittest import TestCase

from jogo.itens.pocoes import (
    PocaoDeVidaFraca,
    ElixirDeVidaFraca,
    PilhaDePocoes,
)
from jogo.personagens.classes import Arqueiro


class TestPilhaDePocao(TestCase):
    def setUp(self):
        self.personagem = Arqueiro('nome', True)
    
    def test_personagem_juntando_pilhas_caso_tenha_duas_pilhas_com_5_pocoes(self):
        pocoes = [PocaoDeVidaFraca() for _ in range(5)]
        pocoes2 = [PocaoDeVidaFraca() for _ in range(5)]
        pilha = PilhaDePocoes(pocoes, pocoes[0].nome)
        pilha2 = PilhaDePocoes(pocoes2, pocoes[0].nome)
        self.personagem.inventario.append(pilha)
        self.personagem.inventario.append(pilha2)
        self.personagem.juntar_pocoes()
        pilha3 = self.personagem.inventario[0]
        self.assertEqual(len(pilha3), 10)
    
    def test_personagem_juntando_pilhas_caso_tenha_3_pilhas_com_3_pocoes_cada(self):
        pocoes = [PocaoDeVidaFraca() for _ in range(3)]
        pocoes2 = [PocaoDeVidaFraca() for _ in range(3)]
        pocoes3 = [PocaoDeVidaFraca() for _ in range(3)]
        pilha = PilhaDePocoes(pocoes, pocoes[0].nome)
        pilha2 = PilhaDePocoes(pocoes2, pocoes2[0].nome)
        pilha3 = PilhaDePocoes(pocoes3, pocoes3[0].nome)
        self.personagem.inventario.append(pilha)
        self.personagem.inventario.append(pilha2)
        self.personagem.inventario.append(pilha3)
        self.personagem.juntar_pocoes()
        pilha4 = self.personagem.inventario[0]
        self.assertEqual(len(pilha4), 9)

    def test_personagem_juntando_pilhas_caso_tenha_3_pilhas_com_tamanhos_diferentes(self):
        pocoes = [PocaoDeVidaFraca() for _ in range(3)]
        pocoes2 = [PocaoDeVidaFraca() for _ in range(7)]
        pocoes3 = [PocaoDeVidaFraca() for _ in range(5)]
        pilha = PilhaDePocoes(pocoes, pocoes[0].nome)
        pilha2 = PilhaDePocoes(pocoes2, pocoes2[0].nome)
        pilha3 = PilhaDePocoes(pocoes3, pocoes3[0].nome)
        self.personagem.inventario.append(pilha)
        self.personagem.inventario.append(pilha2)
        self.personagem.inventario.append(pilha3)
        self.personagem.juntar_pocoes()
        pilha4 = self.personagem.inventario[0]
        pilha5 = self.personagem.inventario[1]
        self.assertEqual(len(pilha4), 10)
        self.assertEqual(len(pilha5), 5)
    
    def test_personagem_juntando_pilhas_caso_tenha_3_pilhas_com_tamanhos_diferentes_com_a_ordem_alterada(self):
        pocoes = [PocaoDeVidaFraca() for _ in range(3)]
        pocoes2 = [PocaoDeVidaFraca() for _ in range(5)]
        pocoes3 = [PocaoDeVidaFraca() for _ in range(7)]
        pilha = PilhaDePocoes(pocoes, pocoes[0].nome)
        pilha2 = PilhaDePocoes(pocoes2, pocoes2[0].nome)
        pilha3 = PilhaDePocoes(pocoes3, pocoes3[0].nome)
        self.personagem.inventario.append(pilha)
        self.personagem.inventario.append(pilha2)
        self.personagem.inventario.append(pilha3)
        self.personagem.juntar_pocoes()
        pilha4 = self.personagem.inventario[0]
        pilha5 = self.personagem.inventario[1]
        self.assertEqual(len(pilha4), 10)
        self.assertEqual(len(pilha5), 5)
    
    def test_personagem_juntando_pilhas_caso_tenha_pilhas_diferentes_com_tamanhos_diferentes(self):
        pocoes = [PocaoDeVidaFraca() for _ in range(3)]
        pocoes2 = [PocaoDeVidaFraca() for _ in range(5)]
        pocoes3 = [PocaoDeVidaFraca() for _ in range(7)]
        pocoes4 = [ElixirDeVidaFraca() for _ in range(3)]
        pocoes5 = [ElixirDeVidaFraca() for _ in range(5)]
        pocoes6 = [ElixirDeVidaFraca() for _ in range(7)]
        pilha = PilhaDePocoes(pocoes, pocoes[0].nome)
        pilha2 = PilhaDePocoes(pocoes2, pocoes2[0].nome)
        pilha3 = PilhaDePocoes(pocoes3, pocoes3[0].nome)
        pilha4 = PilhaDePocoes(pocoes4, pocoes4[0].nome)
        pilha5 = PilhaDePocoes(pocoes5, pocoes5[0].nome)
        pilha6 = PilhaDePocoes(pocoes6, pocoes6[0].nome)
        self.personagem.inventario.append(pilha)
        self.personagem.inventario.append(pilha2)
        self.personagem.inventario.append(pilha3)
        self.personagem.inventario.append(pilha4)
        self.personagem.inventario.append(pilha5)
        self.personagem.inventario.append(pilha6)
        self.personagem.juntar_pocoes()
        pilha7 = self.personagem.inventario[0]
        pilha8 = self.personagem.inventario[1]
        pilha9 = self.personagem.inventario[2]
        pilha10 = self.personagem.inventario[3]
        self.assertEqual(len(pilha7), 10)
        self.assertEqual(len(pilha8), 5)
        self.assertEqual(len(pilha9), 10)
        self.assertEqual(len(pilha10), 5)
    
    def test_personagem_nao_gerando_erro_caso_juntar_pilhas_for_chamado_sem_pilhas(self):
        self.personagem.juntar_pocoes()