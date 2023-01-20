from dashboard.models import (
    Campagne, 
    Post, 
    Account, 
    FacebookUser, 
    FPage,
    Configuration
)
from datetime import datetime
from packages.fb_graph_api import FbGraphAPI
from packages.twilio_api import send_sms

class CampagneCtrl:

    @classmethod
    def operation_posted(cls, account):
        graph_api = FbGraphAPI(account)
        # print(graph_api.fb_get_page_detail())
        campagnes = Campagne.objects.filter(account=account)

        dashboard_data = []
        object_not_publish = []
        message = []

        for item in campagnes:
            today_now = datetime.now()
            date = today_now.date()

            if not item.state:
                if item.close_date == date:
                    item.state = True
                    item.save()
                else:
                    posts = Post.objects.filter(campagne=item)
                    dashboard_data.append({'campagne':item, 'post':posts}) 

        for item in dashboard_data:
            object_not_publish.extend(els for els in item['post'] if not els.is_publish)
        for item in object_not_publish:
            pst_m = item.poste_heure.minute

            if pst_m == 0:
                pst_m = '00'

            poseted_date = f'{item.poste_heure.hour}:{pst_m}'
            today_now = datetime.now()
            date = today_now.date()
            heure = f'{today_now.hour}:{today_now.minute}'

            if item.poste_date == date and poseted_date == heure:
                data = None
                page = FPage.objects.filter(page_id=item.pages_posted)[0]
                message_send = f"""
                #{page.name} #{item.title}
                {item.message}
                """ 
                print(message_send)
                FbGraphAPI.PAGE_TOKEN = page.access_token
                FbGraphAPI.PAGE_ID = page.page_id

                if item.used_file :
                    data = graph_api.fb_put_poste_photo(f'/home/domtry/Documents/ivoirpub/{item.data_file}', message_send)
                else :
                    data = graph_api.fb_put_poste_msg(message_send)

                if 'id' in data.keys():
                    item.is_publish = True
                    item.fb_post_id = data['id']
                    item.save()
                    message.append(f'{page.name}({item.title})')

        if message:
            send_sms(message)
        return message


    @classmethod
    def generate_long_access_token(cls, token):
        return FbGraphAPI.fb_generate_long_access_tk(token)
    

    @classmethod
    def facebook_verify_page_params(cls, data):
        try:
            FbGraphAPI.PAGE_TOKEN = data['page_token']
            FbGraphAPI.PAGE_ID = data['page_id']
            account = Account.objects.get(id=data['account_id'])
            graph_api = FbGraphAPI(account)
            return graph_api.fb_get_page_detail()
        except Exception as error:
            return {"error": f"{error}"}


    # fonction testé
    @classmethod
    def save_facebook_data(cls, user_data, page_data, account):
        try:
            resp_user = CampagneCtrl.save_facekook_user(user_data, account)
            if resp_user["status"]:
                user_obj = FacebookUser.objects.filter(user_id=user_data['user_id'])
                user_obj = user_obj[0]
                resp_page = CampagneCtrl.save_facebook_page(page_data, user_obj)
                if resp_page['status']:
                    config = Configuration.objects.create(
                        aut_generate=True,
                        default_page=page_data[0]['id'],
                        account=account
                    )
                    config.save()
                    return resp_page
        except Exception as error:
            return {"status": False, "message": f"{error}"}


    @classmethod
    def upload_app_configuration(cls, form, account):
        try:
            page = form.cleaned_data['default_page']
            aut_gn = f"{form.cleaned_data['aut_generate']}".capitalize()
            page = FPage.objects.filter(page_id=page)[0]
            config = Configuration.objects.filter(account=account)[0]
            config.aut_generate = aut_gn
            config.default_page = f'{page.page_id}'
            config.save()
            return {"status": True, "message": "update has been success"}
        except Exception as error:
            return {"status": False, "message": f"{error}"}
        else:
            return {"status": True, "message": "update has been success"}


    # fonction testé
    @classmethod
    def save_facekook_user(cls, data, account):
        try:
            resp = FbGraphAPI.fb_generate_long_access_tk(data['access_token'])
            user_id = data['user_id']
            access_token = resp['access_token']
            expires_in = resp['expires_in']

            obj = FacebookUser.objects.create(
                user_id=user_id, 
                access_token=access_token, 
                expires_in=expires_in,
                account=account
                )
            obj.save()
            return {"status": True, "message": "Object has been success"}
        except Exception as error:
            return {"status": False, "message": f"{error}"}


    # fonction testé
    @classmethod
    def save_facebook_page(cls, data, user_obj):
        try:
            for item in data:
                resp = FbGraphAPI.fb_generate_long_access_tk(item['access_token'])
                access_token = resp['access_token']
                page_id = item['id']
                name = item['name']
                category = item['category']
                expires_in = resp['expires_in']

                obj = FPage.objects.create(
                    page_id=page_id, 
                    access_token=access_token, 
                    name=name, 
                    category=category, 
                    expires_in=expires_in, 
                    fb_user=user_obj)
                obj.save()

            return {"status": True, "message": "Object has been success"}
        except Exception as error:
            return {"status": False, "message": f"{error}"}