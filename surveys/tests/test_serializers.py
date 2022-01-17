from django.db.models import Prefetch
from django.test import TestCase
from rest_framework.test import APITestCase

from surveys.models import Survey, Question, Choice, Answer
from surveys.serializers import (SurveysSerializer,
                                 QuestionsSerializer,
                                 ChoicesSerializer,
                                 QuestionsChoicesSerializer,
                                 SurveysRetrieveSerializer,
                                 AnswersSerializer,
                                 CreateAnswerSerializer,
                                 ResultHandleSerializer
                                 )


class SerializersTestCase(TestCase):
    def setUp(self) -> None:
        self.survey_1 = Survey.objects.create(
            name='Название 1',
            start_at='2022-01-02',
            end_at='2022-01-02',
            description='Описание 1'
        )
        self.survey_2 = Survey.objects.create(
            name='Название 2',
            start_at='2022-01-02',
            end_at='2022-01-02',
            description='Описание 2'
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

    def test_survey_with_url_serializer(self):
        data = SurveysSerializer([self.survey_1, self.survey_2], context={'request': None}, many=True).data
        expected_data = [
            {
                'id': self.survey_1.id,
                'name': 'Название 1',
                'start_at': '2022-01-02',
                'end_at': '2022-01-02',
                'description': 'Описание 1',
            },
            {
                'id': self.survey_2.id,
                'name': 'Название 2',
                'start_at': '2022-01-02',
                'end_at': '2022-01-02',
                'description': 'Описание 2',
            },
        ]
        self.assertEqual(expected_data, data)

    def test_choice_serializer(self):
        data = ChoicesSerializer([
            self.choice_1,
            self.choice_2,
            self.choice_3,
            self.choice_4,
            self.choice_5],
            many=True).data

        expected_data = [
            {
                'id': self.choice_1.id,
                'text': 'Choice 1',
            },
            {
                'id': self.choice_2.id,
                'text': 'Choice 2',
            },
            {
                'id': self.choice_3.id,
                'text': 'Choice 3',
            },
            {
                'id': self.choice_4.id,
                'text': 'Choice 4',
            },
            {
                'id': self.choice_5.id,
                'text': 'Choice 5',
            },
        ]

        self.assertEqual(expected_data, data)

    def test_question_without_choices_serializer(self):
        data = QuestionsSerializer([self.question_1, self.question_2, self.question_3], many=True).data
        expected_data = [
            {
                'id': self.question_1.id,
                'text': 'Текст 1',
                'type': Question.TYPE_RADIO,
            },
            {
                'id': self.question_2.id,
                'text': 'Текст 2',
                'type': Question.TYPE_TEXT,
            },
            {
                'id': self.question_3.id,
                'text': 'Текст 3',
                'type': Question.TYPE_CHECKBOX,
            },
        ]
        self.assertEqual(expected_data, data)

    def test_question_with_choices_serializer(self):
        data = QuestionsChoicesSerializer([self.question_1, self.question_2, self.question_3], many=True).data
        expected_data = [
            {
                'id': self.question_1.id,
                'text': 'Текст 1',
                'type': Question.TYPE_RADIO,
                'choices': [
                    {
                        'id': self.choice_1.id,
                        'text': 'Choice 1'
                    },
                    {
                        'id': self.choice_2.id,
                        'text': 'Choice 2'
                    },
                    {
                        'id': self.choice_3.id,
                        'text': 'Choice 3'
                    },
                ]
            },
            {
                'id': self.question_2.id,
                'text': 'Текст 2',
                'type': Question.TYPE_TEXT,
                'choices': []
            },
            {
                'id': self.question_3.id,
                'text': 'Текст 3',
                'type': Question.TYPE_CHECKBOX,
                'choices': [
                    {
                        'id': self.choice_4.id,
                        'text': 'Choice 4'
                    },
                    {
                        'id': self.choice_5.id,
                        'text': 'Choice 5'
                    },
                ]
            },
        ]
        self.assertEqual(expected_data, data)

    def test_retrieve_surveys_serializer(self):
        data = SurveysRetrieveSerializer([self.survey_1, self.survey_2], many=True).data
        expected_data = [
            {
                'id': self.survey_1.id,
                'name': 'Название 1',
                'start_at': '2022-01-02',
                'end_at': '2022-01-02',
                'description': 'Описание 1',
                'questions': [
                    {
                        'id': self.question_1.id,
                        'text': 'Текст 1',
                        'type': Question.TYPE_RADIO,
                        'choices': [
                            {
                                'id': self.choice_1.id,
                                'text': 'Choice 1'
                            },
                            {
                                'id': self.choice_2.id,
                                'text': 'Choice 2'
                            },
                            {
                                'id': self.choice_3.id,
                                'text': 'Choice 3'
                            },
                        ]
                    },
                    {
                        'id': self.question_2.id,
                        'text': 'Текст 2',
                        'type': Question.TYPE_TEXT,
                        'choices': []
                    },
                ]
            },
            {
                'id': self.survey_2.id,
                'name': 'Название 2',
                'start_at': '2022-01-02',
                'end_at': '2022-01-02',
                'description': 'Описание 2',
                'questions': [
                    {
                        'id': self.question_3.id,
                        'text': 'Текст 3',
                        'type': Question.TYPE_CHECKBOX,
                        'choices': [
                            {
                                'id': self.choice_4.id,
                                'text': 'Choice 4'
                            },
                            {
                                'id': self.choice_5.id,
                                'text': 'Choice 5'
                            },
                        ]
                    },
                ]
            },
        ]
        self.assertEqual(expected_data, data)

    def test_answers_serializer(self):
        data = AnswersSerializer([self.answer_1, self.answer_2, self.answer_3], many=True).data
        expected_data = [
            {
                'id': self.answer_1.id,
                'user_id': 1,
                'survey': self.survey_1.id,
                'question':
                    {
                        'id': self.question_1.id,
                        'text': 'Текст 1',
                        'type': Question.TYPE_RADIO,
                    },
                'choice':
                    {
                        'id': self.choice_2.id,
                        'text': 'Choice 2',
                    },
                'text': None
            },
            {
                'id': self.answer_2.id,
                'user_id': 1,
                'survey': self.survey_2.id,
                'question':
                    {
                        'id': self.question_3.id,
                        'text': 'Текст 3',
                        'type': Question.TYPE_CHECKBOX,
                    },
                'choice':
                    {
                        'id': self.choice_1.id,
                        'text': 'Choice 1',
                    },
                'text': None
            },
            {
                'id': self.answer_3.id,
                'user_id': 1,
                'survey': self.survey_1.id,
                'question':
                    {
                        'id': self.question_2.id,
                        'text': 'Текст 2',
                        'type': Question.TYPE_TEXT,
                    },
                'choice': None,
                'text': "Текст ответа 3"
            },
        ]
        self.assertEqual(expected_data, data)

    def test_create_answer_serializer(self):
        test_w_choice = CreateAnswerSerializer(data={
            'survey': self.survey_1.id,
            'question': self.question_2.id,
            'choice': self.choice_2.id,
            'user_id': 1
        })

        test_w_text = CreateAnswerSerializer(data={
            'survey': self.survey_1.id,
            'question': self.question_2.id,
            'text': "Текст 1",
            'user_id': 1
        })

        self.assertTrue(test_w_choice.is_valid())
        self.assertTrue(test_w_text.is_valid())

    def test_create_answer_without_text_or_choice_serializer(self):
        data = CreateAnswerSerializer(data={
            'survey': self.survey_1.id,
            'question': self.question_2.id,
            'user_id': 1
        })

        self.assertFalse(data.is_valid())

    def test_result_handler(self):
        queryset = Survey.objects.filter(
            answers__user_id=1).distinct().prefetch_related(
            Prefetch('answers',
                     queryset=Answer.objects.filter(user_id=1)
                     .select_related('question')
                     .select_related('choice'))
        ).all()
        data = ResultHandleSerializer(queryset, many=True, context={'request': None}).data
        expected_data = [
            {
                'id': self.survey_1.id,
                'name': 'Название 1',
                'start_at': '2022-01-02',
                'end_at': '2022-01-02',
                'description': 'Описание 1',
                'answers': [{
                    'id': self.answer_1.id,
                    'user_id': 1,
                    'survey': self.survey_1.id,
                    'question':
                        {
                            'id': self.question_1.id,
                            'text': 'Текст 1',
                            'type': Question.TYPE_RADIO,
                        },
                    'choice':
                        {
                            'id': self.choice_2.id,
                            'text': 'Choice 2',
                        },
                    'text': None
                }, {
                    'id': self.answer_3.id,
                    'user_id': 1,
                    'survey': self.survey_1.id,
                    'question':
                        {
                            'id': self.question_2.id,
                            'text': 'Текст 2',
                            'type': Question.TYPE_TEXT,
                        },
                    'choice': None,
                    'text': "Текст ответа 3"
                }, ]

            },
            {
                'id': self.survey_2.id,
                'name': 'Название 2',
                'start_at': '2022-01-02',
                'end_at': '2022-01-02',
                'description': 'Описание 2',
                'answers': [{
                    'id': self.answer_2.id,
                    'user_id': 1,
                    'survey': self.survey_2.id,
                    'question':
                        {
                            'id': self.question_3.id,
                            'text': 'Текст 3',
                            'type': Question.TYPE_CHECKBOX,
                        },
                    'choice':
                        {
                            'id': self.choice_1.id,
                            'text': 'Choice 1',
                        },
                    'text': None
                },
                ]
            },
        ]
        self.assertEqual(expected_data, data)
