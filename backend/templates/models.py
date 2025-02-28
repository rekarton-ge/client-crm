from django.db import models
from django.utils.translation import gettext_lazy as _


class MessageTemplate(models.Model):
    """Модель для шаблонов сообщений, которые можно использовать для email или WhatsApp."""

    # Свойства шаблона
    name = models.CharField(_("Название шаблона"), max_length=200)
    description = models.TextField(_("Описание"), blank=True, null=True)

    # Тип шаблона
    TYPE_CHOICES = (
        ('email', _('Email')),
        ('whatsapp', _('WhatsApp')),
    )
    type = models.CharField(_("Тип шаблона"), max_length=10, choices=TYPE_CHOICES)

    # Содержимое
    subject = models.CharField(_("Тема"), max_length=255, blank=True, null=True)  # Только для email
    body = models.TextField(_("Тело шаблона"))

    # Для HTML-писем
    is_html = models.BooleanField(_("HTML формат"), default=True)

    # Переменные шаблона
    variables = models.JSONField(_("Переменные шаблона"), blank=True, null=True,
                                 help_text=_("Доступные переменные, которые можно использовать в этом шаблоне"))

    # Статус
    is_active = models.BooleanField(_("Активен"), default=True)

    # Временные метки
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    # Категории/теги для организации шаблонов
    categories = models.ManyToManyField('TemplateCategory', blank=True, related_name='templates')

    class Meta:
        verbose_name = _("Шаблон сообщения")
        verbose_name_plural = _("Шаблоны сообщений")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_email_template(self):
        return self.type == 'email'

    @property
    def is_whatsapp_template(self):
        return self.type == 'whatsapp'

    def render(self, context):
        """
        Рендерит шаблон с заданным контекстом.

        Args:
            context (dict): Словарь с переменными для использования в шаблоне

        Returns:
            str: Отрендеренное содержимое шаблона
        """
        from django.template import Template, Context

        # Создаем Django шаблон из тела
        template = Template(self.body)

        # Создаем контекст
        template_context = Context(context)

        # Рендерим и возвращаем
        rendered_body = template.render(template_context)

        # Если это email, также рендерим тему
        if self.is_email_template and self.subject:
            subject_template = Template(self.subject)
            rendered_subject = subject_template.render(template_context)
            return {
                'subject': rendered_subject,
                'body': rendered_body
            }

        return {'body': rendered_body}


class TemplateCategory(models.Model):
    """Модель для категоризации шаблонов сообщений."""

    name = models.CharField(_("Название категории"), max_length=100, unique=True)
    description = models.TextField(_("Описание"), blank=True, null=True)

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Категория шаблонов")
        verbose_name_plural = _("Категории шаблонов")
        ordering = ['name']

    def __str__(self):
        return self.name


class TemplateAttachment(models.Model):
    """Модель для файлов, которые можно прикрепить к шаблонам email."""

    template = models.ForeignKey(
        MessageTemplate,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_("Шаблон")
    )
    file = models.FileField(_("Файл"), upload_to='template_attachments/')
    filename = models.CharField(_("Имя файла"), max_length=255)
    content_type = models.CharField(_("Тип содержимого"), max_length=100)

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Вложение шаблона")
        verbose_name_plural = _("Вложения шаблонов")

    def __str__(self):
        return self.filename