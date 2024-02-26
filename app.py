from flask import Flask, render_template, request, redirect, session, flash, url_for


class Treino:
    def __init__(self, nome, categoria, carga):
        self.nome = nome
        self.categoria = categoria
        self.carga = carga
        self.proxima_carga = carga

    
class Usuario:
    def __init__(self,nome,user,senha):
        self.nome = nome
        self.user = user
        self.senha = senha


usuario_1 = Usuario("Leonardo Chinelat", "lchinelato", "leo-9852@")
usuario_2 = Usuario("Joao Oliveira", "joliveira", "joao-123@")
usuario_3 = Usuario("Pedro Castro", "pcastro", "pedro_987@")

usuarios = { usuario_1.user : usuario_1,
             usuario_2.user : usuario_2,
             usuario_3.user : usuario_3 }

lista = []

app = Flask(__name__)
app.secret_key = "chave secreta"
senha_correta = "1234"


@app.route("/")
def index():
    return render_template("index.html", titulo="Treinos", treinos=lista)


@app.route("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login", proxima=url_for("novo")))
    return render_template("novo.html", titulo="Novo Treino")


@app.route("/criar", methods=["POST",])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    carga = request.form["carga"]
    treino = Treino(nome, categoria, carga)
    lista.append(treino)
    return redirect(url_for("index"))


@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    if not proxima or proxima == None:
        proxima = url_for("index")
    return render_template("login.html", proxima=proxima)


@app.route("/autenticar", methods=["POST",])
def autenticar():

    if request.form["usuario"] in usuarios:
        usuario = usuarios[request.form["usuario"]] # exemplo: usuario = usuarios[leo]
        if request.form["senha"] == usuario.senha:
            session["usuario_logado"] = usuario.user
            flash(f"{usuario.user} logado com sucesso")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
    else:
        flash("Usuário ou senha incorretos.")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso.")
    return redirect(url_for("index"))

app.run(debug=True)
