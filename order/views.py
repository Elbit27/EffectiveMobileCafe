from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, Status
from . import serializers

class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('table_number',)
    filterset_fields = ('status',)

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

    @action(['put'], detail=True, url_path='change-status')
    def change_status(self, request, pk):
        order = self.get_object()  # Retrieve the order instance
        new_status = request.data.get('status')

        # Проверяем, передан ли новый статус
        if not new_status:
            return Response(
                {"detail": "The 'status' field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, что статус валиден
        if new_status not in dict(Status.STATUS_CHOICES).keys():
            return Response(
                {"detail": f"Invalid status. Valid options are: {', '.join(dict(Status.STATUS_CHOICES).keys())}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Обновляем статус заказа
        order.status = new_status
        order.save()

        return Response(
            {"detail": "Status updated successfully.", "new_status": new_status},
            status=status.HTTP_200_OK
        )