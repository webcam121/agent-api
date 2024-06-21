from django.db import models


class BasicQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Basic Question'
        verbose_name_plural = 'Basic Questions'
