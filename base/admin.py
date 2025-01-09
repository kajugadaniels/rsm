from base.models import *
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model.
    """
    list_display = ('name', 'slug', 'created_at', 'updated_at', 'action_links')
    search_fields = ('name', 'slug')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    actions = ['export_as_csv']

    def action_links(self, obj):
        """
        Provides direct links to edit and delete the Product instance.
        """
        edit_url = f'/admin/base/product/{obj.id}/change/'
        delete_url = f'/admin/base/product/{obj.id}/delete/'
        return format_html(
            '<a class="button" href="{}">Edit</a> | '
            '<a class="button" href="{}">Delete</a>',
            edit_url,
            delete_url,
        )
    action_links.short_description = 'Actions'
    action_links.allow_tags = True

    @admin.action(description='Export selected products as CSV')
    def export_as_csv(self, request, queryset):
        """
        Exports selected Product instances as a CSV file.
        """
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=products.csv'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Slug', 'Created At', 'Updated At'])

        for product in queryset:
            writer.writerow([product.name, product.slug, product.created_at, product.updated_at])

        self.message_user(request, _("Selected products have been exported as CSV."))

