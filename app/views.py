from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Customer, Product, Cart, PriceAlert
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from .forms import CustomerRegistrationForm,LoginForm,  CustomerProfileform
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
import json
import ast
from datetime import datetime
from rapidfuzz import fuzz
from .models import Category

@csrf_protect
def contact_view(request):
    if request.method == 'POST':
        # handle form submission logic here
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Process form data (save to database or send email)
        return HttpResponse("Message sent successfully!")
    return render(request, 'contact.html')

def get_descendant_categories(category):
    # Category is already imported at the top
    descendants = []
    children = Category.objects.filter(parent=category)
    for child in children:
        descendants.append(child)
        descendants.extend(get_descendant_categories(child))
    return descendants

def home(request):
    from django.conf import settings
    from showcase.views import get_top_posts
    
    # Show latest products as new products
    new_products = Product.objects.order_by('-id')[:8]  # Show latest 8 products
    main_categories = Category.objects.filter(parent=None)
    
    # Get clothing products for slideshow (look for clothing-related categories)
    clothing_keywords = ['cloth', 'fashion', 'shirt', 'dress', 'jeans', 'apparel', 'wear']
    clothing_categories = Category.objects.filter(
        Q(name__icontains='cloth') | 
        Q(name__icontains='fashion') |
        Q(name__icontains='apparel') |
        Q(name__icontains='wear')
    )
    slideshow_products = Product.objects.filter(category__in=clothing_categories)[:6] if clothing_categories.exists() else Product.objects.order_by('-id')[:6]
    
    # Get top posts from showcase
    top_posts = get_top_posts(limit=5)
    
    return render(request, "app/index.html", {
        'new_products': new_products,
        'main_categories': main_categories,
        'slideshow_products': slideshow_products,
        'top_posts': top_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    })
def about(request):
    return render(request, "app/about.html")
def contact(request):
    return render(request, "app/contact.html")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or dashboard
            else:
                messages.error(request, "Invalid login credentials.")
        else:
            messages.error(request, "Form is not valid.")
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})
class CategoryView(View):
    def get(self, request, val=None):
        if not val:
            return redirect('home')
        # Find the selected category by name
        category = Category.objects.filter(name=val).first()
        if not category:
            return render(request, "app/category.html", {"product": [], "pro": val, "title": []})
        # Get children of this category for navigation
        children = Category.objects.filter(parent=category)
        # If the category has children, show products from all descendants
        if children.exists():
            descendant_categories = get_descendant_categories(category)
            if descendant_categories:
                products = Product.objects.filter(category__in=descendant_categories)
            else:
                products = Product.objects.none()
            return render(request, "app/category.html", {"product": products, "pro": category.name, "title": children})
        else:
            # Leaf category: show only products in this category
            products = Product.objects.filter(category=category)
            return render(request, "app/category.html", {"product": products, "pro": category.name, "title": []})

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title= val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
class ProductDetail(View):
    def get(self, request, pk):
        """Fetch the specific product based on pk, return 404 if not found."""
        product = get_object_or_404(Product, pk=pk)
        existing_alert = None
        if request.user.is_authenticated:
            existing_alert = PriceAlert.objects.filter(user=request.user, product=product, fulfilled=False).first()
        return render(request, "app/productdetail.html", {"product": product, "existing_alert": existing_alert})
class CustomerRegistrationView(View):
   def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/rregistration.html', locals())
   def post(self,request):
       form = CustomerRegistrationForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request,"congratulation! You are part of chick style community")
       else:
           messages.warning(request,"Invalid data")
       
       return render(request, 'app/rregistration.html', locals())
class ProfileView(View):
    def get(self,request):
       form =  CustomerProfileform()
       return render(request, 'app/profile.html', locals())
    def post(self,request):
        form = CustomerProfileform(request.POST)
        if form.is_valid():
            user =request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcode=zipcode
            )
            reg.save()
            messages.success(request, 'Your profile has been updated successfully.')
        else:
            # Add error message if form is not valid
            messages.error(request, 'There was an error updating your profile. Please check your inputs.')
        return render(request, 'app/profile.html', locals())
           
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render ( request ,'app/address.html',locals())

