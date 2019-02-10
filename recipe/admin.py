from django.contrib import admin
from django.utils.safestring import mark_safe

from recipe.models import Recipe, Ingredients, Step, UserRecipe


# Register your models here.


class IngredientsInline(admin.TabularInline):
    model = Ingredients
    min_num = 1
    extra = 0


class StepInline(admin.TabularInline):
    model = Step
    min_num = 1
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name_text', 'level', 'get_image', 'cooktime', 'text')
    search_fields = ('name_text', 'cooktime')
    list_filter = ('level',)

    def get_image(self, object):
        url = object.image.url if object.image else None
        if url:
            return mark_safe(f'<img src="{url}"/>')

    inlines = [IngredientsInline, StepInline]


class IngredientsAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('text', 'counter', 'value')


class StepAdmin(admin.ModelAdmin):
    list_display = ('text', 'number', 'get_image_step')
    list_filter = ('number',)
    search_fields = ('number',)

    def get_image_step(self, object):
        url = object.image.url if object.image else None
        if url:
            return mark_safe(f'<img src="{url}"/>')


class UserRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'get_recipe')
    list_filter = ('user',)
    readonly_fields = ('user', 'recipe', 'ingredients', 'step')

    def get_recipe(self, obj):
        return str(obj.recipe.all())

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(UserRecipe, UserRecipeAdmin)
