from django import forms
from dashboard import models
from django.forms import (
    Form, 
    ModelForm, 
    TextInput, 
    PasswordInput, 
    EmailInput,
    Textarea,
    DateInput,
    TimeInput,
    FileInput
)

class LoginForm(Form):
    
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': "au-input au-input--full",
                "placeholder":"Email"
                }
            )
        )
    password = forms.CharField(
        max_length=120, 
        widget=forms.PasswordInput(
            attrs={
                'class': "au-input au-input--full",
                "placeholder":"password"
                }
            )
        )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        return cleaned_data 



class RegisterForm(ModelForm):
    
    class Meta:
        model = models.Account
        fields = ('username', 'email', 'password')
        labels = {
            'name': 'Username',
            'email': 'Email Address',
            'password': 'Password'
        }
        widgets = {
            'username': TextInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"username"
                }
            ),
            'email': EmailInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"email"
                }
            ),
            'password': PasswordInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"password"
                }
            )
        }
        exclude = ('',)



class FacebookAccessForm(ModelForm):
    
    class Meta:
        model = models.Fb_Access
        fields = ('user_lg_token', 'app_secret_key', 'app_id')
        labels = {
            'user_lg_token': "User long token",
            'app_secret_key': 'Secret key application',
            'app_id': 'Application ID',
        }
        widgets = {
            'user_lg_token': TextInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"token"
                }
            ),
            'app_secret_key': TextInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"secret key"
                }
            ),
            'app_id': TextInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"app_id"
                }
            )
        }
        exclude = ('create_date', 'account')

        def clean(self):
            cleaned_data = super(FacebookAccessForm, self).clean()
            return cleaned_data 



class CampagneForm(ModelForm):

    class Meta:
        model = models.Campagne
        fields = ('title', 'description', 'start_date', 'close_date')
        labels = {
            'title': "Titre de la campagne",
            'description': 'Description',
            'start_date': 'Date de demarrage',
            'close_date': 'Date de la cloture'
        }
        widgets = {
            'title': TextInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"title of campagne"
                }
            ),
            'start_date': DateInput(
                attrs={
                'class': "au-input au-input--full",
                'type': 'date'
                }
            ),
            'close_date': DateInput(
                attrs={
                'class': "au-input au-input--full",
                'type': 'date'
                }
            ),
            'description': Textarea(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"campagne description",
                "rows": 3,
                }
            )
        }
        exclude = ('state', 'create_date', 'modify', 'account')



class ObjectifForm(ModelForm):

    class Meta:
        model = models.Objectif
        fields = ('title', 'description', 'poste_date', 'poste_heure', 'message')
        labels = {
            'title': "Titre de l'objectif",
            'description': 'Description',
            'poste_date': 'Date de publication',
            'poste_heure': 'Heure du poste', 
            'message': 'Message',
        }
        widgets = {
            'title': TextInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"title of objectif"
                }
            ),
            'description': Textarea(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"objectif description",
                "rows": 2,
                }
            ),
            'poste_date': DateInput(
                attrs={
                'class': "au-input au-input--full",
                'type': 'date'
                }
            ),
            'poste_heure': DateInput(
                attrs={
                'class': "au-input au-input--full",
                'type': 'time'
                }
            ),
            'message': Textarea(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"post message",
                "rows": 3,
                }
            )
        }
        exclude = ('is_publish', 'create_date', 'campagne')
        

class FacebookPageForm(ModelForm):
    class Meta:
        pass