from django.contrib import admin
from surveys.models import Survey, Question, Choice, Answer


@admin.register(Survey)
class SurveysAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_at', 'end_at', 'description',)
    list_display_links = ('id', 'name')

    def get_readonly_fields(self, request, obj=None):
        """
        ReadOnly for update
        """
        if obj:
            return self.readonly_fields + ('start_at',)
        return self.readonly_fields


@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'survey', 'type',)


@admin.register(Choice)
class ChoicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question',)


@admin.register(Answer)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'survey', 'question', 'choice', 'text')

