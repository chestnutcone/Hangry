# Hangry
Office food ordering web app

## Purpose
Lots of offices orders take out together. Usually, there is a person going around asking what others want and then places the orders.
This web app simplifies that process, aggregates the data, summarizing the everything from orders, to vendor information. 

## Installing
I used Anaconda prompt with Django 3.0 and deployed to Heroku. For more requirements, visit the requirements.txt

1. Clone the heroku_deploy branch (if branch does not exist, clone master)
2. Create a Heroku account if you don't have one. They have a free tier https://signup.heroku.com/
3. Open Anaconda prompt, cd into the folder where you cloned this project. cd to where manage.py resides
  - If you want, create a virtual env with the following command. ENVNAME is whatever name you want.
  ```
  conda create --name ENVNAME
  conda activate ENVNAME
  ```
  
4. In Anaconda prompt, type
```
heroku login
```
5. After logging in to Heroku, create an app. APPNAME is whatever name you want
```
heroku create APPNAME
```
6. Install packages gunicorn, dj-database-url, whitenoise, psycopg2 with pip
7. Commit to git and push to Heroku. BRANCH_NAME is what branch you are pushing from. If pushing from master, just master:master
```
git push heroku RBANCH_NAME:master
```
8. Once done, run 
```
heroku run python manage.py migrate
```
9. Now you can populate database with scripts. To run any scripts, prefix with "heroku run". 
The script for populating Timezone info should be included. You can write your own script to populate your own vendor/meals info.
```
heroku run python populate_datetime.py
```
10. Set up environment variable in Heroku. There are three you need to set up for this app: DJANGO_SECRET_KEY,
GMAIL_USERNAME, GMAIL_PASSWORD. You can use a random string generator and generate 50 chars for DJANGO_SECRET_KEY. GMAIL_USERNAME and 
GMAIL_PASSWORD is used for "forgot password" function, where it sends a link for you to reset the password if any of your users forgets 
their password. Or you can just remove the link about "forgot password" from the login html page if you don't want the feature. 

