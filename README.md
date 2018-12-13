# onlineChat

## Project Description: 
This project is purely for educational purposes to better understand how a frontend application can make requests to a seperate backend. 

It is a simple messenger that does just the foundational functionality of a messenger.

We created it using two different frameworks Vue.js for the front end and Flask for Backend. We did this on purpose, in the case that we work for a company that decides to slowly change its technologies we wanted to be able understand how to integrate two different frameworks. 

## To RUN: 
Make sure all dependencies have been installed.

### Dependencies :
   Flask: 
   ``` pip install Flask```
   Flask Basic Auth: 
   ```pip install Flask-BasicAuth```
   Vue:
   ```npm install vue ```
   npm: 
   ```brew install node```
   
### Running the project
Open a terminal to the backend folder:
   ``` python application.py ```
Open a terminal to the frontend folder: 
   ``` npm run dev ```

## Features 
* Logining in to your profile.
* Being able to create a new user.
* Creating a new conversation to another user.
* Being able to send a message to another user.
* See your message history.
* View all your message conversations.

## Future Features
* Creating a logout menu.
* Being able to delete a user
* Custom setting the color of you chat
* Chatting with multiple people per conversation
* Being able to add rich text and other features

## Current Known Bugs 🦠
* You have to create a user twice for the request do be sent through. 
* Pressing enter for text inputs do not work you need to press the corresponding button.
* Since it runs locally to log you can only login to one user at a time
* Doesnt currently escape sql characters. 


## Pitfalls and necessary fixes 
Since this is just a basic application built to understand the foundations of how a frontend would work and how it can communicate with a simple backend there are a ton of pitfalls.

### Security: 
Here are some basic security pitfalls but there are more... 
* The backend utilizes basic auth for the authentication, but the username and password should be encrypted as it is sent to the backend via the request.
* The messages should also be encrypted as they are sent along to the backend.
