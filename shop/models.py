from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


from users.models import CustomUser


class Category(MPTTModel):
    name = models.CharField(max_length=128)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']


class Manufacturer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Product(models.Model):
    SEASON_CHOICES = (
        ('all', 'Всесезоная'),
        ('sum', 'Зимняя'),
        ('win', 'Летняя'),
    )
    category = models.ManyToManyField(Category, verbose_name='Категория', null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель', null=True)
    name = models.CharField(max_length=128)
    season = models.CharField(max_length=3, choices=SEASON_CHOICES, verbose_name='Сезонность')
    price = models.PositiveIntegerField(default=0, verbose_name='стоимость')
    short_description = models.CharField(max_length=50, verbose_name='Короткое описание', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    attributes = models.JSONField(null=True, blank=True, verbose_name='Атрибуты')
    image = models.ImageField(upload_to='products-image/', verbose_name='Изображение товара', null=True)

    def __str__(self):
        return f'Товар {self.name}, производитель {self.manufacturer.name} '


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Товар {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'Заказанный товар: {self.product.name}'

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(OrderItem)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f'Order for {self.user.username}'

    class Meta:
        ordering = ["-created_timestamp"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
