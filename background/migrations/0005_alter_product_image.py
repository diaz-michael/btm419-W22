# Generated by Django 4.0.3 on 2022-03-18 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('background', '0004_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
