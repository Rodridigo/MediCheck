from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from src.routes.auth import login_required

medicamentos_bp = Blueprint('medicamentos', __name__)

# Dados simulados de medicamentos para demonstração
# Em produção, estes dados viriam do banco de dados
medicamentos_controlados = [
    {
        'id': 1,
        'nome_comercial': 'Rivotril',
        'principio_ativo': 'Clonazepam',
        'concentracao': '2mg',
        'forma_farmaceutica': 'Comprimido',
        'lista_portaria': 'B1',
        'tipo_receituario': 'Notificação de Receita B',
        'cor_receituario': 'Azul',
        'validade_receita_dias': 30,
        'quantidade_maxima': '60 dias de tratamento',
        'dose_maxima_diaria': '20mg',
        'retencao_receita': True
    },
    {
        'id': 2,
        'nome_comercial': 'Ritalina',
        'principio_ativo': 'Metilfenidato',
        'concentracao': '10mg',
        'forma_farmaceutica': 'Comprimido',
        'lista_portaria': 'A3',
        'tipo_receituario': 'Notificação de Receita A',
        'cor_receituario': 'Amarela',
        'validade_receita_dias': 30,
        'quantidade_maxima': '30 dias de tratamento',
        'dose_maxima_diaria': '60mg',
        'retencao_receita': True
    },
    {
        'id': 3,
        'nome_comercial': 'Amoxil',
        'principio_ativo': 'Amoxicilina',
        'concentracao': '500mg',
        'forma_farmaceutica': 'Cápsula',
        'lista_portaria': 'Antimicrobiano',
        'tipo_receituario': 'Receita de Controle Especial',
        'cor_receituario': 'Branca',
        'validade_receita_dias': 10,
        'quantidade_maxima': '90 dias de tratamento',
        'dose_maxima_diaria': '4g',
        'retencao_receita': True
    },
    {
        'id': 4,
        'nome_comercial': 'Gardenal',
        'principio_ativo': 'Fenobarbital',
        'concentracao': '100mg',
        'forma_farmaceutica': 'Comprimido',
        'lista_portaria': 'B1',
        'tipo_receituario': 'Notificação de Receita B',
        'cor_receituario': 'Azul',
        'validade_receita_dias': 30,
        'quantidade_maxima': '60 dias de tratamento',
        'dose_maxima_diaria': '300mg',
        'retencao_receita': True
    },
    {
        'id': 5,
        'nome_comercial': 'Ciprofloxacino',
        'principio_ativo': 'Ciprofloxacino',
        'concentracao': '500mg',
        'forma_farmaceutica': 'Comprimido',
        'lista_portaria': 'Antimicrobiano',
        'tipo_receituario': 'Receita de Controle Especial',
        'cor_receituario': 'Branca',
        'validade_receita_dias': 10,
        'quantidade_maxima': '90 dias de tratamento',
        'dose_maxima_diaria': '1,5g',
        'retencao_receita': True
    }
]

@medicamentos_bp.route('/consultar', methods=['GET', 'POST'])
@login_required
def consultar():
    resultados = []
    termo_busca = ''
    
    if request.method == 'POST':
        termo_busca = request.form.get('termo_busca', '').lower()
        
        if termo_busca:
            resultados = [
                med for med in medicamentos_controlados 
                if termo_busca in med['nome_comercial'].lower() or 
                   termo_busca in med['principio_ativo'].lower()
            ]
            
            if not resultados:
                flash('Nenhum medicamento encontrado com o termo informado.', 'warning')
    
    return render_template('medicamentos/consultar.html', 
                          resultados=resultados, 
                          termo_busca=termo_busca)

@medicamentos_bp.route('/detalhes/<int:medicamento_id>')
@login_required
def detalhes(medicamento_id):
    medicamento = next((med for med in medicamentos_controlados if med['id'] == medicamento_id), None)
    
    if not medicamento:
        flash('Medicamento não encontrado.', 'danger')
        return redirect(url_for('medicamentos.consultar'))
    
    return render_template('medicamentos/detalhes.html', medicamento=medicamento)
