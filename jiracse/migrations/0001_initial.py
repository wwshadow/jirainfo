# Generated by Django 3.2.12 on 2022-05-29 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TbCse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cseid', models.CharField(max_length=100)),
                ('csename', models.CharField(max_length=1000)),
                ('fullname', models.CharField(max_length=1000)),
                ('customername', models.CharField(blank=True, max_length=1000, null=True)),
                ('csestatus', models.CharField(max_length=100)),
                ('projectname', models.CharField(blank=True, max_length=1000, null=True)),
                ('version', models.CharField(max_length=10)),
                ('maintenancedate', models.CharField(blank=True, max_length=100, null=True)),
                ('environmenttype', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tb_cse',
            },
        ),
        migrations.CreateModel(
            name='TbEsdesk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issueid', models.CharField(max_length=50)),
                ('jiraid', models.CharField(max_length=50)),
                ('esdeskname', models.CharField(max_length=50)),
                ('issuetype', models.CharField(max_length=1000)),
                ('issuestatus', models.CharField(max_length=1000)),
                ('createdata', models.CharField(max_length=1000)),
                ('epicid', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'tb_esdesk',
            },
        ),
        migrations.CreateModel(
            name='TbJirauser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jiraemail', models.CharField(blank=True, max_length=50, null=True)),
                ('jiraid', models.CharField(blank=True, max_length=50, null=True)),
                ('jirakey', models.CharField(blank=True, max_length=50, null=True)),
                ('jiraname', models.CharField(blank=True, max_length=50, null=True)),
                ('sessiontoken', models.CharField(blank=True, max_length=200, null=True)),
                ('jiratotptoken', models.CharField(blank=True, max_length=200, null=True)),
                ('tempotoken', models.CharField(blank=True, max_length=200, null=True)),
                ('projectname', models.CharField(blank=True, max_length=50, null=True)),
                ('groups', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'tb_jirauser',
            },
        ),
    ]
