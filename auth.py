from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Simulação de usuários para demonstração
# Em produção, isso seria armazenado no banco de dados com senhas criptografadas
users = {
    'Rodrigo': {
        'id': 1,
        'password': '78909807',
        'nome': 'Rodrigo',
        'crf': 'CRF-RJ 12345'
    }
}

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session['user_id'] = users[username]['id']
            session['username'] = username
            session['nome'] = users[username]['nome']
            session['crf'] = users[username]['crf']
            session.permanent = True
            
            flash(f'Bem-vindo, {users[username]["nome"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))
