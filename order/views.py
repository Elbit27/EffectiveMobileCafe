from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from . import serializers

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def perform_create(self, serializer):           # сохраняет объект в базу данных
        serializer.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.OrderListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.OrderCreateUpdateSerializer
        elif self.action == 'retrieve':
            return serializers.OrderDetailSerializer

    # переопределяем метод destroy, чтобы он при удалении выводил сообщение об успешном удалении.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем объект по ID
        self.perform_destroy(instance)  # Удаляем объект
        return Response({"detail": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

