# Generated by Django 5.1.1 on 2024-10-09 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0002_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='profiles.profile')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractor', to='profiles.profile')),
            ],
        ),
    ]
