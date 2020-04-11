from dashboard.models import Campagne, Objectif
from datetime import datetime
from packages.fb_graph_api import FbGraphAPI

class CampagneCtrl:

    @classmethod
    def operation_posted(cls, account):
        graph_api = FbGraphAPI(account)
        # print(graph_api.fb_get_page_detail())
        campagnes = Campagne.objects.filter(account=account)

        dashboard_data = []
        object_not_publish = []
        message = []

        for item in campagnes :
            if not item.state :
                data_objectif = Objectif.objects.filter(campagne=item)
                dashboard_data.append({'campagne':item, 'objectif':data_objectif}) 
        
        for item in dashboard_data:
            for els in item['objectif']:
                if not els.is_publish :
                    object_not_publish.append(els)

        for item in object_not_publish:
            pst_m = item.poste_heure.minute
            if pst_m == 0:
                pst_m = f'00'
            poseted_date = f'{item.poste_heure.hour}:{pst_m}'
            today_now = datetime.now()
            date = today_now.date()
            heure = f'{today_now.hour}:{today_now.minute}'
            if item.poste_date == date and poseted_date == heure:
                data = graph_api.fb_put_poste_msg(item.message)
                if 'id' in data.keys():
                    item.is_publish = True
                    item.save()
                    message.append(item.title)
        return message
