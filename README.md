# Django-E-Portfolio

![Django logo](./django-logo-negative.png)  
This repository will contain everything associated with my E-Portfolio about Django.  
Feel free to visit the official Django documentation to get some more insights: https://www.djangoproject.com/. You can
also view the presentation slides for a rough overview.

## Requirements

To run the project you need to install the Python interpreter from https://www.python.org/. Afterwards you can install
Django by running  
`python -m pip install django` or `py -m pip install django` if you are on Windows.

## Important commands

- `django-admin startproject <project-name>`  
  Starts a Django project and therefore creates a basic folder structure with necessary files. The folder structure
  should look something like this:
  ```
  \---<project-name>
    |   manage.py
    |   
    \---<project-name>
            asgi.py
            settings.py
            urls.py
            wsgi.py
            __init__.py      
  ```
- `python manage.py runserver`  
  Starts the development server on 127.0.0.1:8000. You can change this behavior by passing a different port as command
  line parameter: `python manage.py runserver <port-number>`.
- `python manage.py startapp <app-name>`  
  Creates a Django app with basic folder structure and necessary files. The app can be added to the project inside the 
*settings.py* file. The structure of an app looks something like this:
   ```
  \---<app-name>
    |   admin.py
    |   apps.py
    |   models.py
    |   tests.py
    |   views.py
    |   __init__.py
    |   
    \---migrations
            __init__.py
   ```
- `python manage.py makemigrations`  
  Creates a file inside the migrations folder of your app that contains the necessary changes for the database. Should
  be executed every time a new model was created or an existing model was modified. After modifying the models a bit and
  running this command three times the migrations folder could look something like this:
  ```
  \---migrations
    |   0001_initial.py
    |   0002_alter_todoitem_description.py
    |   0003_todoitem_done.py
    |   __init__.py
  ```
- `python manage.py sqlmigrate <app-name> <migration>`  
  Prints the changes/migrations to be made for the app named `<app-name>` and migration with the id `<migrate>`. An
  example output could look like this:
   ```
  python manage.py sqlmigrate 0003
  
  BEGIN;
  --
  -- Add field done to todoitem
  --
  CREATE TABLE "new__todo_app_todoitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "done" bool NOT NULL, "title" varchar(50) NOT NULL, "description" text NOT NULL, "due_date" datetime NOT NULL);
  INSERT INTO "new__todo_app_todoitem" ("id", "title", "description", "due_date", "done") SELECT "id", "title", "description", "due_date", 0 FROM "todo_app_todoitem";
  DROP TABLE "todo_app_todoitem";
  ALTER TABLE "new__todo_app_todoitem" RENAME TO "todo_app_todoitem";
  COMMIT;
   ```
- `python manage.py migrate`  
  Applies all the changes/migrations to the database.
- `python manage.py createsuperuser`  
  Prompts you to enter username, password and e-mail. Afterwards you are able to login to the administrator site of
  Django using these credentials (by visiting 127.0.0.1:8000/admin):  
  ![Django administration login](./django-administration-login.png)

## Step-by-step guide for creating a task-tracker app

### 1. Start a new project and app

Open a terminal inside a directory where your django project should live and run the command
`django-admin startproject django_example`. Go inside the folder of your project and run
`python manage.py startapp todo_app`. Inside the *settings.py* file add your app to *INSTALLED_APPS* like so:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo_app'
]
```

### 2. Create a database model

Inside the *models.py* file add a new model to represent a task:

```python
from django.db import models


