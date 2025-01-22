from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.price} ₽'

    class Meta:
        db_table = 'menu'
        verbose_name = 'menu'
        verbose_name_plural = 'menu'

class Status(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Заказ в ожидании.'),
        ('ready', 'Заказ готов.'),
        ('paid', 'Заказ оплачен.'),
    ]

class Order(models.Model):
    table_number = models.IntegerField()
    items = models.ManyToManyField(Menu)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    status = models.CharField(max_length=20, choices=Status.STATUS_CHOICES, default='waiting', blank=False)

    def __str__(self):
        queryset = self.items.all()
        item_names = ", ".join(item.name for item in queryset)
        self.total_price = sum(item.price for item in queryset)

        return f"Столик {self.table_number}: {item_names}  -  (Итог: {self.total_price} ₽)"

    def save(self, *args, **kwargs):
        # Вычисляем сумму цен всех связанных items
        if self.pk:  # Проверяем, что объект уже существует в базе
            self.total_price = sum(item.price for item in self.items.all())
        super().save(*args, **kwargs)  # Вызываем оригинальный метод save()