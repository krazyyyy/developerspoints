# Generated by Django 3.2.6 on 2021-09-23 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_auto_20210923_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectimages',
            name='responsive',
            field=models.BooleanField(default=False),
        ),
    ]