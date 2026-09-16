from django.core.management.base import BaseCommand
from store.models import Category,Product
class Command(BaseCommand):
 def handle(self,*a,**k):
  data={'Electronics':['Wireless Headphones','Smart Watch','Bluetooth Speaker'],'Fashion':['Running Shoes','Denim Jacket','Backpack'],'Home':['Table Lamp','Coffee Maker','Smart Fan'],'Beauty':['Face Wash','Skin Care Kit','Perfume']}
  for c,names in data.items():
   cat,_=Category.objects.get_or_create(name=c)
   for i,n in enumerate(names): Product.objects.get_or_create(name=n,category=cat,defaults={'description':f'Premium {n} with excellent quality and fast delivery.','price':999+i*500,'discount':10+i*5,'stock':20,'rating':4.5})
  self.stdout.write(self.style.SUCCESS('Demo products created successfully.'))
