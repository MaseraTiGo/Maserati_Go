# Generated by Django 2.0.5 on 2018-05-09 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('pic', models.ImageField(default='D:\\TDdownload\\Pic\\download', upload_to='')),
                ('summary', models.CharField(max_length=500)),
                ('date_old', models.DateField()),
                ('date_new', models.DateField()),
            ],
        ),
    ]
