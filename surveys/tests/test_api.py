import datetime
import json

from django.db.models import Prefetch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from surveys.models import Survey, Question, Choice, Answer
from surveys.serializers import SurveysSerializer, SurveysRetrieveSerializer, ResultHandleSerializer


class SurveysApiTestCase(APITestCase):
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

    def test_get_list(self):
        url = reverse('survey-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_data = SurveysSerializer([self.survey_1, self.survey_2], many=True).data
        self.assertEqual(expected_data, response.data)

    def test_get_detail(self):
        url = reverse('survey-detail', args=(self.survey_1.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_data = SurveysRetrieveSerializer(self.survey_1).data
        self.assertEqual(expected_data, response.data)

    def test_content_type(self):
        url = reverse('survey-list')
        response = self.client.get(url)
        content_type = 'application/json'
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(content_type, response['Content-Type'])


class ResultApiTestCase(APITestCase):
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

    def test_create_result_w_choice(self):
        url = reverse('result-list')
        self.assertEqual(3, Answer.objects.all().count())

        data = {
            "user_id": 1,
            "survey": self.survey_1.id,
            "question": self.question_2.id,
            "choice": self.choice_1.id
        }
        json_data = json.dumps(data)

        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(4, Answer.objects.all().count())

    def test_create_result_w_text(self):
        url = reverse('result-list')
        self.assertEqual(3, Answer.objects.all().count())

        data = {
            "user_id": 1,
            "survey": self.survey_1.id,
            "question": self.question_2.id,
            "text": "Some text"
        }
        json_data = json.dumps(data)

        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(4, Answer.objects.all().count())

    def test_create_result_without_choice_text(self):
        url = reverse('result-list')
        self.assertEqual(3, Answer.objects.all().count())

        data = {
            "user_id": 1,
            "survey": self.survey_1.id,
            "question": self.question_2.id,
        }
        json_data = json.dumps(data)

        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(3, Answer.objects.all().count())

    def test_get_result(self):
        url = reverse('result-list')
        url_user_id = f"{url}?user_id=1"
        response = self.client.get(url_user_id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        queryset = Survey.objects.filter(
            answers__user_id=1).distinct().prefetch_related(
            Prefetch('answers',
                     queryset=Answer.objects.filter(user_id=1)
                     .select_related('question')
                     .select_related('choice')))
        expected_data = ResultHandleSerializer(queryset, many=True).data
        self.assertEqual(expected_data, response.data)

    def test_get_without_query_params(self):
        url = reverse('result-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

