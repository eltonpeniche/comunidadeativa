# Generated by Django 4.2.1 on 2023-05-30 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comunidadeativa", "0003_alter_demonstracoescontabeis_options_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DemonstracoesContabeis",
            new_name="Relatorio",
        ),
    ]
