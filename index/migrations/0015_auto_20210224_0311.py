# Generated by Django 3.1.3 on 2021-02-23 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0014_auto_20210223_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainarticle',
            name='category',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='mainarticle', to='index.category'),
        ),
    ]