class TodoItem(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    due_date = models.DateTimeField()
    done = models.BooleanField(default=False)
```

### 3. Create templates

The application should consist of two views. One view will show a list of all tasks which are currently unresolved and
also the tasks that are done. The other view will be used to create a new task. To achieve this, create a new folder
called "templates" inside the "todo_app" folder. Inside the "templates" folder create another folder with the same name
as the app. In this case that is "todo_app". This is necessary because otherwise it can cause problems if there are
views with the same name in different apps. Create two HTML files "create-view.html" and "list-view.html". These will be
the templates.

### 4. Create views

To render the templates create two functions inside *views.py* like this:

```python
from django.shortcuts import render


def list_view(request):
    return render(request, 'todo_app/list-view.html')


def create_view(request):
    return render(request, 'todo_app/create-task.html')
```

Additionally, you have to provide information to Django about when to render these templates. Add a new file inside
the "todo_app" folder called "urls.py". Here you can map URLs to specific views:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view, name='list-view'),
    path('new', views.create_view, name='new')
]
```

Those paths refer only to the application itself so the last thing to do is to map this file inside the *urls.py* in
the "django_example" project folder:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('todo_app.urls'))
]
```

Now it should be possible to run the development server with `python manage.py runserver`and visit the list view at
*/todo* as well as the creation view at */todo/new*. Note how the names of the templates do not show up in the URL
itself. Only the specified paths in *urlpatterns* matter.

### 4. Pass data to views

In the list view template we need access to the tasks in our database, and we also want to distinguish between tasks
which are done and those that are not done. The filter function comes in handy for that. To pass the retrieved data to
the template a context can be passed to the render function. The context maps data to specified names. Edit the
*list_view*
function inside *views.py* like this:

```python
from django.shortcuts import render
from .models import TodoItem


def list_view(request):
    todo_items = TodoItem.objects.filter(done=False).order_by('due_date')
    todo_items_done = TodoItem.objects.filter(done=True).order_by('due_date')
    context = {
        'todo_items': todo_items,
        'todo_items_done': todo_items_done
    }
    return render(request, 'todo_app/list-view.html', context)
```

### 5. Access data inside a template

It is possible to access the data by using the names specified in the context variable. E.g. with
`{% for item in todo_items %}` it is possible to iterate over all todo items whose attribute *done* ist set to *False*.
With `{% if todo_items %}` you would check if the list exists or if it is empty. With this knowledge it is possible to
finish up the list view. Do not forget that there should also be a possibility to get to the view for creating a new
task. You can view the whole file [here](./django_example/todo_app/templates/todo_app/list-view.html).  
In case you want to test your app right now you will get an error telling you something about missing tables. This
happens because in order to create tables in the database and apply the changes made to the models (in fact you created
a completely new one) you have to run `python manage.py makemigrations` and `python manage.py migrate`.

### 6. Creating a new record from form-data

The view to create a new task should contain an HTML form which uses the method *POST* with all necessary inputs to
provide data for a new task and a submit button to submit the form. The *action* attribute should refer to an internal
method in *views.py* which creates a new task from the form-data. For the POST-Request to work you must
add `{% csrf_token %}`
inside the form for security reasons. Your method in *views.py* could look something like this:

```python
from django.shortcuts import render, redirect
from .models import TodoItem


def create(request):
    _title = request.POST.get('title', 'Title')
    _description = request.POST.get('description', 'Description')
    _due_date = request.POST.get('due-date', '1970-01-01 00:00')
    todo = TodoItem(title=_title, description=_description,
                    due_date=_due_date)
    todo.save()
    return redirect('list-view')
```

The first parameter of the *get* function refers to the name of the HTML input tag. The second parameter is a default
value. Do not forget to call *save()* on the instance. Otherwise, it will not be saved to the database. Also note the
redirect at the end which takes the name of the view to redirect to as a parameter. This function must be mapped to the
URL you specified in the form-action inside the *urls.py*:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view, name='list-view'),
    path('new', views.create_view),
    path('create', views.create)
]
```

Refer to this file for the [create view template](./django_example/todo_app/templates/todo_app/create-view.html).

### 7. Interacting with task items

Now that it is possible to add new tasks the user should be able to delete a task or mark it as done. This can be done
very similarly to the implementation of creating a task. You can just go to a specific URL on a button click and map
this URL to a function which handles the rest. To delete an item the function could look like this:

```python
def delete(request, todo_id):
    TodoItem.objects.filter(id=todo_id).delete()
    return redirect('list-view')
```

We retrieve the object by id, delete it and then refresh/redirect back to the list view. Note that every task has such an
id even though it was not added as an attribute when we defined the model. Django does this by itself. Again we map the
function to an URL but this time we also pass a parameter called "todo_id" with it:

```python
urlpatterns = [
    path('', views.list_view, name='list-view'),
    path('new', views.create_view),
    path('create', views.create),
    path('delete/<int:todo_id>', views.delete)
]
```

We can do the same for updating a task by defining a function which retrieves the object (by id) and sets its *done* 
attribute to *False* or *True* depending on its current state.

Hurray, you successfully created a task tracker app with Django!