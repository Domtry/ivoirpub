from dashboard.models import (
    Campagne, 
    Post, 
    Account, 
    FacebookUser, 
    FPage,
    Configuration
)
from packages.fb_graph_api import FbGraphAPI
import random
import json

class ChartJS:
    
    def chart_camp_get_post_commets(self, camp, account):
        total = {}
        commets = []
        bk_color = []
        bd_color = []

        graph_api = FbGraphAPI(account)
        posteds = Post.objects.filter(campagne=camp)
        for item in posteds :
            if item.fb_post_id is not None :
                commets = graph_api.fb_get_post_commet(item.fb_post_id)
                total[item.title] = len(commets)
            else :
                total[item.title] = 0

            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            bk_color.append(f'rgba({r},{g},{b}, 0.2)')
            bd_color.append(f'rgba({r},{g},{b}, 1)')

        return {
            'type': 'bar',
            'data': {
                'labels': list(total.keys()),
                'datasets': [
                    {
                        'label': camp.title,
                        'backgroundColor': bd_color,
                        'borderColor': bd_color,
                        'data': list(total.values()),
                    }
                ],
            },
            'options': {},
        }



    def get_all_posted_commet(self, account):
        graph_api = FbGraphAPI(account)
        rspns = graph_api.fb_get_all_commets()
        page_data = rspns['data']
        posts = [item["id"] for item in page_data]
        for post in posts:
            rspn = graph_api.fb_get_post_commet(post)
            print(rspn)