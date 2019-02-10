from django.db import models
from django.conf import settings


class Recipe(models.Model):
    MIN = 1
    MAX = 5
    LEVELS = [(i, i) for i in range(MIN, MAX + 1, 1)]
    name_text = models.CharField(
        max_length=200,
        verbose_name='name'
    )
    image = models.ImageField(
        verbose_name='image',
        null=True
    )
    level = models.PositiveSmallIntegerField(
        choices=LEVELS,
        default=MIN
    )
    cooktime = models.SmallIntegerField(default=True)
    text = models.CharField(
        max_length=20,
        verbose_name='time',
        null=True
    )

    def __str__(self):
        return self.name_text

    class Meta:
        verbose_name = 'Recipe'


class Ingredients(models.Model):
    text = models.CharField(max_length=150)
    counter = models.PositiveIntegerField(default=1)
    value = models.CharField(max_length=20)
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text


class Step(models.Model):
    text = models.CharField(max_length=1000000)
    number = models.PositiveIntegerField(default=1)
    image = models.ImageField(
        blank=True,
        verbose_name='image_step',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='steps',
        on_delete=models.CASCADE
    )


class UserRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredients)
    step = models.ManyToManyField(Step)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    class Meta:
        unique_together = (
            ('recipe', 'user'),
        )
