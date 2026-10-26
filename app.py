import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import IntegrityError
from db import conectar

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def inicio():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM funcionarios")
    total_funcionarios = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM equipamentos")
    total_equipamentos = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM equipamentos WHERE status = 'disponivel'")
    disponiveis = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM emprestimos WHERE data_devolucao IS NULL")
    emprestimos_ativos = cursor.fetchone()["total"]

    cursor.close()
    conexao.close()

    resumo = {
        "funcionarios": total_funcionarios,
        "equipamentos": total_equipamentos,
        "disponiveis": disponiveis,
        "emprestimos_ativos": emprestimos_ativos
    }
    return render_template("inicio.html", resumo=resumo)

@app.route("/funcionarios")
def listar_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM funcionarios")
    funcionarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("funcionarios.html", funcionarios=funcionarios)

@app.route("/funcionarios/novo", methods=["GET", "POST"])
def novo_funcionario():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        departamento = request.form["departamento"]
        cargo = request.form["cargo"]

        conexao = conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO funcionarios (nome, email, departamento, cargo) VALUES (%s, %s, %s, %s)",
                (nome, email, departamento, cargo)
            )
            conexao.commit()
            flash("Funcionário cadastrado com sucesso!", "sucesso")
        except IntegrityError:
            conexao.rollback()
            flash("Já existe um funcionário com este e-mail.", "erro")
            return redirect(url_for("novo_funcionario"))
        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for("listar_funcionarios"))

    return render_template("funcionario_form.html")


@app.route("/funcionarios/<int:id>/editar", methods=["GET", "POST"])
def editar_funcionario(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        departamento = request.form["departamento"]
        cargo = request.form["cargo"]

        try:
            cursor.execute(
                "UPDATE funcionarios SET nome = %s, email = %s, departamento = %s, cargo = %s WHERE id = %s",
                (nome, email, departamento, cargo, id)
            )
            conexao.commit()
            flash("Funcionário atualizado com sucesso!", "sucesso")
            return redirect(url_for("listar_funcionarios"))
        except IntegrityError:
            conexao.rollback()
            flash("Já existe outro funcionário com este e-mail.", "erro")
            return redirect(url_for("editar_funcionario", id=id))
        finally:
            cursor.close()
            conexao.close()

    cursor.execute("SELECT * FROM funcionarios WHERE id = %s", (id,))
    funcionario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return render_template("funcionario_form.html", funcionario=funcionario)


@app.route("/funcionarios/<int:id>/excluir", methods=["POST"])
def excluir_funcionario(id):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM funcionarios WHERE id = %s", (id,))
        conexao.commit()
        flash("Funcionário excluído com sucesso!", "sucesso")
    except IntegrityError:
        conexao.rollback()
        flash("Não é possível excluir: este funcionário possui empréstimos registrados.", "erro")
    finally:
        cursor.close()
        conexao.close()
    return redirect(url_for("listar_funcionarios"))

# ---------- EQUIPAMENTOS ----------

@app.route("/equipamentos")
def listar_equipamentos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM equipamentos ORDER BY id")
    equipamentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("equipamentos.html", equipamentos=equipamentos)


@app.route("/equipamentos/novo", methods=["GET", "POST"])
def novo_equipamento():
    if request.method == "POST":
        numero_serie = request.form["numero_serie"]
        tipo = request.form["tipo"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        status = request.form["status"]
        data_aquisicao = request.form["data_aquisicao"] or None

        conexao = conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO equipamentos (numero_serie, tipo, marca, modelo, status, data_aquisicao) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (numero_serie, tipo, marca, modelo, status, data_aquisicao)
            )
            conexao.commit()
            flash("Equipamento cadastrado com sucesso!", "sucesso")
        except IntegrityError:
            conexao.rollback()
            flash("Já existe um equipamento com este número de série.", "erro")
            return redirect(url_for("novo_equipamento"))
        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for("listar_equipamentos"))

    return render_template("equipamento_form.html")


