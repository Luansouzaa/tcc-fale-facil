from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

#Configuração do banco de dados(MySQL)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin123',
    'database': 'feedback_db',
    'charset': 'utf8mb4'
}

def get_connection():
    """Retorna uma conexão com o MySQL."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

# Rotas (caminho das páginas)

@app.route('/')
def index():
    """Página inicial com lista de feedbacks."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    filtro = request.args.get('filtro', '')
    categoria = request.args.get('categoria', '')

    query = "SELECT * FROM feedbacks WHERE 1=1"
    params = []

    if filtro:
        query += " AND (titulo LIKE %s OR descricao LIKE %s OR funcionario LIKE %s)"
        like = f"%{filtro}%"
        params.extend([like, like, like])

    if categoria:
        query += " AND categoria = %s"
        params.append(categoria)

    query += " ORDER BY criado_em DESC"

    cursor.execute(query, params)
    feedbacks = cursor.fetchall()

    # Estatísticas
    cursor.execute("SELECT COUNT(*) AS total FROM feedbacks")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM feedbacks WHERE status = 'Pendente'")
    pendentes = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM feedbacks WHERE status = 'Resolvido'")
    resolvidos = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM feedbacks WHERE DATE(criado_em) = CURDATE()")
    hoje = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    stats = {'total': total, 'pendentes': pendentes, 'resolvidos': resolvidos, 'hoje': hoje}
    return render_template('index.html', feedbacks=feedbacks, stats=stats,
                           filtro=filtro, categoria=categoria)


@app.route('/novo', methods=['GET', 'POST'])
def novo_feedback():
    """Cadastrar novo feedback."""
    if request.method == 'POST':
        funcionario = request.form['funcionario'].strip()
        departamento = request.form['departamento'].strip()
        categoria = request.form['categoria']
        titulo = request.form['titulo'].strip()
        descricao = request.form['descricao'].strip()
        prioridade = request.form['prioridade']
        anonimo = request.form.get('anonimo') == '1'

        if anonimo:
            funcionario = 'Anônimo'
            departamento = 'Não informado'
        
        if not all([categoria, titulo, descricao]):
            flash('Preencha todos os campos obrigatórios.', 'erro')
            return render_template('form.html', modo='novo', dados=request.form)

        if not anonimo and not all([funcionario, departamento]):
            flash('Preencha todos os campos obrigatórios.', 'erro')
            return render_template('form.html', modo='novo', dados=request.form)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO feedbacks (funcionario, departamento, categoria, titulo, descricao, prioridade)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (funcionario, departamento, categoria, titulo, descricao, prioridade)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Feedback cadastrado com sucesso!', 'sucesso')
        return redirect(url_for('index'))

    return render_template('form.html', modo='novo', dados={})


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_feedback(id):
    """Editar um feedback existente."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        funcionario = request.form['funcionario'].strip()
        departamento = request.form['departamento'].strip()
        categoria = request.form['categoria']
        titulo = request.form['titulo'].strip()
        descricao = request.form['descricao'].strip()
        prioridade = request.form['prioridade']
        status = request.form['status']

        cursor.execute(
            """UPDATE feedbacks SET funcionario=%s, departamento=%s, categoria=%s,
               titulo=%s, descricao=%s, prioridade=%s, status=%s
               WHERE id=%s""",
            (funcionario, departamento, categoria, titulo, descricao, prioridade, status, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Feedback atualizado com sucesso!', 'sucesso')
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM feedbacks WHERE id = %s", (id,))
    feedback = cursor.fetchone()
    cursor.close()
    conn.close()

    if not feedback:
        flash('Feedback não encontrado.', 'erro')
        return redirect(url_for('index'))

    return render_template('form.html', modo='editar', dados=feedback)


@app.route('/excluir/<int:id>', methods=['POST'])
def excluir_feedback(id):
    """Excluir um feedback."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedbacks WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Feedback excluído com sucesso.', 'info')
    return redirect(url_for('index'))


@app.route('/detalhe/<int:id>')
def detalhe_feedback(id):
    """Visualizar detalhe completo do feedback."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedbacks WHERE id = %s", (id,))
    feedback = cursor.fetchone()
    cursor.close()
    conn.close()

    if not feedback:
        flash('Feedback não encontrado.', 'erro')
        return redirect(url_for('index'))

    return render_template('detalhe.html', feedback=feedback)


@app.route('/atualizar_status/<int:id>', methods=['POST'])
def atualizar_status(id):
    """Atualizar apenas o status ."""
    data = request.get_json()
    novo_status = data.get('status')

    if novo_status not in ['Pendente', 'Em Analise', 'Resolvido']:
        return jsonify({'erro': 'Status inválido'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE feedbacks SET status=%s WHERE id=%s", (novo_status, id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'sucesso': True, 'status': novo_status})


# ── Inicialização ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
