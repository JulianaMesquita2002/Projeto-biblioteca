from flask import Flask
from database import criar_tabelas
from controllers.rotas import biblioteca_bp

app = Flask (__name__)

criar_tabelas()

app.register_blueprint(biblioteca_bp)

if __name__ == "__main__":
    app.run(debug=True)
