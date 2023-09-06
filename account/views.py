from django.contrib import messages
from django.contrib.auth import logout, authenticate, update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from .forms import AccountAuthenticationForm
from logic.utils import get_landing_page, extract_name, current_time


@login_required(login_url=reverse_lazy('login'))
def home_screen_view(request):
    context = {}
    return render(request, 'account/home.html', context)


@method_decorator([never_cache], 'dispatch')
class LoginView(View):
    template_name = "account/login.html"

    def get(self, request, *args, **kwargs):
        context = {}
        form = AccountAuthenticationForm()
        context['login_form'] = form
        user = request.user
        if user.is_authenticated:
            landing_page = get_landing_page(user)
            return redirect(landing_page)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = AccountAuthenticationForm(request.POST)
        context['login_form'] = form

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=extract_name(username), password=password)
            if user:
                login(request, user)
                update_session_auth_hash(request, user)
                landing_page = "home"

                _welcome = "<span class='toast-l-text'>Welcome back,</span> <span class='toast-r-text'>%s</span>!" % user.first_name.title()
                if not user.last_access:
                    _welcome = "<span class='toast-l-text'>Welcome,</span> <span class='toast-r-text'>%s</span>! " \
                               "<span class='ml3'>Great to have you on board.</span>" % user.first_name.title()
                    user.last_access = current_time()
                    user.save()

                landing_page = get_landing_page(user)
                link = request.GET.get('next', None)
                if link:
                    landing_page = str(link)
                return redirect(landing_page)
        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    return redirect('login')


class FAQView(View):
    template_name = 'logic/faqs.html'

    def get(self, request, *args, **kwargs):
        # context = {"faqs": FAQ.objects.all()}
        return render(request, self.template_name, {})
