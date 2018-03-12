from django.contrib import admin

from quora.models import Question, Answer, Topic


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'questioner']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [AnswerInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class TopicAdmin(admin.ModelAdmin):
    fields = ['topic_text', 'questions']
    inline = [QuestionInline]
    list_display = ('topic_text',)
    list_filter = ['topic_text']
    search_fields = ['topic_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)
