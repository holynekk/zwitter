# Generated by Django 4.0.4 on 2022-05-04 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=280, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
