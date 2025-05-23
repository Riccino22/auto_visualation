# Generated by Django 5.1.7 on 2025-04-02 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vslt_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('file_name', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('data_json', models.JSONField(default=dict)),
            ],
        ),
    ]