class updateAdress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileform(instance=add)
        return render ( request ,'app/updateaddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileform(request.POST)
        if form.is_valid():
          add = Customer.objects.get(pk=pk)
          add.name = form.cleaned_data['name']
          add.locality = form.cleaned_data['locality']
          add.city = form.cleaned_data['city']
          add.mobile = form.cleaned_data['mobile']
          add.state = form.cleaned_data['state']
          add.zipcode = form.cleaned_data['zipcode']

          add.save()
          messages.success(request,"Congratulations! profile updated")
        
        else:
          messages.warning(request,"invalid data :)")
        return redirect("address")
@login_required(login_url='login')
def add_to_cart(request):
    """Add product to user's cart. If already exists, increment quantity."""
    user = request.user
    
    # Get product_id from both GET and POST parameters
    product_id = request.GET.get('prod_id') or request.POST.get('prod_id')
    
    # Validate product_id exists
    if not product_id:
        messages.error(request, 'No product selected.')
        return redirect('home')
    
    # Try to get the product, redirect if not found
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found. It may have been removed.')
        return redirect('home')
    except (ValueError, TypeError):
        messages.error(request, 'Invalid product ID.')
        return redirect('home')
    
    # Get or create cart item, increment quantity if exists
    cart_item, created = Cart.objects.get_or_create(
        user=user, 
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Item already exists, increment quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'{product.title} quantity updated!')
    else:
        messages.success(request, f'{product.title} added to cart!')
    
    return redirect("showcart")

@login_required
def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40

    return render (request ,'app/addtocart.html',locals())
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        # Allow GET request for logout
        return super().get(request, *args, **kwargs)
def logout_view(request):
   

    logout(request)  # This function clears the session and logs out the user.
    return redirect('login')     

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data= {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data= {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)

    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data= {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)

# ---------------------------------------------------------------------------
#  PRICE ALERTS
# ---------------------------------------------------------------------------

@login_required
@require_POST
def set_price_alert(request, pk):
    """Handle the form submission coming from the product-detail page."""
    product = get_object_or_404(Product, pk=pk)

    try:
        target_price = float(request.POST.get('target_price'))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid price value.")
        return redirect('product-detail', pk=pk)

    buy_when_drop = bool(request.POST.get('buy_when_drop'))

    alert, created = PriceAlert.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={
            'target_price': target_price,
            'buy_when_drop': buy_when_drop,
            'fulfilled': False,
        }
    )

    if created:
        msg = f"Alert set at ₹{target_price}. We'll notify you when the price drops!"
    else:
        msg = f"Alert updated to ₹{target_price}."
    if buy_when_drop:
        msg += " We'll automatically buy at that price."
    messages.success(request, msg)

    return redirect('product-detail', pk=pk)

@login_required(login_url='login')
def buy_now(request):
    """Add item to cart (if not already) and go straight to checkout."""
    user = request.user
    
    # Get product_id from both GET and POST parameters
    product_id = request.GET.get('prod_id') or request.POST.get('prod_id')
    
    # Validate product_id exists
    if not product_id:
        messages.error(request, 'No product selected.')
        return redirect('home')
    
    # Try to get the product, redirect if not found
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found. It may have been removed.')
        return redirect('home')
    except (ValueError, TypeError):
        messages.error(request, 'Invalid product ID.')
        return redirect('home')
    
    # Add to cart and proceed to checkout
    Cart.objects.get_or_create(user=user, product=product, defaults={'quantity': 1})
    return redirect('checkout')

def search(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        results = Product.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
    return render(request, 'app/search_results.html', {'query': query, 'results': results})

def assistant(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
    chat_history = request.session['chat_history']
    response = None
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Handle AJAX requests for chatbot
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user_query = request.POST.get("query", "")
        
        # Get Gemini API key
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            load_dotenv()
            GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        
        if not GEMINI_API_KEY:
            return JsonResponse({
                'success': False,
                'response': 'Gemini API key is missing. Please set GEMINI_API_KEY in your .env file.'
            })
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Check if it's a recipe/cooking request
        is_recipe = any(word in user_query.lower() for word in ['cook', 'make', 'prepare', 'recipe', 'how to'])
        
        if is_recipe:
            response_html = handle_recipe_query(user_query, model)
        else:
            response_html = handle_product_query(user_query, model)
        
        chat_history.append({'user': user_query, 'assistant': response_html, 'timestamp': now})
        request.session['chat_history'] = chat_history
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'response': response_html
        })
    
    if request.method == "POST":
        if 'clear_chat' in request.POST or request.POST.get('clear_chat') is not None:
            request.session['chat_history'] = []
            return render(request, 'app/assistant.html', {'chat_history': []})
        user_query = request.POST.get("query", "")
        # Always try to get the Gemini API key from the environment
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            load_dotenv()
            GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            response = "<div class='text-danger'>Gemini API key is missing. Please set GEMINI_API_KEY in your .env file or environment variables.</div>"
            chat_history.append({'user': user_query, 'assistant': response, 'timestamp': now, 'type': 'current'})
            request.session['chat_history'] = chat_history
            return render(request, 'app/assistant.html', {'chat_history': chat_history})
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Detect if the query is a recipe/cooking request
        is_recipe = any(word in user_query.lower() for word in ['cook', 'make', 'prepare', 'recipe', 'how to'])
        if is_recipe:
            # 1. Get recipe and ingredients under budget
            recipe_prompt = f"""
            Give me a simple recipe for: {user_query}. List the ingredients and their approximate prices in INR, total cost under the mentioned budget if possible. Format as:
            Recipe: ...
Ingredients:
- item1 (price)
- item2 (price)
...
Instructions: ...
            """
            recipe_response = model.generate_content(recipe_prompt)
            recipe_text = recipe_response.text.strip()
            # 2. Extract keywords for product matching
            keyword_prompt = f"""
            From this recipe and ingredient list, extract keywords that could match products in an online grocery or general store. Return as a Python list of strings.\n\n{recipe_text}
            """
            keyword_response = model.generate_content(keyword_prompt)
            import ast
            try:
                keywords = ast.literal_eval(keyword_response.text.strip().split('```')[-1] if '```' in keyword_response.text else keyword_response.text)
                if not isinstance(keywords, list):
                    keywords = []
            except Exception:
                keywords = []
            import re
            budget_match = re.search(r'under\s*₹?\s*(\d+)', user_query, re.IGNORECASE)
            budget = int(budget_match.group(1)) if budget_match else 100  # Default to 100 if not found
            # Build product list under budget
            available_products = Product.objects.filter(discounted_price__lte=budget)
            product_list = [
                f"{p.title} - ₹{p.discounted_price}: {p.description[:50]}" for p in available_products
            ]
            product_list_str = "\n".join(product_list)
            gemini_match_prompt = f"""
User query: {user_query}
Here is a list of products available (title, price, short description):

{product_list_str}

Which of these products best match the user's request? Only return a valid Python list of product titles. Do not include any explanation or summary.
"""
            gemini_match_response = model.generate_content(gemini_match_prompt)
            try:
                selected_titles = ast.literal_eval(gemini_match_response.text.strip().split('```')[-1] if '```' in gemini_match_response.text else gemini_match_response.text)
                if not isinstance(selected_titles, list):
                    selected_titles = []
            except Exception:
                selected_titles = []
            matched_products = Product.objects.filter(title__in=selected_titles)
            # Fallback: If Gemini returns no matches, use keyword matching for all ingredients
            if not matched_products.exists() and keywords:
                print("Fallback keyword matching triggered. Keywords:", keywords)  # Debug print
                matched_products = Product.objects.none()
                for kw in keywords:
                    # --- NEW LOGIC: hierarchical category matching ---
                    cat_qs = Category.objects.filter(name__icontains=kw)
                    if cat_qs.exists():
                        all_cats = []
                        for cat in cat_qs:
                            all_cats.append(cat)
                            all_cats.extend(get_descendant_categories(cat))
                        matched_products = matched_products | Product.objects.filter(
                            discounted_price__lte=budget,
                            category__in=all_cats
                        )
                    # --- End new logic ---
                    matched_products = matched_products | Product.objects.filter(
                        discounted_price__lte=budget,
                        title__icontains=kw
                    )
                    matched_products = matched_products | Product.objects.filter(
                        discounted_price__lte=budget,
                        description__icontains=kw
                    )
                matched_products = matched_products.distinct()
                print("Matched products after fallback:", list(matched_products))  # Debug print
            # Final fallback: fuzzy match user query words to product title/description words if still no products
            if not matched_products.exists() and budget:
                print("Final fallback: fuzzy matching user query to product words.")
                from rapidfuzz import fuzz
                user_words = re.findall(r'\b\w+\b', user_query)
                all_titles = Product.objects.values_list('title', flat=True)
                all_descriptions = Product.objects.values_list('description', flat=True)
                combined_text = " ".join(list(all_titles) + list(all_descriptions)).lower()
                db_keywords = list(set(re.findall(r'\b\w+\b', combined_text)))
                matched_keywords = []
                for user_word in user_words:
                    for db_word in db_keywords:
                        if fuzz.partial_ratio(user_word, db_word) > 85:
                            matched_keywords.append(db_word)
                from django.db.models import Q
                keyword_filter = Q()
                for kw in matched_keywords:
                    keyword_filter |= Q(title__icontains=kw) | Q(description__icontains=kw)
                matched_products = Product.objects.filter(
                    discounted_price__lte=budget
                ).filter(keyword_filter)
                matched_products = matched_products.distinct()
                print("Matched products after fuzzy fallback:", list(matched_products))
            # 4. Prepare product cards
            product_cards = []
            for p in matched_products:
                detail_url = f"/product-detail/{p.pk}/"
                add_to_cart_url = f"/add-to-cart/?prod_id={p.pk}"
                card = f"""
                <div class='card mb-3' style='max-width: 500px;'>
                    <div class='row g-0'>
                        <div class='col-md-4'>
                            <img src='{p.product_image.url if p.product_image else ''}' class='img-fluid rounded-start' alt='{p.title}'>
                        </div>
                        <div class='col-md-8'>
                            <div class='card-body'>
                                <h5 class='card-title'>{p.title}</h5>
                                <p class='card-text'><b>₹{p.discounted_price}</b></p>
                                <p class='card-text'><small class='text-muted'>{p.description}</small></p>
                                <a href='{detail_url}' class='btn btn-outline-primary btn-sm' target='_blank'>View Product</a>
                                <a href='{add_to_cart_url}' class='btn btn-success btn-sm ms-2'>Add to Cart</a>
                            </div>
                        </div>
                    </div>
                </div>
                """
                product_cards.append(card)
            # 5. Compose the response
            summary = f"<div class='mb-2'><b>Recipe & Ingredients:</b><br>{recipe_text.replace('\n','<br>')}</div>"
            if matched_products.exists():
                summary += "<div class='mb-2'><b>Recommended products from our store under your budget:</b></div>"
                summary += ''.join(product_cards)
            else:
                summary += "<div class='mb-2 text-muted'>No matching products found in our store under your budget, but here's a recipe you can try!" + "</div>"
            response = summary
        else:
            # --- Product recommendation logic ---
            response = handle_product_query_full(user_query, model)
            
        chat_history.append({'user': user_query, 'assistant': response, 'timestamp': now, 'type': 'current'})
        request.session['chat_history'] = chat_history
        return render(request, 'app/assistant.html', {'chat_history': chat_history})
    return render(request, 'app/assistant.html', {'chat_history': chat_history})


def handle_recipe_query(user_query, model):
    """Handle recipe-related queries and return formatted HTML response."""
    recipe_prompt = f"""
    Give me a simple recipe for: {user_query}. List the ingredients and their approximate prices in INR, total cost under the mentioned budget if possible. Format as:
    Recipe: ...
    Ingredients:
    - item1 (price)
    - item2 (price)
    ...
    Instructions: ...
    """
    recipe_response = model.generate_content(recipe_prompt)
    recipe_text = recipe_response.text.strip()
    
    # Extract budget
    budget_match = re.search(r'under\s*₹?\s*(\d+)', user_query, re.IGNORECASE)
    budget = int(budget_match.group(1)) if budget_match else 100
    
    # Build product list under budget
    available_products = Product.objects.filter(discounted_price__lte=budget)
    product_list = [f"{p.title} - ₹{p.discounted_price}" for p in available_products]
    product_list_str = "\n".join(product_list)
    
    matched_products = Product.objects.none()
    if product_list:
        gemini_match_prompt = f"""
        User query: {user_query}
        Here is a list of products available (title, price):
        {product_list_str}
        Which of these products best match the user's request for ingredients? Return only product titles as a comma-separated list.
        """
        try:
            gemini_match_response = model.generate_content(gemini_match_prompt)
            selected_titles_text = gemini_match_response.text.strip()
            selected_titles = [t.strip() for t in selected_titles_text.split(',') if t.strip()]
            matched_products = Product.objects.filter(title__in=selected_titles)
        except Exception:
            pass
    
    # Prepare product cards
    product_cards = []
    for p in matched_products:
        detail_url = f"/product-detail/{p.pk}/"
        add_to_cart_url = f"/add-to-cart/?prod_id={p.pk}"
        card = f"""
        <div class='product-card'>
            <img src='{p.product_image.url if p.product_image else ''}' alt='{p.title}'>
            <div class='product-info'>
                <h6>{p.title}</h6>
                <p class='price'>₹{p.discounted_price}</p>
                <div class='product-actions'>
                    <a href='{detail_url}' class='btn-view' target='_blank'>View</a>
                    <a href='{add_to_cart_url}' class='btn-cart'>Add to Cart</a>
                </div>
            </div>
        </div>
        """
        product_cards.append(card)
    
    # Format recipe text nicely
    recipe_html = recipe_text.replace('\n', '<br>')
    summary = f"<div class='recipe-response'><strong>Recipe & Ingredients:</strong><br>{recipe_html}</div>"
    
    if matched_products.exists():
        summary += "<div class='products-header'><strong>Recommended products from our store:</strong></div>"
        summary += '<div class="products-grid">' + ''.join(product_cards) + '</div>'
    else:
        summary += "<div class='info-message'>No matching products found in our store, but here's a recipe you can try!</div>"
    
    return summary


def handle_product_query(user_query, model):
    """Handle product recommendation queries and return formatted HTML response."""
    # Simple keyword extraction instead of complex Gemini parsing
    user_query_lower = user_query.lower()
    
    # Extract budget from query
    budget = None
    budget_match = re.search(r'under\s*₹?\s*(\d+)', user_query, re.IGNORECASE)
    if budget_match:
        budget = int(budget_match.group(1))
    
    # Direct category matching from user query
    category = None
    
    # Get all categories from database
    all_categories = Category.objects.all()
    category_names = [cat.name.lower() for cat in all_categories]
    
    # Check if any category name is in the user query
    for cat in all_categories:
        if cat.name.lower() in user_query_lower:
            category = cat.name
            break
    
    # If no exact match, try common shopping keywords
    if not category:
        keyword_mapping = {
            'laptop': 'Electronics',
            'phone': 'Electronics',
            'mobile': 'Electronics',
            'computer': 'Electronics',
            'cloth': 'Clothing',
            'dress': 'Clothing',
            'shirt': 'Clothing',
            'pant': 'Clothing',
            'jeans': 'Clothing',
            'ethnic': 'Clothing',
            'traditional': 'Clothing',
            'western': 'Clothing',
            'kurta': 'Clothing',
            'saree': 'Clothing',
            'lehenga': 'Clothing',
            'shoes': 'Shoes',
            'footwear': 'Shoes',
            'watch': 'Watches',
            'jewel': 'Jewellery',
            'beauty': 'Health & Beauty',
            'cosmetic': 'Health & Beauty',
            'kids': 'Kids & Babies',
            'baby': 'Kids & Babies',
            'sport': 'Sports',
            'home': 'Home & Garden',
            'garden': 'Home & Garden',
        }
        
        for keyword, cat_name in keyword_mapping.items():
            if keyword in user_query_lower:
                # Check if this category exists in database
                if Category.objects.filter(name__icontains=cat_name).exists():
                    category = cat_name
                    break
    
    matched_products = Product.objects.none()
    response = None
    
    if category:
        cat_qs = Category.objects.filter(Q(name__icontains=category))
        if cat_qs.exists():
            all_cats = []
            for cat in cat_qs:
                all_cats.append(cat)
                all_cats.extend(get_descendant_categories(cat))
            
            if budget:
                matched_products = Product.objects.filter(
                    category__in=all_cats,
                    discounted_price__lte=budget
                )
            else:
                matched_products = Product.objects.filter(category__in=all_cats)
                # If no budget specified and no products, suggest specifying budget
                if not matched_products.exists():
                    return f"<div class='info-message'>I found the category '{category}'. Please specify your budget to see products. For example: 'Show me {category} under ₹5000'</div>"
        else:
            return f"<div class='info-message'>Sorry, I couldn't find products in the '{category}' category. Try browsing our categories or ask me about Electronics, Clothing, Shoes, Watches, or other categories.</div>"
    else:
        # No category found - provide helpful guidance
        available_categories = Category.objects.filter(parent=None)[:6]
        cat_list = ', '.join([cat.name for cat in available_categories])
        return f"<div class='info-message'>Please specify what you're looking for! Try asking about: {cat_list}, or tell me what product you need.</div>"
    
    # If we have matching products, build product cards
    if matched_products.exists():
        product_cards = []
        display_count = min(matched_products.count(), 6)  # Show max 6 products
        for p in matched_products[:display_count]:
            detail_url = f"/product-detail/{p.pk}/"
            add_to_cart_url = f"/add-to-cart/?prod_id={p.pk}"
            card = f"""
            <div class='product-card'>
                <img src='{p.product_image.url if p.product_image else ''}' alt='{p.title}'>
                <div class='product-info'>
                    <h6>{p.title}</h6>
                    <p class='price'>₹{p.discounted_price}</p>
                    <div class='product-actions'>
                        <a href='{detail_url}' class='btn-view' target='_blank'>View</a>
                        <a href='{add_to_cart_url}' class='btn-cart'>Add to Cart</a>
                    </div>
                </div>
            </div>
            """
            product_cards.append(card)
        
        budget_text = f" under ₹{budget}" if budget else ""
        response = f"<div class='products-header'><strong>Found {matched_products.count()} products in {category}{budget_text}:</strong></div>"
        response += '<div class="products-grid">' + ''.join(product_cards) + '</div>'
        
        if matched_products.count() > 6:
            response += f"<div class='info-message'>Showing 6 of {matched_products.count()} products. Visit the category page to see all items.</div>"
    elif budget:
        response = f"<div class='info-message'>No products found in {category} under ₹{budget}. Try increasing your budget or browse other categories.</div>"
    else:
        response = f"<div class='info-message'>No products found in {category}. Please check our other categories.</div>"
    
    return response


def handle_product_query_full(user_query, model):
    """Full handler for product queries (non-AJAX version)."""
    return handle_product_query(user_query, model)


# ---------------------------------------------------------------------------
#  STRIPE PAYMENT INTEGRATION
# ---------------------------------------------------------------------------

import stripe
from django.conf import settings
from decimal import Decimal

# Configure Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url='login')
def checkout_view(request):
    """
    Create Stripe checkout session from cart items.
    Calculates total, creates order with pending status, and redirects to Stripe.
    """
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('showcart')
    
    # Calculate total from database (NEVER trust frontend)
    line_items = []
    total_amount = Decimal('0.00')
    
    for cart_item in cart_items:
        product = cart_item.product
        quantity = cart_item.quantity
        price = int(product.discounted_price * 100)  # Convert to paise
        
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': product.title,
                    'description': product.description[:255] if product.description else '',
                    'images': [request.build_absolute_uri(product.product_image.url)] if product.product_image else [],
                },
                'unit_amount': price,
            },
            'quantity': quantity,
        })
        
        total_amount += Decimal(product.discounted_price) * quantity
    
    # Add shipping cost (₹40)
    line_items.append({
        'price_data': {
            'currency': 'inr',
            'product_data': {
                'name': 'Shipping',
            },
            'unit_amount': 4000,  # ₹40 in paise
        },
        'quantity': 1,
    })
    total_amount += Decimal('40.00')
    
    try:
        # Create Stripe session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/payment-success/?session_id={CHECKOUT_SESSION_ID}'),
            cancel_url=request.build_absolute_uri('/payment-cancel/'),
            customer_email=user.email,
        )
        
        # Create order with pending status
        from .models import Order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_status='pending',
            stripe_session_id=session.id,
        )
        
        # Store order ID in session for server-side verification
        request.session['pending_order_id'] = order.id
        
        return redirect(session.url)
        
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('showcart')


