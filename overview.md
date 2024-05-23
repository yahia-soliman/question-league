# Question League
### A platform with competitive multiplayer questions.

This means it is the last step of the ALX Software Engineering Foundation journey, I'm delighted to share what I have learned by working on a complete full stack web application from the idea to the final product.

So this was the last project of the curriculum and we were free to choose what ever idea we need to create, my inspiration is to test my ability to do the whole SDLC (software development life cycle) alone, I've done it with a team twice before, but I was mainly working on the back end.

Starting from the idea, I was interested on making a CLI application, create a Python/JavaScript library, integrating AI with a back-end service, or creating a real-time multiplayer game, the ceiling of ambition was really high, but the last one was the most aligned to my current ability and with the most predectable risks, that was the first lesson is how to decide what project you need to start, so I decided to go on with a simple multiplayer game to learn how this type of applications works and to sharpen the skills learned from ALX.

After having an idea you have to have a plan, how your gonna achieve what you wan't, you will never calcute a 100% accurate plan but it is necessary to attach your ideas with what is there in realty, for example you want to make a multiplayer game


Moving to the development, I choosed to use Python, and that choice alone learnt me the importance of concurrency and non-blocking IO, Python's (before async) is blocking IO means every thread can do one job at a time and in our case the websocket connection will own and block that thread as long as the connection is open, so actually if we have one thread there would be no more than one socket connection (in a multiplayer game!) and the worst that while that special connection is open, normal http requests are blocked alose untill the websocket connection is closed, to mitigate the effect of this I've gevent with gunicorn to make 1000 thread working at the same time, that also means that if 1000 players are connect to a socket the web site will not be accessable unless at least one connection is closed. But that solution was temporary, the better solution was to use an ASGI approach, and this would be possible if we migrated from gunicorn to hypercorn and by using WSGI to ASGI to turn the Flask app to be ASGI compatible and the even better is to migrate the whole Flask code to Quart, and why not since Quart is a micro framework that is similar to flask and was build on Python's native async feature where it is possible for requests to be hadeled in parallel from the same thread, that somthing I learnd and I will learn more when I do the actual migration, excited to see the deffernce!

One of the things that I learned and loved a lot was TailwindCSS, this is really very convenient way to do styling even if you are not a front-end wizard like me, with really acceptable results without too much burnout.


## Team
**Yahia Soliman.**  
I decided to work alone because in the last 6 months I’ve learned a lot of things that I want to consolidate together, to fill important gaps by learning more things, and to ensure that I’m capable of doing the full SDLC alone, at least in a small project.


## Technologies
For the backend I will primarily use Python and MySQL, and for the front end I will use HTML, JavaScript, and Tailwindcss, and if things seem to be too much to handle with JavaScript, I will use Angular.

I can choose MongoDB instead of MySQL, but I want to practise working with SQL, same for Node.js, I might use them in the future for other parts of the project.

## Challenges
To have real-time connections for users playing in the same party.  
The project will not solve the problem of making a social platform where people can communicate.  
The users would be a group of people chilling out for some minutes  
The project will be in English as a start  


## Infrastructure
Code will be available in Github, after having an MVP, I will start versioning the project and have different branches for feature development, and for production.  
I’m planning to split the project into microservices deployed using containers, in order to be scalable in the future, and to adopt more competitive games.  
Part of the data in the project will rely on the opentdb.com API, and it will be just to get the questions, and any other data will be tailored for the needs of the project, for example the users, scores, ranks, etc…  
For the unit tests will be tested using fabric just before the deployment  


## Risks
Technical: finishing the project without the need for a frontend framework, but if things get over what I can do with JavaScript (and I don't think it will), I will go for Angular or react.  


## Existing solutions
There are all the .io games out there like gartic.io, it is similar to our project in the way it handles multiplayer, but the game itself is different.  


# MVP specification

## Architecture

## API endpoints
/api/v1/questions
GET: returns a random question, you can specify category and/or difficulty using query string.
/api/v1/questions/<question_id>/<answer>
POST: status 200 OK if the answer is correct, and 418 I'm a teapot if incorrect.
/api/v1/categories
GET: get all available categories, and number of questions in each category
/api/v1/users
GET: get top 10 players by score, you can specify a category.
/api/v1/users/<user_id>
PUT: update user data
/api/v1/users/register
POST: register a new user
/api/v1/users/login
POST: update user data
For questions I will use opentdb api, make some changes, and store it in MySQL
GET https://opentdb.com/api.php?amount=50


## User Stories
### As a user...
- I want to spend some time to improve my knowledge -general or specific- by trying to answer various questions.
- I want to know the correct answer even if I'm wrong.
- I prefere to get questions about topics i'm interested in
- It would be useful for me to know how hard the question is, and how many players get it right
- It would be rewading if there is a way to know how I compare with people intersted in the same topics as me, and to compete with them on
- I want to have special traits that shows my skill level
- I want to be able to challenege my friends in how can answer a question faster
As a user...

I want to spend some time to improve my knowledge -general or specific- by trying to answer various questions.
I want to know the correct answer even if I'm wrong.
I prefere to get questions about topics i'm interested in
It would be useful for me to know how hard the question is, and how many players get it right
It would be rewading if there is a way to know how I compare with people intersted in the same topics as me, and to compete with them on
I want to have special traits that shows my skill level
I want to be able to challenege my friends in how can answer a question faster
