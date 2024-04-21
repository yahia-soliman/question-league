# Question League
### A platform with competitive multiplayer questions.

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
