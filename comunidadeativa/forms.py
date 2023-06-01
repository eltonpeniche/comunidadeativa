import re

from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_select2 import forms as s2forms
from django_select2.forms import Select2MultipleWidget, Select2Widget

from comunidadeativa.models import Categoria_Post, Contato, Relatorio, Tag

from .models import Post


# ModelSelect2MultipleWidget
# 
class TagWidget(s2forms.ModelSelect2TagWidget):
    search_fields = [
        "nome__icontains",
    ]

    queryset = Tag.objects.all()

    def value_from_datadict(self, data, files, name):
        
        values = list(set(super().value_from_datadict(data, files, name)))
        
        cleaned_values = []
        for value in values:
            if value.isnumeric():
                cleaned_values.append(value)
            else:
                obj,_ = Tag.objects.get_or_create(nome=value)
                cleaned_values.append(obj.id)
        
        
        return cleaned_values

class CategoriaWidget(s2forms.ModelSelect2TagWidget):
    search_fields = [
        "nome__icontains",
    ]

    queryset = Categoria_Post.objects.all()

    def value_from_datadict(self, data, files, name):
        
        values = list(set(super().value_from_datadict(data, files, name)))
        
        cleaned_values = []
        for categoria in values:
            if categoria.isnumeric():
                cleaned_values.append(categoria)
            else:
                obj,_ = Categoria_Post.objects.get_or_create(nome=categoria)
                cleaned_values.append(obj.id)
        
        
        return cleaned_values

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'publicado', 'capa_post', 'categoria', 'tags']

        widgets = {
            'tags': TagWidget,
            'categoria': CategoriaWidget
        }


#Formulario de autenticação de usuários
class LoginForm(forms.Form):
    login = forms.CharField(
        label=False,
        max_length=100,
        required=True,
        widget= forms.TextInput(attrs={'placeholder':'Login', 'class':'form-control' }))
    
    senha = forms.CharField(
        label=False,
        max_length=100,
        required=True,
        widget = forms.PasswordInput(attrs={'placeholder':'Senha', 'class':'form-control'})
    )

#TRANSPARENCIA
class RelatorioForm(forms.ModelForm):

    class Meta:
        model = Relatorio
        fields = ['titulo', 'arquivo', ]


#Fale Conosco | contato
class ContatoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome"].widget.attrs.update({"class": "form-control","placeholder": "Nome"})
        self.fields["email"].widget.attrs.update({"class": "form-control","placeholder": "email"})
        self.fields["assunto"].widget.attrs.update({"class": "form-control","placeholder": "assunto"})
        self.fields["mensagem"].widget.attrs.update({"class": "form-control","placeholder": "menssagem"})

    class Meta:
        model = Contato
        fields = ['nome', 'email', 'assunto', 'mensagem']
        
        widgets = {
            'tags': TagWidget,
            'categoria': CategoriaWidget
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        
        if not re.fullmatch(regex, email):
            raise ValidationError("Endereço de e-mail inválido")
            
        return email