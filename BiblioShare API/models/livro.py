from database import conectar

class Livro:
    def __init__(self, titulo, autor, membro_id=None, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.membro_id = membro_id

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO livros (titulo, autor, membro_id) VALUES (?, ?, ?)",
            (self.titulo, self.autor, self.membro_id)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def buscar_por_id(livro_id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, titulo, autor, membro_id FROM livros WHERE id = ?",
            (livro_id,)
        )
        livro = cursor.fetchone()
        conn.close()

        return livro

    @staticmethod
    def listar_disponiveis():
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, titulo, autor FROM livros WHERE membro_id IS NULL"
        )
        livros = cursor.fetchall()
        conn.close()

        return livros

