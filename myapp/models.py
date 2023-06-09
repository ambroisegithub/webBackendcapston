from django.db import models

# Create your models here.
class MenuItem(models.Model):
    first_name = models.CharField(max_length=255)
    reservation_data = models.DateField(max_length=255)
    reservation_slot = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.first_name
    
    
class CustomUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)
    
    def __str__(self):
        return self.username        
            
    
    