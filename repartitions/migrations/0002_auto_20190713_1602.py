# Generated by Django 2.1.7 on 2019-07-13 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repartitions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('num', models.IntegerField()),
                ('min_eleves', models.IntegerField()),
                ('max_eleves', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Voeux',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('voeux', models.TextField()),
                ('isNew', models.BooleanField(default=True)),
                ('outcome', models.IntegerField(default=-1)),
            ],
        ),
        migrations.AddField(
            model_name='repartition',
            name='equirepartition',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='voeux',
            name='campagne',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repartitions.Repartition'),
        ),
        migrations.AddField(
            model_name='voeux',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposition',
            name='campagne',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repartitions.Repartition'),
        ),
    ]
