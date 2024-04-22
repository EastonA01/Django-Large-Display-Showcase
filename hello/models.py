from django.db import models
from django.utils import timezone

class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

# TODO: Write a successful improved model of the LogMessage Model utilizing the Userbase once wrote into code, so that the Logs may show who the message was logged by.

# class ChatMessage(models.Model):
#     message = models.CharField(max_length=300)
#     log_date = models.DateTimeField("date logged")
#     logged_by = models.CharField(max_length=150)

#     def __str__(self):
#         """Returns a string representation of a message. Now with Username Logs"""
#         date = timezone.localtime(self.log_date)
#         return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}, posted by {self.logged_by}"