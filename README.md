# Web Journal
#### Description:
This is a web based journaling app. Build by using flask framework. People can use the journal to document about their day.
You can register and login to the webapp. Once you logged in you can start journaling about your day.
I have used python as the main programming language and flask as the web framework. Html,CSS and javascript is used to frontend
development. Finally Used SQL for the database.

Application.py

First the headers are defined and the app is configured. Next the login_required function is created and then
the file disables caching of responses. Then it configures the application to store the session in the localfile system.
It then configures the SQL database for storing data. Then the at the home page I have called the login_required function
to check whether a user is logged in or not. And there are seperate routes for each page which uses get and post methods.
A logout route is also created to clear all the sessions recorded and to let the user logout. When saving password a hash
function is used to hash the password entered by the user for better privacy.

journal.db

This is the database file based on SQL. Inside the journal.db there are 2 tables named users and data. Users which contains the
information about the users who are registered and Data table which contains the date and the journal the user wrotes each day.
Users table store a id, username and a password which is hashed using a hash function. The data table contains an Id a user_id
to indicate which users data is, info colomun which contains the journal wrote by the user, date which contains the time when
the user entered the data and a time column which contains the time which the data is entered.

Requirements.txt

This file contains the packages that is used in the flask application.

static/

contains some of the css styles and some images used by the application.

templates/

contains the html webpages which are stylished by CSS and bootstrap.Layout.html contains the basic layout which is used for
every other html page using jinja syntax. Error.html will load if any error is occured it will prompt to the user with the
error returned application.py. Login.html, register.html, home.html are also there in the directory.

How to work with the application

1) First the user need to get registered
2) click on the register button , you need to enter a username and a password
3) After clicking register you will be redirected to the login page and enter the login details
4) AFter entering the correct login details, You will be redirected to the home page
5) Click on "Add+" to write a about your day. After entering data hit save
6) You will see a line is added to the chart in the home page with today's date.
7) click the view button to see the journal you wrote

Possible improvements
1) Letting the user to make changes to the journal written before
2) Enhance the UI look
3) Select a tag about the day (like productive or Not, Happy or Sad)