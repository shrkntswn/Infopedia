# Generated by Django 3.1.3 on 2021-02-24 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0016_auto_20210224_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subarticle',
            old_name='reference_link',
            new_name='external_link',
        ),
        migrations.AddField(
            model_name='subarticle',
            name='other_reference',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='subarticle',
            name='title_to_external_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]