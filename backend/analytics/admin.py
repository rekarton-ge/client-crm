from django.contrib import admin
from .models import MessageAnalytics, ClientEngagement, ReportData


@admin.register(MessageAnalytics)
class MessageAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'message_type', 'campaign', 'sent_count', 'delivered_count', 'open_rate', 'click_rate')
    list_filter = ('message_type', 'date', 'campaign')
    search_fields = ('campaign__name',)
    date_hierarchy = 'date'
    readonly_fields = ('delivery_rate', 'open_rate', 'click_rate')
    fieldsets = (
        ('Основная информация', {
            'fields': ('message_type', 'date', 'campaign')
        }),
        ('Счетчики', {
            'fields': ('sent_count', 'delivered_count', 'open_count', 'click_count',
                      'unique_open_count', 'unique_click_count', 'bounce_count', 'complaint_count')
        }),
        ('Показатели', {
            'fields': ('delivery_rate', 'open_rate', 'click_rate')
        })
    )
    actions = ['recalculate_rates']

    def recalculate_rates(self, request, queryset):
        for analytics in queryset:
            analytics.recalculate_rates()
        self.message_user(request, f"Показатели для {queryset.count()} записей пересчитаны.")
    recalculate_rates.short_description = "Пересчитать показатели для выбранных записей"


@admin.register(ClientEngagement)
class ClientEngagementAdmin(admin.ModelAdmin):
    list_display = ('client', 'engagement_score', 'email_sent_count', 'email_open_count',
                    'whatsapp_sent_count', 'whatsapp_read_count', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('client__first_name', 'client__last_name', 'client__email')
    readonly_fields = ('engagement_score',)
    fieldsets = (
        ('Клиент', {
            'fields': ('client', 'engagement_score')
        }),
        ('Email статистика', {
            'fields': ('email_sent_count', 'email_open_count', 'email_click_count',
                      'last_email_sent', 'last_email_opened', 'last_email_clicked')
        }),
        ('WhatsApp статистика', {
            'fields': ('whatsapp_sent_count', 'whatsapp_delivered_count', 'whatsapp_read_count',
                      'last_whatsapp_sent', 'last_whatsapp_delivered', 'last_whatsapp_read')
        })
    )
    actions = ['calculate_engagement_score']

    def calculate_engagement_score(self, request, queryset):
        for engagement in queryset:
            engagement.calculate_engagement_score()
        self.message_user(request, f"Оценка вовлеченности для {queryset.count()} клиентов пересчитана.")
    calculate_engagement_score.short_description = "Пересчитать оценку вовлеченности"


@admin.register(ReportData)
class ReportDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'period_start', 'period_end', 'campaign', 'client', 'created_at')
    list_filter = ('report_type', 'period_start', 'period_end', 'created_at')
    search_fields = ('title', 'description', 'campaign__name', 'client__first_name', 'client__last_name')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'report_type')
        }),
        ('Период и фильтры', {
            'fields': ('period_start', 'period_end', 'campaign', 'client')
        }),
        ('Данные отчета', {
            'fields': ('report_data',)
        })
    )