from django.contrib import admin
from .models import Client, ClientTag, ClientGroup


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'whatsapp', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'tags')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'whatsapp')
    date_hierarchy = 'created_at'
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'whatsapp')
        }),
        ('Дополнительная информация', {
            'fields': ('company', 'position', 'address', 'tags', 'status', 'source', 'notes')
        }),
        ('Временные метки', {
            'fields': ('last_contacted',),
            'classes': ('collapse',)
        })
    )


@admin.register(ClientTag)
class ClientTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name', 'description')


@admin.register(ClientGroup)
class ClientGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_dynamic', 'created_at')
    list_filter = ('is_dynamic', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('clients',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'clients')
        }),
        ('Динамическая группировка', {
            'fields': ('is_dynamic', 'filter_criteria'),
            'classes': ('collapse',)
        })
    )