# onlineChat

## Project Description: 
This project is purely for educational purposes to better understand how a frontend application can make requests to a seperate backend. 

It is a simple messenger that does just the foundational functionality of a messenger.


### Pitfalls: 
Since this is just a basic application built to understand the foundations of how a frontend would work and how it can communicate with a simple backend there are a ton of pitfalls.

### Security: 
Here are some basic security pitfalls but there are more... 
* The backend utilizes basic auth for the authentication, but the username and password should be encrypted as it is sent to the backend via the request.
* The messages should also be encrypted as they are sent along to the backend.
