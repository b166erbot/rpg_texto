def vender(equipamento, personagem):
    index = personagem.inventario.index(equipamento)
    personagem.pratas += equipamento.preco
    personagem.inventario.pop(index)
