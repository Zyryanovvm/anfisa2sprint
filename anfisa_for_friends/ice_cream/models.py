from django.contrib import admin
from django.db import models

from core.models import PublishedModel


class Category(PublishedModel):
    title = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Слаг', max_length=64, unique=True)
    output_order = models.PositiveSmallIntegerField(verbose_name='Порядок отображения', default=100)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Topping(PublishedModel):
    title = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Слаг', max_length=64, unique=True)

    class Meta:
        verbose_name = 'топпинг'
        verbose_name_plural = 'Топпинги'

    def __str__(self):
        return self.title


class Wrapper(PublishedModel):
    title = models.CharField(verbose_name='Название',
                             max_length=256,
                             help_text='Уникальное название обёртки, не более 256 символов')

    class Meta:
        verbose_name = 'обертка'
        verbose_name_plural = 'Обертки'

    def __str__(self):
        return self.title


class IceCream(PublishedModel):
    title = models.CharField(verbose_name='Название', max_length=256)
    description = models.TextField(verbose_name='Описание')
    wrapper = models.OneToOneField(
        Wrapper,
        on_delete=models.SET_NULL,
        related_name='ice_cream',
        null=True,
        blank=True,
        verbose_name='Обёртка'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='ice_creams',
        verbose_name='Категория'
    )
    toppings = models.ManyToManyField(Topping, verbose_name='Топпинги')
    is_on_main = models.BooleanField(verbose_name='На главную', default=False)

    class Meta:
        verbose_name = 'Мороженое'
        verbose_name_plural = 'Мороженое'

    def __str__(self):
        return self.title


class IceCreamAdmin(admin.ModelAdmin):
    #  Какие поля будут показаны на странице списка объектов
    list_display = (
        'title',
        'description',
        'is_published',
        'is_on_main',
        'category',
        'wrapper'
    )
    #  Какие поля можно редактировать прямо на странице списка объектов
    list_editable = (
        'is_published',
        'is_on_main',
        'category'
    )
    #  Кортеж с перечнем полей, по которым будет проводиться поиск
    search_fields = ('title',)
    #  Кортеж с полями, по которым можно фильтровать записи.
    list_filter = ('category',)
    #  Поля, при клике на которые можно перейти на страницу просмотра и редактирования записи
    list_display_links = ('title',)
    #  По умолчанию вместо "-" будет выводится
    empty_value_display = 'Не задано'
    # Указываем, для каких связанных моделей нужно включить интерфейс отдельной таблички с выбором:
    filter_horizontal = ('toppings',)


# Для отображения связанных записей в таблицу Категории
# TabularInline - в линию
# StackedInline - в таблицу
class IceCreamInline(admin.TabularInline):
    model = IceCream
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        IceCreamInline,
    )
    list_display = (
        'title',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(IceCream, IceCreamAdmin)
