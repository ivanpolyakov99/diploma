from django.urls import path

from recipe.views import index, SignupView, recipe_details, UserRecipeView

urlpatterns = [
    path('', index, name='index'),
    path('details/<int:id>', recipe_details, name='details'),
    path('add-recipe/<int:id>', UserRecipeView.as_view(), name='add_recipe'),
    path('signup', SignupView.as_view(), name='signup')
]
