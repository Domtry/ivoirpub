import json
import facebook
import requests
from dashboard.models import Fb_Access, Fb_Page

class FbGraphAPI(object):
    
    APP_ID = '' # Identifiant de l'application
    PAGE_ID = ''  # Identifiant de la page facebook
    PAGE_TOKEN = '' # jeton d'acces page 
    USER_TOKEN = '' # jeton d'acces utilisateur 
    PAGE_LG_TK = '' # long jeton d'acces page 
    USER_LG_TK = '' # long jeton d'acces utilisateur 
    APP_SECRET_KEY = '' # jeton d'acces de l'application


    def __init__(self, account) :
        super().__init__()
        data = Fb_Access.objects.filter(account=account)
        fb_access = data[0]
        data_page = Fb_Page.objects.filter(fb_access=fb_access)
        fb_page = data_page[0]
        FbGraphAPI.APP_ID = fb_access.app_id
        FbGraphAPI.USER_TOKEN = fb_access.user_lg_token
        FbGraphAPI.PAGE_ID = fb_page.page_id
        FbGraphAPI.PAGE_LG_TK = fb_page.page_lg_tk
        self.obj_graph = facebook.GraphAPI(FbGraphAPI.PAGE_LG_TK)
    

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
        resp = self.obj_graph.get_object("/me/")
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


    def fb_generate_long_access_tk(self):
        # requete permettant de recuperer le jeton d'acces de longue durée
        token = [FbGraphAPI.USER_TOKEN, FbGraphAPI.PAGE_TOKEN]
        long_access_tk = []
        for tk in token:
            access_tk_url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(FbGraphAPI.APP_ID, FbGraphAPI.APP_SECRET_KEY, tk)
            r = requests.get(access_tk_url)
            # formatage de la données en format json
            access_token_info = r.json()
            # recuperation du jeton de longue durée
            long_access_tk.append(access_token_info['access_token'])
        return long_access_tk


    def fb_recup_long_access_token(self):
        long_token_generate = self.fb_generate_long_access_tk()
        FbGraphAPI.PAGE_LG_TK = long_token_generate[1]
        FbGraphAPI.USER_LG_TK = long_token_generate[0]



    def fb_get_visitor_number(self):
        pass


if __name__ == "__main__":
    obj = FbGraphAPI()
    result = obj.fb_get_page_detail()
    print(result)