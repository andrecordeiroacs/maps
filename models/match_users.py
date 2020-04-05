class Match_Users:
    
    def __init__(self, nome, ramo, telefone, email):
        self.nome = nome
        self.ramo = ', '.join(["%s" % v for v in ramo])
        self.telefone = telefone
        self.email = email