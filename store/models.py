from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    image = models.ImageField(upload_to='category_images/',
                              null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    image = models.ImageField(upload_to='sub_category_images/',
                              null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True, related_name='category_products')
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE,
                                     null=True, related_name='sub_category_products')
    image = models.ImageField(upload_to='product_images/%Y/%m/%d')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_published = models.BooleanField(default=True, verbose_name='is_available')

    def __str__(self):
        return self.name


class Order(models.Model):
    class DeliveryChoices(models.IntegerChoices):
        not_out_yet = 1, _("Not out yet")
        on_the_way = 2, _("On the way")
        delivered = 3, _("Delivered")
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    comment = models.CharField(max_length=255,
                               blank=True, null=True)  # Позволяет быть пустым и в базе данных
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2, default=0.0)  # Значение по умолчанию
    date_ordered = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=32,
                                   blank=True, null=True)
    delivery_status = models.PositiveSmallIntegerField(
        verbose_name=_("Delivery status"),
        choices=DeliveryChoices.choices,
        default=1,
    )

    def __str__(self):
        return f'Order ID: {self.id}, ' \
               f'User: {self.name}, ' \
               f'Total Price: {self.total_price}, ' \
               f'Date: {self.date_ordered}'


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=12, decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"), default=1
    )

    def __str__(self):
        return f"Order ID: {self.order.id}; " \
               f"Product ID: {self.product.id}; " \
               f"Product Name: {self.product}; " \
               f"Product Quantity: {self.quantity}"

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")