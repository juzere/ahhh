# Generated by Django 5.0.1 on 2024-02-02 12:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aaaa', '0003_alter_produto_imagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='DispositivoMedicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dado', models.CharField(max_length=255)),
                ('produto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dispositivo', to='aaaa.produto')),
            ],
        ),
    ]