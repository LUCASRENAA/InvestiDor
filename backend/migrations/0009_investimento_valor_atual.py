# Generated by Django 4.1.2 on 2022-11-12 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_calculofuturo_investimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='investimento',
            name='valor_atual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
