# Generated by Django 2.2.12 on 2020-06-12 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation_webapp', '0002_auto_20200610_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=500, null=True)),
                ('title', models.CharField(max_length=500, null=True)),
                ('synopsis', models.TextField()),
                ('genre', models.CharField(max_length=500, null=True)),
                ('aired', models.CharField(max_length=500, null=True)),
                ('episodes', models.CharField(max_length=500, null=True)),
                ('members', models.CharField(max_length=500, null=True)),
                ('popularity', models.CharField(max_length=500, null=True)),
                ('ranked', models.CharField(max_length=500, null=True)),
                ('score', models.CharField(max_length=500, null=True)),
                ('img_url', models.TextField()),
                ('link', models.TextField()),
            ],
        ),
    ]
