# Generated by Django 4.2 on 2023-05-13 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0010_ordercomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordercomment',
            old_name='comment',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='ordercomment',
            old_name='employee',
            new_name='consultant',
        ),
    ]
