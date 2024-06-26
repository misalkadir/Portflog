from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.

# Defines categories and automatically creates slug fields. (Kategorileri tanımlar ve slug alanını otomatik oluşturur.)
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False,blank=True, unique=True, db_index=True, editable=False, max_length=50)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Defines blog entries and automatically creates slug fields. (Blogları tanımlar ve slug alanını otomatik oluşturur.)
class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blogs")
    description = RichTextField()
    is_active = models.BooleanField()
    is_home = models.BooleanField()
    slug = models.SlugField(default="",blank=True,null=False, unique=True, db_index=True, editable=False)
    categories = models.ManyToManyField(Category, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



