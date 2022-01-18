from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, exceptions
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from surveys.models import Survey
from surveys.querysets import get_result_queryset
from surveys.serializers import (
    SurveysSerializer,
    SurveysRetrieveSerializer,
    CreateAnswerSerializer,
    ResultHandleSerializer
)


class ActiveSurveysViewSet(viewsets.ReadOnlyModelViewSet):
    """
        Активные опросы
    """

    def get_serializer_class(self):
        if 'list' in self.action:
            return SurveysSerializer
        if 'retrieve' in self.action:
            return SurveysRetrieveSerializer

    def get_queryset(self):
        if 'list' in self.action:
            return Survey.now_active()
        if 'retrieve' in self.action:
            return Survey.now_active().prefetch_related('questions__choices')


class ResultViewSet(
    CreateModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet
):
    """
        Результаты опросов пользователя
    """
    user_id_param = openapi.Parameter(
        'user_id',
        openapi.IN_QUERY,
        description="Обязательный параметр user_id",
        type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[user_id_param])
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def get_serializer_class(self):
        if 'create' in self.action:
            return CreateAnswerSerializer
        if 'list' in self.action:
            return ResultHandleSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            raise exceptions.ParseError('Требуется user_id')

        queryset = get_result_queryset(int(user_id))
        return queryset

