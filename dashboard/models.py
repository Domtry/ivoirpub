from django.db import models

# Create your models here.

class Account(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=120)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'

    def update_account(self, obj):
        account = Account.objects.get (id=obj.id)
        account.username = obj.username
        account.email = obj.email
        account.password = obj.password
        account.save(update_fields = ['username', 'email', 'password'])


class Campagne(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=500, null=True, blank=True)
    state = models.BooleanField(default=False)
    start_date = models.DateField()
    close_date = models.DateField()
    create_date = models.DateField(auto_now_add=True)
    modify = models.DateField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.state}'


class Post(models.Model):
    title = models.CharField(max_length=80)
    message = models.TextField(max_length=500, null=True, blank=True)
    poste_date = models.DateField()
    poste_heure = models.TimeField()
    data_file = models.FileField(upload_to = 'uploads', null=True, blank=True)
    is_publish = models.BooleanField(default=False)
    used_file = models.BooleanField(default=False)
    fb_post_id = models.CharField(max_length=80, null=True, blank=True)
    pages_posted = models.CharField(max_length=150, null=True, blank=True)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.is_publish}'



class FacebookUser(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    access_token = models.CharField(max_length=1000)
    expires_in = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id}'


class FPage(models.Model):
    page_id = models.CharField(max_length=20, unique=True)
    access_token = models.TextField(max_length=1000)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=70)
    expires_in = models.IntegerField()
    fb_user = models.ForeignKey(FacebookUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Configuration(models.Model):
    aut_generate = models.BooleanField(default=True)
    default_page = models.CharField(max_length=30)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)