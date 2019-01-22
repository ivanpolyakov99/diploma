from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Recipe
# Register your models here.


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name_text', 'level', 'get_image')
    search_fields = ('name_text',)
    list_filter = ('level',)

    def get_image(self, object):
        url = object.image.url if object.image else None
        if url:
            return mark_safe(f'<img src="{url}"/>')


admin.site.register(Recipe, RecipeAdmin)