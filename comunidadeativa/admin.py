from django.contrib import admin

from comunidadeativa.models import (Categoria_Post, Contato, Post, Relatorio,
                                    Tag)

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo','autor','criado_em'
,'atualizado_em', 'publicado'   )
    list_display_links = ('id', 'titulo', 'autor','criado_em'
,'atualizado_em' )
    ordering = ('-id',)
    prepopulated_fields = {
        "slug": ('titulo',)
    }

    list_per_page = 25
    list_editable = 'publicado',
    autocomplete_fields = ('tags','categoria')


@admin.register(Categoria_Post)
class CategoriaPostAdmin(admin.ModelAdmin):
    search_fields = 'id', 'nome',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'nome', 'slug',
    list_display_links = 'id', 'slug',
    search_fields = 'id', 'slug', 'nome',
    list_per_page = 25
    list_editable = 'nome',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('nome',),
    }

# TRANSPARENCIA


@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = 'id', 'titulo'
    list_display_links = 'id', 'titulo',
    search_fields = 'id', 'titulo',
    list_per_page = 25
    ordering = '-id',

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = 'id', 'nome', 'assunto', 'email'
    list_display_links = 'id', 'nome', 'assunto', 'email'
    search_fields = 'id', 'nome','email'
    list_per_page = 25
    ordering = '-id',