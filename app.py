from datetime import date

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

usuarios = [
    {"id": 1, 
     "nome": "Usuário 1", 
     "email": "user1@example.com",
     "celular": "1234567890", 
     "nivel": "Usuário"},
    {"id": 2, 
     "nome": "Usuário 2", 
     "email": "user2@example.com",
     "celular": "9876543210", 
     "nivel": "Administrador"},
]

produtos = [
    {"id": 1, 
     "modelo": "CG 160 Start", 
     "marca": "Honda", 
     "categoria": "Street",
     "cilindrada": "160", 
     "ano": "2026", 
     "cor": "Vermelha", 
     "preco": 17900.00, 
     "estoque": 5},
    {"id": 2, "modelo": "MT-03", "marca": "Yamaha", "categoria": "Street",
     "cilindrada": "321", "ano": "2026", "cor": "Azul", "preco": 31990.00, "estoque": 2},
    {"id": 3, "modelo": "Biz 125", "marca": "Honda", "categoria": "Scooter",
     "cilindrada": "125", "ano": "2026", "cor": "Preta", "preco": 15500.00, "estoque": 4},
]

vendas = [
    {"id": 1, "data": "2026-10-01", "cliente_id": 1, "cliente": "Usuário 1",
     "produto_id": 1, "produto": "CG 160 Start", "quantidade": 1,
     "pagamento": "À vista", "total": 17900.00},
]

NIVEIS = ["Usuário", "Administrador"]
ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
           "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
CATEGORIAS = ["Street", "Esportiva", "Trail", "Scooter", "Custom"]
PAGAMENTOS = ["À vista", "Pix", "Cartão de Crédito", "Financiamento"]


def proximo_id(lista):
    return max([item["id"] for item in lista], default=0) + 1


def buscar_por_id(lista, id):
    for item in lista:
        if item["id"] == id:
            return item
    abort(404)


@app.template_filter("real")
def formatar_real(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


@app.template_filter("data_br")
def formatar_data(data_iso):
    ano, mes, dia = data_iso.split("-")
    return f"{dia}/{mes}/{ano}"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("dashboard"))
    
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/usuarios")
def usuarios_listar():
    return render_template("usuarios/usuarios.html", usuarios=usuarios)


@app.route("/usuarios/novo", methods=["GET", "POST"])
def usuarios_novo():
    if request.method == "POST":
        usuario = request.form.to_dict()
        usuario["id"] = proximo_id(usuarios)
        usuarios.append(usuario)
        return redirect(url_for("usuarios_listar"))
    
    return render_template("usuarios/usuarios_form.html", titulo="Cadastro de Usuários",
                           dados={}, niveis=NIVEIS, estados=ESTADOS)


@app.route("/usuarios/<int:id>/editar", methods=["GET", "POST"])
def usuarios_editar(id):
    usuario = buscar_por_id(usuarios, id)
    if request.method == "POST":
        usuario.update(request.form.to_dict())
        return redirect(url_for("usuarios_listar"))
    return render_template("usuarios/usuarios_form.html", titulo="Edição de Usuário",
                           dados=usuario, niveis=NIVEIS, estados=ESTADOS)


@app.route("/usuarios/<int:id>/excluir", methods=["POST"])
def usuarios_excluir(id):
    usuarios.remove(buscar_por_id(usuarios, id))
    return redirect(url_for("usuarios_listar"))


def ler_produto_do_formulario():
    produto = request.form.to_dict()
    produto["preco"] = float(produto["preco"])
    produto["estoque"] = int(produto["estoque"])
    return produto


@app.route("/produtos")
def produtos_listar():
    return render_template("produtos/produtos.html", produtos=produtos)


@app.route("/produtos/novo", methods=["GET", "POST"])
def produtos_novo():
    if request.method == "POST":
        produto = ler_produto_do_formulario()
        produto["id"] = proximo_id(produtos)
        produtos.append(produto)
        return redirect(url_for("produtos_listar"))
    
    return render_template("produtos/produtos_form.html", titulo="Cadastro de Produtos",
                           dados={}, categorias=CATEGORIAS)


@app.route("/produtos/<int:id>/editar", methods=["GET", "POST"])
def produtos_editar(id):
    produto = buscar_por_id(produtos, id)

    if request.method == "POST":
        produto.update(ler_produto_do_formulario())
        return redirect(url_for("produtos_listar"))
    
    return render_template("produtos/produtos_form.html", titulo="Edição de Produto",
                           dados=produto, categorias=CATEGORIAS)


@app.route("/produtos/<int:id>/excluir", methods=["POST"])
def produtos_excluir(id):
    produtos.remove(buscar_por_id(produtos, id))
    return redirect(url_for("produtos_listar"))


def ler_venda_do_formulario(id_venda):
    cliente = buscar_por_id(usuarios, int(request.form["cliente_id"]))
    produto = buscar_por_id(produtos, int(request.form["produto_id"]))
    quantidade = int(request.form["quantidade"])

    return {
        "id": id_venda,
        "data": request.form["data"],
        "cliente_id": cliente["id"],
        "cliente": cliente["nome"],
        "produto_id": produto["id"],
        "produto": produto["modelo"],
        "quantidade": quantidade,
        "pagamento": request.form["pagamento"],
        "total": produto["preco"] * quantidade,
    }


@app.route("/vendas")
def vendas_listar():
    return render_template("vendas/vendas.html", vendas=vendas)


@app.route("/vendas/novo", methods=["GET", "POST"])
def vendas_novo():
    if request.method == "POST":
        vendas.append(ler_venda_do_formulario(proximo_id(vendas)))
        return redirect(url_for("vendas_listar"))
    
    return render_template("vendas/vendas_form.html", titulo="Cadastro de Vendas",
                           dados={"data": date.today().isoformat()},
                           usuarios=usuarios, produtos=produtos, pagamentos=PAGAMENTOS)


@app.route("/vendas/<int:id>/editar", methods=["GET", "POST"])
def vendas_editar(id):
    venda = buscar_por_id(vendas, id)

    if request.method == "POST":
        venda.update(ler_venda_do_formulario(id))
        return redirect(url_for("vendas_listar"))
    
    return render_template("vendas/vendas_form.html", titulo="Edição de Venda", dados=venda,
                           usuarios=usuarios, produtos=produtos, pagamentos=PAGAMENTOS)


@app.route("/vendas/<int:id>/excluir", methods=["POST"])
def vendas_excluir(id):
    vendas.remove(buscar_por_id(vendas, id))
    return redirect(url_for("vendas_listar"))


if __name__ == "__main__":
    app.run(debug=True)