import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template, redirect, url_for, flash, request, session
from src.models.user import db
from src.routes.user import user_bp
from src.routes.medicamentos import medicamentos_bp
from src.routes.receitas import receitas_bp
from src.routes.relatorios import relatorios_bp
from src.routes.auth import auth_bp
from datetime import timedelta

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(medicamentos_bp, url_prefix='/medicamentos')
app.register_blueprint(receitas_bp, url_prefix='/receitas')
app.register_blueprint(relatorios_bp, url_prefix='/relatorios')

# Habilitar banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criar tabelas no banco de dados
with app.app_context():
    db.create_all()

# Middleware para verificar autenticação
@app.before_request
def check_auth():
    # Rotas que não precisam de autenticação
    public_routes = ['/auth/login', '/auth/logout', '/static/', '/favicon.ico']
    
    # Verificar se a rota atual está na lista de rotas públicas
    for route in public_routes:
        if request.path.startswith(route):
            return None
    
    # Verificar se o usuário está autenticado
    if 'user_id' not in session:
        if request.path != '/auth/login':
            flash('Por favor, faça login para acessar o sistema.', 'warning')
            return redirect(url_for('auth.login'))

# Rota principal
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('receitas.listar'))
    return redirect(url_for('auth.login'))

# Rota para servir arquivos estáticos
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        return "Arquivo não encontrado", 404

# Manipulador de erro 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Manipulador de erro 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
