from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from src.routes.auth import login_required
from datetime import datetime

receitas_bp = Blueprint('receitas', __name__)

# Configuração dos limites de medicamentos por tipo de receita
LIMITES_MEDICAMENTOS = {
    'Notificação de Receita A': 1,
    'Notificação de Receita B': 1,
    'Receita de Controle Especial': 3,
    'Antimicrobiano': 3
}

# Dados simulados de receitas para demonstração
# Em produção, estes dados viriam do banco de dados
receitas = [
    {
        'id': 1,
        'tipo_receita': 'Notificação de Receita B',
        'numero_notificacao': 'B1234567',
        'data_emissao': '2025-05-10',
        'data_dispensacao': '2025-05-19',
        'prescritor_nome': 'Dr. Carlos Silva',
        'prescritor_registro': 'CRM-RJ 12345',
        'prescritor_uf': 'RJ',
        'paciente_nome': 'Maria Oliveira',
        'paciente_endereco': 'Rua das Flores, 123 - Rio de Janeiro/RJ',
        'farmaceutico': 'Rodrigo',
        'status': 'aprovada',
        'medicamentos': [
            {
                'nome': 'Rivotril',
                'principio_ativo': 'Clonazepam',
                'concentracao': '2mg',
                'posologia': '1 comprimido à noite',
                'quantidade': '30 comprimidos',
                'duracao_tratamento': '30 dias'
            }
        ]
    },
    {
        'id': 2,
        'tipo_receita': 'Receita de Controle Especial',
        'numero_notificacao': '',
        'data_emissao': '2025-05-15',
        'data_dispensacao': '2025-05-19',
        'prescritor_nome': 'Dra. Ana Beatriz',
        'prescritor_registro': 'CRM-RJ 54321',
        'prescritor_uf': 'RJ',
        'paciente_nome': 'João Santos',
        'paciente_endereco': 'Av. Brasil, 500 - Rio de Janeiro/RJ',
        'farmaceutico': 'Rodrigo',
        'status': 'aprovada',
        'medicamentos': [
            {
                'nome': 'Amoxil',
                'principio_ativo': 'Amoxicilina',
                'concentracao': '500mg',
                'posologia': '1 cápsula de 8 em 8 horas',
                'quantidade': '21 cápsulas',
                'duracao_tratamento': '7 dias'
            }
        ]
    },
    {
        'id': 3,
        'tipo_receita': 'Notificação de Receita A',
        'numero_notificacao': 'A9876543',
        'data_emissao': '2025-05-01',
        'data_dispensacao': '2025-05-18',
        'prescritor_nome': 'Dr. Roberto Mendes',
        'prescritor_registro': 'CRM-RJ 98765',
        'prescritor_uf': 'RJ',
        'paciente_nome': 'Pedro Almeida',
        'paciente_endereco': 'Rua Visconde de Pirajá, 595 - Rio de Janeiro/RJ',
        'farmaceutico': 'Rodrigo',
        'status': 'rejeitada',
        'motivo_rejeicao': 'Receita com data de emissão superior a 30 dias',
        'medicamentos': [
            {
                'nome': 'Ritalina',
                'principio_ativo': 'Metilfenidato',
                'concentracao': '10mg',
                'posologia': '1 comprimido pela manhã',
                'quantidade': '30 comprimidos',
                'duracao_tratamento': '30 dias'
            }
        ]
    }
]

@receitas_bp.route('/listar')
@login_required
def listar():
    return render_template('receitas/listar.html', receitas=receitas)

@receitas_bp.route('/detalhes/<int:receita_id>')
@login_required
def detalhes(receita_id):
    receita = next((r for r in receitas if r['id'] == receita_id), None)
    
    if not receita:
        flash('Receita não encontrada.', 'danger')
        return redirect(url_for('receitas.listar'))
    
    return render_template('receitas/detalhes.html', receita=receita)

