import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError

from surveys.models import Survey, Question, Choice, Answer


class SurveyModelTestCase(TestCase):
    def setUp(self) -> None:
        self.survey = Survey.objects.create(
            name='Опрос',
            start_at=datetime.datetime.today(),
            end_at=datetime.datetime.today() + datetime.timedelta(days=1),
            description='Описание'
        )

    def test_model_verbose_name(self):
        survey = Survey.objects.get(pk=self.survey.id)

        verbose_name = survey._meta.verbose_name
        verbose_name_plural = survey._meta.verbose_name_plural

        self.assertEqual('Опрос', verbose_name)
        self.assertEqual('Опросы', verbose_name_plural)

    def test_name_verbose_name(self):
        survey = Survey.objects.get(pk=self.survey.id)
        verbose_name = survey._meta.get_field('name').verbose_name
        self.assertEqual('Название опроса', verbose_name)

    def test_name_max_length(self):
        survey = Survey.objects.get(pk=self.survey.id)
        max_length = survey._meta.get_field('name').max_length
        self.assertEqual(255, max_length)

    def test_start_at_verbose_name(self):
        survey = Survey.objects.get(pk=self.survey.id)
        verbose_name = survey._meta.get_field('start_at').verbose_name
        self.assertEqual('Дата старта', verbose_name)

    def test_end_at_verbose_name(self):
        survey = Survey.objects.get(pk=self.survey.id)
        verbose_name = survey._meta.get_field('end_at').verbose_name
        self.assertEqual('Дата окночания', verbose_name)

    def test_description_verbose_name(self):
        survey = Survey.objects.get(pk=self.survey.id)
        verbose_name = survey._meta.get_field('description').verbose_name
        self.assertEqual('Подробное описание', verbose_name)

    def test_active_survey(self):
        survey = Survey.objects.get(pk=self.survey.id)
        self.assertTrue(survey.now_active())

    def test_expired_survey(self):
        Survey.objects.create(
            name='Опрос 2',
            start_at=datetime.datetime.today() - datetime.timedelta(days=2),
            end_at=datetime.datetime.today() - datetime.timedelta(days=1),
            description='Описание 2'
        )
        surveys = Survey.objects.all()
        active_surveys = Survey.now_active()

        self.assertEqual(2, surveys.count())
        self.assertEqual(1, active_surveys.count())

    def test_model_returned_str(self) -> None:
        survey = Survey.objects.get(pk=self.survey.id)
        self.assertEqual(f"ID {survey.id}: {survey.name}", survey.__str__())

    def test_date_validate(self):
        survey = Survey(
            name='Опрос 2',
            start_at=datetime.datetime.today(),
            end_at=datetime.datetime.today() - datetime.timedelta(days=1),
            description='Описание 2'
        )
        self.assertRaises(ValidationError, survey.full_clean)

    def test_date_empty(self):
        survey = Survey(
            name='Опрос 2',
            start_at=datetime.datetime.today(),
            end_at=None,
            description='Описание 2'
        )
        self.assertRaises(ValidationError, survey.full_clean)


class QuestionModelTestCase(TestCase):
    def setUp(self) -> None:
        self.survey = Survey.objects.create(
            name='Опрос',
            start_at=datetime.datetime.today(),
            end_at=datetime.datetime.today() + datetime.timedelta(days=1),
            description='Описание'
        )
        self.question = Question.objects.create(
            text='Текст 1',
            type=Question.TYPE_RADIO,
            survey=self.survey
        )

    def test_model_verbose_name(self):
        question = Question.objects.get(pk=self.question.id)
        verbose_name = question._meta.verbose_name
        verbose_name_plural = question._meta.verbose_name_plural

        self.assertEqual('Вопрос', verbose_name)
        self.assertEqual('Вопросы', verbose_name_plural)

    def test_text_verbose_name(self):
        question = Question.objects.get(pk=self.question.id)
        verbose_name = question._meta.get_field('text').verbose_name
        self.assertEqual('Текст вопроса', verbose_name)

    def test_type_verbose_name(self):
        question = Question.objects.get(pk=self.question.id)
        verbose_name = question._meta.get_field('type').verbose_name
        self.assertEqual('Тип ответа', verbose_name)

    def test_type_max_length(self):
        question = Question.objects.get(pk=self.question.id)
        max_length = question._meta.get_field('type').max_length
        self.assertEqual(255, max_length)

    def test_survey_verbose_name(self):
        question = Question.objects.get(pk=self.question.id)
        verbose_name = question._meta.get_field('survey').verbose_name
        self.assertEqual('Опрос', verbose_name)

    def test_types(self):
        self.assertTrue(Question.TYPE_RADIO == 'radio')
        self.assertTrue(Question.TYPE_TEXT == 'text')
        self.assertTrue(Question.TYPE_CHECKBOX == 'checkbox')

        types = (
            (Question.TYPE_TEXT, 'Ответ текстом'),
            (Question.TYPE_RADIO, 'Один вариант'),
            (Question.TYPE_CHECKBOX, 'Несколько вариантов'),
        )

        self.assertTupleEqual(types, Question.TYPES)

    def test_relations(self):
        self.assertEqual(self.survey, self.question.survey)
        self.assertEqual(True, self.question in self.survey.questions.all())

    def test_model_returned_str(self):
        question = Question.objects.get(pk=self.question.id)

        self.assertEqual(f"ID {question.id}: {question.text[:100]}", question.__str__())


