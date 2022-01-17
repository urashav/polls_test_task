from django.db.models import Prefetch
from rest_framework import viewsets, exceptions

from surveys.models import Survey, Answer
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


class ResultViewSet(viewsets.ModelViewSet):
    """
        Результаты опросов пользователя
    """

    def get_serializer_class(self):
        if 'create' in self.action:
            return CreateAnswerSerializer
        if 'list' in self.action:
            return ResultHandleSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            raise exceptions.ParseError('Требуется user_id')

        queryset = Survey.objects.filter(
            answers__user_id=user_id).distinct().prefetch_related(
            Prefetch('answers',
                     queryset=Answer.objects.filter(user_id=user_id)
                     .select_related('question')
                     .select_related('choice'))
        )
        return queryset