@receitas_bp.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        # Obter dados do formulário
        tipo_receita = request.form.get('tipo_receita')
        data_emissao = request.form.get('data_emissao')
        
        # Contar medicamentos no formulário
        medicamentos_count = 1  # Sempre tem pelo menos um medicamento
        medicamentos_list = []
        
        # Adicionar o primeiro medicamento
        medicamentos_list.append({
            'nome': request.form.get('medicamento'),
            'principio_ativo': request.form.get('principio_ativo'),
            'concentracao': request.form.get('concentracao'),
            'posologia': request.form.get('posologia'),
            'quantidade': request.form.get('quantidade'),
            'duracao_tratamento': request.form.get('duracao_tratamento')
        })
        
        # Verificar medicamentos adicionais
        i = 2
        while f'medicamento_{i}' in request.form and request.form.get(f'medicamento_{i}'):
            medicamentos_count += 1
            medicamentos_list.append({
                'nome': request.form.get(f'medicamento_{i}'),
                'principio_ativo': request.form.get(f'principio_ativo_{i}', ''),
                'concentracao': request.form.get(f'concentracao_{i}', ''),
                'posologia': request.form.get(f'posologia_{i}', ''),
                'quantidade': request.form.get(f'quantidade_{i}', ''),
                'duracao_tratamento': request.form.get(f'duracao_tratamento_{i}', '')
            })
            i += 1
        
        # Validar quantidade de medicamentos por tipo de receita
        if tipo_receita in LIMITES_MEDICAMENTOS and medicamentos_count > LIMITES_MEDICAMENTOS[tipo_receita]:
            flash(f'Receita rejeitada: Excede o limite de {LIMITES_MEDICAMENTOS[tipo_receita]} medicamento(s) para {tipo_receita}. Conforme legislação vigente, este tipo de receita tem limite específico de medicamentos.', 'danger')
            return render_template('receitas/cadastrar.html')
        
        # Verificar validade da receita
        data_emissao_obj = datetime.strptime(data_emissao, '%Y-%m-%d')
        data_atual = datetime.now()
        dias_diferenca = (data_atual - data_emissao_obj).days
        
        # Validações específicas por tipo de receita
        if tipo_receita == 'Notificação de Receita A' and dias_diferenca > 30:
            flash('Receita com data de emissão superior a 30 dias. Conforme Portaria 344/98, receitas da Lista A têm validade de 30 dias.', 'danger')
            return render_template('receitas/cadastrar.html')
            
        elif tipo_receita == 'Notificação de Receita B' and dias_diferenca > 30:
            flash('Receita com data de emissão superior a 30 dias. Conforme Portaria 344/98, receitas da Lista B têm validade de 30 dias.', 'danger')
            return render_template('receitas/cadastrar.html')
            
        elif tipo_receita == 'Receita de Controle Especial':
            # Verificar se algum medicamento é antimicrobiano
            is_antimicrobiano = False
            for med in medicamentos_list:
                if 'antimicrobiano' in med['nome'].lower() or 'antibiótico' in med['nome'].lower():
                    is_antimicrobiano = True
                    break
            
            if is_antimicrobiano and dias_diferenca > 10:
                flash('Receita com data de emissão superior a 10 dias. Conforme RDC 471/2021, receitas de antimicrobianos têm validade de 10 dias.', 'danger')
                return render_template('receitas/cadastrar.html')
            elif dias_diferenca > 30:
                flash('Receita com data de emissão superior a 30 dias. Conforme Portaria 344/98, Receitas de Controle Especial têm validade de 30 dias.', 'danger')
                return render_template('receitas/cadastrar.html')
        
        # Criar nova receita
        nova_receita = {
            'id': len(receitas) + 1,
            'tipo_receita': tipo_receita,
            'numero_notificacao': request.form.get('numero_receita', ''),
            'data_emissao': data_emissao,
            'data_dispensacao': request.form.get('data_dispensacao'),
            'prescritor_nome': request.form.get('prescritor_nome'),
            'prescritor_registro': request.form.get('prescritor_crm'),
            'prescritor_uf': 'RJ',  # Fixo para o estado do RJ conforme requisito
            'paciente_nome': request.form.get('paciente_nome'),
            'paciente_endereco': request.form.get('paciente_endereco', ''),
            'farmaceutico': session.get('nome', 'Rodrigo'),  # Usuário logado
            'status': 'aprovada',
            'medicamentos': medicamentos_list
        }
        
        # Adicionar à lista de receitas (em produção, seria salvo no banco de dados)
        receitas.append(nova_receita)
        
        # Se passou por todas as validações
        flash(f'Receita cadastrada com sucesso! Contém {medicamentos_count} medicamento(s).', 'success')
        return redirect(url_for('receitas.listar'))
    
    return render_template('receitas/cadastrar.html')

@receitas_bp.route('/validar/<int:receita_id>', methods=['GET', 'POST'])
@login_required
def validar(receita_id):
    receita = next((r for r in receitas if r['id'] == receita_id), None)
    
    if not receita:
        flash('Receita não encontrada.', 'danger')
        return redirect(url_for('receitas.listar'))
    
    if request.method == 'POST':
        status = request.form.get('status')
        motivo_rejeicao = request.form.get('motivo_rejeicao', '')
        
        # Em produção, atualizaria o status no banco de dados
        receita['status'] = status
        if status == 'rejeitada':
            receita['motivo_rejeicao'] = motivo_rejeicao
        
        flash('Status da receita atualizado com sucesso!', 'success')
        return redirect(url_for('receitas.detalhes', receita_id=receita_id))
    
    return render_template('receitas/validar.html', receita=receita)
