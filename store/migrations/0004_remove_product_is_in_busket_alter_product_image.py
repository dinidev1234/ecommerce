# Generated by Django 4.2.6 on 2023-10-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_in_busket',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='product_images/<django.db.models.query_utils.DeferredAttribute object at 0x00000145E600D350>'),
        ),
    ]