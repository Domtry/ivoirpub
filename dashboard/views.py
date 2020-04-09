from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from dashboard import models
from dashboard import forms
from packages.fb_graph_api import FbGraphAPI

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if email and password:
                response = models.Account.objects.filter(email=email, password=password)
                if len(response) == 1:
                    user_auth = response[0]
                    context = {'username':user_auth.username, 'email':user_auth.email, 'user_id': user_auth.id}
                    request.session['logged_user_id'] = context
                    return redirect('/dashboard')
                else :
                    context = {
                        'error': "Nom d'utilisateur ou mot de passe incorrect !",
                        'form': form
                    }
                    return render(request, 'dashboard/login.html', context)
        else :
            return render(request, 'dashboard/login.html', {'form': form})
    form = forms.LoginForm()
    return render(request, 'dashboard/login.html', {'form': form})


def home_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        dashboard_data = []
        campagnes = models.Campagne.objects.filter(account=account)

        for item in campagnes :
            data_objectif = models.Objectif.objects.filter(campagne=item)
            dashboard_data.append({'campagne':item, 'objectif':data_objectif})   
        context = {'username':username, 'email':email, 'dashboard_data': dashboard_data}
        return render(request, 'dashboard/index.html', context)
    else :
        return redirect('/login')


def init_config(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        if request.method == 'POST':
            form = forms.FacebookAccessForm(request.POST)
            account = models.Account.objects.get(id=logged_user_id['user_id'])
            if form.is_valid():
                resp = models.Fb_Access(
                    user_lg_token=form.cleaned_data['user_lg_token'],
                    app_secret_key=form.cleaned_data['app_secret_key'],
                    app_id=form.cleaned_data['app_id'],
                    account=account
                )
                resp.save()
                return redirect('/dashboard')
            else :
                return render(request, 'dashboard/init_config_app.html', {'form': form})
        else :
            form = forms.FacebookAccessForm()
            return render(request, 'dashboard/init_config_app.html', {'form': form})
    else:
        return redirect('/login')


def registre_page(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            email = form.cleaned_data['email']
            response = models.Account.objects.filter(email=email)
            if len(response) == 1:
                user_auth = response[0]
                context = {'username':user_auth.username, 'email':user_auth.email, 'user_id': user_auth.id}
                request.session['logged_user_id'] = context
            return redirect('/init_config')
        else:
            return render(request, 'dashboard/register.html', {'form': form})
    form = forms.RegisterForm()
    return render(request, 'dashboard/register.html', {'form': form})


def campagne_detail_page(request, cmp_id):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        campagne = models.Campagne.objects.get(id=eval(cmp_id))
        data_objectif = models.Objectif.objects.filter(campagne=campagne)
        context = {'username':username, 'email':email, 'campagne': campagne, 'data_objectif': data_objectif}
        
        if request.method == 'POST':
            form = forms.ObjectifForm(request.POST)
            if form.is_valid() :
                title = form.cleaned_data['title']
                descrip = form.cleaned_data['description']
                poste_date = form.cleaned_data['poste_date']
                poste_heure = form.cleaned_data['poste_heure']
                message = form.cleaned_data['message']
                resp = models.Objectif(
                    title=title,
                    description=descrip,
                    poste_date=poste_date,
                    poste_heure=poste_heure,
                    message=message,
                    campagne=campagne)
                resp.save()
                return redirect(f'/dashboard/campagne/{cmp_id}')
            else :
                context['form'] = forms.ObjectifForm()
                return render(request, 'dashboard/detail_cmp.html', context)
        else :
            context['form'] = forms.ObjectifForm()
            return render(request, 'dashboard/detail_cmp.html', context)
    else :
        return redirect('/login')



def campagne_home_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        data = models.Campagne.objects.filter(account=account)
        context = {'username':username, 'email':email, 'data':data}

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
    else :
        return redirect('/login')



def forget_password_page(request):
    return render(request, 'dashboard/forget_password.html')


def disconnect(request):
    if 'logged_user_id' in request.session :
        del request.session['logged_user_id']
        return redirect('/login')
    else:
        return redirect('/login')