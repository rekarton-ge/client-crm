from django.contrib import admin
from .models import MessageTemplate, TemplateCategory, TemplateAttachment


class TemplateAttachmentInline(admin.TabularInline):
    model = TemplateAttachment
    extra = 1


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_html', 'is_active', 'created_at', 'updated_at')
    list_filter = ('type', 'is_html', 'is_active', 'created_at', 'categories')
    search_fields = ('name', 'description', 'subject', 'body')
    date_hierarchy = 'created_at'
    filter_horizontal = ('categories',)
    inlines = [TemplateAttachmentInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'type', 'is_active')
        }),
        ('Содержимое', {
            'fields': ('subject', 'body', 'is_html')
        }),
        ('Переменные и категории', {
            'fields': ('variables', 'categories')
        })
    )
    actions = ['duplicate_template']

    def duplicate_template(self, request, queryset):
        for template in queryset:
            # Создание дубликата шаблона
            template.pk = None
            template.name = f"{template.name} (копия)"
            template.save()

            # После сохранения добавляем связи Many-to-Many
            for category in template.categories.all():
                template.categories.add(category)

            # Дублирование вложений
            for attachment in TemplateAttachment.objects.filter(template_id=template.pk):
                attachment.pk = None
                attachment.template = template
                attachment.save()

        self.message_user(request, f"{queryset.count()} шаблонов было успешно дублировано.")

    duplicate_template.short_description = "Дублировать выбранные шаблоны"


@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')


@admin.register(TemplateAttachment)
class TemplateAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'template', 'content_type', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('filename', 'template__name')