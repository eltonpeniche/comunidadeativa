import os
import string
from random import SystemRandom

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Tag(models.Model):
    nome = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.nome}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Categoria_Post(models.Model):
    nome = models.CharField(max_length=65)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = _('Categoria Post')
        verbose_name_plural = _('Categorias Posts')
    
class Post(models.Model):

    titulo  = models.CharField(max_length=200, unique=True, verbose_name=_('Título')) 
    slug   = models.CharField(max_length=200, unique=True)
    autor   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    criado_em   = models.DateTimeField(auto_now_add=True)
    atualizado_em   = models.DateTimeField(auto_now=True)
    conteudo   = RichTextUploadingField()
    publicado = models.BooleanField(default = False)
    capa_post = models.ImageField(upload_to='fotos/%Y/%m/%d/', blank=True)

    categoria = models.ManyToManyField(Categoria_Post, blank=True, default='')

    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return f'Titulo = {self.titulo}'
    
    
    @staticmethod
    def resize_image(image, new_width=1024):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.titulo}-{rand_letters}')

        saved = super().save(*args, **kwargs)

        if self.capa_post:
            try:
                self.resize_image(self.capa_post, 1024)
            except FileNotFoundError:
                ...

        return saved
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


    
#- TRANSPARENCIA
class TIPO_RELATORIO(models.TextChoices):
    DEMONSTRATIVOS_CONTABEIS = 'DC', _('Demonstrativos Contábeis E Financeiros')
    TERMOS_PARCERIA = 'TM', _('Termos De Parceiros')
    CERTIDOES = 'CE', _('Certidões')
    Editais = 'ED', _('Editais')

class Relatorio(models.Model):
    titulo = models.CharField(max_length=200, unique=True, verbose_name=_('Título'))
    arquivo = models.FileField(upload_to='transparencia/dc/%Y/%m/%d/', blank=False, null=False)

    tipo_relatorio = models.CharField( max_length=2, choices=TIPO_RELATORIO.choices, blank=False, null=False, default='DC')

    class Meta:
        verbose_name = _('Relatório')
        verbose_name_plural = _('Relatórios')

#Fale Conosco | contato
class Contato(models.Model):
    nome = models.CharField(max_length=200 )
    email = models.CharField(max_length=200 )
    assunto = models.CharField(max_length=200)
    mensagem = models.TextField()