from django import forms
from django.shortcuts import get_object_or_404
from django_select2 import forms as s2forms
from django_select2.forms import Select2MultipleWidget, Select2Widget

from comunidadeativa.models import Categoria_Post, Tag

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
        label_attrs={'class': 'meu-campo-label'}

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
