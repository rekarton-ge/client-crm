from django.contrib import admin
from .models import Message, MessageAttachment, MessageEvent


class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 1


class MessageEventInline(admin.TabularInline):
    model = MessageEvent
    extra = 0
    readonly_fields = ('occurred_at', 'event_type', 'ip_address', 'user_agent', 'url', 'metadata')
    can_delete = False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'direction', 'client', 'subject', 'status', 'created_at', 'sent_at')
    list_filter = ('type', 'direction', 'status', 'created_at', 'sent_at')
    search_fields = ('subject', 'body', 'from_email', 'to_email', 'from_number', 'to_number')
    date_hierarchy = 'created_at'
    inlines = [MessageAttachmentInline, MessageEventInline]
    readonly_fields = ('sent_at', 'delivered_at', 'read_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('type', 'direction', 'client', 'campaign', 'template')
        }),
        ('Содержимое', {
            'fields': ('subject', 'body', 'has_attachments')
        }),
        ('Контактная информация', {
            'fields': ('from_email', 'to_email', 'from_number', 'to_number')
        }),
        ('Статус и отслеживание', {
            'fields': ('status', 'status_details', 'track_opens', 'track_clicks')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'scheduled_at', 'sent_at', 'delivered_at', 'read_at'),
            'classes': ('collapse',)
        })
    )
    actions = ['mark_as_sent', 'mark_as_delivered', 'mark_as_read']

    def mark_as_sent(self, request, queryset):
        for message in queryset:
            message.mark_as_sent()
        self.message_user(request, f"{queryset.count()} сообщений отмечены как отправленные.")
    mark_as_sent.short_description = "Отметить выбранные сообщения как отправленные"

    def mark_as_delivered(self, request, queryset):
        for message in queryset:
            message.mark_as_delivered()
        self.message_user(request, f"{queryset.count()} сообщений отмечены как доставленные.")
    mark_as_delivered.short_description = "Отметить выбранные сообщения как доставленные"

    def mark_as_read(self, request, queryset):
        for message in queryset:
            message.mark_as_read()
        self.message_user(request, f"{queryset.count()} сообщений отмечены как прочитанные.")
    mark_as_read.short_description = "Отметить выбранные сообщения как прочитанные"


@admin.register(MessageAttachment)
class MessageAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'message', 'content_type', 'file_size', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('filename', 'message__subject')


@admin.register(MessageEvent)
class MessageEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'message', 'occurred_at', 'ip_address')
    list_filter = ('event_type', 'occurred_at')
    search_fields = ('message__subject', 'ip_address', 'user_agent')
    readonly_fields = ('message', 'event_type', 'occurred_at', 'ip_address', 'user_agent', 'url', 'metadata')