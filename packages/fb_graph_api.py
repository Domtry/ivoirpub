import json
import facebook
import requests
import time
from dashboard.models import FacebookUser, FPage, Configuration

class FbGraphAPI(object):
    
    APP_ID = '10444......' # Identifiant de l'application
    APP_SECRET_KEY = '45c550.........' # jeton d'acces de l'application

    PAGE_ID = ''  # Identifiant de la page facebook
    PAGE_TOKEN = '' # jeton d'acces page 
    USER_TOKEN = '' # jeton d'acces utilisateur 

    HOST = 'https://graph.facebook.com/v6.0'


    def __init__(self, account) :
        super().__init__()
        fb_access = FacebookUser.objects.filter(account=account)[0]
        fb_page = FPage.objects.filter(fb_user=fb_access)[0]
        FbGraphAPI.USER_TOKEN = fb_access.access_token
        FbGraphAPI.PAGE_ID = fb_page.page_id
        FbGraphAPI.PAGE_TOKEN = fb_page.access_token
        self.obj_graph = facebook.GraphAPI(FbGraphAPI.PAGE_TOKEN)
        
    

    def fb_get_all_posted_visitors(self, id):
        list_resp = []
        data = self.obj_graph.get_all_connections(id, 'visitor_posts')
        for item in data:
            list_resp.append(item)
        return list_resp


    def fb_get_all_posted_page(self, id):
        list_resp = []
        data = self.obj_graph.get_all_connections(id, 'posts')
        for item in data:
            list_resp.append(item)
        return list_resp

    
    def fb_put_poste_msg(self, msg):
        resp =  self.obj_graph.put_object('me', 'feed', message=msg)
        return resp

    
    def fb_put_poste_photo(self, urlimg, msg):
        """
        Exemple
        resp = obj.fb_put_poste_photo(
        urlimg='/home/domtry/Documents/picture_1.png', 
        msg='une simple image de couverture')
        """
        resp = self.obj_graph.put_photo(
            image=open(urlimg, 'rb'),  
            album_path="me/photos", 
            caption=msg, 
            published=True)
        return resp


    def fb_pub_postes_photos(self, list_post):
        """
        Exemple
        resp = obj.fb_pub_postes_photos([
            {
                'title':'Poste_1', 
                'url':'/home/domtry/Documents/images.jpeg', 
                'descrip':"Vous connaissez les ...."
            }, 
            {
                'title':'Poste_2', 
                'url':'/home/domtry/Documents/images_2.jpeg', 
                'descrip':'Django est réputé pour avoir .....'
            }])
        print(resp)
        """
        resp = {}
        for item in list_post:
            title = item["title"]
            img = item["url"]
            descrip = item["descrip"]
            result = self.fb_put_poste_photo(img, descrip)
            resp[title]=result
        return resp

    
    def fb_get_post_commet(self, post_id):
        """
        result = obj.fb_get_post_commet('106220841008568_107919960838656')
        print(result)
        """
        list_resp = []
        data = self.obj_graph.get_all_connections(post_id, 'comments')
        for item in data:
            list_resp.append(item)
        return list_resp


    def fb_get_page_detail(self):
        """
        Exemple
        result = obj.fb_get_page_detail()
        print(result)
        """
        resp = self.obj_graph.get_object(FbGraphAPI.PAGE_ID)
        return resp


    def fb_get_page_token(self):
        """
        result = obj.fb_get_page_token()
        print(result)
        """
        page_token = ""
        pages_data = self.fb_get_page_detail()
        for item in pages_data:
            if item['id'] == FbGraphAPI.PAGE_ID:
                page_token = item['access_token']
        return page_token



    @classmethod
    def fb_generate_long_access_tk(cls, token):
        access_tk_url = f"https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={FbGraphAPI.APP_ID}&client_secret={FbGraphAPI.APP_SECRET_KEY}&fb_exchange_token={token}"
        r = requests.get(access_tk_url)
        # formatage de la données en format json
        access_token_info = r.json()
        # long_access_tk = access_token_info['access_token']
        return access_token_info


    @classmethod
    def fb_get_all_commets(cls):
        curl = f'{cls.HOST}/{cls.PAGE_ID}/posts?access_token={cls.PAGE_TOKEN}'
        r = requests.get(curl)
        data = r.json()
        return data


    def fb_get_visitor_number(self):
        pass

        

    def fb_get_all_posted_commet(self):
        posted = {}
        rspn = self.obj_graph.get_all_posted_page()
        
        for item in rspn:
            post_id = item['id']
            comets = self.obj_graph.get_post_commet(post_id)
            posted[post_id] = comets
        
        return posted

if __name__ == "__main__":
    obj = FbGraphAPI()
    result = obj.fb_get_page_detail()
    print(result)
