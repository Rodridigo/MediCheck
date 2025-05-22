from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from src.routes.auth import login_required
from datetime import datetime, timedelta
import calendar

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/')
@login_required
def index():
    return render_template('relatorios/index.html')

@relatorios_bp.route('/diario', methods=['GET', 'POST'])
@login_required
def diario():
    # Simulação de dados para relatório diário
    data_atual = datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        data_selecionada = request.form.get('data')
    else:
        data_selecionada = data_atual
    
    # Dados simulados para demonstração
    receitas_diarias = [
        {
            'id': 1,
            'tipo_receita': 'Notificação de Receita B',
            'medicamento': 'Rivotril 2mg',
            'paciente': 'Maria Oliveira',
            'prescritor': 'Dr. Carlos Silva',
            'status': 'aprovada',
            'hora': '09:15'
        },
        {
            'id': 2,
            'tipo_receita': 'Receita de Controle Especial',
            'medicamento': 'Amoxil 500mg',
            'paciente': 'João Santos',
            'prescritor': 'Dra. Ana Beatriz',
            'status': 'aprovada',
            'hora': '10:30'
        },
        {
            'id': 3,
            'tipo_receita': 'Notificação de Receita A',
            'medicamento': 'Ritalina 10mg',
            'paciente': 'Pedro Almeida',
            'prescritor': 'Dr. Roberto Mendes',
            'status': 'rejeitada',
            'hora': '14:45'
        }
    ]
    
    resumo = {
        'total': len(receitas_diarias),
        'aprovadas': len([r for r in receitas_diarias if r['status'] == 'aprovada']),
        'rejeitadas': len([r for r in receitas_diarias if r['status'] == 'rejeitada']),
        'controlados': len([r for r in receitas_diarias if r['tipo_receita'] in ['Notificação de Receita A', 'Notificação de Receita B']]),
        'antimicrobianos': len([r for r in receitas_diarias if 'Amoxil' in r['medicamento']])
    }
    
    return render_template('relatorios/diario.html', 
                          receitas=receitas_diarias, 
                          resumo=resumo, 
                          data_selecionada=data_selecionada,
                          data_atual=data_atual)

@relatorios_bp.route('/mensal', methods=['GET', 'POST'])
@login_required
def mensal():
    # Simulação de dados para relatório mensal
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    if request.method == 'POST':
        mes = int(request.form.get('mes', mes_atual))
        ano = int(request.form.get('ano', ano_atual))
    else:
        mes = mes_atual
        ano = ano_atual
    
    # Dados simulados para demonstração
    dados_mensais = {
        'total_receitas': 87,
        'aprovadas': 78,
        'rejeitadas': 9,
        'por_tipo': {
            'Notificação de Receita A': 15,
            'Notificação de Receita B': 42,
            'Receita de Controle Especial': 30
        },
        'por_medicamento': [
            {'nome': 'Rivotril', 'quantidade': 28},
            {'nome': 'Ritalina', 'quantidade': 15},
            {'nome': 'Amoxil', 'quantidade': 12},
            {'nome': 'Gardenal', 'quantidade': 10},
            {'nome': 'Ciprofloxacino', 'quantidade': 8}
        ],
        'por_dia': [3, 5, 2, 4, 3, 0, 0, 4, 5, 3, 2, 4, 3, 0, 0, 5, 4, 3, 5, 4, 3, 0, 0, 4, 5, 3, 4, 3, 2, 0]
    }
    
    meses = [
        {'numero': 1, 'nome': 'Janeiro'},
        {'numero': 2, 'nome': 'Fevereiro'},
        {'numero': 3, 'nome': 'Março'},
        {'numero': 4, 'nome': 'Abril'},
        {'numero': 5, 'nome': 'Maio'},
        {'numero': 6, 'nome': 'Junho'},
        {'numero': 7, 'nome': 'Julho'},
        {'numero': 8, 'nome': 'Agosto'},
        {'numero': 9, 'nome': 'Setembro'},
        {'numero': 10, 'nome': 'Outubro'},
        {'numero': 11, 'nome': 'Novembro'},
        {'numero': 12, 'nome': 'Dezembro'}
    ]
    
    anos = list(range(ano_atual - 5, ano_atual + 1))
    
    return render_template('relatorios/mensal.html', 
                          dados=dados_mensais, 
                          mes_selecionado=mes,
                          ano_selecionado=ano,
                          meses=meses,
                          anos=anos)

@relatorios_bp.route('/medicamentos')
@login_required
def medicamentos():
    # Simulação de dados para relatório de medicamentos
    dados_medicamentos = [
        {
            'nome': 'Rivotril',
            'principio_ativo': 'Clonazepam',
            'lista': 'B1',
            'total_dispensado': 145,
            'receitas': 28
        },
        {
            'nome': 'Ritalina',
            'principio_ativo': 'Metilfenidato',
            'lista': 'A3',
            'total_dispensado': 78,
            'receitas': 15
        },
        {
            'nome': 'Amoxil',
            'principio_ativo': 'Amoxicilina',
            'lista': 'Antimicrobiano',
            'total_dispensado': 252,
            'receitas': 12
        },
        {
            'nome': 'Gardenal',
            'principio_ativo': 'Fenobarbital',
            'lista': 'B1',
            'total_dispensado': 60,
            'receitas': 10
        },
        {
            'nome': 'Ciprofloxacino',
            'principio_ativo': 'Ciprofloxacino',
            'lista': 'Antimicrobiano',
            'total_dispensado': 168,
            'receitas': 8
        }
    ]
    
    resumo_listas = {
        'A': 15,
        'B': 38,
        'C': 22,
        'Antimicrobianos': 20
    }
    
    return render_template('relatorios/medicamentos.html', 
                          medicamentos=dados_medicamentos,
                          resumo_listas=resumo_listas)
