from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    icon = models.ImageField(upload_to='service-category-icons/')
    basePrice = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name
