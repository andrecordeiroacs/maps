class Match_Users:

    def __init__(self, nome, ramo, telefone, email, id_user):
        self.nome = nome
        self.ramo = ', '.join(["%s" % v for v in ramo])
        self.telefone = telefone
        self.email = email
        self.id_user = id_user
