from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from video.models import Video, Comment, Tag, Like, Requesto
from video.forms import CommentForm
from django.utils import timezone
from video.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
def index(request):

    popvids = Video.objects.order_by('-likes')[:4]
    newvids = Video.objects.order_by('-uploaded')[:4]
    context_dict = {'popvids': popvids, 'newvids': newvids}

    return render(request, 'video/index.html', context_dict)

def watchVid(request, video_id):
    context_dict = {'id': video_id}

    if request.method == 'POST':
        r = request.POST
        c = Comment.objects.get_or_create(
            name=request.user.username,
            user_id=request.user.pk,
            text=r['text'],
            video_id=video_id,
            posted=timezone.now(),
        )

    context_dict['comments'] = Comment.objects.filter(video_id=video_id)

    try:
        v = Video.objects.get(video_id=video_id)
        context_dict['video'] = v
        context_dict['favorite'] = Like.objects.filter(video_id=video_id, name=request.user.pk).exists()
    except Video.DoesNotExist:
        pass

    return render(request, 'video/watchVid.html', context_dict)

def search(request, tag=None):

    if tag:
        t = Tag.objects.filter(name=tag).values_list('video_id', flat=True)
        searchResult = Video.objects.filter(video_id__in=t)
        context_dict = {'query': tag}
    else:
        query = request.GET['query']
        context_dict = {'query': query}

        querylist = query.split()

        searchResult = Video.objects.all()
        for q in querylist:
            searchResult = searchResult.filter(name__contains=q)

    searchResult5 = []
    hit = len(searchResult)
    for i in range(0, hit, 4):
        searchResult5 += [searchResult[i:min(i+4, hit)]]

    context_dict['result'] = searchResult5
    context_dict['hit'] = hit

    return render(request, 'video/search.html', context_dict)

def register(request):

    registered = False
    context_dict = {}

    if request.method == 'POST':
        print(request.POST)
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
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

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            context_dict['fail'] = True
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered

    # Render the template depending on the context.
    return render(request,
            'video/register.html',
            context_dict)

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
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
                return HttpResponseRedirect('/video/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Video account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'video/login.html', {'fail': True})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'video/login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/video/')

def mypage(request, sort=0):
    if request.method == 'POST':
        Like.objects.get_or_create(
            name=request.user.pk,
            video_id=request.POST['id'],
            timestamp=timezone.now(),
        )
        v = Video.objects.get(video_id=request.POST['id'])
        v.likes = len(Like.objects.filter(video_id=request.POST['id']))
        v.save()

    like_id = Like.objects.values_list('video_id', flat=True).filter(name=request.user.pk)

    likes = Video.objects.filter(video_id__in=like_id)

    likeResult4 = []
    hit = len(likes)
    for i in range(0, hit, 4):
        likeResult4 += [likes[i:min(i+4, hit)]]

    context_dict = {'likes': likeResult4}

    # Eventually make this a script that runs once a day for active users and updates their list of recommendations
    v = Video.objects.all()

    if sort == 1:
        v = v[::-1]
    elif sort == 2:
        v = v.order_by('name')
    elif sort == 3:
        v = v.order_by('-likes')
    elif sort == 4:
        v = v.order_by('-uploaded')

    v_rank = {}
    for video in v:
        v_rank[video.video_id] = 0.0
    if len(like_id) > 0:
        for user in User.objects.filter(~Q(pk=request.user.pk)):
            l_user = Like.objects.values_list('video_id', flat=True).filter(name=user.pk)
            l_self = like_id
            if len(l_user) > 0:
                overlap = len(set(l_user).intersection(l_self))/len(l_user)
                for vid in l_user:
                    v_rank[vid] += overlap

        for vid in like_id:
            v_rank[vid] = 0

        top4id = sorted(v_rank, key=v_rank.get, reverse=True)[:4]

        context_dict['osusume'] = Video.objects.filter(video_id__in=top4id)
    else:
        context_dict['osusume'] = None

    return render(request, 'video/mypage.html', context_dict)

def random(request):
    v = Video.objects.order_by('?').first()

    context_dict = {'comments': Comment.objects.filter(video_id=v.video_id)}

    try:
        context_dict['video'] = v
        context_dict['favorite'] = Like.objects.filter(video_id=v.video_id, name=request.user.pk).exists()
    except Video.DoesNotExist:
        pass

    return render(request, 'video/watchVid.html', context_dict)

def tags(request):
    t = Tag.objects.order_by('name').values_list('name', flat=True)
    context_dict = {'tags': set(t)}
    return render(request, 'video/tags.html', context_dict)

def requesto(request):
    requested = False
    if request.method == 'POST':
        r = request.POST
        if len(Requesto.objects.all()) < 100:
            c = Requesto.objects.get_or_create(
                user_id=request.user.pk,
                text=r['text'],
            )
        requested = True
    context_dict = {'request': requested}
    return render(request, 'video/requesto.html', context_dict)

def info(request):
    return render(request, 'video/info.html')