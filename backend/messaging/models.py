from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import Client


class Message(models.Model):
    """Базовая модель для сообщений (email, WhatsApp) в системе."""

    # Типы сообщений
    TYPE_CHOICES = (
        ('email', _('Email')),
        ('whatsapp', _('WhatsApp')),
    )
    type = models.CharField(_("Тип сообщения"), max_length=10, choices=TYPE_CHOICES)

    # Направление
    DIRECTION_CHOICES = (
        ('incoming', _('Входящее')),
        ('outgoing', _('Исходящее')),
    )
    direction = models.CharField(_("Направление"), max_length=10, choices=DIRECTION_CHOICES)

    # Информация об отправителе и получателе
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_("Клиент"),
        null=True, blank=True  # Для системных сообщений или кампаний
    )
    from_email = models.EmailField(_("От кого (email)"), blank=True, null=True)
    from_number = models.CharField(_("От кого (номер)"), max_length=20, blank=True, null=True)
    to_email = models.EmailField(_("Кому (email)"), blank=True, null=True)
    to_number = models.CharField(_("Кому (номер)"), max_length=20, blank=True, null=True)

    # Содержимое
    subject = models.CharField(_("Тема"), max_length=255, blank=True, null=True)  # Для email
    body = models.TextField(_("Текст сообщения"))

    # Вложения
    has_attachments = models.BooleanField(_("Есть вложения"), default=False)

    # Статус
    STATUS_CHOICES = (
        ('draft', _('Черновик')),
        ('queued', _('В очереди')),
        ('sent', _('Отправлено')),
        ('delivered', _('Доставлено')),
        ('read', _('Прочитано')),
        ('failed', _('Ошибка')),
    )
    status = models.CharField(_("Статус"), max_length=10, choices=STATUS_CHOICES, default='draft')
    status_details = models.TextField(_("Детали статуса"), blank=True, null=True)  # Для сообщений об ошибках

    # Отслеживание
    track_opens = models.BooleanField(_("Отслеживать открытия"), default=True)  # Для email
    track_clicks = models.BooleanField(_("Отслеживать клики"), default=True)  # Для email и ссылок WhatsApp

    # Связанная кампания
    campaign = models.ForeignKey(
        'campaigns.Campaign',
        on_delete=models.SET_NULL,
        related_name='messages',
        verbose_name=_("Кампания"),
        null=True, blank=True
    )

    # Использованный шаблон (если есть)
    template = models.ForeignKey(
        'templates.MessageTemplate',
        on_delete=models.SET_NULL,
        related_name='messages',
        verbose_name=_("Шаблон"),
        null=True, blank=True
    )

    # Временные метки
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    scheduled_at = models.DateTimeField(_("Запланировано на"), blank=True, null=True)
    sent_at = models.DateTimeField(_("Дата отправки"), blank=True, null=True)
    delivered_at = models.DateTimeField(_("Дата доставки"), blank=True, null=True)
    read_at = models.DateTimeField(_("Дата прочтения"), blank=True, null=True)

    class Meta:
        verbose_name = _("Сообщение")
        verbose_name_plural = _("Сообщения")
        ordering = ['-created_at']

    def __str__(self):
        if self.subject:
            return f"{self.get_type_display()}: {self.subject[:50]}"
        else:
            return f"{self.get_type_display()}: {self.body[:50]}"

    @property
    def is_email(self):
        return self.type == 'email'

    @property
    def is_whatsapp(self):
        return self.type == 'whatsapp'

    @property
    def is_read(self):
        return self.status == 'read' and self.read_at is not None

    def mark_as_sent(self):
        """Отметить сообщение как отправленное с текущей отметкой времени."""
        from django.utils import timezone
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at'])

    def mark_as_delivered(self):
        """Отметить сообщение как доставленное с текущей отметкой времени."""
        from django.utils import timezone
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save(update_fields=['status', 'delivered_at'])

    def mark_as_read(self):
        """Отметить сообщение как прочитанное с текущей отметкой времени."""
        from django.utils import timezone
        self.status = 'read'
        self.read_at = timezone.now()
        self.save(update_fields=['status', 'read_at'])


class MessageAttachment(models.Model):
    """Модель для вложений сообщений."""

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_("Сообщение")
    )
    file = models.FileField(_("Файл"), upload_to='message_attachments/')
    filename = models.CharField(_("Имя файла"), max_length=255)
    file_size = models.PositiveIntegerField(_("Размер файла"), help_text=_("Размер в байтах"))
    content_type = models.CharField(_("Тип содержимого"), max_length=100)

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Вложение сообщения")
        verbose_name_plural = _("Вложения сообщений")

    def __str__(self):
        return self.filename


class MessageEvent(models.Model):
    """Модель для отслеживания событий сообщений (открытия, клики и т.д.)."""

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name=_("Сообщение")
    )

    EVENT_TYPES = (
        ('open', _('Открытие')),
        ('click', _('Клик')),
        ('bounce', _('Отказ')),
        ('complaint', _('Жалоба')),
        ('delivery', _('Доставка')),
        ('read', _('Прочтение')),  # Подтверждение прочтения WhatsApp
    )
    event_type = models.CharField(_("Тип события"), max_length=20, choices=EVENT_TYPES)

    occurred_at = models.DateTimeField(_("Время события"), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_("IP-адрес"), blank=True, null=True)
    user_agent = models.TextField(_("User Agent"), blank=True, null=True)

    # Для событий клика
    url = models.URLField(_("URL"), blank=True, null=True)

    # Дополнительные данные
    metadata = models.JSONField(_("Метаданные"), blank=True, null=True)

    class Meta:
        verbose_name = _("Событие сообщения")
        verbose_name_plural = _("События сообщений")
        ordering = ['-occurred_at']

    def __str__(self):
        return f"{self.get_event_type_display()} для сообщения {self.message.id}"