@login_required(login_url='login')
def payment_success_view(request):
    """
    Verify Stripe payment status and mark order as paid.
    Retrieves session using session_id from URL query parameter.
    """
    from .models import Order
    
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, 'Invalid payment session. Please contact support.')
        return redirect('home')
    
    try:
        # Retrieve session from Stripe API
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Verify payment status
        if session.payment_status != 'paid':
            messages.error(request, 'Payment was not completed. Please try again.')
            return redirect('showcart')
        
        # Find order by stripe_session_id
        try:
            order = Order.objects.get(stripe_session_id=session_id, user=request.user)
        except Order.DoesNotExist:
            messages.error(request, 'Order not found. Please contact support.')
            return redirect('home')
        
        # Mark order as paid
        order.payment_status = 'paid'
        order.save()
        
        # Create OrderItems from cart
        cart_items = Cart.objects.filter(user=request.user)
        from .models import OrderItem
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.discounted_price,
            )
        
        # Clear cart after order confirmation
        cart_items.delete()
        
        messages.success(request, f'Payment successful! Order #{order.id} confirmed.')
        
        return render(request, 'app/payment_success.html', {
            'order': order,
        })
        
    except stripe.error.InvalidRequestError:
        messages.error(request, 'Invalid payment session. Please contact support.')
        return redirect('home')
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment verification error: {str(e)}')
        return redirect('showcart')


