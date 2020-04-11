from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=120)
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
    description = models.TextField(max_length=500, default='')
    state = models.BooleanField(default=False)
    start_date = models.DateField()
    close_date = models.DateField()
    create_date = models.DateField(auto_now_add=True)
    modify = models.DateField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.state}'


class Objectif(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=100, default='')
    message = models.TextField(max_length=500)
    poste_date = models.DateField()
    poste_heure = models.TimeField()
    create_date = models.DateField(auto_now_add=True)
    is_publish = models.BooleanField(default=False)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.is_publish}'


class Fb_Access(models.Model):
    user_lg_token = models.CharField(max_length=300)
    app_secret_key = models.CharField(max_length=50)
    app_id = models.CharField(max_length=30)
    create_date = models.DateField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.app_id}'


class Fb_Page(models.Model):
    title = models.CharField(max_length=70)
    page_id = models.CharField(max_length=30)
    page_lg_tk = models.CharField(max_length=300)
    fb_access = models.ForeignKey(Fb_Access, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.page_id}'
