# Generated by Django 3.2.6 on 2023-06-19 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0008_auto_20230619_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='concept',
            field=models.CharField(default='Symmetric Encryption', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='field',
            field=models.CharField(default='Cybersecurity', max_length=100),
            preserve_default=False,
        ),
    ]
