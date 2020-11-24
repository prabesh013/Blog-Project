from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # image = models.ImageField(default='default.png',upload_to='profile_pics')
    image  = CloudinaryField('image',default='https://res.cloudinary.com/prabesh-media/image/upload/v1606198637/default_b4zesp.png')
    # image = https://res.cloudinary.com/prabesh-media/image/upload/v1606198637/default_b4zesp.png
    def __str__(self):
        return f'{self.user.username} Profile'
    
    # def save(self,*args,**kwargs):
    #     super(UserProfile, self).save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
        # else:
        #     output_size = (300,300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
