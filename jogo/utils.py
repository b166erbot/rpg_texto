from jogo.itens.armas import (
    Espada_longa, Machado, Espada_curta, Cajado, Cajado_negro, Arco_longo,
    Arco_curto, Adaga
)
from jogo.itens.vestes import Roupa, tudo as roupas
from jogo.personagens.classes import (
    Arqueiro, Guerreiro, Mago, Assassino, Clerigo
)

o_que_equipar = {
    Guerreiro: [Espada_longa, Machado, Espada_curta],
    Arqueiro: [Arco_longo, Arco_curto],
    Mago: [Cajado, Cajado_negro],
    Assassino: [Adaga],
    Clerigo: [Cajado]
}


def equipar(equipamento, personagem):
    for nome in o_que_equipar:
        if isinstance(personagem, nome):
            for nome2 in o_que_equipar[nome]:
                if isinstance(equipamento, nome2):
                    personagem.arma = equipamento
    if equipamento.nome in personagem.equipamentos:
        personagem.equipamentos[equipamento.nome] = equipamento
