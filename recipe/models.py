from django.db import models
# Create your models here.


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
        null=True,
        blank=True
    )
    level = models.PositiveSmallIntegerField(
        choices=LEVELS,
        default=MIN
    )

    def __str__(self):
        return self.name_text


class Ingredients(models.Model):
    text = models.CharField(max_length=150)
    counter = models.PositiveIntegerField(default=1)
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
    image = models.ImageField()
    recipe = models.ForeignKey(
        Recipe,
        related_name='steps',
        on_delete=models.CASCADE
    )
