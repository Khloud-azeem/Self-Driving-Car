# Generated by Django 4.0.3 on 2022-03-31 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receivePic', '0004_scannednum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(max_length=10)),
            ],
        ),
    ]
