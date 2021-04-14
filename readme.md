SUPERHERO DATABASE API

This project is the backend for a superhero database.  It stores basic information about superheros and superhero teams.  It also links heroes to teams in a many-to-many relationship.

All code follows PEP8 style guidelines in accordance with pycodestyle 2.7.0.

GETTING STARTED
From the folder run:
pip3 install requirements.txt 
All required packages are included in the requirements file. 

To activate the backendrun the following commands:

export FLASK_APP=app.py
flask run

The application is run on http://127.0.0.1:5000/ by default.

The live application can be reached at https://mandelbaumherodb.herokuapp.com/

TESTING

In order to run tests, install Postman and import the herodb Tests Postman Collection.

Use the following link to register and receive tokens to test the non-public endpoints:
https://mandelbaum-fsnd.us.auth0.com/authorize?audience=herodb&response_type=token&client_id=gfTZ0dp5jrD5Ts3Xi3OxVdEsMo9v6Zz7&redirect_uri=http://localhost

All tests are kept in the postman collection and should be maintained as updates are made to app functionality.  Tokens will need to be updated in the postman collection for tests - the built-in tokens expired on April 14, 2021.

ROLES AND PERMISSIONS

There are two different possible roles:  contributor and administrator.  The contributor can add heroes and teams to the database, update their information, and link heroes to teams.  The administrator do all of those actions and can additionally delete heroes and teams from the database.

API REFERENCE

ERROR HANDLING

Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return two error types when requests fail:

    404: Resource Not Found 
    422: Not Processable - only returned on database errors

The API will also return several authentication errors if tokens are not present, invalid, or expired.

ENDPOINT LIBRARY

GET /heroes

General:  This is a public endpoint.  Returns a list of heroes and their information in the database, including a list of the names of teams they are associated with, a success value, and the total number of heroes in the database.
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.  Returns 404 if no heroes are in the database or if the page number is too high

Sample:  curl https://mandelbaumherodb.herokuapp.com/heroes?page=1

Return: 
{
    "heroes": [
        {
            "hometown":"Smallville",
            "id":1,
            "name":"Superman",
            "power_level":10,
            "secret_identity":"Clark Kent",
            "team_memberships":[
                "Justice League"
            ]
        },
        {
            "hometown":"Gotham",
            "id":2,
            "name":"Batman",
            "power_level":7,
            "secret_identity":"Bruce Wayne",
            "team_memberships":[
                "Justice League",
                "Bat Family"
            ]
        },
        {
            "hometown":"New York",
            "id":3,
            "name":"Captain America",
            "power_level":7,
            "secret_identity":"Steve Rodgers",
            "team_memberships":[
                "Avengers"
            ]
        },
        {
            "hometown":"Los Alamos",
            "id":4,
            "name":"The Hulk",
            "power_level":10,
            "secret_identity":"Bruce Banner",
            "team_memberships":[
                "Avengers"
            ]
        }
    ],
    "success":true,
    "total_heroes":4
}

GET /heroes/{hero_id}

General:  This is a public endpoint.  Returns a particular hero's information and a success value.
Returns 404 if no hero exists with the given ID.

Sample:  curl https://mandelbaumherodb.herokuapp.com/heroes/1

Return:
{
    "hero":{
        "hometown":"Smallville",
        "id":1,
        "name":"Superman",
        "power_level":10,
        "secret_identity":"Clark Kent",
        "team_memberships":[
            "Justice League"
        ]
    },
    "success":true
}

POST /heroes

General:  This is a private route that requires Contributor or Administrator privileges.  Allows new heroes to be posted.  All values are needed to post a new hero.  Returns a success value and the new hero object if it was posted successfully.
Returns 422 if a needed value is missing or if there was a database error.

Sample:  curl https://mandelbaumherodb.herokuapp.com/heroes -X POST -H "Content-Type: application/json" -d '{'name': 'Green Lantern', 'hometown': 'Coast City', 'secret_identity': 'Hal Jordan', 'power_level'= 8}' -H "Authorization: bearer $TOKEN"

Return:
{
    "hero":{
        "hometown":"Coast City",
        "id":5,
        "name":"Green Lantern",
        "power_level":8,
        "secret_identity":"Hal Jordan",
        "team_memberships":[]
    },
    "success":true
}

PATCH /heroes/{hero_id}

General:  This is a private route that requires Contributor or Administrator privileges.  Allows hero's information to be edited.  Any value can be changed - not all the values are needed to submit.  Returns a success value and the edited hero object if it was posted successfully.
Returns 404 if no hero exists with the given ID.
Returns 422 if there was a database error.

Sample:  curl https://mandelbaumherodb.herokuapp.com/heroes/5 -X PATCH -H "Content-Type: application/json" -d '{'secret_identity': 'John Stewart'}' -H "Authorization: bearer $TOKEN"

