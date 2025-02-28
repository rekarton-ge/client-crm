from django.db import models
from django.utils.translation import gettext_lazy as _
from clients.models import Client
from campaigns.models import Campaign


class MessageAnalytics(models.Model):
    """Модель для аналитики по сообщениям."""

    # Типы сообщений
    MESSAGE_TYPE_CHOICES = (
        ('email', _('Email')),
        ('whatsapp', _('WhatsApp')),
    )
    message_type = models.CharField(_("Тип сообщения"), max_length=10, choices=MESSAGE_TYPE_CHOICES)

    # Дата отправки (используется для группировки по дням/месяцам)
    date = models.DateField(_("Дата"))

    # Связанная кампания (если есть)
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.SET_NULL,
        related_name='daily_analytics',
        verbose_name=_("Кампания"),
        null=True, blank=True
    )

    # Счетчики статистики
    sent_count = models.PositiveIntegerField(_("Отправлено"), default=0)
    delivered_count = models.PositiveIntegerField(_("Доставлено"), default=0)
    open_count = models.PositiveIntegerField(_("Открыто"), default=0)
    click_count = models.PositiveIntegerField(_("Кликов"), default=0)
    unique_open_count = models.PositiveIntegerField(_("Уникальных открытий"), default=0)
    unique_click_count = models.PositiveIntegerField(_("Уникальных кликов"), default=0)
    bounce_count = models.PositiveIntegerField(_("Отказов"), default=0)
    complaint_count = models.PositiveIntegerField(_("Жалоб"), default=0)

    # Проценты (для быстрого доступа)
    delivery_rate = models.FloatField(_("Показатель доставки"), default=0.0)  # delivered/sent
    open_rate = models.FloatField(_("Показатель открытий"), default=0.0)  # unique_open/delivered
    click_rate = models.FloatField(_("Показатель кликов"), default=0.0)  # unique_click/unique_open

    # Временная метка обновления
    updated_at = models.DateTimeField(_("Последнее обновление"), auto_now=True)

    class Meta:
        verbose_name = _("Аналитика сообщений")
        verbose_name_plural = _("Аналитика сообщений")
        ordering = ['-date']
        unique_together = ('message_type', 'date', 'campaign')

    def __str__(self):
        campaign_name = self.campaign.name if self.campaign else "Все кампании"
        return f"{self.get_message_type_display()} - {self.date} - {campaign_name}"

    def recalculate_rates(self):
        """Пересчитывает проценты на основе счетчиков."""
        if self.sent_count > 0:
            self.delivery_rate = (self.delivered_count / self.sent_count) * 100

        if self.delivered_count > 0:
            self.open_rate = (self.unique_open_count / self.delivered_count) * 100

        if self.unique_open_count > 0:
            self.click_rate = (self.unique_click_count / self.unique_open_count) * 100

        self.save(update_fields=['delivery_rate', 'open_rate', 'click_rate'])


class ClientEngagement(models.Model):
    """Модель для отслеживания вовлеченности клиентов."""

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='engagement_metrics',
        verbose_name=_("Клиент")
    )

    # Счетчики взаимодействий
    email_sent_count = models.PositiveIntegerField(_("Email отправлено"), default=0)
    email_open_count = models.PositiveIntegerField(_("Email открыто"), default=0)
    email_click_count = models.PositiveIntegerField(_("Email кликов"), default=0)

    whatsapp_sent_count = models.PositiveIntegerField(_("WhatsApp отправлено"), default=0)
    whatsapp_delivered_count = models.PositiveIntegerField(_("WhatsApp доставлено"), default=0)
    whatsapp_read_count = models.PositiveIntegerField(_("WhatsApp прочитано"), default=0)

    # Последние взаимодействия
    last_email_sent = models.DateTimeField(_("Последний email отправлен"), blank=True, null=True)
    last_email_opened = models.DateTimeField(_("Последний email открыт"), blank=True, null=True)
    last_email_clicked = models.DateTimeField(_("Последний email клик"), blank=True, null=True)

    last_whatsapp_sent = models.DateTimeField(_("Последний WhatsApp отправлен"), blank=True, null=True)
    last_whatsapp_delivered = models.DateTimeField(_("Последний WhatsApp доставлен"), blank=True, null=True)
    last_whatsapp_read = models.DateTimeField(_("Последний WhatsApp прочитан"), blank=True, null=True)

    # Оценка вовлеченности (рассчитывается на основе активности)
    engagement_score = models.FloatField(_("Оценка вовлеченности"), default=0.0)

    # Временные метки
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Вовлеченность клиента")
        verbose_name_plural = _("Вовлеченность клиентов")
        ordering = ['-engagement_score']

    def __str__(self):
        return f"Вовлеченность - {self.client.get_full_name()}"

    def calculate_engagement_score(self):
        """
        Рассчитывает оценку вовлеченности на основе взаимодействий клиента.
        Формула может быть настроена по желанию.
        """
        # Пример формулы вовлеченности (можно настроить)
        email_weight = 1.0
        whatsapp_weight = 1.5
        open_weight = 2.0
        click_weight = 3.0
        read_weight = 2.5

        email_score = (
                self.email_sent_count * email_weight +
                self.email_open_count * open_weight +
                self.email_click_count * click_weight
        )

        whatsapp_score = (
                self.whatsapp_sent_count * whatsapp_weight +
                self.whatsapp_delivered_count * email_weight +
                self.whatsapp_read_count * read_weight
        )

        # Общая оценка вовлеченности
        self.engagement_score = email_score + whatsapp_score
        self.save(update_fields=['engagement_score'])

        return self.engagement_score


class ReportData(models.Model):
    """Модель для хранения данных отчетов."""

    REPORT_TYPE_CHOICES = (
        ('daily', _('Ежедневный')),
        ('weekly', _('Еженедельный')),
        ('monthly', _('Ежемесячный')),
        ('campaign', _('По кампании')),
        ('client', _('По клиенту')),
        ('custom', _('Пользовательский')),
    )
    report_type = models.CharField(_("Тип отчета"), max_length=10, choices=REPORT_TYPE_CHOICES)

    title = models.CharField(_("Заголовок"), max_length=200)
    description = models.TextField(_("Описание"), blank=True, null=True)

    # Период отчета
    period_start = models.DateField(_("Начало периода"), blank=True, null=True)
    period_end = models.DateField(_("Конец периода"), blank=True, null=True)

    # Связанная кампания (если применимо)
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.SET_NULL,
        related_name='reports',
        verbose_name=_("Кампания"),
        null=True, blank=True
    )

    # Связанный клиент (если применимо)
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        related_name='reports',
        verbose_name=_("Клиент"),
        null=True, blank=True
    )

    # Данные отчета
    report_data = models.JSONField(_("Данные отчета"))

    # Временные метки
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Данные отчета")
        verbose_name_plural = _("Данные отчетов")
        ordering = ['-created_at']

    def __str__(self):
        return self.title