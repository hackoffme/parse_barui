import json
from pytils.translit import slugify

from django.core.management.base import BaseCommand


from my import models

def load_json():
    with open('./delivery/data/data.txt', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data
        

class Command(BaseCommand):
    help = 'load data from old site'
    
    def handle(self, *args, **options):
        data = load_json()
        for item in data:
            cat = models.Categories.objects.create(name=item['cat'], slug=slugify(item['cat']))
            for menu in item['menu']:
                sc = models.SubCategories.objects.filter(name=menu['subcategory'].replace('  ', ' ')).first()
                if menu['subcategory']=='гр.':
                    menu['subcategory'] =None
                else:
                    menu['subcategory'] = sc or\
                                        models.SubCategories.objects.create(
                                                                        name=menu['subcategory'].replace('  ',' '), 
                                                                        slug=slugify(menu['subcategory']))                   
                    
                if menu['image']:
                    image =  f"media/old/{menu['image']}"
                else:
                    image = None
                m = models.Products(
                    name=menu['name'],
                    slug=slugify(menu['name']+menu['subcategory'].__str__()),
                    category=cat,
                    description=menu['description'],
                    price=menu['price'],
                    image=image,
                    subcategory = menu['subcategory']
                )
                m.save()
