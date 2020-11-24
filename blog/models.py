from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(help_text='Generated automatically',max_length=100, unique=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # return reverse('post_by_category', args = [self.slug])
        # return reverse('home')
        return reverse('post_create')
    
    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Tags')
    slug = models.SlugField(help_text='Generated automatically',max_length=100, unique=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.CASCADE)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag,self).save(*args, **kwargs)

    def get_absolute_url(self):
        # return reverse('post_by_tag', args = [self.slug])
        # return reverse('home')
        return reverse('post_create')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True, help_text='Generated automatically',max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('post_draft_list')

    def save(self, *args, **kwargs):
        slug_str = f"{self.title} {self.id}" 
        self.slug = slugify(slug_str)
        super(Post, self).save(*args, **kwargs)    

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

class Feedback(models.Model):
     name = models.CharField(max_length=200, help_text="Name")
     email = models.EmailField(max_length=200, help_text="Email")
     subject = models.CharField(max_length=150, help_text="Subject")
     message = models.TextField()
     date = models.DateTimeField(default=timezone.now)

     def __str__(self):
         return self.name+ "|" + self.email

    #  def get_absolut_url(self):
    #      return reverse('feedback')

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("home")

    def __str__(self):
        return f"{self.text} | {self.author}" 