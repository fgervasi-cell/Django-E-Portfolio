# Generated by Django 3.2.8 on 2021-11-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_alter_todoitem_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
