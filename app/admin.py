from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient

# Register your models here.


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "instructions",
        "cooking_time",
        "description",
        # "ingredient",#this many to many field which cannot show on admin panel it throws error
        "image_url",
    ]


@admin.register(RecipeIngredient)
class RecipeIngredient(admin.ModelAdmin):
    list_display = [
        "id",
        "recipe",
        "ingredient",
    ]
