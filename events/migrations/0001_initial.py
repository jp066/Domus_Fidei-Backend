# Generated by Django 5.0.14 on 2025-06-21 13:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RetiroAcampamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_retiro', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('local', models.CharField(max_length=100)),
                ('numero_participantes', models.IntegerField(default=0)),
                ('limite_participantes', models.IntegerField(default=0)),
                ('custo', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('ativo', models.BooleanField(default=True)),
                ('logo', models.FileField(upload_to='midias_galeria/', verbose_name='Arquivo da Mídia')),
                ('coordenador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retiros_coordenados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
