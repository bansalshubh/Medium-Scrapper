# Generated by Django 3.2.3 on 2022-02-01 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('SearchId', models.AutoField(primary_key=True, serialize=False)),
                ('SearchTagName', models.CharField(max_length=500)),
                ('SearchDate', models.DateField()),
            ],
        ),
    ]
