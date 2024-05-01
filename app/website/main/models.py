from django.db import models
from django.contrib.auth.models import User
    
class Task(models.Model):
    STATUS_CHOICES = (
        ('do zrobienia', 'Do zrobienia'),
        ('w trakcie', 'W trakcie'),
        ('zakończone', 'Zakończone')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks_assigned', blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')

    def __str__(self):
        return self.title + "\n" + self.description