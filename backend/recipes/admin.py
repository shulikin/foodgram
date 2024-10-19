# -*- coding: utf-8 -*-

from django.contrib import admin

import csv

from .forms import ImportForm
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import (
    FavoriteRecipe,
    Import,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)

INGREDIENT_MIN_AMOUNT = 1


class RecipeIngredientInline(admin.TabularInline):
    """Ингредиент в Рецепте"""

    model = RecipeIngredient
    extra = 1
    min_num = INGREDIENT_MIN_AMOUNT


class RecipeAdmin(admin.ModelAdmin):
    """Рецепт"""

    list_display = (
        'name',
        'author'
    )
    list_display_links = (
        'name',
        'author'
    )
    search_fields = (
        'name',
        'author__username'
    )
    search_help_text = 'Поиск по названию рецепта или `username` автора'
    filter_horizontal = ('tags',)
    list_filter = ('tags',)
    readonly_fields = ('subscriber',)
    inlines = [RecipeIngredientInline]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'author',
                    ('name', 'cooking_time', 'subscriber'),
                    'text',
                    'image',
                    'tags',
                )
            },
        ),
    )

    def subscriber(self, obj):
        """Подписки"""
        return FavoriteRecipe.objects.filter(recipe=obj).count()

    subscriber. short_description = "Добавили в избранное"


class TagAdmin(admin.ModelAdmin):
    """Тег"""

    list_display = (
        'id',
        'name',
        'slug'
    )
    list_display_links = (
        'id',
        'name',
        'slug'
    )


class IngredientAdmin(admin.ModelAdmin):
    """Ингредиент"""

    list_display = (
        'name',
        'measurement_unit'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    search_help_text = 'Поиск по названию ингредиента'

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(
            -1,
            path(
                'csv-upload/',
                self.upload_csv
            )
        )
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = ImportForm(
                request.POST,
                request.FILES
            )
            if form.is_valid():
                form_object = form.save()
                with form_object.csv_file.open(mode='r') as csv_file:
                    rows = csv.reader(
                        csv_file,
                        delimiter=','
                    )
                    for row in rows:
                        Ingredient.objects.update_or_create(
                            name=row[0],
                            measurement_unit=row[1]
                        )
                url = reverse('admin:index')
                messages.success(
                    request,
                    'Файл импортирован'
                )
                return HttpResponseRedirect(url)
        form = ImportForm()
        return render(
            request,
            'admin/csv_import_page.html',
            {'form': form}
        )


@admin.register(FavoriteRecipe, ShoppingCart)
class AuthorRecipeAdmin(admin.ModelAdmin):
    """Корзина"""

    list_display = (
        'id',
        '__str__'
    )
    list_display_links = (
        'id',
        '__str__'
    )


@admin.register(Import)
class BookImportAdmin(admin.ModelAdmin):
    list_display = (
        'csv_file',
        'date_added'
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
