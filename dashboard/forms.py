from django import forms
from dashboard import models
from django.forms import (
    Form, 
    ModelForm, 
    TextInput, 
    CheckboxInput,
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
                "placeholder":"Adresse E-mail"
                }
            )
        )
    password = forms.CharField(
        max_length=120, 
        widget=forms.PasswordInput(
            attrs={
                'class': "au-input au-input--full",
                "placeholder":"Mot de passe"
                }
            )
        )

    def clean(self):
        return super(LoginForm, self).clean() 



class RegisterForm(ModelForm):
    
    class Meta:
        model = models.Account
        fields = ('email', 'password')
        labels = {
            'email': 'Adresse E-mail',
            'password': 'Mot de passe'
        }
        widgets = {
            'email': EmailInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"exemple: ivoirpub@gmail.com"
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



class PostForm(ModelForm):

    class Meta:
        model = models.Post
        fields = (
            'title', 
            'poste_date', 
            'poste_heure', 
            'message',
            'pages_posted',
            'data_file')
        labels = {
            'title': "Titre",
            'poste_date': 'Date de publication',
            'poste_heure': 'Heure du poste', 
            'message': 'Message',
            'data_file': 'Ajouter un fichier multi-media',
        }
        widgets = {
            'title': TextInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"Titre du post"
                }
            ),
            'pages_posted': TextInput(
                attrs={
                'class': "au-input au-input--full block-hidden",
                "placeholder":"Titre du post"
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
                "placeholder":"Saisissez un beau message pour vos internautes ",
                "rows": 3,
                }
            ),
            'data_file' : FileInput(
                attrs={
                'class': "au-input au-input--full",
                "placeholder":"Aucun fichier selectionné"
                }
            ), 
        }
        exclude = ('is_publish', 'campagne', 'used_file')



class ConfigurationForm(ModelForm):

    class Meta:
        model = models.Configuration
        fields = ('aut_generate', 'default_page')
        labels = {
            'aut_generate': 'Auto generation du token',
            'default_page': 'Page de publication pas defaut'
        }
        widgets = {
        'aut_generate': CheckboxInput(
            attrs={
            'class': "switch-input close",
            }
        ),
        'default_page': TextInput(
            attrs={
            'disabled': 'true',
            'class': "au-input au-input--full",
            "placeholder":"Titre du post"
            })
        }
        exclude = ('account',)