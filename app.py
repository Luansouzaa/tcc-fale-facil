from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import mysql.connector
from functools import wraps
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'fale_facil_chave_secreta_2025'

DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'admin123',
    'database': 'fale_facil_db',
    'charset':  'utf8mb4'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faca login para continuar.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        if session.get('perfil') != 'admin':
            flash('Acesso restrito a administradores.', 'erro')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email'].strip()
        senha = request.form['senha']

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s",
                       (email, hash_senha(senha)))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            session['usuario_id'] = usuario['id']
            session['nome']       = usuario['nome']
            session['perfil']     = usuario['perfil']
            session['email']      = usuario['email']
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos.', 'erro')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    filtro    = request.args.get('filtro', '')
    categoria = request.args.get('categoria', '')

    if session['perfil'] == 'admin':
        query  = "SELECT f.*, u.nome as autor FROM feedbacks f LEFT JOIN usuarios u ON f.usuario_id = u.id WHERE 1=1"
        params = []
    else:
        query  = "SELECT f.*, u.nome as autor FROM feedbacks f LEFT JOIN usuarios u ON f.usuario_id = u.id WHERE f.usuario_id = %s"
        params = [session['usuario_id']]

    if filtro:
        query += " AND (f.titulo LIKE %s OR f.descricao LIKE %s)"
        like   = f"%{filtro}%"
        params.extend([like, like])

    if categoria:
        query += " AND f.categoria = %s"
        params.append(categoria)

    query += " ORDER BY f.criado_em DESC"
    cursor.execute(query, params)
    feedbacks = cursor.fetchall()

    if session['perfil'] == 'admin':
        cursor.execute("SELECT COUNT(*) AS n FROM feedbacks")
        total = cursor.fetchone()['n']
        cursor.execute("SELECT COUNT(*) AS n FROM feedbacks WHERE status='Pendente'")
        pendentes = cursor.fetchone()['n']
        cursor.execute("SELECT COUNT(*) AS n FROM feedbacks WHERE status='Resolvido'")
        resolvidos = cursor.fetchone()['n']
        cursor.execute("SELECT COUNT(*) AS n FROM feedbacks WHERE DATE(criado_em)=CURDATE()")
        hoje = cursor.fetchone()['n']
    else:
        uid = session['usuario_id']
        cursor.execute("SELECT COUNT(*) AS n FROM feedbacks WHERE usuario_id=%s", (uid,))
        total = cursor.fetchone()['n']
        cursor.execute("SELECT COUNT(*) AS n FROM feedbacks WHERE usuario_id=%s AND status='Pendente'", (uid,))
        pendentes = cursor.fetchone()['n']
        cursor.execute("SELECT COUNT(*) AS n FROM feedbacks WHERE usuario_id=%s AND status='Resolvido'", (uid,))
        resolvidos = cursor.fetchone()['n']
        cursor.execute("SELECT COUNT(*) AS n FROM feedbacks WHERE usuario_id=%s AND DATE(criado_em)=CURDATE()", (uid,))
        hoje = cursor.fetchone()['n']

    cursor.close()
    conn.close()

    stats = {'total': total, 'pendentes': pendentes, 'resolvidos': resolvidos, 'hoje': hoje}
    return render_template('index.html', feedbacks=feedbacks, stats=stats,
                           filtro=filtro, categoria=categoria)

