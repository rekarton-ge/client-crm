from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import Client, ClientGroup
from templates.models import MessageTemplate


class Campaign(models.Model):
    """Модель для управления кампаниями рассылок."""

    # Свойства кампании
    name = models.CharField(_("Название кампании"), max_length=200)
    description = models.TextField(_("Описание"), blank=True, null=True)

    # Тип кампании
    TYPE_CHOICES = (
        ('email', _('Email')),
        ('whatsapp', _('WhatsApp')),
        ('mixed', _('Смешанная')),  # И email, и WhatsApp
    )
    type = models.CharField(_("Тип кампании"), max_length=10, choices=TYPE_CHOICES)

    # Целевая аудитория
    client_group = models.ForeignKey(
        ClientGroup,
        on_delete=models.SET_NULL,
        related_name='campaigns',
        verbose_name=_("Группа клиентов"),
        null=True, blank=True
    )

    # Индивидуальные клиенты (если не используется группа)
    clients = models.ManyToManyField(
        Client,
        related_name='targeted_campaigns',
        verbose_name=_("Клиенты"),
        blank=True
    )

    # Шаблоны для использования
    email_template = models.ForeignKey(
        MessageTemplate,
        on_delete=models.SET_NULL,
        related_name='email_campaigns',
        verbose_name=_("Шаблон email"),
        null=True, blank=True,
        limit_choices_to={'type': 'email'}
    )
    whatsapp_template = models.ForeignKey(
        MessageTemplate,
        on_delete=models.SET_NULL,
        related_name='whatsapp_campaigns',
        verbose_name=_("Шаблон WhatsApp"),
        null=True, blank=True,
        limit_choices_to={'type': 'whatsapp'}
    )

    # Опции расписания
    is_scheduled = models.BooleanField(_("По расписанию"), default=False)
    scheduled_start = models.DateTimeField(_("Запланированное начало"), blank=True, null=True)
    scheduled_end = models.DateTimeField(_("Запланированное окончание"), blank=True, null=True)

    # Частота для повторяющихся кампаний
    FREQUENCY_CHOICES = (
        ('once', _('Однократно')),
        ('daily', _('Ежедневно')),
        ('weekly', _('Еженедельно')),
        ('monthly', _('Ежемесячно')),
        ('custom', _('Пользовательская')),
    )
    frequency = models.CharField(_("Частота"), max_length=10, choices=FREQUENCY_CHOICES, default='once')

    # Для пользовательской частоты
    custom_schedule = models.JSONField(_("Пользовательское расписание"), blank=True, null=True)

    # Статус кампании
    STATUS_CHOICES = (
        ('draft', _('Черновик')),
        ('scheduled', _('Запланирована')),
        ('active', _('Активна')),
        ('paused', _('Приостановлена')),
        ('completed', _('Завершена')),
        ('cancelled', _('Отменена')),
    )
    status = models.CharField(_("Статус"), max_length=10, choices=STATUS_CHOICES, default='draft')

    # Ограничения
    max_messages_per_day = models.PositiveIntegerField(_("Макс. сообщений в день"), blank=True, null=True)

    # Статистика
    total_recipients = models.PositiveIntegerField(_("Всего получателей"), default=0)
    sent_count = models.PositiveIntegerField(_("Отправлено"), default=0)
    delivered_count = models.PositiveIntegerField(_("Доставлено"), default=0)
    read_count = models.PositiveIntegerField(_("Прочитано"), default=0)
    error_count = models.PositiveIntegerField(_("Ошибок"), default=0)

    # Временные метки
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)
    started_at = models.DateTimeField(_("Дата начала"), blank=True, null=True)
    completed_at = models.DateTimeField(_("Дата завершения"), blank=True, null=True)

    class Meta:
        verbose_name = _("Кампания")
        verbose_name_plural = _("Кампании")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def is_completed(self):
        return self.status == 'completed'

    def update_statistics(self):
        """Обновляет статистику кампании на основе связанных сообщений."""
        from messaging.models import Message

        # Получаем все сообщения этой кампании
        messages = Message.objects.filter(campaign=self)

        # Обновляем счетчики
        self.total_recipients = messages.count()
        self.sent_count = messages.filter(status='sent').count()
        self.delivered_count = messages.filter(status='delivered').count()
        self.read_count = messages.filter(status='read').count()
        self.error_count = messages.filter(status='failed').count()

        self.save(update_fields=[
            'total_recipients', 'sent_count', 'delivered_count',
            'read_count', 'error_count'
        ])


class CampaignSchedule(models.Model):
    """Модель для детального управления расписанием кампаний."""

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_("Кампания")
    )

    # Тип расписания
    SCHEDULE_TYPE_CHOICES = (
        ('fixed', _('Фиксированное время')),
        ('recurring', _('Повторяющееся')),
    )
    schedule_type = models.CharField(_("Тип расписания"), max_length=10, choices=SCHEDULE_TYPE_CHOICES)

    # Для фиксированного времени
    scheduled_time = models.DateTimeField(_("Запланированное время"), blank=True, null=True)

    # Для повторяющегося расписания
    days_of_week = models.JSONField(_("Дни недели"), blank=True, null=True)  # [0, 1, 2, 3, 4, 5, 6] для Пн-Вс
    time_of_day = models.TimeField(_("Время дня"), blank=True, null=True)

    # Статус
    is_active = models.BooleanField(_("Активно"), default=True)

    # Временные метки
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Расписание кампании")
        verbose_name_plural = _("Расписания кампаний")
        ordering = ['scheduled_time', 'time_of_day']

    def __str__(self):
        if self.schedule_type == 'fixed':
            return f"{self.campaign.name} - {self.scheduled_time}"
        else:
            days = ','.join(str(day) for day in self.days_of_week) if self.days_of_week else 'все'
            return f"{self.campaign.name} - {days} в {self.time_of_day}"