from django.shortcuts import render,get_object_or_404,redirect,HttpResponse, HttpResponseRedirect
from votie.models import Position, Candidate, User, Voter
from .forms import PositionForm, InfoForm,InfoEditForm,Send_complaintForm, Send_updateForm
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from votie.decorators import admin_required
import csv, io
# Create your views here.

@login_required()
def info_list(request):

    pos = Position.objects.all()

    context = {
        'pos': pos
    }

    return render(request, 'admin/position/infolist_page.html', context)

@login_required()
def info_detail(request, poss_id):
    pos = Position.objects.all()
    poss = get_object_or_404(Position, id=poss_id)

    context = {
        'poss': poss,
        'pos': pos

    }

    return render(request, 'admin/position/info_detail.html', context)

@login_required()
@admin_required()
def add_position(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('info_list')

    else:
        form = PositionForm()

        context = {
        'form': form
    }

    return render(request, 'admin/position/add_position.html', context)

@login_required()
@admin_required()
def edit_position(request, poss_id):

    poss = get_object_or_404(Position, id=poss_id)

    if request.method == 'POST':

        form = PositionForm(request.POST, instance=poss)
        if form.is_valid():
            form.save()
            return redirect('info_list')

    else:
        form = PositionForm(instance=poss)

        context = {
            'poss': poss,
        'form': form
    }

    return render(request, 'admin/position/edit_position.html', context)

@login_required()
@admin_required()
def delete_position(request, poss_id):
    poss = get_object_or_404(Position, id=poss_id)

    if request.method == 'POST':
        poss.delete()

        return redirect('info_list')


    return render(request, 'admin/position/delete_position.html', {'poss':poss})

@login_required()
@admin_required()
def add_info(request, poss_id):
    poss = get_object_or_404(Position, pk=poss_id)
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            new_info = form.save(commit=False)
            new_info.poss = poss
            new_info.save()
            return redirect('info_list')
    else:
        form = InfoForm()

    context = {
        'form': form
    }
    return render(request, 'admin/position/add_info.html', context)

@login_required()
@admin_required()
def edit_candidate_info(request, candidate_id):
   can = get_object_or_404(Candidate, id=candidate_id)
   pos = Position.objects.all()

   if request.method == 'POST':
       form = InfoEditForm(request.POST, request.FILES,  instance=can)
       if form.is_valid():
           form.save()
           return redirect('info_list')
   else:
            form = InfoEditForm(instance=can)

            context = {
            'can': can,
           'form': form,
           'pos':pos
            }

   return render(request, 'admin/position/edit_candidate.html', context)

@login_required()
def send_complaint(request):

    form = Send_complaintForm
    if request.method == "POST":
        form = Send_complaintForm(request.POST)
        if form.is_valid():
            subject = f'Message from {request.user.matric_no}'
            message = form.cleaned_data['message']
            from_email = request.user.email
            recipients = [settings.EMAIL_HOST_USER]

            try:
                send_mail(subject, message, from_email, recipients, fail_silently=True)

            except BadHeaderError:
                return HttpResponse('Invalid header found')
            messages.info(request, 'Your complaint has been sent successfully')

            return redirect('poll_page')

    return render(request, 'voter/complain_page.html', {'form': form, })


def send_update(request):

    form = Send_updateForm
    if request.method == "POST":
        form = Send_updateForm(request.POST)
        if form.is_valid():
            print ('form valid')
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            recipients = list(User.objects.filter(is_active=True).values_list('email', flat=True))
            

            try:
                msg = EmailMultiAlternatives(subject, message, from_email, bcc=recipients)
                msg.send()

            except BadHeaderError:
                return HttpResponse('Invalid header found')
            messages.info(request, 'Updates sent to users email successfully')

            return redirect('poll_page')

    return render(request, 'admin/voter/email_update.html', {'form': form, })


def import_csv(request):
    template = 'admin/poll/import_csv.html'
    if request.method== 'GET':
        return render(request, template)
    csv_file= request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.success(request, 'This is  not a csv file')
        return render(request, template)
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created= User.objects.update_or_create(
            matric_no = column[0],
            first_name = column[1],
            last_name=column[2],
            email=column[3],
            password=column[4],

        )

    context = {}
    return render(request, template, context)


def export(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Matric no', 'First name', 'Last name', 'Email', 'Password'])

    for user in User.objects.all().values_list('matric_no', 'first_name', 'last_name', 'email', 'password'):
        writer.writerow(user)

    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    return response


from django.template.loader import get_template
from xhtml2pdf import pisa

def render_pdf_view(request):
    voters = User.objects.all()





    template_path = 'admin/voter/voter_pdf_page.html'
    context = {
        'voters': voters
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="voterinfo.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