@app.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_feedback():
    if session.get('perfil') == 'admin':
        flash('Administradores nao podem enviar feedbacks.', 'info')
        return redirect(url_for('index'))

    if request.method == 'POST':
        anonimo      = request.form.get('anonimo') == '1'
        funcionario  = 'Anonimo' if anonimo else request.form.get('funcionario', '').strip()
        departamento = 'Nao informado' if anonimo else request.form.get('departamento', '').strip()
        categoria    = request.form.get('categoria', '')
        titulo       = request.form.get('titulo', '').strip()
        descricao    = request.form.get('descricao', '').strip()
        prioridade   = request.form.get('prioridade', 'Media')

        if not all([categoria, titulo, descricao]):
            flash('Preencha todos os campos obrigatorios.', 'erro')
            return render_template('form.html', modo='novo', dados=request.form)

        if not anonimo and not all([funcionario, departamento]):
            flash('Preencha seu nome e departamento.', 'erro')
            return render_template('form.html', modo='novo', dados=request.form)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO feedbacks (usuario_id, funcionario, departamento, categoria, titulo, descricao, prioridade, anonimo)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (session['usuario_id'], funcionario, departamento, categoria, titulo, descricao, prioridade, anonimo)
        )
        conn.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        conn.close()

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM feedbacks WHERE id = %s", (novo_id,))
        feedback = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template('sucesso.html', feedback=feedback)

    return render_template('form.html', modo='novo', dados={})

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_feedback(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedbacks WHERE id = %s", (id,))
    feedback = cursor.fetchone()

    if not feedback:
        flash('Feedback nao encontrado.', 'erro')
        cursor.close(); conn.close()
        return redirect(url_for('index'))

    flash('Edicao de feedbacks nao e permitida.', 'erro')
    cursor.close(); conn.close()
    return redirect(url_for('index'))

    if request.method == 'POST':
        anonimo      = request.form.get('anonimo') == '1'
        funcionario  = 'Anonimo' if anonimo else request.form.get('funcionario', '').strip()
        departamento = 'Nao informado' if anonimo else request.form.get('departamento', '').strip()
        categoria    = request.form.get('categoria', '')
        titulo       = request.form.get('titulo', '').strip()
        descricao    = request.form.get('descricao', '').strip()
        prioridade   = request.form.get('prioridade', 'Media')
        status       = request.form.get('status', feedback['status']) if session['perfil'] == 'admin' else feedback['status']

        cursor.execute(
            """UPDATE feedbacks SET funcionario=%s, departamento=%s, categoria=%s,
               titulo=%s, descricao=%s, prioridade=%s, status=%s, anonimo=%s WHERE id=%s""",
            (funcionario, departamento, categoria, titulo, descricao, prioridade, status, anonimo, id)
        )
        conn.commit()
        cursor.close(); conn.close()

        flash('Feedback atualizado com sucesso!', 'sucesso')
        return redirect(url_for('index'))

    cursor.close(); conn.close()
    return render_template('form.html', modo='editar', dados=feedback)



@app.route('/detalhe/<int:id>')
@login_required
def detalhe_feedback(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedbacks WHERE id = %s", (id,))
    feedback = cursor.fetchone()
    cursor.close(); conn.close()

    if not feedback:
        flash('Feedback nao encontrado.', 'erro')
        return redirect(url_for('index'))

    if session['perfil'] != 'admin' and feedback['usuario_id'] != session['usuario_id']:
        flash('Voce nao tem permissao para ver este feedback.', 'erro')
        return redirect(url_for('index'))

    return render_template('detalhe.html', feedback=feedback)
@app.route('/perfil')
@login_required
def perfil():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, email, perfil FROM usuarios WHERE id = %s", (session['usuario_id'],))
    usuario = cursor.fetchone()
    cursor.close(); conn.close()
    return render_template('perfil.html', usuario=usuario)

@app.route('/atualizar_status/<int:id>', methods=['POST'])
@admin_required
def atualizar_status(id):
    data = request.get_json()
    novo_status = data.get('status')

    if novo_status not in ['Pendente', 'Em Analise', 'Resolvido']:
        return jsonify({'erro': 'Status invalido'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE feedbacks SET status=%s WHERE id=%s", (novo_status, id))
    conn.commit()
    cursor.close(); conn.close()

    return jsonify({'sucesso': True, 'status': novo_status})

@app.route('/usuarios')
@admin_required
def usuarios():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, email, perfil, criado_em FROM usuarios ORDER BY criado_em DESC")
    usuarios = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/usuarios/novo', methods=['GET', 'POST'])
@admin_required
def novo_usuario():
    if request.method == 'POST':
        nome   = request.form['nome'].strip()
        email  = request.form['email'].strip()
        senha  = request.form['senha']
        perfil = request.form['perfil']

        if not all([nome, email, senha]):
            flash('Preencha todos os campos.', 'erro')
            return render_template('form_usuario.html', dados=request.form)

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, perfil) VALUES (%s, %s, %s, %s)",
                (nome, email, hash_senha(senha), perfil)
            )
            conn.commit()
            flash('Usuario criado com sucesso!', 'sucesso')
            return redirect(url_for('usuarios'))
        except mysql.connector.IntegrityError:
            flash('Este email ja esta cadastrado.', 'erro')
        finally:
            cursor.close(); conn.close()

    return render_template('form_usuario.html', dados={})


@app.route('/usuarios/excluir/<int:id>', methods=['POST'])
@admin_required
def excluir_usuario(id):
    if id == session['usuario_id']:
        flash('Voce nao pode excluir seu proprio usuario.', 'erro')
        return redirect(url_for('usuarios'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()
    cursor.close(); conn.close()

    flash('Usuario removido.', 'info')
    return redirect(url_for('usuarios'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
