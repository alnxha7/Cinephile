from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login, logout
from .models import User, Movies, Review, AspirantPosts, Reactions
from datetime import datetime
from django.db.models import Q, Count

def home(request):
    return render(request, 'index.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        location = request.POST.get('location')
        role = request.POST.get('role')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        if User.objects.create(username=username, 
                            mobile=mobile, 
                            email=email, 
                            location=location, 
                            role=role, 
                            password=make_password(password), 
                            image=image):
            
            return redirect('login')
        else:
            return redirect('register_user')

    return render(request, 'register_user.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                login(request, user)

                if user.is_superuser:
                    print('user is superuser')
                    return redirect('admin_index')
                elif user.role == 'critics':
                    if user.verification_status == True:
                        print('user is critics')
                        return redirect('critics_index')
                    else:
                        return render(request, 'login.html', {'message': 'The admin is not approved you'})
                    
                elif user.role == 'aspirant':
                    if user.verification_status == True:
                        print('user is aspirant')
                        return redirect('aspirant_index')
                    else:
                        return render(request, 'login.html', {'message': 'The admin is not approved you'})
                    
                elif user.role == 'agency':
                    if user.verification_status == True:
                        print('user is agency')
                        return redirect('agency_index')
                    else:
                        return render(request, 'login.html', {'message': 'The admin is not approved you'}) 
                
            else:
                print('invalid email or password')
                return redirect('login')
        except User.DoesNotExist:
            print('user dows not exist')
            return redirect('home')
        
    return render(request, 'login.html')

def admin_index(request):
    return render(request, 'admin_index.html')

def agency_index(request):
    return render(request, 'agency_index.html')

def critics_index(request):
    return render(request, 'critics_index.html')

def aspirant_index(request):
    return render(request, 'aspirant_index.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def user_approval(request):
    users = User.objects.filter(verification_status=False, is_superuser=False)
    approved_users = User.objects.filter(verification_status=True, is_superuser=False)
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        if action == 'approve':
            user = User.objects.get(id=user_id)
            user.verification_status = True
            user.save()
        elif action == 'remove':
            user = User.objects.get(id=user_id)
            user.delete()
        
    return render(request, 'user_approval.html', {'users': users, 'approved_users': approved_users})

def add_movie(request):
    movies = Movies.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        year = request.POST.get('year')
        director = request.POST.get('director')
        language = request.POST.get('language')
        image = request.FILES.get('image')
        action = request.POST.get('action')

        if action == 'add':
            Movies.objects.create(title=title, year=year, director=director, language=language, image=image)
            return redirect('add_movie')
        elif action == 'delete':
            movie_id = request.POST.get('movie_id')
            movie = Movies.objects.get(id=movie_id)
            movie.delete()
        elif action == 'edit':
            movie_id = request.POST.get('movie_id')
            return redirect('edit_movie', movie_id=movie_id)
        elif action == 'show':
            movie_id = request.POST.get('movie_id')
            return redirect('admin_manage_reviews', movie_id=movie_id)
    return render(request, 'add_movie.html', {'movies': movies})

def edit_movie(request, movie_id):
    movie = Movies.objects.get(id=movie_id)
    movies = Movies.objects.all()

    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.year = request.POST.get('year')
        movie.director = request.POST.get('director')
        movie.language = request.POST.get('language')
        if request.FILES.get('image'):
            movie.image = request.FILES.get('image')

        movie.save()
    return render(request, 'edit_movie.html', {'movie': movie, 'movies': movies})

def critics_view_movies(request):
    movies = Movies.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        movie_id = request.POST.get('movie_id')
        if action == 'review':
            return redirect('review_movie', movie_id)
    return render(request, 'critics_view_movies.html', {'movies': movies})

def review_movie(request, movie_id):
    movie = Movies.objects.get(id=movie_id)
    movie_reviews = Review.objects.filter(movie=movie, user__role='critics')
    count = len(movie_reviews)

    try:
        review = Review.objects.get(user=request.user, movie=movie)
        context = {'movie': movie, 
                   'review': review, 
                   'movie_reviews': movie_reviews, 
                   'count': count}
        
        return render(request, 'review_movie.html', context)
    except Exception as e:
        print(e)

    if request.method == 'POST':
        user = request.user
        rating = int(request.POST.get('rating'))
        review = request.POST.get('comment')

        Review.objects.create(user=user, rating=rating, review=review, movie=movie, date=datetime.now())
        return redirect('critics_view_movies')

    return render(request, 'review_movie.html', {'movie': movie, 'movie_reviews': movie_reviews, 'movie_reviews': movie_reviews, 'count': count})

def admin_manage_reviews(request, movie_id):
    movie = Movies.objects.get(id=movie_id)
    movie_reviews = Review.objects.filter(movie=movie, user__role='critics')
    count = len(movie_reviews)
    return render(request, 'admin_manage_reviews.html', {'movie': movie, 'movie_reviews': movie_reviews, 'count': count})

def delete_review(request, movie_review_id):
    review = Review.objects.get(id=movie_review_id)
    movie_id = review.movie.id
    review.delete()
    return redirect('admin_manage_reviews', movie_id)

def aspirant_view_movies(request):
    movies = Movies.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        movie_id = request.POST.get('movie_id')
        if action == 'review':
            return redirect('aspirant_review', movie_id)
    return render(request, 'aspirant_view_movies.html', {'movies': movies})

def aspirant_review(request, movie_id):
    movie = Movies.objects.get(id=movie_id)
    movie_reviews = Review.objects.filter(movie=movie, user__role='critics')
    count = len(movie_reviews)
    context = {'movie_reviews': movie_reviews, 'count': count, 'movie': movie }
    try:
        review = Review.objects.get(user=request.user, movie=movie)
        context = {'movie': movie, 
                   'review': review, 
                   'movie_reviews': movie_reviews, 
                   'count': count}
        
        return render(request, 'aspirant_review.html', context)
    except Exception as e:
        print(e)

    if request.method == 'POST':
        user = request.user
        rating = int(request.POST.get('rating'))

        Review.objects.create(user=user, rating=rating, movie=movie, date=datetime.now())
        return redirect('aspirant_view_movies')

    return render(request, 'aspirant_review.html', context)

def aspirant_posts(request):
    posts = AspirantPosts.objects.filter(user=request.user)
    if request.method == 'POST':
        description = request.POST.get('description')
        file = request.FILES.get('file')
        action = request.POST.get('action')
        post_id = request.POST.get('post_id')

        if action == 'delete':
            post = AspirantPosts.objects.get(id=post_id)
            post.delete()
            return redirect('aspirant_posts')
        elif action == 'view':
            return redirect('post_details', post_id)

        try:
            AspirantPosts.objects.create(user=request.user, description=description, file=file)
            return redirect('aspirant_posts')
        except Exception as e:
            print(e)

    return render(request, 'aspirant_posts.html', {'posts': posts})

def post_details(request, post_id):
    # Fetch the post and reactions
    post = get_object_or_404(AspirantPosts, id=post_id)
    reactions = Reactions.objects.filter(post=post, is_commented=True)
    likes = Reactions.objects.filter(like=True, post=post).count()
    comments = Reactions.objects.filter(is_commented=True, post=post).count()

    # Get the user's reaction if it exists
    self_reaction = Reactions.objects.filter(user=request.user, post=post).first()

    if request.method == 'POST':
        # Handle form submission
        like = request.POST.get('like') == 'true'  # Convert to boolean
        comment = request.POST.get('comment', '')

        if self_reaction:
            # Update the existing reaction
            self_reaction.like = like
            self_reaction.comment = comment
            self_reaction.save()
        else:
            # Create a new reaction
            Reactions.objects.create(post=post, user=request.user, like=like, comment=comment)

        return redirect('post_details', post_id=post_id)

    # Render the template
    context = {
        'post': post,
        'likes': likes,
        'comments': comments,
        'reactions': reactions,
        'self_reaction': self_reaction,
    }
    return render(request, 'post_details.html', context)

def post_approval(request):
    posts = AspirantPosts.objects.filter(verification=False)
    approved_posts = AspirantPosts.objects.filter(verification=True)

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(AspirantPosts, id=post_id)

        if action == 'approve':
            post.verification = True
            post.save()
            return redirect('post_approval')
        elif action == 'delete':
            post.delete()
            return redirect('post_approval')
        elif action == 'remove':
            post.verification = False
            post.save()
            return redirect('post_approval')
    return render(request, 'post_approval.html', {'posts': posts, 'approved_posts': approved_posts})

def all_posts(request):
    posts = AspirantPosts.objects.filter(verification=True).annotate(
        like_count=Count('reactions', filter=Q(reactions__like=True)),
        comment_count=Count('reactions', filter=Q(reactions__is_commented=True))
    ).order_by('-uploaded_at')

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        if action == 'react':
            return redirect('agency_react', post_id)
    return render(request, 'all_posts.html', {'posts': posts})

def agency_react(request, post_id):
    post = get_object_or_404(AspirantPosts, id=post_id)
    reactions = Reactions.objects.filter(post=post, is_commented=True)
    likes = Reactions.objects.filter(post=post, like=True).count()
    comments = Reactions.objects.filter(is_commented=True, post=post).count()

    self_reaction = Reactions.objects.filter(post=post, user=request.user).first()
    if request.method == 'POST':
        # Handle form submission
        like = request.POST.get('like') == 'true'  # Convert to boolean
        comment = request.POST.get('comment', '').strip()

        if self_reaction:
            # Update the existing reaction
            self_reaction.like = like
            self_reaction.comment = comment
            self_reaction.save()
        else:
            # Create a new reaction
            Reactions.objects.create(post=post, user=request.user, like=like, comment=comment)
        return redirect('agency_react', post_id)
    
    context = {'reactions': reactions, 'post': post, 'likes': likes, 'comments': comments, 'self_reaction': self_reaction}
    return render(request, 'agency_react.html', context)