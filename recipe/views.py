from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import FormView, DetailView

from recipe.forms import MyModelForm, UserCreateForm, UserRecipeForm
from recipe.models import Recipe


def index(request, *args, **kwargs):
    return render(
        request,
        'recipe/index.html',
        context={
            "recipes": Recipe.objects.all(),
        }
    )


@login_required
def recipe_details(request, *args, **kwargs):
    _id = kwargs['id']
    test = get_object_or_404(Recipe, id=_id)
    form = MyModelForm()
    if request.POST:
        form = MyModelForm(request.POST)
        if form.is_valid():
            form.save()
    return render(
        request,
        'recipe/detail.html',
        context={
            "test": test,
            "form": form
        }
    )


class RecipeDetailsView(DetailView):
    template_name = 'recipe/detail.html'

    def get_object(self, queryset=None):
        return Recipe.objects.get(id=self.kwargs['id'])


@require_POST
@login_required
def add_recipe(requset, *args, **kwargs):
    recipe_id = kwargs['id']
    ingredient_ids = requset.POST.getlist(str(recipe_id))
    step_ids = requset.POST.getlist(str(recipe_id))

    form = UserRecipeForm(
        user=requset.user,
        data={
            'recipe_id': recipe_id,
            'ingredient_ids': ingredient_ids,
            'step_ids': step_ids
        }
    )
    if form.is_valid():
        form.save()
        return redirect(reverse('details', kwargs={'id': 3}))
    else:
        return HttpResponse('', status=400)


class UserRecipeView(FormView):
    form_class = UserRecipeForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        recipe_id = self.kwargs['id']
        ingredient_ids = self.request.POST.getlist(str(recipe_id))
        step_ids = self.request.POST.getlist(str(recipe_id))
        return {
            'user': self.request.user,
            'data': {
                'recipe_id': recipe_id,
                'ingredient_ids': ingredient_ids,
                'step_ids': step_ids
            }
        }

    def form_valid(self, form):
        form.save()
        return redirect(reverse('details', kwargs={'id': form.ingredient.recipe.id}))

    def form_invalid(self, form):
        return redirect(reverse('details', kwargs={'id': form.ingredient.recipe.id}))


class SignupView(FormView):
    form_class = UserCreateForm
    template_name = 'recipe/signup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        user = authenticate(
            request=self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return super().form_valid(form)
