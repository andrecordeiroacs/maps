class AjudeLocal_Server:
    def __init__(self, id, conn):
        self.id = id

    def get_server(self, id, nome, ramo, telefone, email):
        self.id = id
        self.nome = nome
        self.ramo = ramo
        self.telefone = telefone
        self.email = email

