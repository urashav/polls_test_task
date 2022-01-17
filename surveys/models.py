import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Survey(models.Model):
    """ Модель опроса """
    name = models.CharField(max_length=255, verbose_name='Название опроса')
    start_at = models.DateField(verbose_name='Дата старта')
    end_at = models.DateField(verbose_name='Дата окночания')
    description = models.TextField(null=True, verbose_name='Подробное описание')

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return f"ID {self.id}: {self.name}"

    @staticmethod
    def now_active():
        date_now = timezone.now().date()
        surveys = Survey.objects.filter(start_at__lte=date_now, end_at__gte=date_now)
        return surveys

    def clean(self):
        super().clean()
        self._date_validate()

    def _date_validate(self):
        if isinstance(self.start_at, datetime.date) and isinstance(self.end_at, datetime.date):
            if self.start_at > self.end_at:
                raise ValidationError("Дата начала опроса не может быть позже даты окончания опроса")
        else:
            raise ValidationError("Некорректная дата или дата не передана")


class Question(models.Model):
    """ Модель вопроса """
    TYPE_TEXT = 'text'
    TYPE_RADIO = 'radio'
    TYPE_CHECKBOX = 'checkbox'
    TYPES = (
        ('text', 'Ответ текстом'),
        ('radio', 'Один вариант'),
        ('checkbox', 'Несколько вариантов'),
    )

    text = models.TextField(verbose_name='Текст вопроса')
    type = models.CharField(max_length=255, choices=TYPES, verbose_name='Тип ответа')
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Опрос'
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"ID {self.id}: {self.text[:100]}"


class Choice(models.Model):
    """ Модель вариантов ответа """
    text = models.CharField(max_length=100, verbose_name='Текст')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name="Вопрос"
    )

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return f"ID {self.id}: {self.text[:100]}"


class Answer(models.Model):
    """ Модель ответов пользователя """
    text = models.TextField(null=True, verbose_name='Текст ответа')
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Опрос'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Ответ'
    )
    choice = models.ForeignKey(
        Choice,
        null=True,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вариант ответа')
    user_id = models.IntegerField(verbose_name='ID пользователя')

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"ID {self.id}"
