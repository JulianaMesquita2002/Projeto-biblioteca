from database import conectar

class Membro:
    def __init__(self, nome, telefone, id=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO membros (nome, telefone) VALUES (?, ?)",
            (self.nome, self.telefone)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def buscar_por_id(membro_id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, telefone FROM membros WHERE id = ?",
            (membro_id,)
        )
        membro = cursor.fetchone()
        conn.close()

        return membro
