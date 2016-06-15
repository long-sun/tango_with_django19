from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. of likes in descending order.
    # Retrive the top 5 only -or all if less than 5
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # mvpage_list is the list of the most views pages
    # add it in the context_dict above
    mvpage_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = mvpage_list
    # Return a rendered response to send to the client.
    # We make use of the shortcut funtion to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'boldmessage' : "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/about.html', context=context_dict)

def category(request, category_name_slug):
    # Creat a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrive all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['pages'] = pages
        context_dict['category_name_slug'] = category_name_slug
        context_dict['category'] = category
    except:
        pass

    return render(request, 'rango/category.html', context_dict)
    
@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to database
            form.save(commit=True)

            # Now call the index() view
            # The user will be shown to the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()
    # Bad form (or form details), no form supplied...
    # Render the form with error message (if any)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)  # If you call save() with commit=False, 
                page.category = cat             # then it will return an object that 
                page.views = 0                  # hasn’t yet been saved to the database
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm

    context_dict = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # process with the picture from input if it exist.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', 
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):

    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
            # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
            # because the request.POST.get('<variable>') return None, if the value does not exist,
            # while the request.POST['variable'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inaactive account was used - no logging in!
                return HttpResponse('Your Rango account is disabled.')
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username,password))
            return HttpResponse("Invalid login details supplied")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET
    else:
        # No context variables to pass to the template system, hence the blank dictionary object..
        return render(request, 'rango/login.html', {})