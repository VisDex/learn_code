from django.contrib.auth.models import User
from django.views.generic import TemplateView
from home.forms import HomeForm
from django.shortcuts import render, HttpResponseRedirect

from home.models import Post, Friend


def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return HttpResponseRedirect('/home/')


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        form = HomeForm()
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()

        args = {'form': form, 'posts': posts, 'users': users,
                'friends': friends}
        return render(request, self.template_name, args)

    def post(self, request, text=None):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            text = form.cleaned_data['post']
            form = HomeForm()
            return HttpResponseRedirect('/home/')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)
