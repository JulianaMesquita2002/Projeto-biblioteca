from flask import Flask
from database import criar_tabelas
from controllers.rotas import biblioteca_bp

app = Flask(__name__)

criar_tabelas()
app.register_blueprint(biblioteca_bp)

@app.route("/")
def home():
    return "OK"

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8081,
        debug=False,
        use_reloader=False
    )



