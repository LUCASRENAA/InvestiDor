# Generated by Django 4.1.2 on 2022-11-13 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_tipoinvestimentosemideiadenome'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoinvestimentosemideiadenome',
            name='variavel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backend.variavel'),
            preserve_default=False,
        ),
    ]