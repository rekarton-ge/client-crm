from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """Модель, представляющая клиента в CRM-системе."""

    # Основная информация
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    email = models.EmailField(_("Email"), unique=True)
    phone = models.CharField(_("Телефон"), max_length=20, blank=True, null=True)
    whatsapp = models.CharField(_("WhatsApp"), max_length=20, blank=True, null=True)

    # Дополнительная информация
    company = models.CharField(_("Компания"), max_length=200, blank=True, null=True)
    position = models.CharField(_("Должность"), max_length=200, blank=True, null=True)
    address = models.TextField(_("Адрес"), blank=True, null=True)

    # Теги для фильтрации и категоризации
    tags = models.ManyToManyField('ClientTag', blank=True, related_name='clients')

    # Статус и источник
    STATUS_CHOICES = (
        ('active', _('Активен')),
        ('inactive', _('Неактивен')),
        ('lead', _('Лид')),
        ('prospect', _('Проспект')),
        ('customer', _('Клиент')),
    )
    status = models.CharField(_("Статус"), max_length=20, choices=STATUS_CHOICES, default='active')
    source = models.CharField(_("Источник"), max_length=100, blank=True, null=True)

    # Временные метки
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)
    last_contacted = models.DateTimeField(_("Последний контакт"), blank=True, null=True)

    # Заметки
    notes = models.TextField(_("Заметки"), blank=True, null=True)

    class Meta:
        verbose_name = _("Клиент")
        verbose_name_plural = _("Клиенты")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Возвращает полное имя клиента."""
        return f"{self.first_name} {self.last_name}"


class ClientTag(models.Model):
    """Модель для тегов клиентов для категоризации."""

    name = models.CharField(_("Название тега"), max_length=100, unique=True)
    color = models.CharField(_("Цвет"), max_length=7, default="#000000")  # Hex код цвета
    description = models.TextField(_("Описание"), blank=True, null=True)

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Тег клиента")
        verbose_name_plural = _("Теги клиентов")
        ordering = ['name']

    def __str__(self):
        return self.name


class ClientGroup(models.Model):
    """Модель для группировки клиентов для целевых кампаний."""

    name = models.CharField(_("Название группы"), max_length=100)
    description = models.TextField(_("Описание"), blank=True, null=True)
    clients = models.ManyToManyField('Client', related_name='groups')

    # Критерии фильтрации (можно использовать для динамической группировки)
    filter_criteria = models.JSONField(_("Критерии фильтрации"), blank=True, null=True)
    is_dynamic = models.BooleanField(_("Динамическая группа"), default=False)

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Группа клиентов")
        verbose_name_plural = _("Группы клиентов")
        ordering = ['-created_at']

    def __str__(self):
        return self.name