import requests
import json
from bs4 import BeautifulSoup

doc = requests.get('http://1-0ui.ru/pizza')
data = []
soup = BeautifulSoup(doc.text, 'lxml')
t=0
for group, menu in zip(soup.find_all('h2'), soup.find_all(attrs={'class': 'card-deck justify-content-center'})):
    if group.text.strip() == 'Акция' or group.text.strip() =='Внимание!' :
        continue
    category = group.text.strip()
    m = []
    for item in menu.find_all(attrs={'class': 'card'}):
        if not item.find('p'):
            old = m[-1].copy()
            old['price'] = int(item.find(attrs={'class': 'card-price'}).text.split()[0])
            old['subcategory'] = item.find(attrs={'class': 'card-weight text-muted'}).text.strip()
            m.append(old)
            continue

        name = item.h5.text.strip()
        image = item.find('img')
        if image:
            q = requests.get(image['src'])
            with  open(f'./img/{t}.png', 'wb') as f:
                f.write(q.content)
            image = f'{t}.png'
            t+=1
            ...
        description = item.find('p').get_text()
        price = int(item.find(attrs={'class': 'card-price'}).text.split()[0])
        subcategory = item.find(attrs={'class': 'card-weight text-muted'}).text.strip()
        
        b = {
            'name': name,
            'image': image,
            'description': description,
            'price': price,
            'subcategory': subcategory
        }
        m.append(b)

    data.append({
        'cat': category,
        'menu': m
    })
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)
