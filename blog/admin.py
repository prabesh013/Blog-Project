from django.contrib import admin
from .models import Post, Category, Tag, Feedback, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','date']
    class Meta:
        model = Feedback

admin.site.register(Feedback,FeedbackAdmin)

