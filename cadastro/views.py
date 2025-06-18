from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ProfessorForm, DisciplinaForm, AlunoForm
import json
import os
import re

#Temporario
TEMP_STORAGE_FILE = 'temp_storage/dados_temp.json'

def home(request):
    return render(request, 'cadastro/home.html')
#Carrega as disciplinas do professor logado e exibe na página inicial
def index(request):
    data = load_data()
    cpf_professor = request.session.get('usuario')
    disciplinas = [d for d in data.get('disciplinas', []) if d.get('cpf_professor') == cpf_professor]
    return render(request, 'cadastro/index.html', {'disciplinas': disciplinas})

def load_data():
    if os.path.exists(TEMP_STORAGE_FILE):
        with open(TEMP_STORAGE_FILE, 'r') as file:
            return json.load(file)
    return {'usuarios': [], 'professores': [], 'disciplinas': [], 'alunos': []}
#Para salvar
def save_data(data):
    with open(TEMP_STORAGE_FILE, 'w') as file:
        json.dump(data, file)
# FLogin         
def login_view(request):
    error = None
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        data = load_data()
        usuario = next((u for u in data.get('usuarios', []) if u.get('cpf') == cpf and u.get('senha') == senha), None)
        if usuario:
            request.session['usuario'] = usuario['cpf']
            request.session['nome_completo'] = usuario['nome']
            return redirect('index')
        else:
            error = 'CPF ou senha inválidos!'
    return render(request, 'cadastro/login.html', {'error': error})

def cadastro_usuario(request):
    error = None
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        rg = request.POST.get('rg')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        data = load_data()
        if len(cpf) != 11 or not cpf.isdigit():
            error = 'CPF deve conter exatamente 11 dígitos numéricos.'
        elif len(rg) != 7 or not rg.isdigit():
            error = 'RG deve conter exatamente 7 dígitos numéricos.'
        elif any(u.get('cpf') == cpf for u in data.get('usuarios', [])):
            error = 'Usuário já cadastrado com esse CPF!'
        else:
            data.setdefault('usuarios', []).append({
                'cpf': cpf,
                'nome': nome,
                'rg': rg,
                'email': email,
                'senha': senha
            })
            save_data(data)
            return redirect('login')
    return render(request, 'cadastro/cadastro_usuario.html', {'error': error})

def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            data = load_data()
            data['professores'].append(form.cleaned_data)
            save_data(data)
            return redirect('cadastrar_professor')
    else:
        form = ProfessorForm()
    return render(request, 'cadastro/cadastrar_professor.html', {'form': form})

def cadastrar_disciplina(request):
    sucesso = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        ano = request.POST.get('ano')
        data = load_data()
        cpf_professor = request.session.get('usuario')
        data.setdefault('disciplinas', []).append({
            'nome': nome,
            'ano': ano,
            'cpf_professor': cpf_professor,
            'alunos': []
        })
        save_data(data)
        sucesso = 'Disciplina cadastrada com sucesso!'
    return render(request, 'cadastro/cadastrar_disciplina.html', {'sucesso': sucesso})

def cadastrar_aluno(request):
    sucesso = None
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        nome = request.POST.get('nome')
        data = load_data()
        cpf_professor = request.session.get('usuario')
        if len(matricula) != 11 or not matricula.isdigit():
            sucesso = 'A matrícula deve conter exatamente 11 dígitos numéricos.'
        elif any(char.isdigit() for char in nome):
            sucesso = 'O nome não pode conter números.'
        elif any(a['matricula'] == matricula and a.get('cpf_professor') == cpf_professor for a in data.get('alunos', [])):
            sucesso = 'Já existe um aluno com essa matrícula!'
        else:
            data.setdefault('alunos', []).append({
                'matricula': matricula,
                'nome': nome,
                'cpf_professor': cpf_professor
            })
            save_data(data)
            sucesso = 'Aluno cadastrado com sucesso!'
    return render(request, 'cadastro/cadastrar_aluno.html', {'sucesso': sucesso})
# Detalhe da disciplina
def detalhe_disciplina(request, disciplina_id):
    data = load_data()
    cpf_professor = request.session.get('usuario')
    disciplinas = [d for d in data.get('disciplinas', []) if d.get('cpf_professor') == cpf_professor]
    if 0 <= disciplina_id < len(disciplinas):
        disciplina = disciplinas[disciplina_id]
        alunos = [a for a in data.get('alunos', []) if a.get('cpf_professor') == cpf_professor]
        sucesso = None

        if 'alunos' not in disciplina:
            disciplina['alunos'] = []
        if request.method == 'POST':
            matricula = request.POST.get('aluno_matricula')
            if matricula and matricula not in [a['matricula'] for a in disciplina['alunos']]:
                aluno = next((a for a in alunos if a['matricula'] == matricula), None)
                if aluno:
                    disciplina['alunos'].append({
                        'matricula': aluno['matricula'],
                        'nome': aluno['nome'],
                        'nota_1va': None,
                        'nota_2va': None,
                        'nota_3va': None,
                        'nota_final': None
                    })
                    save_data(data)
                    sucesso = 'Aluno adicionado com sucesso!'
        matriculas_na_disciplina = [a['matricula'] for a in disciplina['alunos']]
        alunos_disponiveis = [a for a in alunos if a['matricula'] not in matriculas_na_disciplina]
        alunos_disciplina = []
        for a in disciplina['alunos']:
            notas = [a.get('nota_1va'), a.get('nota_2va'), a.get('nota_3va'), a.get('nota_final')]
            notas_validas = [n for n in notas[:2] if n is not None]
            media_geral = None
            situacao = None
            if len(notas_validas) == 2:
                media = sum(notas_validas) / 2
                if media >= 7:
                    media_geral = media
                    situacao = "APV"
                elif a.get('nota_3va') is not None:
                    notas_3 = notas_validas + [a.get('nota_3va')]
                    media_3 = sum(n for n in notas_3 if n is not None) / 3
                    if media_3 >= 7:
                        media_geral = media_3
                        situacao = "APV"
                    elif a.get('nota_final') is not None:
                        notas_final = notas_3 + [a.get('nota_final')]
                        media_final = sum(n for n in notas_final if n is not None) / 4
                        media_geral = media_final
                        situacao = "APV" if media_final >= 7 else "RPV"
                    else:
                        situacao = None
                elif a.get('nota_final') is not None:
                    notas_final = notas_validas + [a.get('nota_final')]
                    media_final = sum(n for n in notas_final if n is not None) / 3
                    media_geral = media_final
                    situacao = "APV" if media_final >= 7 else "RPV"
                else:
                    situacao = None
            alunos_disciplina.append({
                **a,
                'media_geral': media_geral,
                'situacao': situacao
            })
        return render(request, 'cadastro/detalhe_disciplina.html', {
            'disciplina': disciplina,
            'alunos_disponiveis': alunos_disponiveis,
            'alunos_disciplina': alunos_disciplina,
            'sucesso': sucesso
        })
    else:
        return render(request, 'cadastro/detalhe_disciplina.html', {'disciplina': None})
# Lista de alunos do professor logado
def lista_alunos(request):
    data = load_data()
    cpf_professor = request.session.get('usuario')
    alunos = sorted(
        [a for a in data.get('alunos', []) if a.get('cpf_professor') == cpf_professor],
        key=lambda x: x['nome'].lower()
    )
    return render(request, 'cadastro/lista_alunos.html', {'alunos': alunos})

def logout_view(request):
    request.session.flush()
    return redirect('home')