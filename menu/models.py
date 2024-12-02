from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(upload_to='dishes/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return self.name
