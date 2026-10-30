from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/usuarios/listar")
def listar_usuarios():
    return render_template("usuarios/usuarios-listar.html")


@app.route("/usuarios/inserir")
def inserir_usuario():
    return render_template("usuarios/usuarios-form.html")


@app.route("/perfis/listar")
def listar_perfis():
    return render_template("perfis/perfis-listar.html")


@app.route("/perfis/inserir")
def inserir_perfil():
    return render_template("perfis/perfis-form.html")


@app.route("/produtos/listar")
def listar_produtos():
    return render_template("produtos/produtos-listar.html")


@app.route("/produtos/inserir")
def inserir_produto():
    return render_template("produtos/produtos-form.html")


@app.route("/vendas/listar")
def listar_vendas():
    return render_template("vendas/vendas-listar.html")


@app.route("/vendas/inserir")
def inserir_venda():
    return render_template("vendas/vendas-form.html")


if __name__ == "__main__":
    app.run(debug=True)
