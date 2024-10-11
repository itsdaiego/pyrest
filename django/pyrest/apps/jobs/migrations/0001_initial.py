# Generated by Django 5.1.1 on 2024-10-09 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('paid', models.BooleanField()),
                ('payment_date', models.DateTimeField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
    ]