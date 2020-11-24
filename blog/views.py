from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Feedback, Comment
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from .forms import FeedbackForm,CommentForm

def about(request):
    return render(request,'blog/about.html')

class HomeView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ['-published_date']
    paginate_by = 5 

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','text','category','tags']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','text','category','tags']
    template_name = "blog/post_update.html"

    def form_valid(self,form):
        form.instance.author = self.request.user
        form.instance.published_date = None
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = "post"
    success_url = reverse_lazy('home')
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name="blog/post_draft_list.html"
    redirect_field_name = "blog/home.html"
    context_object_name = "posts"
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('home')

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'blog/category_form.html'
    fields = ['name']
    def form_valid(self,form):
        # form.instance.author = Author.objects.get(user = self.request.user)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR,'Category names must be unique.')
            return render(request, template_name=self.template_name, context=self.get_context_data())

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = 'blog/tag_form.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self,request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.error(request, 'Tag Already Exists')
            return render(request, template_name = self.template_name, context = self.get_context_data())

def post_by_category(request, n):
    category = Category.objects.all().filter(name = n).first()

    post = Post.objects.filter(category__name = n,published_date__isnull=False).order_by('-published_date')

    category_context = {
        'category': category,
        'posts': post
    }
    return render(request, 'blog/post_by_category.html', context=category_context)

def post_by_tag(request, n):
    tag = Tag.objects.all().filter(name = n)
    post = Post.objects.filter(tags__name = n,published_date__isnull=False).order_by('-published_date')

    tag_context = {
        'tag':tag[0],
        'posts': post
    }

    return render(request, 'blog/post_by_tag.html', context=tag_context)


def user_posts(request,pk):
    try:
        a = User.objects.get(id=pk)
    except ObjectDoesNotExist:
        a = None
        print("Error")
    finally:
        if a:
            exist = True 
            posts= Post.objects.filter(author=a,published_date__isnull=False).order_by('-published_date')
            paginator = Paginator(posts, 4)

            page_number = request.GET.get('page',1)
            page_obj = paginator.get_page(page_number)
            print(page_obj)
            return render(request,'blog/user_posts.html',context={'posts':posts,'author':a,'exist':exist,'page_obj':page_obj})
        else:
            exist= False
            return render(request,'blog/user_posts.html',context={'exist':exist})

# @login_required
# def user_category_view(request,n):
#     c = Category.objects.get(name=n)
#     posts= Post.objects.filter(category=c,published_date__isnull=False).order_by('-published_date')
#     return render(request,'blog/user_category.html',context={'posts':posts,'category':c})

class UserCategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'blog/user_category.html'
    context_object_name = 'category'

    def get_queryset(self):
        a = User.objects.get(id = self.request.user.id)
        return Category.objects.filter(author = a)

class UserTagView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'blog/user_tag.html'
    context_object_name = 'tag'
    
    def get_queryset(self):
        # author = Author.objects.get(user = self.request.user)
        a = User.objects.get(id = self.request.user.id)
        return Tag.objects.filter(author = a)


def feedback_form(request):
    if request.method =="POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request,'blog/feedback_thanks.html')

    else:
        form = FeedbackForm()
        return render(request,'blog/feedback.html',{'form':form})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)