# Generated by Django 4.0.3 on 2022-03-30 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receivePic', '0003_direction'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScannedNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scannedNum', models.CharField(max_length=10)),
            ],
        ),
    ]
