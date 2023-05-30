
 



from django.urls import path

from comunidadeativa import views

app_name = 'amazoncred'

urlpatterns = [
     path('', views.index, name='index'),
     path('contato/', views.contato, name='contato'),
     path('perguntas-frequentes/', views.perguntas_frequentes, name='perguntas-frequentes'),
     path('programas/', views.programas, name='programas'),
     path('nossos-enderecos/', views.nossos_enderecos, name='nossos-enderecos'),
     path('noticias/', views.blog, name='blog'),
     path('noticias/post/novo' , views.post_novo, name='post_novo'),
     path('noticias/post/pesquisar/', views.pesquisar_post_htmx, name='pesquisar_post_htmx'),
     
     path('noticias/post/pesquisar/1/', views.pesquisar_post, name='pesquisar_post'),
     
     path('noticias/post/<slug:slug>' , views.post_detalhes, name='post-detalhes'),
     
     path('login' , views.login, name='login'),
     path('logout/', views.logout, name='logout'),

     path('transparencia/', views.transparencia, name='transparencia'),
     path('transparencia/tab/', views.tab, name='tab'),
     path('transparencia/novo_relatorio', views.novo_relatorio, name='novo_relatorio'),

     #path('blog/tags/<slug:slug>/', views.RecipeListViewTag.as_view(), name="tag"),


]


