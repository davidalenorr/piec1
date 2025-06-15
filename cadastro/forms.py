from django import forms

class ProfessorForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome do Professor')
    email = forms.EmailField(label='Email do Professor')

class DisciplinaForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome da Disciplina')
    professor = forms.CharField(max_length=100, label='Professor Responsável')

class AlunoForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome do Aluno')
    matricula = forms.CharField(max_length=20, label='Matrícula do Aluno')