from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()

def get_product_url(obj, url_pattern_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(url_pattern_name, kwargs= {'ct_model': ct_model,
                                              'slug': obj.slug})

class Category(models.Model):

    name = models.CharField(max_length= 255, verbose_name= 'Имя категории')
    slug = models.SlugField(unique= True)

    def __str__(self):
        return self.name

class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name= 'Категория', on_delete= models.CASCADE)
    title = models.CharField(max_length= 255, verbose_name= 'Наименование')
    slug = models.SlugField(unique= True)
    image = models.ImageField(verbose_name= 'Изображение')
    description = models.TextField(verbose_name= 'Описание', null= True)
    price = models.DecimalField(max_digits= 9, decimal_places= 2, verbose_name= 'Цена')

    def __str__(self):
        return self.title

class Notebook(Product):

    diagonal = models.CharField(max_length= 255, verbose_name= 'Диагональ')
    display = models.CharField(max_length=255, verbose_name='Дисплей')
    processor = models.CharField(max_length=255, verbose_name='Процессор')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    no_charge_time = models.CharField(max_length=255, verbose_name='Время без подзарядки')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'products')

class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display = models.CharField(max_length=255, verbose_name='Дисплей')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    camera = models.CharField(max_length=255, verbose_name='Основная камера')
    front_cam = models.CharField(max_length=255, verbose_name='Фронтальная камера')
    accum = models.CharField(max_length=255, verbose_name='Объем батареи')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'products')



class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name= 'Покупатель', on_delete= models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name= 'Корзина', on_delete= models.CASCADE, related_name= 'related_products')
    content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default= 1)
    total_price = models.DecimalField(max_digits= 9, decimal_places= 2, verbose_name= 'Общая стоимость')

    def __str__(self):
        return 'Продукт: {}'.format(self.product.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name= 'Владелец', on_delete= models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank= True, related_name= 'related_cart')
    total_products = models.PositiveIntegerField(default= 0)
    final_price = models.DecimalField(max_digits= 9, decimal_places= 2, verbose_name= 'Общая стоимость')

    def __str__(self):
        return str(self.id)

class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name= 'Пользователь', on_delete= models.CASCADE)
    phone_number = models.CharField(max_length= 20, verbose_name= 'Номер телефона')
    adress = models.CharField(max_length= 255, verbose_name= 'Адрес')

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)

# class Specific(models.Model):
#
#      content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE)
#      object_id = models.PositiveIntegerField()
#      name = models.CharField(max_length= 255, verbose_name= 'Наименование товара')
#
#      def __str__(self):
#          return 'Характеристики: {}'.format(self.name)







