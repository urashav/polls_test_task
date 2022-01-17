from rest_framework import serializers

from surveys.models import Survey, Question, Choice, Answer


class ChoicesSerializer(serializers.ModelSerializer):
    """ Варианты ответов """

    class Meta:
        model = Choice
        fields = ('id', 'text')


class QuestionsSerializer(serializers.ModelSerializer):
    """ Вопросы без вариантов ответов """

    class Meta:
        model = Question
        fields = ('id', 'text', 'type')


class QuestionsChoicesSerializer(serializers.ModelSerializer):
    """ Вопросы с вариантами ответа """
    choices = ChoicesSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'choices')


class SurveysSerializer(serializers.ModelSerializer):
    """ Опросы """

    class Meta:
        model = Survey
        fields = ('id', 'name', 'start_at', 'end_at', 'description')


class SurveysRetrieveSerializer(serializers.ModelSerializer):
    """ Детали опроса """
    questions = QuestionsChoicesSerializer(read_only=True, many=True)

    class Meta:
        model = Survey
        fields = ('id', 'name', 'start_at', 'end_at', 'description', 'questions')


class AnswersSerializer(serializers.ModelSerializer):
    """ Ответы пользователя """
    question = QuestionsSerializer(read_only=True)
    choice = ChoicesSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'user_id', 'survey', 'question', 'choice', 'text')


class ResultHandleSerializer(serializers.ModelSerializer):
    """ Результаты всех пройденных опросов пользователем """
    answers = AnswersSerializer(read_only=True, many=True)

    class Meta:
        model = Survey
        fields = ('id', 'name', 'start_at', 'end_at', 'description', 'answers')


class CreateAnswerSerializer(serializers.ModelSerializer):
    """ Ответы пользователя для записи в базу """

    class Meta:
        model = Answer
        fields = ('id', 'survey', 'question', 'choice', 'text', 'user_id')

    def validate(self, attrs):
        message = "Введите текст или выберите подходящий вариант ответа."

        if not any([attrs.get('text'), attrs.get('choice')]):
            raise serializers.ValidationError(message, code='required')
        return attrs