class ChoiceModelTestCase(TestCase):
    def setUp(self) -> None:
        self.survey = Survey.objects.create(
            name='Опрос',
            start_at=datetime.datetime.today(),
            end_at=datetime.datetime.today() + datetime.timedelta(days=1),
            description='Описание'
        )
        self.question = Question.objects.create(
            text='Текст 1',
            type=Question.TYPE_RADIO,
            survey=self.survey
        )

        self.choice = Choice.objects.create(text='Choice 1', question=self.question)

    def test_text_verbose_name(self):
        choice = Choice.objects.get(id=self.choice.id)
        expected_field = choice._meta.get_field('text').verbose_name
        self.assertEqual('Текст', expected_field)

    def test_text_max_length(self):
        choice = Choice.objects.get(id=self.choice.id)
        expected_field = choice._meta.get_field('text').max_length
        self.assertEqual(100, expected_field)

    def test_question_verbose_name(self):
        choice = Choice.objects.get(id=self.choice.id)
        expected_field = choice._meta.get_field('question').verbose_name
        self.assertEqual('Вопрос', expected_field)

    def test_relations(self):
        choice = Choice.objects.get(id=self.choice.id)

        self.assertEqual(self.question, choice.question)
        self.assertEqual(True, choice in self.question.choices.all())

    def test_model_verbose_name(self):
        choice = Choice.objects.get(id=self.choice.id)

        verbose_name = choice._meta.verbose_name
        verbose_name_plural = choice._meta.verbose_name_plural

        self.assertEqual(verbose_name, 'Вариант ответа')
        self.assertEqual(verbose_name_plural, 'Варианты ответов')

    def test_model_returned_str(self):
        choice = Choice.objects.get(id=self.choice.id)

        self.assertEqual(f"ID {choice.id}: {choice.text[:100]}", choice.__str__())


class AnswerModelTestCase(TestCase):
    def setUp(self) -> None:
        self.survey = Survey.objects.create(
            name='Опрос',
            start_at=datetime.datetime.today(),
            end_at=datetime.datetime.today() + datetime.timedelta(days=1),
            description='Описание'
        )
        self.question = Question.objects.create(
            text='Текст 1',
            type=Question.TYPE_RADIO,
            survey=self.survey
        )

        self.choice = Choice.objects.create(text='Choice 1', question=self.question)

        self.answer = Answer.objects.create(
            user_id=1,
            survey=self.survey,
            question=self.question,
            choice=self.choice
        )

    def test_user_id_verbose_name(self):
        answer = Answer.objects.get(id=self.answer.id)
        verbose_name = answer._meta.get_field('user_id').verbose_name

        self.assertEqual('ID пользователя', verbose_name)

    def test_text_verbose_name(self):
        answer = Answer.objects.get(id=self.answer.id)
        verbose_name = answer._meta.get_field('text').verbose_name

        self.assertEqual('Текст ответа', verbose_name)

    def test_survey_verbose_name(self):
        answer = Answer.objects.get(id=self.answer.id)
        verbose_name = answer._meta.get_field('survey').verbose_name

        self.assertEqual('Опрос', verbose_name)

    def test_question_verbose_name(self):
        answer = Answer.objects.get(id=self.answer.id)
        verbose_name = answer._meta.get_field('question').verbose_name

        self.assertEqual('Ответ', verbose_name)

    def test_choice_verbose_name(self):
        answer = Answer.objects.get(id=self.answer.id)
        verbose_name = answer._meta.get_field('choice').verbose_name

        self.assertEqual('Вариант ответа', verbose_name)

    def test_model_verbose_name(self):
        answer = Answer.objects.get(id=self.answer.id)

        verbose_name = answer._meta.verbose_name
        verbose_name_plural = answer._meta.verbose_name_plural

        self.assertEqual('Ответ', verbose_name)
        self.assertEqual('Ответы', verbose_name_plural)

    def test_model_returned_str(self):
        answer = Answer.objects.get(id=self.answer.id)

        self.assertEqual(f"ID {answer.id}", answer.__str__())

    def test_survey_relation(self):
        answer = Answer.objects.get(id=self.answer.id)

        self.assertEqual(self.survey, answer.survey)
        self.assertEqual(True, answer in self.survey.answers.all())

    def test_question_relation(self):
        answer = Answer.objects.get(id=self.answer.id)

        self.assertEqual(self.question, answer.question)
        self.assertEqual(True, answer in self.question.answers.all())

    def test_choice_relation(self):
        answer = Answer.objects.get(id=self.answer.id)

        self.assertEqual(self.choice, answer.choice)
        self.assertEqual(True, answer in self.choice.answers.all())

