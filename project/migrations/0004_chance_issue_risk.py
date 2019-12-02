# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-06 11:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20171105_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('date', models.DateField(verbose_name='Discovery Date')),
                ('cost', models.PositiveIntegerField(choices=[(1, 'Low'), (2, 'High'), (3, 'Very High')], verbose_name='Cost of the Chance')),
                ('impact', models.PositiveIntegerField(choices=[(1, 'Small'), (2, 'Big'), (3, 'Very Big')], verbose_name='Impact of the Chance')),
                ('used', models.BooleanField(default=False, verbose_name='Chance used')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chances', related_query_name='chance', to='project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('date', models.DateField(verbose_name='Discovery Date')),
                ('severity', models.PositiveIntegerField(choices=[(1, 'Low'), (2, 'High'), (3, 'Very High')], verbose_name='Severity of the Risk')),
                ('counter_measurement', models.TextField(verbose_name='Counter Measurement')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', related_query_name='issue', to='project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('date', models.DateField(verbose_name='Discovery Date')),
                ('probability', models.PositiveIntegerField(choices=[(1, 'Unlikely'), (2, 'Likely'), (3, 'Very Likely')], verbose_name='Probability of the Risk')),
                ('severity', models.PositiveIntegerField(choices=[(1, 'Low'), (2, 'High'), (3, 'Very High')], verbose_name='Severity of the Risk')),
                ('counter_measurement', models.TextField(verbose_name='Counter Measurement')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risks', related_query_name='risk', to='project.Project')),
            ],
        ),
    ]