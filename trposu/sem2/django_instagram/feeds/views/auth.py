from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from feeds.forms import RegisterUserForm, LoginForm
from feeds.models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect(to='/')

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user_profile = Profile.objects.create(user=user)
            messages.success(request, mark_safe('<h4>Успешная регистрация!</h4><hr class="mt-0 mb-2"><p class="mb-0">' 
                                                f'Поздравляем! Ваш аккаунт создан с именем пользователя {username}.<br>'
                                                'Чтобы продолжить, войдите в свою новую учетную запись.</p>'))
            return redirect(to='login')
    else:
        form = RegisterUserForm()

    context = {
        'form': form,
    }
    return render(request, 'auth/register.html', context)


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)
