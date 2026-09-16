from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product,Category,Order,OrderItem
from django.db.models import Q

def home(r): return render(r,'home.html',{'products':Product.objects.all()[:8],'categories':Category.objects.all()})
def products(r):
 qs=Product.objects.all(); q=r.GET.get('q',''); cat=r.GET.get('category',''); sort=r.GET.get('sort','')
 if q: qs=qs.filter(Q(name__icontains=q)|Q(description__icontains=q))
 if cat: qs=qs.filter(category__name=cat)
 if sort=='low': qs=qs.order_by('price')
 if sort=='high': qs=qs.order_by('-price')
 return render(r,'products.html',{'products':qs,'categories':Category.objects.all(),'q':q})
def product_detail(r,pk): return render(r,'product_detail.html',{'product':get_object_or_404(Product,pk=pk)})
def cart(r):
 ids=r.session.get('cart',[]); counts={str(i):ids.count(i) for i in set(ids)}; ps=Product.objects.filter(id__in=ids); total=sum(float(p.sale_price)*counts[str(p.id)] for p in ps); return render(r,'cart.html',{'products':ps,'counts':counts,'total':total})
def add_cart(r,pk):
 cart=r.session.get('cart',[]); cart.append(pk); r.session['cart']=cart; messages.success(r,'Product added to cart.'); return redirect(r.META.get('HTTP_REFERER','/'))
def remove_cart(r,pk): r.session['cart']=[x for x in r.session.get('cart',[]) if x!=pk]; return redirect('cart')
def update_cart(r):
 new=[]
 for k,v in r.POST.items():
  if k.startswith('qty_'):
   pk=int(k[4:]); new += [pk]*max(0,int(v or 0))
 r.session['cart']=new; return redirect('cart')
def wishlist(r): return render(r,'wishlist.html',{'products':Product.objects.filter(id__in=r.session.get('wishlist',[]))})
def toggle_wishlist(r,pk):
 w=r.session.get('wishlist',[]); w.remove(pk) if pk in w else w.append(pk); r.session['wishlist']=w; return redirect(r.META.get('HTTP_REFERER','/'))
def checkout(r):
 if not r.user.is_authenticated: return redirect('/login/?next=/checkout/')
 ids=r.session.get('cart',[]); ps=Product.objects.filter(id__in=ids); counts={i:ids.count(i) for i in set(ids)}; total=sum(float(p.sale_price)*counts[p.id] for p in ps)
 if r.method=='POST':
  o=Order.objects.create(user=r.user,full_name=r.POST['full_name'],address=r.POST['address'],city=r.POST['city'],pincode=r.POST['pincode'],mobile=r.POST['mobile'],payment_method=r.POST['payment_method'],total=total)
  for p in ps: OrderItem.objects.create(order=o,product=p,quantity=counts[p.id],price=p.sale_price); p.stock=max(0,p.stock-counts[p.id]); p.save()
  r.session['cart']=[]; return render(r,'success.html',{'order':o})
 return render(r,'checkout.html',{'products':ps,'counts':counts,'total':total})
def orders(r):
 if not r.user.is_authenticated:return redirect('/login/')
 return render(r,'orders.html',{'orders':Order.objects.filter(user=r.user).order_by('-created_at')})
def register(r):
 if r.method=='POST':
  if User.objects.filter(username=r.POST['username']).exists(): messages.error(r,'Username already exists.')
  else: u=User.objects.create_user(username=r.POST['username'],email=r.POST['email'],password=r.POST['password']); login(r,u); return redirect('home')
 return render(r,'register.html')
def user_login(r):
 if r.method=='POST':
  u=authenticate(username=r.POST['username'],password=r.POST['password'])
  if u: login(r,u); return redirect(r.GET.get('next','/'))
  messages.error(r,'Invalid username or password.')
 return render(r,'login.html')
def user_logout(r): logout(r); return redirect('home')
