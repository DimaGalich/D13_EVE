from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import ReplyForm, PostForm
from .models import Post, Reply, Author, Category


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = ''
    form_class = PostForm
    template_name = 'post_create.html'

    def post(self, request, *args, **kwargs):
        obj = Post(
            title=request.POST['title'],
            content=request.POST['content'],
            category=Category.objects.get(id=request.POST['category']),
            author=Author.objects.get(name=request.user)
        )
        obj.save()
        return redirect('index')

class IndexView(ListView):
    model = Post
    ordering = '-created'
    template_name = 'index.html'
    context_object_name = 'posts'

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    success_url = reverse_lazy('index')
    fields = ['title', 'content', 'category']
    template_name = 'post_update.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('index')
    template_name = 'post_delete.html'

class PostDetailView(DetailView):
    model = Post
    ordering = '-created'
    template_name = 'post_detail.html'
    context_object_name = 'post'


# Not the best fulfillment ...
@login_required
def reply(request, pk):
    author, status = Author.objects.get_or_create(name=request.user)
    post = Post.objects.get(id=pk)
    form = ReplyForm()
    context = {'post': post,
               'form': form,
               'author': author
               }
    return render(request, 'reply.html', context)


def replied(request, pk):
    content = request.POST['content']
    author = Author.objects.get(name=request.user)
    post = Post.objects.get(id=pk)
    Reply.objects.create(author=author, post=post, content=content)
    return redirect('index')


class PrivateOfficeView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'private_office.html'
    context_object_name = 'replies'

    def get_queryset(self):
        author, status = Author.objects.get_or_create(name=self.request.user)
        queryset = Reply.objects.filter(post__author=author).order_by('-created')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['current_user'] = Author.objects.get(name=self.request.user)
        return context


class SortedByPostView(ListView):
    model = Reply
    template_name = 'replies_by_post.html'
    ordering = '-created'
    context_object_name = 'replies'

    def get_queryset(self):
        queryset = Reply.objects.filter(post=Post.objects.get(id=self.kwargs['post_id']))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['this_post'] = Post.objects.get(id=self.kwargs['post_id'])
        return context


class ReplyDetailView(DetailView):
    model = Reply
    ordering = '-created'
    template_name = 'reply_detail.html'
    context_object_name = 'reply'


class ReplyDeleteView(DeleteView):
    model = Reply
    success_url = reverse_lazy('private_office')
    template_name = 'reply_delete.html'


def reply_approve(request, pk):
    obj = Reply.objects.get(id=pk)
    obj.approved = True
    obj.save()
    return redirect('/private')


@login_required
def subscribe(request):
    obj = Author.objects.get(name=request.user)
    obj.is_subscriber = True
    obj.save()
    return redirect('/private')


@login_required
def unsubscribe(request):
    obj = Author.objects.get(name=request.user)
    obj.is_subscriber = False
    obj.save()
    return redirect('/private')
