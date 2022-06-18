class Experiencia:
    def __init__(self, xp: int, leveis: list, level: int = 1):
        self.xp = 0
        leveis += [float('inf')]
        self._leveis_dict = dict(enumerate(leveis, 1))
        self.level = level
        self.depositar_experiencia(xp)


    def __repr__(self):
        return f"{self.xp}"

    def __str__(self):
        return f"{self.xp}"

    def __int__(self):
        return self.xp

    def depositar_experiencia(self, xp: int):
        xp_requerido = self._leveis_dict.get(self.level)
        self.xp += xp
        while self.xp >= xp_requerido:
            diferenca = self.xp - xp_requerido
            if diferenca >= 0:
                self.xp -= xp_requerido
                self.level += 1
            else:
                self.xp -= diferenca
            xp_requerido = self._leveis_dict.get(self.level)
        if xp_requerido == float('inf'):
            self.xp = 0
