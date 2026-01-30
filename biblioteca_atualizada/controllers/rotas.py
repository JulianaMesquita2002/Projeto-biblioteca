from flask import Blueprint, request, jsonify
from models.livro import Livro
from models.membro import Membro
from database import conectar

biblioteca_bp = Blueprint("biblioteca", __name__)


@biblioteca_bp.route("/membros", methods=["POST"])
def cadastrar_membro():
    dados = request.json

    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    membro = Membro(
        nome=dados["nome"],
        telefone=dados["telefone"]
    )
    membro.salvar()

    return jsonify({"mensagem": "Membro cadastrado com sucesso"}), 201

@biblioteca_bp.route("/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.json

    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    livro = Livro(
        titulo=dados["titulo"],
        autor=dados.get("autor", "")
    )
    livro.salvar()

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

@biblioteca_bp.route("/emprestar", methods=["PATCH"])
def emprestar_livro():
    dados = request.json

    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    livro_id = dados.get("livro_id")
    membro_id = dados.get("membro_id")

    if not livro_id or not membro_id:
        return jsonify({"erro": "livro_id e membro_id são obrigatórios"}), 400

    livro = Livro.buscar_por_id(livro_id)
    if livro is None:
        return jsonify({"erro": "Livro não encontrado"}), 404

    membro = Membro.buscar_por_id(membro_id)
    if membro is None:
        return jsonify({"erro": "Membro não encontrado"}), 404

    if livro[3] is not None:
        return jsonify({"erro": "Livro já emprestado"}), 400

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE livros SET membro_id = ? WHERE id = ?",
        (membro_id, livro_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Livro emprestado com sucesso"})

@biblioteca_bp.route("/devolver", methods=["PATCH"])
def devolver_livro():
    dados = request.json

    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    livro_id = dados.get("livro_id")

    if not livro_id:
        return jsonify({"erro": "livro_id é obrigatório"}), 400

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE livros SET membro_id = NULL WHERE id = ?",
        (livro_id,)
    )
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Livro devolvido com sucesso"})


@biblioteca_bp.route("/livros/disponiveis", methods=["GET"])
def listar_disponiveis():
    livros = Livro.listar_disponiveis()

    resultado = []
    for livro in livros:
        resultado.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2]
        })

    return jsonify(resultado), 200


@biblioteca_bp.route("/membros/<int:membro_id>/historico", methods=["GET"])
def historico_membro(membro_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, titulo, autor
        FROM livros
        WHERE membro_id = ?
    """, (membro_id,))

    livros = cursor.fetchall()
    conn.close()

    resultado = []
    for livro in livros:
        resultado.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2]
        })

    return jsonify(resultado)


