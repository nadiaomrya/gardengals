# Generated by Django 5.2 on 2025-05-05 17:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('content', models.TextField()),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-published_at'],
            },
        ),
    ]
