from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from dashboard import models
from dashboard import forms
import json
from django.http import JsonResponse
from packages.campagne_ctrl import CampagneCtrl


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
            posts = models.Post.objects.filter(campagne=item)
            dashboard_data.append({'campagne':item, 'posts':posts})   
        context = {'username':username, 'email':email, 'dashboard_data': dashboard_data}
        return render(request, 'dashboard/index.html', context)
    else :
        return redirect('/login')



def init_config(request):
    if 'logged_user_id' in request.session :
        return render(request, 'dashboard/init_config_app.html')
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
        posts = models.Post.objects.filter(campagne=campagne)
        context = {'username':username, 'email':email, 'campagne': campagne, 'posts': posts}
        
        if request.method == 'POST':
            form = forms.PostForm(request.POST, request.FILES)
            if form.is_valid() :
                title = form.cleaned_data['title']
                poste_date = form.cleaned_data['poste_date']
                poste_heure = form.cleaned_data['poste_heure']
                message = form.cleaned_data['message']
                used_file = False

                if len(message) == 0:
                    message = request.POST['media_message']
                    used_file = True

                post = models.Post.objects.create(
                    title= form.cleaned_data['title'],
                    poste_date= form.cleaned_data['poste_date'],
                    poste_heure= form.cleaned_data['poste_heure'],
                    message= message,
                    used_file= used_file,
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



def edit_login_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        context = {'username':username, 'email':email}

        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                account = models.Account.objects.get(email=email)
                account.username = form.cleaned_data['username']
                account.email = form.cleaned_data['email']
                account.password = form.cleaned_data['password']
                account.save()
                user_auth = account
                session_data = {'username':user_auth.username, 'email':user_auth.email, 'user_id': user_auth.id}
                request.session['logged_user_id'] = session_data
                context['success'] = "Votre compte a bien été modifié "
                return render(request, 'dashboard/edit_login.html', context)
            else :
                context['form']= form
                return render(request, 'dashboard/edit_login.html', context)

        form = forms.RegisterForm(initial={
            'username': username,
            'email': email
        })
        context['form']= form
        return render(request, 'dashboard/edit_login.html', context)
    else :
        redirect('/login')


def app_config_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        fb_user = models.FacebookUser.objects.filter(account=account)[0]
        fb_pages = models.FPage.objects.filter(fb_user=fb_user)
        context = {
            'username': username, 
            'email': email,
            'fb_user': fb_user,
            'fb_pages': fb_pages,  
            'data': account
        }
        return render(request, 'dashboard/config.html', context)
    else :
        redirect('/login')


def disconnect(request):
    if 'logged_user_id' in request.session :
        del request.session['logged_user_id']
        return redirect('/login')
    else:
        return redirect('/login')


def campagne_control_dashboard(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
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
            
            if query == 'verify_app':
                print('Verify processuss')
                data = {
                    'app_id': request.GET['app_id'],
                    'lg_token': request.GET['lg_token'],
                    'app_key': request.GET['app_key'],
                }
                resp = CampagneCtrl.facebook_verify_app_params(data)
                return JsonResponse(resp)

            if query == 'verify_page':
                print('Verify processus')
                data = {
                    'account_id': logged_user_id['user_id'],
                    'title': request.GET['title'],
                    'page_id': request.GET['page_id'],
                    'page_token': request.GET['lg_tk'],
                }
                resp = CampagneCtrl.facebook_verify_page_params(data)
                return JsonResponse(resp)
    else:
        return redirect('/login')



def facebook_control_dashboard(request):
    if 'logged_user_id' in request.session :
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
                    page = {}
                    page['access_token'] = data[f'pages[{cpt}][access_token]']
                    page['category'] = data[f'pages[{cpt}][category]']
                    page['id'] = data[f'pages[{cpt}][id]']
                    page['name'] = data[f'pages[{cpt}][name]']
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
            username = logged_user_id['username']
            account = models.Account.objects.get(id=logged_user_id['user_id'])
            response = CampagneCtrl.save_facebook_data(user_data, all_pages, account)
            if response['status'] :
                return JsonResponse(response)
        except Exception as error:
            response = {'status':False, 'message': "Ce compte existe deja connecté vous pour le modifier"}
            return JsonResponse(response)
