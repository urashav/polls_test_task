import datetime
from django.test import TestCase

from django.db.models import Prefetch

from surveys.models import Survey, Question, Choice, Answer
from surveys.querysets import get_result_queryset


class SurveysApiTestCase(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.survey_1 = Survey.objects.create(
            name='Название 1',
            start_at=datetime.date.today(),
            end_at=datetime.date.today() + datetime.timedelta(days=1),
            description='Описание 1'
        )
        self.survey_2 = Survey.objects.create(
            name='Название 2',
            start_at=datetime.date.today(),
            end_at=datetime.date.today() + datetime.timedelta(days=1),
            description='Описание 2'
        )
        self.survey_3 = Survey.objects.create(
            name='Название 3',
            start_at=datetime.date.today() - datetime.timedelta(days=7),
            end_at=datetime.date.today() - datetime.timedelta(days=1),
            description='Описание 3'
        )

        self.question_1 = Question.objects.create(
            text='Текст 1',
            type=Question.TYPE_RADIO,
            survey=self.survey_1
        )

        self.question_2 = Question.objects.create(
            text='Текст 2',
            type=Question.TYPE_TEXT,
            survey=self.survey_1
        )

        self.question_3 = Question.objects.create(
            text='Текст 3',
            type=Question.TYPE_CHECKBOX,
            survey=self.survey_2
        )

        self.choice_1 = Choice.objects.create(text='Choice 1', question=self.question_1)
        self.choice_2 = Choice.objects.create(text='Choice 2', question=self.question_1)
        self.choice_3 = Choice.objects.create(text='Choice 3', question=self.question_1)
        self.choice_4 = Choice.objects.create(text='Choice 4', question=self.question_3)
        self.choice_5 = Choice.objects.create(text='Choice 5', question=self.question_3)

        self.answer_1 = Answer.objects.create(
            user_id=1,
            survey=self.survey_1,
            question=self.question_1,
            choice=self.choice_2
        )
        self.answer_2 = Answer.objects.create(
            user_id=1,
            survey=self.survey_2,
            question=self.question_3,
            choice=self.choice_1
        )
        self.answer_3 = Answer.objects.create(
            user_id=1,
            survey=self.survey_1,
            question=self.question_2,
            text="Текст ответа 3"
        )

    def test_get_result_queryset(self):
        user_id = 1
        queryset = get_result_queryset(user_id)
        expected_queryset = Survey.objects.filter(
            answers__user_id=user_id).distinct().prefetch_related(
            Prefetch('answers',
                     queryset=Answer.objects.filter(user_id=user_id)
                     .select_related('question')
                     .select_related('choice'))
        ).all()
        self.assertQuerysetEqual(
            queryset,
            expected_queryset,
            ordered=False,
        )
