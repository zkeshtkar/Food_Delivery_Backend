# Food_Delivery_Backend
# Introduction

The purpose of this project is to implement the general features of https://snappfood.ir
# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/zkeshtkar/Food_Delivery_Backend.git
    $ cd Food_Delivery_Backend
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements

Change password and name of database in config/settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your name',
        'USER': 'your user',
        'PASSWORD': 'your password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

```
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver

# Run tests
When you want to run tests,you should use this comments in your terminal :

You can now run the development server:

    $ python manage.py test "tests/" 

#Todo

* Add more tests

#Contact
Zahra Keshtkar - [zkeshtkarz@gmail.com](zkeshtkarz@gmail.com)

#Contributing
This project can definitely be improved ,and your feedback will help me. so please feel free to fix bugs, improve things. Just send a pull request.




