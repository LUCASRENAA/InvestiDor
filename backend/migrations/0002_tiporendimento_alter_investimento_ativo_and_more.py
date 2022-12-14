# Generated by Django 4.1.2 on 2022-11-05 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoRendimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='investimento',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='investimentorendimento',
            name='tipo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backend.tiporendimento'),
            preserve_default=False,
        ),
    ]
