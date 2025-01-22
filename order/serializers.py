from rest_framework import serializers
from .models import Order


class OrderListSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)  # Показывает строковое представление объектов Menu

    class Meta:
        model = Order
        fields = ('id', 'table_number', 'items', 'total_price')

class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True  # Поле только для чтения
    )

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        # Извлекаем связанные items
        items = validated_data.pop('items', [])
        # Создаем заказ
        order = Order.objects.create(**validated_data)
        # Привязываем items и пересчитываем итоговую цену
        if items:
            order.items.set(items)
            order.total_price = sum(item.price for item in order.items.all())
            order.save()
        return order

    def update(self, instance, validated_data):
        # Извлекаем связанные items
        items = validated_data.pop('items', None)
        # Обновляем данные заказа
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Пересчитываем итоговую цену, если обновляются items
        if items is not None:
            instance.items.set(items)
            instance.total_price = sum(item.price for item in instance.items.all())
        instance.save()
        return instance

class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)  # Показывает строковое представление объектов Menu

    class Meta:
        model = Order
        fields = '__all__'