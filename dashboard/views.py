from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from dashboard import models
from dashboard import forms
from django.http import JsonResponse
from packages.campagne_ctrl import CampagneCtrl
from packages.bilan_chart import ChartJS
from django.views.generic import TemplateView
import datetime 
import json


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'dashboard/login.html', {'form': form})
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        if email and password:
            response = models.Account.objects.filter(email=email, password=password)
            if len(response) == 1:
                user_auth = response[0]
                context = {'email':user_auth.email, 'user_id': user_auth.id}
                request.session['logged_user_id'] = context
                return redirect('/dashboard')
            else :
                context = {
                    'error': "Nom d'utilisateur ou mot de passe incorrect !",
                    'form': form
                }
                return render(request, 'dashboard/login.html', context)
    form = forms.LoginForm()
    return render(request, 'dashboard/login.html', {'form': form})


def edit_campagne(request, cmp_id):
    if 'logged_user_id' not in request.session:
        return redirect('/login')
    logged_user_id = request.session['logged_user_id']
    email = logged_user_id['email']

    account = models.Account.objects.get(id=logged_user_id['user_id'])
    campagne = models.Campagne.objects.get(id=cmp_id)

    context = {'email':email}

    form_default = forms.CampagneForm(initial={
        'title': campagne.title,
        'description' : campagne.description,
        'start_date': campagne.start_date,
        'close_date': campagne.close_date,
    })

    if request.method == 'POST':
        form = forms.CampagneForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            descrip = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            close_date = form.cleaned_data['close_date']

            campagne.title = title
            campagne.description = descrip
            campagne.start_date = start_date
            campagne.close_date = close_date

            today_now = datetime.datetime.now()
            date = today_now.date()

            if close_date != date :
                campagne.statu = False

            campagne.save()
            context['form'] = form_default
            context['success'] = 'Votre campagne a bien été modifié'
        else:
            context['form'] = form
    else:
        context['form'] = form_default
    return render(request, 'dashboard/edit_cmp.html', context)


def home_page(request):
    if 'logged_user_id' not in request.session:
        return redirect('/login')
    logged_user_id = request.session['logged_user_id']
    email = logged_user_id['email']

    account = models.Account.objects.get(id=logged_user_id['user_id'])
    dashboard_data = []
    campagnes = models.Campagne.objects.filter(account=account)

    for item in campagnes :
        posts = models.Post.objects.filter(campagne=item)
        dashboard_data.append({'campagne':item, 'posts':posts})
    context = {'email':email, 'dashboard_data': dashboard_data}
    return render(request, 'dashboard/index.html', context)



def init_config(request):
    if 'logged_user_id' in request.session :
        return render(request, 'dashboard/init_config_app.html')
    else:
        return redirect('/login')



def registre_page(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'dashboard/register.html', {'form': form})
        form.save(commit=True)
        email = form.cleaned_data['email']
        response = models.Account.objects.filter(email=email)
        if len(response) == 1:
            user_auth = response[0]
            context = {'email':user_auth.email, 'user_id': user_auth.id}
            request.session['logged_user_id'] = context
        return redirect('/init_config')
    form = forms.RegisterForm()
    return render(request, 'dashboard/register.html', {'form': form})