@app.route("/equipamentos/<int:id>/editar", methods=["GET", "POST"])
def editar_equipamento(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":
        numero_serie = request.form["numero_serie"]
        tipo = request.form["tipo"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        status = request.form["status"]
        data_aquisicao = request.form["data_aquisicao"] or None

        try:
            cursor.execute(
                "UPDATE equipamentos SET numero_serie = %s, tipo = %s, marca = %s, modelo = %s, "
                "status = %s, data_aquisicao = %s WHERE id = %s",
                (numero_serie, tipo, marca, modelo, status, data_aquisicao, id)
            )
            conexao.commit()
            flash("Equipamento atualizado com sucesso!", "sucesso")
            return redirect(url_for("listar_equipamentos"))
        except IntegrityError:
            conexao.rollback()
            flash("Já existe outro equipamento com este número de série.", "erro")
            return redirect(url_for("editar_equipamento", id=id))
        finally:
            cursor.close()
            conexao.close()

    cursor.execute("SELECT * FROM equipamentos WHERE id = %s", (id,))
    equipamento = cursor.fetchone()
    cursor.close()
    conexao.close()
    return render_template("equipamento_form.html", equipamento=equipamento)


@app.route("/equipamentos/<int:id>/excluir", methods=["POST"])
def excluir_equipamento(id):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM equipamentos WHERE id = %s", (id,))
        conexao.commit()
        flash("Equipamento excluído com sucesso!", "sucesso")
    except IntegrityError:
        conexao.rollback()
        flash("Não é possível excluir: este equipamento possui empréstimos registrados.", "erro")
    finally:
        cursor.close()
        conexao.close()
    return redirect(url_for("listar_equipamentos"))

# ---------- EMPRÉSTIMOS ----------

@app.route("/emprestimos")
def listar_emprestimos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT emp.id, f.nome, f.departamento,
               e.tipo, e.marca, e.modelo, e.numero_serie,
               emp.data_entrega, emp.data_devolucao, emp.observacao
        FROM emprestimos emp
        JOIN equipamentos e ON emp.equipamento_id = e.id
        JOIN funcionarios f ON emp.funcionario_id = f.id
        ORDER BY emp.id DESC
    """)
    emprestimos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("emprestimos.html", emprestimos=emprestimos)


@app.route("/emprestimos/novo", methods=["GET", "POST"])
def novo_emprestimo():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":
        equipamento_id = request.form["equipamento_id"]
        funcionario_id = request.form["funcionario_id"]
        data_entrega = request.form["data_entrega"]
        observacao = request.form["observacao"] or None

        try:
            # Só muda para em_uso se o equipamento AINDA estiver disponível
            cursor.execute(
                "UPDATE equipamentos SET status = 'em_uso' WHERE id = %s AND status = 'disponivel'",
                (equipamento_id,)
            )
            if cursor.rowcount == 0:
                conexao.rollback()
                flash("Este equipamento não está mais disponível para empréstimo.", "erro")
                return redirect(url_for("novo_emprestimo"))

            cursor.execute(
                "INSERT INTO emprestimos (equipamento_id, funcionario_id, data_entrega, observacao) "
                "VALUES (%s, %s, %s, %s)",
                (equipamento_id, funcionario_id, data_entrega, observacao)
            )
            conexao.commit()
            flash("Empréstimo registrado com sucesso!", "sucesso")
        except IntegrityError:
            conexao.rollback()
            flash("Funcionário ou equipamento inválido.", "erro")
            return redirect(url_for("novo_emprestimo"))
        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for("listar_emprestimos"))

    cursor.execute("SELECT id, nome, departamento FROM funcionarios ORDER BY nome")
    funcionarios = cursor.fetchall()

    cursor.execute(
        "SELECT id, tipo, marca, modelo, numero_serie FROM equipamentos "
        "WHERE status = 'disponivel' ORDER BY tipo"
    )
    equipamentos = cursor.fetchall()

    cursor.close()
    conexao.close()
    return render_template(
        "emprestimo_form.html",
        funcionarios=funcionarios,
        equipamentos=equipamentos,
        hoje=date.today().isoformat()
    )


@app.route("/emprestimos/<int:id>/devolver", methods=["POST"])
def devolver_emprestimo(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT equipamento_id FROM emprestimos WHERE id = %s AND data_devolucao IS NULL",
            (id,)
        )
        emprestimo = cursor.fetchone()

        if emprestimo is None:
            flash("Empréstimo não encontrado ou já devolvido.", "erro")
            return redirect(url_for("listar_emprestimos"))

        cursor.execute(
            "UPDATE emprestimos SET data_devolucao = CURDATE() WHERE id = %s",
            (id,)
        )
        cursor.execute(
            "UPDATE equipamentos SET status = 'disponivel' WHERE id = %s",
            (emprestimo["equipamento_id"],)
        )
        conexao.commit()
        flash("Devolução registrada! O equipamento está disponível novamente.", "sucesso")
    finally:
        cursor.close()
        conexao.close()
    return redirect(url_for("listar_emprestimos"))


if __name__ == "__main__":
    app.run(debug=True)