# Generated by Django 4.1.2 on 2022-11-12 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_investimento_valor_atual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculofuturo',
            name='investimento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.investimento'),
        ),
    ]
