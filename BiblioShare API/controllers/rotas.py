from flask import Blueprint, request, jsonify
from models.livro import Livro
from database import conectar

biblioteca_bp = Blueprint("biblioteca", __name__)

@biblioteca_bp.route("/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.json

    livro = Livro(
        titulo=dados["titulo"],
        autor=dados.get("autor", "")
    )
    livro.salvar()

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

@biblioteca_bp.route("/emprestar", methods=["PATCH"])
def emprestar_livro():
    dados = request.json
    livro_id = dados["livro_id"]
    membro_id = dados["membro_id"]

    livro = Livro.buscar_por_id(livro_id)

    if livro is None:
        return jsonify({"erro": "Livro não encontrado"}), 404

 
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
    livro_id = dados["livro_id"]

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

    return jsonify(resultado)
