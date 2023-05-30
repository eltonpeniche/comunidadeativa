from datetime import datetime, timezone
from time import sleep

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import LoginForm, PostForm, RelatorioForm
from .models import Categoria_Post, Post, Relatorio, Tag
from .utils import utils


def index(request):
     posts_recentes = Post.objects.all().order_by('-id')[:3]
     return render(request, 'pages/index.html', {'posts': posts_recentes})

def contato(request):
     return render(request, 'pages/contato.html')

def perguntas_frequentes(request):
     return render(request, 'pages/perguntas-frequentes.html')

def programas(request):
     return render(request, 'pages/programas.html')


def nossos_enderecos(request):
     return render(request, 'pages/nossos-enderecos.html')

def blog(request):
     posts = Post.objects.all().order_by('-id')
     return render(request, 'pages/noticias/blog.html', {'posts': posts })

def post_detalhes(request, slug):
     if request.method == 'GET':
          post = Post.objects.get(slug=slug)
          postado_ha = utils.calcular_diferenca_datas(post.atualizado_em, datetime.now(timezone.utc))
          posts_recentes = Post.objects.exclude(id=post.id).order_by('-id')[:5]
          
          #Categorias
          
          categorias_posts = Categoria_Post.objects.all()
          categorias_e_qtd_post = []
          for categoria in categorias_posts:
               qtd_posts = categoria.post_set.count()
               if qtd_posts > 0:
                    categorias_e_qtd_post.append([categoria.nome, qtd_posts])
          
          categorias_e_qtd_post = sorted(categorias_e_qtd_post,key=lambda x: x[1],reverse= True)[:6]
          #TAGs
          tags = Tag.objects.all()[:12]

          contexto = {  
               'post': post, 
               'postado_ha': postado_ha, 
               'categorias_posts': categorias_e_qtd_post,
               'tags':tags,
               'posts_recentes': posts_recentes
               }
          return render(request, 'pages/noticias/blog-details.html', contexto)
     
def post_novo(request):
     if request.method == 'GET':
          form = PostForm()
          contexto = {  
                    'form': form
               }
          return render(request, 'pages/noticias/blog-details-edit.html', contexto)
     else:
          
          form = PostForm(request.POST, request.FILES)
          if form.is_valid():
               post = form.save(commit=False)
               post.autor = request.user
               post.save()
               form.save_m2m()
               messages.success(request, "Posto salvo com sucesso")
               return  redirect(reverse('amazoncred:blog'))
          
          return render(request, 'pages/noticias/blog-details-edit.html', {'form':form})
          
          

@login_required
def logout(request):
    auth.logout(request)
    print("Logout realizado com sucesso")
    return redirect(reverse('amazoncred:index'))

def login(request):

     if request.user.is_authenticated:
        return redirect(reverse('amazoncred:index'))

     if request.method == 'POST':
          form = LoginForm(request.POST)
          if form.is_valid():
               login = form['login'].value().lower().strip()
               senha = form['senha'].value()
               usuario = auth.authenticate(
                    request,
                    username=login,
                    password=senha
               )
               if usuario is not None:
                    auth.login(request, usuario)
                    next = request.GET.get("next", None)
                    if next is not None:
                         return redirect(next)
                    return redirect('amazoncred:login')

            
          messages.error(request, "Login ou Senha incorretos")
          return render(request, 'pages/login/login-page.html', {'form': form})
     else:
          parametro = request.GET.get('parametro')
          formLogin = LoginForm()
          contexto = {
               'form': formLogin
          }
     template_name = 'partials/login/_login_partial.html' if parametro else 'pages/login/login-page.html'
               
     return render(request, template_name, contexto)

def pesquisar_post_htmx(request):
     termo_pesquisado = request.POST.get('q', '').strip()
     print(termo_pesquisado)
     if not termo_pesquisado:
          return render(request, 'partials/noticias/_list_posts_search.html')

     posts = Post.objects.filter( 
                    Q(titulo__icontains = termo_pesquisado)
                    ).order_by('-id')[:11]
     return render(request, 'partials/noticias/_list_posts_search.html', {'posts': posts })

def pesquisar_post(request):
     termo_pesquisado = request.POST.get('q', '').strip()
     print(termo_pesquisado)
     if not termo_pesquisado:
          return render(request, 'partials/noticias/_list_posts_search.html')

     posts = Post.objects.filter( 
                    Q(titulo__icontains = termo_pesquisado)
                    ).order_by('-id')[:11]
     
     return render(request, 'pages/noticias/blog.html', {'posts': posts })


def transparencia(request):

     return render(request, 'pages/transparencia/transparencia.html')

def tab(request):

     tipo = request.GET.get('tipo')
     relatorios = Relatorio.objects.filter(tipo_relatorio = tipo.upper()).order_by('-id')
     contexto = {   'obj_list': relatorios,
                    'tipo': tipo
               }

     return render(request, 'pages/transparencia/partials/_lista_relatorios.html', contexto)


def novo_relatorio(request):
     
     if request.method == "POST":
          tipo = request.POST.get('tipo')
          form = RelatorioForm(request.POST, request.FILES)
          if form.is_valid():
               relatorio = form.save(commit=False)
               relatorio.tipo_relatorio = tipo.upper()
               relatorio.save()
          demonstracoes_contabeis = Relatorio.objects.filter(tipo_relatorio = tipo.upper()).order_by('-id')
          
          return render(request, 'pages/transparencia/partials/_lista_relatorios.html',{'obj_list': demonstracoes_contabeis})
     else:
          tipo = request.GET.get('tipo')
          form = RelatorioForm()
          contexto = {'form': form,
                      'tipo': tipo}
          return render(request, 'pages/transparencia/partials/_novo_relatorio.html', contexto)

"""
class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': page_title,
        })

        return ctx

"""