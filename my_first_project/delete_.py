import os

os.environ[
    'PYTHONPATH'] = r'F:\AI and machine learning\sobhan\00 Python\Corey Schafe playlists\Django Tutorials\my_first_project'
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_first_project.settings'

from django.db import models

from blog.models import Post
from django.contrib.auth.models import User

# This gets all of the users
users = User.objects.all()
## >>> <QuerySet [<User: mhzavareh90>, <User: Testuser>]>

# These get the first and last users
user1 = User.objects.first()  # = users[0]
## >>> <User: mhzavareh90>
user2 = User.objects.last()  # != users[-1]  # The negative indexing does not work on queryset arrays.
## >>> <User: Testuser>

# we can filter tthe results by using filter method.
user_filtered = User.objects.filter(username='mhzavareh90')
## >>> <QuerySet [<User: mhzavareh90>]> # we can access this unique user by applying first or get method on user_filtered

# here we can access to methods and attributes of a single query (e.g. user1)
user1.id ## >>> 1 # this is equivalent to user.pk (primary key)

# the get method returns only one query (and not a queryset). Otherwise, get returns exception.
user1 = User.objects.get(id=1)

# we create a post which is written by user1
post1 = Post(title='Blog 1', content='First Post Content', author=user1)
post1.save() # this is required if we want to add this object to our Post table
## without save method, we can see Post.objects.all() returns an empty queryset.

# The above two commands can be written in a single line as follows (without need to any save method)
post1 = Post.objects.create(title='Blog 1', content='First Post Content', author=user1)
"""
post 1 >>> <Post: Blog 1> 
Note that we didn't need any date argument because it is automatically generated by now function.
"""

# we retreive the first post (which we just created)
post1 = Post.objects.first()

# we create a second post
post2 = Post.objects.create(title='Blog 2', content='Second Post Content', author_id=user1.id)
## note that we can use both author (which accept a User instance) and author id (which accepts id of a User instance)

# here we check the attributes of Post instance
post1.content # >>> 'First Post Content'
post1.date_posted # >>> datetime.datetime(2020, 10, 20, 10, 53, 28, 290898, tzinfo=<UTC>)
post1.author # >>> <User: mhzavareh90>

# the post author is entire author object. Therefore, e can have access to its attrbiutes
post1.author.id # >>> 1
post1.author.email # >>> 'mhzavareh90@yahoo.com'



# if we want to get all posts written by user1, django provides us a simple syntanx
posts_user1 = user1.post_set.all()
## >>> <QuerySet [<Post: Blog 1>, <Post: Blog 2>]>
"""
note that we could use the Post table and filter its results based on the author. 
But the above code is much simpler.
"""

# we can use the above technique to create a new post for user1 (no user argument is required)
user1.post_set.create(title='Blog 3', content='Third Post Content!') # >>> <Post: Blog 3>
user1.post_set.all() # >>> <QuerySet [<Post: Blog 1>, <Post: Blog 2>, <Post: Blog 3>]>

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


""" In django suppose:
    Class1 = AccessMixin
    Class2 = LoginRequiredMixin
    Class3 = CreateView (however this class does not inherit from Class1)
    Class4 = PostCreateView
This is called Method resolution order (MRO).
"""
class Class1:
    pass

class Class2(Class1):
    def m(self):
        print("In Class2")
        super().m()

class Class3(Class1):
    def m(self):
        print("In Class3")
        #super().m() # here if we uncomment this, it raises an error.

class Class4(Class2, Class3):
    def m(self):
        print("In Class4")
        super().m()

obj = Class4()
obj.m()


#%% paginator
from django.core.paginator import Paginator
posts = ['1', '2', '3', '4', '5']
p = Paginator(posts, 2) # paginator object
p.num_pages # >>> 3
p.count # total number of objects, across all pages >>> 5
for page in p.page_range: # this is an attribute but returns python range
    print(page)
"""
>>> 1
    2
    3
"""
p1 = p.page(1) # returns page1. It is equivalent to p.get_page(1)
# >>> <Page 1 of 3>
p1.number # page number >>> 1
p1.object_list # >>> ['1', '2']
p1.has_previous() # There is no previous page >>> False
p1.has_next() # There are two next pages >>> True
p1.start_index()  # >>> 1
"""
start_index returns the 1-based index of the first object on the page, 
relative to all of the objects in the paginator’s list.
"""
p1.end_index() # >>> 2
"""
end_index returns the 1-based index of the last object on the page, 
relative to all of the objects in the paginator’s list.
"""

p1.next_page_number() # >>> 2
p1.previous_page_number() # >>> error. That page number is less than 1


from django.core.paginator import Paginator
from django.shortcuts import render

from myapp.models import Contact

def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page') # get page parameter from the url
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})