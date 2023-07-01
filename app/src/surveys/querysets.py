from django.db.models import QuerySet, Prefetch

from surveys.models import Survey, Answer


def get_result_queryset(user_id: int) -> QuerySet:
    """
    Возвращает QuerySet результатов всех опросов
    Пройденных пользователем user_id

    :param user_id: ID пользователя
    :return QuerySet:
    """
    queryset = Survey.objects.filter(
        answers__user_id=user_id).distinct().prefetch_related(
        Prefetch('answers',
                 queryset=Answer.objects.filter(user_id=user_id)
                 .select_related('question')
                 .select_related('choice'))
    )
    return queryset
