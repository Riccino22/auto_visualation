from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    regist_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class CSVData(models.Model):
    title = models.CharField(max_length=200)
    file_name = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    data_json = models.JSONField(default=dict)  # Store the CSV content as JSON
    
    def __str__(self):
        return self.title