def campagne_detail_page(request, cmp_id):
    if 'logged_user_id' not in request.session:
        return redirect('/login')
    logged_user_id = request.session['logged_user_id']
    email = logged_user_id['email']

    account = models.Account.objects.get(id=logged_user_id['user_id'])
    fb_user = models.FacebookUser.objects.filter(account=account)[0]
    pages_posted = models.FPage.objects.filter(fb_user=fb_user)
    campagne = models.Campagne.objects.get(id=eval(cmp_id))
    posts = models.Post.objects.filter(campagne=campagne)

    config = models.Configuration.objects.filter(account=account)[0]
    page_default = models.FPage.objects.filter(page_id=config.default_page)[0]
    context = {

        'email':email, 
        'campagne': campagne, 
        'posts': posts,
        'pages': pages_posted,
        'page_default': page_default
        }

    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid() :
            title = form.cleaned_data['title']
            poste_date = form.cleaned_data['poste_date']
            poste_heure = form.cleaned_data['poste_heure']
            message = form.cleaned_data['message']
            page_id = form.cleaned_data['pages_posted']
            used_file = False

            if page_id is None:
                page_id = page_default.page_id

            if len(message) == 0:
                message = request.POST['media_message']
                used_file = True

            page = models.FPage.objects.filter(page_id=page_id)[0]

            post = models.Post.objects.create(
                title = form.cleaned_data['title'],
                poste_date = form.cleaned_data['poste_date'],
                poste_heure = form.cleaned_data['poste_heure'],
                message = message,
                used_file = used_file,
                pages_posted = page_id,
                data_file = form.cleaned_data['data_file'],
                campagne = campagne
            )
            post.save()
            return redirect(f'/dashboard/campagne/{cmp_id}')

        else :
            print(form)
            context['form'] = form
            return render(request, 'dashboard/detail_cmp.html', context)
    else :
        context['form'] = forms.PostForm()
        return render(request, 'dashboard/detail_cmp.html', context)



def campagne_home_page(request):
    if 'logged_user_id' not in request.session:
        return redirect('/login')
    logged_user_id = request.session['logged_user_id']
    email = logged_user_id['email']

    account = models.Account.objects.get(id=logged_user_id['user_id'])
    data = models.Campagne.objects.filter(account=account)
    context = {'email':email, 'data':data}

    if request.method == 'POST':
        form = forms.CampagneForm(request.POST)
        if form.is_valid() :
            title = form.cleaned_data['title']
            descrip = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            close_date = form.cleaned_data['close_date']
            resp = models.Campagne(
                title=title,
                description=descrip,
                start_date=start_date,
                close_date=close_date,
                account=account
                )
            resp.save()
            return redirect('/dashboard/campagne')
        else :
            context['form'] = form
            return render(request, 'dashboard/cmp_home.html', context)
    else :
        form = forms.CampagneForm()
        context['form'] = form
        return render(request, 'dashboard/cmp_home.html', context)



def forget_password_page(request):
    return render(request, 'dashboard/forget_password.html')