@login_required(login_url='login')
def payment_cancel_view(request):
    """
    Payment cancelled by user. Order remains in pending state.
    """
    return render(request, 'app/payment_cancel.html')


@csrf_exempt  # Stripe webhook doesn't include CSRF token
@require_http_methods(["POST"])
def stripe_webhook_view(request):
    """
    Stripe webhook handler. Verifies signature and processes checkout.session.completed event.
    """
    from .models import Order, OrderItem
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        # Verify Stripe signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session['id']
        
        try:
            # Find order by Stripe session ID
            order = Order.objects.get(stripe_session_id=session_id)
            
            # Mark order as paid
            order.payment_status = 'paid'
            order.save()
            
            # Save order items from cart
            cart_items = Cart.objects.filter(user=order.user)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.discounted_price,
                )
            
            # Clear cart
            cart_items.delete()
            
            return JsonResponse({'success': True}, status=200)
            
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
    
    return JsonResponse({'success': True}, status=200)


@login_required(login_url='login')
def order_history_view(request):
    """
    Display order history for logged-in user.
    """
    from .models import Order
    from django.core.paginator import Paginator
    
    user = request.user
    orders = Order.objects.filter(user=user).prefetch_related('items__product')
    
    # Add pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'app/order_history.html', {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
    })


@login_required(login_url='login')
def order_detail_view(request, order_id):
    """
    Display details of a specific order.
    """
    from .models import Order
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'app/order_detail.html', {
        'order': order,
    })
