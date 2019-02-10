from django import forms
from django.contrib.auth.forms import UserCreationForm

from recipe.models import Recipe, UserRecipe


class MyModelForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'level', 'cooktime', 'text')


class UserRecipeForm(forms.Form):
    recipe_id = forms.IntegerField()
    ingredient_ids = forms.MultipleChoiceField()
    step_ids = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.recipe = None
        super().__init__(*args, **kwargs)
        self.fields['ingredient_ids'].clean = lambda x: x
        self.fields['step_ids'].clean = lambda x: x

    def save(self):
        user_recipe = UserRecipe.objects.create(
            recipe=self.cleaned_data['recipe_id'],
            user=self.user
        )
        user_recipe.recipe.add(*self.cleaned_data['ingredient_ids'])
        user_recipe.recipe.add(*self.cleaned_data['step_ids'])


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = () + UserCreationForm.Meta.fields