def edit_login_page(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']

        context = {'email':email}

        form_default = forms.RegisterForm(initial={
            'email': email
        })

        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                account = models.Account.objects.filter(email=email)[0]
                account.email = form.cleaned_data['email']
                account.password = form.cleaned_data['password']
                account.save()
                user_auth = account
                session_data = {'email':user_auth.email, 'user_id': user_auth.id}
                request.session['logged_user_id'] = session_data
                context['form']= form_default
                context['success'] = "Votre compte a bien été modifié "
            else:
                context['form']= form
            return render(request, 'dashboard/edit_login.html', context)
        context['form']= form_default
        return render(request, 'dashboard/edit_login.html', context)
    else:
        redirect('/login')


def app_config_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        fb_user = models.FacebookUser.objects.filter(account=account)[0]
        fb_pages = models.FPage.objects.filter(fb_user=fb_user)
        config_apps = models.Configuration.objects.filter(account=account)[0]

        form = forms.ConfigurationForm(initial={
            'aut_generate': config_apps.aut_generate,
            'default_page': config_apps.default_page
        })

        context = {
            'email': email,
            'fb_user': fb_user,
            'fb_pages': fb_pages,  
            'data': account,
            'form': form
        }
        return render(request, 'dashboard/config.html', context)
    else :
        redirect('/login')


def disconnect(request):
    if 'logged_user_id' in request.session:
        del request.session['logged_user_id']
    return redirect('/login')


def edit_campagne_post(request, post_id, cmp_id):
    if 'logged_user_id' not in request.session:
        return redirect('/login')
    logged_user_id = request.session['logged_user_id']
    email = logged_user_id['email']

    account = models.Account.objects.get(id=logged_user_id['user_id'])

    fb_user = models.FacebookUser.objects.filter(account=account)[0]
    fb_pages = models.FPage.objects.filter(fb_user=fb_user)
    campagne = models.Campagne.objects.get(id=eval(cmp_id))

    config = models.Configuration.objects.filter(account=account)[0]
    page_default = models.FPage.objects.filter(page_id=config.default_page)[0]

    post = models.Post.objects.get(id=post_id)
    pages_posted = models.FPage.objects.filter(page_id=post.pages_posted)[0]

    context = {

        'email':email, 
        'post': post,
        'pages': fb_pages,
        'page_default': pages_posted.name
        }

    form = forms.PostForm(initial={
        'title': post.title,
        'poste_date': post.poste_date,
        'poste_heure': post.poste_heure,
        'message': post.message,
        'pages_posted': post.pages_posted,
        'data_file': post.data_file,
    })

    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.poste_date = form.cleaned_data['poste_date']
            post.pages_posted = form.cleaned_data['pages_posted']
            post.poste_heure = form.cleaned_data['poste_heure']
            post.is_publish = False

            if form.cleaned_data['data_file'] is not '':
                print('Avec fichier')
                post.used_file = True
                if request.POST['media_message'] == '':
                    post.message = request.POST['message']
                else :
                    post.message = request.POST['media_message']
                post.data_file = form.cleaned_data['data_file']
            else :
                post.used_file = False
                print('Sans fichier')
                if form.cleaned_data['message'] == '':
                    post.message = request.POST['message']
                else :
                    post.message = form.cleaned_data['message']

            post.save()
            context['success'] = "Votre post a bien été modifier"
            return redirect(f'/dashboard/edit_post/{cmp_id}/{post_id}')
        else :
            context['form']= form
            return render(request, 'dashboard/edit_post.html', context)

    else :
        context['form'] = form
        return render(request, 'dashboard/edit_post.html', context)


def campagne_control_dashboard(request):
    if 'logged_user_id' not in request.session:
        return redirect('/login')
    logged_user_id = request.session['logged_user_id']
    email = logged_user_id['email']

    account = models.Account.objects.get(id=logged_user_id['user_id'])

    if request.method == 'GET':
        query = request.GET['query']
        if query == 'execute':
            print('Execute processuss')
            resp = CampagneCtrl.operation_posted(account)        
            data = {
                "statu":"success",
                "message": resp
                }
            return JsonResponse(data)

    if request.method == 'POST':
        form = forms.ConfigurationForm(request.POST)
        if form.is_valid():
            resp = CampagneCtrl.upload_app_configuration(form, account)
        else:
            resp = {
            "statu":"error",
            "message": "Données mal renseignée"}
        return JsonResponse(resp)


def facebook_control_dashboard(request):
    if 'logged_user_id' not in request.session:
        return
    data = request.POST
    user_data = {}
    pages = []
    all_pages = []
    cpt = 0
    incrt = 0

    for item in data:
        if 'pages'  not in item :
            user_data[item] = data[item]
        else :
            pages.append(item)

    while True:
        try:
            if f'pages[{cpt}]' in pages[incrt]:
                page = {
                    'access_token': data[f'pages[{cpt}][access_token]'],
                    'category': data[f'pages[{cpt}][category]'],
                    'id': data[f'pages[{cpt}][id]'],
                    'name': data[f'pages[{cpt}][name]'],
                }
                all_pages.append(page)
                cpt+=1
                incrt+=4
            else:
                break
        except IndexError as error:
            print('list has clear ::: >')
            break

    try:
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']

        account = models.Account.objects.get(id=logged_user_id['user_id'])
        response = CampagneCtrl.save_facebook_data(user_data, all_pages, account)
        if response['status'] :
            return JsonResponse(response)
    except Exception as error:
        response = {'status':False, 'message': "Ce compte existe deja connecté vous pour le modifier"}
        return JsonResponse(response)


def dashboard_bilan(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        campagnes = models.Campagne.objects.filter(account=account)
        chart = ChartJS()
        chart.get_all_posted_commet(account)
        camp_chart = []
        for item in campagnes : 
            data = chart.chart_camp_get_post_commets(item, account)
            camp_chart.append(data)
        # print(json.dumps(camp_chart))
        context = {'data': json.dumps(camp_chart)}
        return render(request, 'dashboard/bilan.html', context)