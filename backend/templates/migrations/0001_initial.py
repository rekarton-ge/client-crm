# Generated by Django 4.2.9 on 2025-02-28 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название шаблона')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('type', models.CharField(choices=[('email', 'Email'), ('whatsapp', 'WhatsApp')], max_length=10, verbose_name='Тип шаблона')),
                ('subject', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тема')),
                ('body', models.TextField(verbose_name='Тело шаблона')),
                ('is_html', models.BooleanField(default=True, verbose_name='HTML формат')),
                ('variables', models.JSONField(blank=True, help_text='Доступные переменные, которые можно использовать в этом шаблоне', null=True, verbose_name='Переменные шаблона')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Шаблон сообщения',
                'verbose_name_plural': 'Шаблоны сообщений',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TemplateCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название категории')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Категория шаблонов',
                'verbose_name_plural': 'Категории шаблонов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TemplateAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='template_attachments/', verbose_name='Файл')),
                ('filename', models.CharField(max_length=255, verbose_name='Имя файла')),
                ('content_type', models.CharField(max_length=100, verbose_name='Тип содержимого')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='templates.messagetemplate', verbose_name='Шаблон')),
            ],
            options={
                'verbose_name': 'Вложение шаблона',
                'verbose_name_plural': 'Вложения шаблонов',
            },
        ),
        migrations.AddField(
            model_name='messagetemplate',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='templates', to='templates.templatecategory'),
        ),
    ]
