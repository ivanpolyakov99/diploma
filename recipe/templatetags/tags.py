from django import template
from recipe.models import UserRecipe

register = template.Library()


@register.filter('check_recipe')
def check_recipe(recipe, user):
    user_recipes = UserRecipe.objects.all(
        user=user,
        recipe=recipe
    ).first()
    if not user_recipes:
        return
    recipes = user_recipes.recipe.filter(
    ).values_list('is_correct', flat=True)
    return all(recipes)
