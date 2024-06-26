from django.db import models

# Create your models here.
# Defines database tables using models. (Veritabanı tablolarını temsil eden modelleri tanımlar.)

# Defines projects model. (Proje modelini tanımlar)
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="blogs")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Defines user profile information model. (Kullanıcı profili bilgi modelini tanımlar)    
class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    experience_years = models.PositiveIntegerField()
    happy_customers = models.PositiveIntegerField()
    projects_finished = models.PositiveIntegerField()
    digital_awards = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    