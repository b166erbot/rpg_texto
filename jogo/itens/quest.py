class ItemQuest:
    def __init__(self, nome):
        self.nome = nome
        self.tipo = 'quest'

    def __repr__(self):
        return f"Item de quest: {self.nome}"
