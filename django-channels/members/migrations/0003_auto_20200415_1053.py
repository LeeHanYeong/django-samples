# Generated by Django 3.0.5 on 2020-04-15 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20200415_0959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userchathistory',
            old_name='history',
            new_name='content',
        ),
    ]
