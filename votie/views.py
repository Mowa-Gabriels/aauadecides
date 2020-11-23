from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Poll, Choice, Vote, Position, User
from .forms import PollForm, PollEditForm, ChoiceForm, ChoiceEditForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import voter_required,admin_required

# Create your views here.
@login_required()
def poll_page(request):

    polls = Poll.objects.all()
    pos = Position.objects.all()

    context = {
        'polls': polls,
        'pos':pos
    }
    if request.session['otp_session_is_valid']:
        if request.user.is_authenticated:
            if not request.user.is_voter:
                return render(request, 'admin/poll/poll_page.html', context)

        return render(request, 'voter/poll_page.html', context)
    return redirect('otp_page')



@login_required()
def poll_detail(request, poll_id):

    poll = get_object_or_404(Poll, id=poll_id)
    pos = Position.objects.all()
    user_can_vote = poll.user_can_vote(request.user)

    context = {
        'poll': poll,
        'pos':pos,
        'user_can_vote': user_can_vote
    }

    return render(request, 'voter/poll_detail.html', context)

@login_required()
@admin_required()
def poll_result(request, poll_id):

    poll = get_object_or_404(Poll, id=poll_id)
    pos = Position.objects.all()
    context = {
        'poll': poll,
        'pos':pos
    }

    return render(request, 'admin/poll/polls_result.html', context)

@login_required()
@admin_required()
def add_poll(request):

    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save()

            new_choice =Choice(

                poll = new_poll,
                choice_text =form.cleaned_data['choice1']
            ).save()
            messages.info(request, 'Poll Created successfully')

        return redirect('poll_page')

    else:
        form = PollForm()

        context = {
        'form':form,


    }

    return render(request, 'admin/poll/create_poll.html', context)

@login_required()
@admin_required()
def poll_edit(request,poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == 'POST':
        form = PollEditForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()

        return redirect('poll_page')

    else:
        form = PollEditForm(instance=poll)

        context = {
        'poll': poll,
      'form': form
           }
        return render(request, 'admin/poll/poll_edit.html', context)

@login_required()
@admin_required()
def poll_delete(request,poll_id):

    poll = get_object_or_404(Poll, id=poll_id)
    poll.delete()
    messages.info(request, 'Poll deleted successfully')
    return redirect('poll_page')


@login_required()
@voter_required()
def vote_poll(request,poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if not poll.user_can_vote(request.user):
        messages.info(request, 'Sorry you cannot vote twice')
        return HttpResponseRedirect(reverse('poll_detail', args=(poll_id)))

    choice_id =request.POST.get('choice')
    '''this line easily sends a get POST request to get the choice_id that was selected'''

    if choice_id:

        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user=request.user, poll=poll, choice=choice)
        new_vote.save()
        messages.info(request, 'Choice Saved!')
        return redirect('poll_page')

    else:
        messages.info(request, ' you made an invalid selection')
        return HttpResponseRedirect(reverse('poll_detail', args=(poll_id)))

    return render(request, 'admin/poll/poll_page.html', {'poll':poll} )

@login_required()
@admin_required()
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            return HttpResponseRedirect(reverse('poll_edit', args=(poll_id)))
    else:
        form = ChoiceForm()

    context = {
        'form': form,

    }
    return render(request, 'admin/choice/add_choice.html', context)


@login_required()
@admin_required()
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)

    if request.method == 'POST':
        form = ChoiceEditForm(request.POST, request.FILES, instance=choice)
        if form.is_valid():
            form.save()
            messages.info(request, 'Choice Edited Succesfully')
            return redirect('poll_page')
    else:
        form = ChoiceEditForm(instance=choice)

        context = {
         'form': form,
         'choice': choice,


       }
    return render(request, 'admin/choice/edit_choice.html', context)

@login_required()
@admin_required()
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    choice.delete()
    messages.info(request, 'Choice deleted successfully')
    return redirect('poll_page')


from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import random



@login_required()
def home(request):
    context = {}
    if request.session['otp_session_is_valid']:
        return render(request, 'login/index.html', context)
    # when otp is not valid redirect to otp_page
    return redirect('otp_page')


@login_required()
def generate_and_send_otp(request):
    rand_no = random.randint(100000, 999999)
    otp = str(rand_no)
    subject = 'NASS(AAUA) DECIDES'
    context = {'otp': otp}
    message = render_to_string('admin/login/otp_email.html', context)
    sender = settings.EMAIL_HOST_USER
    recipients = [request.user.email]
    send_mail(subject, message, sender, recipients, fail_silently=True)
    messages.success(request, ('An OTP has been sent to your mail!'))

    request.session['otp'] = otp
    return render(request, 'admin/login/otp_page.html', context)


@login_required()
def validate_otp(request):
    polls = Poll.objects.all()
    pos = Position.objects.all()

    context = {
        'polls': polls,
        'pos': pos
    }


    user_otp = request.POST.get("otp")

    if user_otp == request.session['otp']:
        set_otp_session(request)
        if request.user.is_voter:
            return render(request, 'voter/poll_page.html', context)
        else:
            return render(request, 'admin/poll/poll_page.html', context)




    messages.warning(request, "Incorrect OTP")
    return redirect('otp_page')


def set_otp_session(request):
    request.session['otp_session_is_valid'] = True


def invalidate_otp_session(request):
    request.session['otp_session_is_valid'] = False


def login_user(request):
    context = {}
    return render(request, 'Registration/login_page.html', context)


def login_validate(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('otp_page'))
        else:
            messages.warning(request, "Invalid Login Details")

    context = {}
    return render(request, 'Registration/login_page.html', context)


def logout_user(request):
    logout(request)
    invalidate_otp_session(request)
    request.session['otp'] = None
    return redirect('login')
