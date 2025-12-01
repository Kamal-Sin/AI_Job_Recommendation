# from django.db import models

# # Create your models here.
# class Job(models.Model):
#     company_name = models.CharField(max_length=255)
#     job_title = models.CharField(max_length=255)
#     description_text = models.TextField()
#     location = models.CharField(max_length=255)
#     salary_formatted = models.CharField(max_length=100, blank=True, null=True)
#     company_rating = models.FloatField(blank=True, null=True)
#     apply_link = models.URLField(blank=True, null=True)
#     is_expired = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.job_title} at {self.company_name}"
