from django.shortcuts import render, HttpResponse
from votie.models import User
from django.views.generic import CreateView
from .forms import VoterSignUpForm,AdminSignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from votie.decorators import admin_required,voter_required
from django.utils.decorators import method_decorator


# Create your views here.

@login_required()
@admin_required()
def voters_page(request):
    voters = User.objects.all()

    context = {
        'voters': voters
    }
    return render(request,  'admin/voter/voterpage.html', context)

@method_decorator([login_required, admin_required], name='dispatch')
class VoterSignUp(LoginRequiredMixin,CreateView):
    template_name = 'registration/voter/signup_page.html'
    form_class = VoterSignUpForm
    model = User
    success_url = reverse_lazy('poll_page')

    def get_context_data(self, **kwargs):
        kwargs['header'] = 'voter'
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class AdminSignUp(LoginRequiredMixin,CreateView):
    template_name = 'registration/admin/signup_page.html'
    form_class = AdminSignUpForm
    model = User
    success_url = reverse_lazy('poll_page')

    def get_context_data(self, **kwargs):
        kwargs['header'] = 'admin'
        return super().get_context_data(**kwargs)

