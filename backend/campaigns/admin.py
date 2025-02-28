from django.contrib import admin
from .models import Campaign, CampaignSchedule


class CampaignScheduleInline(admin.TabularInline):
    model = CampaignSchedule
    extra = 1


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'is_scheduled', 'scheduled_start', 'sent_count', 'created_at')
    list_filter = ('type', 'status', 'frequency', 'is_scheduled', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    filter_horizontal = ('clients',)
    inlines = [CampaignScheduleInline]
    readonly_fields = (
    'total_recipients', 'sent_count', 'delivered_count', 'read_count', 'error_count', 'started_at', 'completed_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'type', 'status')
        }),
        ('Получатели', {
            'fields': ('client_group', 'clients')
        }),
        ('Шаблоны', {
            'fields': ('email_template', 'whatsapp_template')
        }),
        ('Расписание', {
            'fields': ('is_scheduled', 'scheduled_start', 'scheduled_end', 'frequency', 'custom_schedule')
        }),
        ('Ограничения', {
            'fields': ('max_messages_per_day',),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('total_recipients', 'sent_count', 'delivered_count', 'read_count', 'error_count'),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('started_at', 'completed_at'),
            'classes': ('collapse',)
        })
    )
    actions = ['update_statistics', 'duplicate_campaign', 'start_campaign', 'pause_campaign', 'complete_campaign']

    def update_statistics(self, request, queryset):
        for campaign in queryset:
            campaign.update_statistics()
        self.message_user(request, f"Статистика для {queryset.count()} кампаний обновлена.")

    update_statistics.short_description = "Обновить статистику выбранных кампаний"

    def duplicate_campaign(self, request, queryset):
        for campaign in queryset:
            # Создание дубликата кампании
            campaign.pk = None
            campaign.name = f"{campaign.name} (копия)"
            campaign.status = 'draft'
            campaign.started_at = None
            campaign.completed_at = None
            campaign.total_recipients = 0
            campaign.sent_count = 0
            campaign.delivered_count = 0
            campaign.read_count = 0
            campaign.error_count = 0
            campaign.save()

            # После сохранения добавляем связи Many-to-Many
            for client in campaign.clients.all():
                campaign.clients.add(client)

            # Дублирование расписаний
            for schedule in CampaignSchedule.objects.filter(campaign_id=campaign.pk):
                schedule.pk = None
                schedule.campaign = campaign
                schedule.save()

        self.message_user(request, f"{queryset.count()} кампаний было успешно дублировано.")

    duplicate_campaign.short_description = "Дублировать выбранные кампании"

    def start_campaign(self, request, queryset):
        from django.utils import timezone
        for campaign in queryset:
            campaign.status = 'active'
            campaign.started_at = timezone.now()
            campaign.save(update_fields=['status', 'started_at'])
        self.message_user(request, f"{queryset.count()} кампаний запущено.")

    start_campaign.short_description = "Запустить выбранные кампании"

    def pause_campaign(self, request, queryset):
        for campaign in queryset:
            campaign.status = 'paused'
            campaign.save(update_fields=['status'])
        self.message_user(request, f"{queryset.count()} кампаний приостановлено.")

    pause_campaign.short_description = "Приостановить выбранные кампании"

    def complete_campaign(self, request, queryset):
        from django.utils import timezone
        for campaign in queryset:
            campaign.status = 'completed'
            campaign.completed_at = timezone.now()
            campaign.save(update_fields=['status', 'completed_at'])
        self.message_user(request, f"{queryset.count()} кампаний завершено.")

    complete_campaign.short_description = "Завершить выбранные кампании"


@admin.register(CampaignSchedule)
class CampaignScheduleAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'schedule_type', 'scheduled_time', 'time_of_day', 'is_active')
    list_filter = ('schedule_type', 'is_active', 'created_at')
    search_fields = ('campaign__name',)
    date_hierarchy = 'created_at'