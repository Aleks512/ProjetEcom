# Generated by Django 4.2 on 2023-05-10 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0008_remove_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(choices=[(1000, '1000'), (2000, '2000'), (3000, '3000'), (4000, '4000'), (5000, '5000'), (6000, '6000'), (7000, '7000'), (8000, '8000'), (9000, '9000'), (10000, '10000')], default=1000),
        ),
    ]
