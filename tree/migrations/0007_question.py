# Generated by Django 3.2.6 on 2023-06-06 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0006_auto_20230606_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concept', models.CharField(max_length=100)),
                ('field', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=100)),
                ('qtype', models.CharField(max_length=100)),
                ('key_text', models.TextField()),
                ('distractor_text', models.TextField()),
                ('stem', models.TextField()),
                ('options', models.TextField()),
                ('answer', models.TextField()),
                ('datetime', models.DateTimeField()),
            ],
        ),
    ]