Return:
{
    "hero":{
        "hometown":"Coast City",
        "id":5,
        "name":"Green Lantern",
        "power_level":8,
        "secret_identity":"John Stewart",
        "team_memberships":[]
    },
    "success":true
}

DELETE /heroes/{hero_id}

General:  This is a private route that requires administrator privileges.  Deletes the hero with given hero ID.  Returns a success value and the hero's ID if the delete was successful.
Returns 404 if no hero exists with the given ID.
Returns 422 if there was a database error.

Sample: curl https://mandelbaumherodb.herokuapp.com/heroes/5 -X DELETE -H "Authorization: bearer $TOKEN"

Return:
{
    "success":true,
    "delete": 5
}

POST /heroes/{hero_id}

General:  This is a private route that requires Contributor or Administrator privileges.  Allows a hero to be linked to a team in the database. The team's id must be submitted as a JSON object.  Returns a success value and the edited hero object if it was posted successfully.
Returns 404 if no hero exists with the given ID or if no team exists with the given team id.
Returns 422 if there was a database error. 

Sample:  curl https://mandelbaumherodb.herokuapp.com/heroes/5 -X POST -H "Content-Type: application/json" -d '{'team_id': '2'}' -H "Authorization: bearer $TOKEN"

Return:
{
    "hero":{
        "hometown":"Coast City",
        "id":5,
        "name":"Green Lantern",
        "power_level":8,
        "secret_identity":"John Stewart",
        "team_memberships":[
            "Justice League"
        ]
    },
    "success":true
}

GET /teams

General:  This is a public endpoint.  Returns a list of teams and their information in the database, including a list of the names of members associated with the team, a success value, and the total number of teams in the database.
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.  Returns 404 if no teams are in the database or if the page number is too high

Sample:  curl https://mandelbaumherodb.herokuapp.com/teams?page=1

Return:
{
    "success":true,
    "teams":[
        {
            "id":1,
            "location":"New York",
            "members":[
                "Captain America",
                "The Hulk"
            ],
            "name":"Avengers"
        },
        {
            "id":2,
            "location":"Outer Space",
            "members":[
                "Superman",
                "Batman"
            ],
            "name":"Justice League"
        },
        {
            "id":3,
            "location":"Gotham",
            "members":[
                "Batman"
            ],
            "name":"Bat Family"
            }
    ],
    "total_teams":3
}

GET /teams/{team_id}

General:  This is a public endpoint.  Returns a particular teams's information and a success value.
Returns 404 if no team exists with the given ID.

Sample:  curl https://mandelbaumherodb.herokuapp.com/teams/1

Result:
{
    "success":true,
    "team":{
        "id":1,
        "location":"New York",
        "members":[
            "Captain America",
            "The Hulk
        "],
        "name":"Avengers"
    }
}

POST /teams

General:  This is a private route that requires Contributor or Administrator privileges.  Allows new teams to be posted.  All values are needed to post a new team.  Returns a success value and the new team object if it was posted successfully.
Returns 422 if a needed value is missing or if there was a database error.

Sample:  curl https://mandelbaumherodb.herokuapp.com/teams -X POST -H "Content-Type: application/json" -d '{'name': 'Green Lantern Corps', 'location': 'Oa'}' -H "Authorization: bearer $TOKEN"

Return:
{
    "success":true,
    "team":{
        "id":4,
        "location":"Oa",
        "members":[],
        "name":"Green Lantern Corps"
    }
}

PATCH /teams/{team_id}

General:  This is a private route that requires Contributor or Administrator privileges.  Allows teams's information to be edited.  Any value can be changed - not all the values are needed to submit.  Returns a success value and the edited team object if it was posted successfully.
Returns 404 if no team exists with the given ID.
Returns 422 if there was a database error.

Sample:  curl https://mandelbaumherodb.herokuapp.com/teams/4 -X PATCH -H "Content-Type: application/json" -d '{''location': 'Mogo'}' -H "Authorization: bearer $TOKEN"

Return:
{
    "success":true,
    "team":{
        "id":4,
        "location":"Mogo",
        "members":[],
        "name":"Green Lantern Corps"
    }
}

DELETE /teams/{team_id}

General:  This is a private route that requires administrator privileges.  Deletes the team with given team ID.  Returns a success value and the team's ID if the delete was successful.
Returns 404 if no team exists with the given ID.
Returns 422 if there was a database error.

Sample: curl https://mandelbaumherodb.herokuapp.com/teams/4 -X DELETE -H "Authorization: bearer $TOKEN"

Return:
{
    "success":true,
    "delete": 4
}

CREDITS

Written by Uri Mandelbaum

ACKNOWLEDGEMENTS

Additional credit is to the Udacity course instructors and team