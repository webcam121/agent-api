from django.db import models

from agent.apps.accounts.models import GiftReceiver
from agent.apps.basic_questions.models import BasicQuestion


class BasicAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    receiver = models.ForeignKey(GiftReceiver, on_delete=models.CASCADE, related_name='answers', null=False)
    basic_question = models.ForeignKey(BasicQuestion, on_delete=models.CASCADE, related_name='basic_answers', null=False)
    answer = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Basic Answer'
        verbose_name_plural = 'Basic Answers'

    def __str__(self):
        return self.answer
