# Generated by Django 5.0.7 on 2024-07-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('extenal_id', models.CharField(max_length=60, unique=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Activo'), (2, 'Inactivo')])),
                ('score', models.DecimalField(decimal_places=2, max_digits=12)),
                ('preapproved_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]