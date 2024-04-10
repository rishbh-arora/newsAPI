# News API

Tech Stack: Django Rest Framework, PostgreSQL, AWS EC2, AWS RDS
Data source: https://newsapi.org/
Base API URL:

---

# Endpoints

## Create an account

- **POST** /register: Client sends username and password to create a new account. Returns a json containing authentication token. The system checks for unique usernames.<br/>
  Request body template:

  ```
  body: {
      "username": "John_doe",
      "password": "Johnpa"
  }
  ```

  <br/>
  Response body template:

  ```
    body: {
        "username":  "John_doe"
    }
  ```

## Authentication

The API uses Django's out of the box **Token Authentication** to autheticate users.

- **POST** /token: Client sends username and password for autheticataion. Returns a json containing authentication token if user authenticated.<br/>
  Request body template:

  ```
  body: {
      "username": "John_doe",
      "password": "Johnpa"
  }
  ```

  <br/>
  Response body template:

  ```
    body: {
        "token":  "XXXXXXXXXX"
    }
  ```

**All endpoints moving forward will be protected and will require an Authorization Header containing the recieved token.**

```
  header: {
    ....
      "Authorization":  "Token XXXXXXXXXX"
    ....
  }
```

## News

The API implements various search and filter endpoints which can be accessed using query parameters and URL parameters. The reponse body may contain one or more news articles each of which comprises of the following fields:

- id: Primary key for each news article
- Comments: List of all comments posted for the particular article. Attached to the news article fetch to reduce API calls
- Source: The publishing organizaion/individual of the article
- Author: The author of the article
- title: The headline or title of the article.
- Description: A description or snippet from the article.
- url: The direct URL to the article.
- publishedAt: The date and time that the article was published, in UTC (+000)
- content: The unformatted content of the article, where available. This is truncated to 200 chars.

### GET /news

Returns all available news articles in the database
Response body template: **/news**

```
body: [
 ....
 {
     "id": 2,
     "comments": [],
     "source": "Wired",
     "author": "Scott Gilbertson",
     "title": "How I Became a Python Programmer—and Fell Out of Love With the Machine",
     "description": "When I started coding, I was suspicious of all the abstractions. Then I discovered the Django framework.",
     "url": "https://www.wired.com/story/how-i-became-a-python-programmer-and-distanced-myself-from-the-machine/",
     "publishedAt": "2024-04-08T10:00:00Z",
     "content": "The difficulty with any new programming language is the sharp learning curve, all that drudgery and bashing your forehead into the keyboard. There was no Codecademy or Stack Overflow in those days. W… [+3459 chars]"
 },
 {
     "id": 3,
     "comments": [],
     "source": "BBC News",
     "author": "https://www.facebook.com/bbcnews",
     "title": "'I got my first death threat before I was elected'",
     "description": "With £31m committed to improving politicians' safety, how bad is the abuse our local leaders face?",
     "url": "https://www.bbc.co.uk/news/uk-england-68562310",
     "publishedAt": "2024-03-17T02:54:28Z",
     "content": "They are responsible for planning, potholes and policing. But our local politicians are facing unprecedented levels of abuse and harassment. The government has committed £31m to improving safety and … [+6530 chars]"
 },
 {
     "id": 4,
     "comments": [],
     "source": "Gizmodo.com",
     "author": "Oscar Gonzalez",
     "title": "'I Never Thought That What I Was Doing Was Illegal,' SBF Says as He Begins Prison Sentence",
     "description": "Days after Sam Bankman-Fried received a 25-year prison sentence, the FTX founder released a statement to ABC News saying how sorry he was about his crimes. He says he made some “bad decisions” and didn’t realize that his billion-dollar Ponzi scheme wasn’t ill…",
     "url": "https://gizmodo.com/i-never-thought-that-what-i-was-doing-was-illegal-sbf-1851379761",
     "publishedAt": "2024-04-01T20:45:00Z",
     "content": "Days after Sam Bankman-Fried received a 25-year prison sentence, the FTX founder released a statement to ABC News saying how sorry he was about his crimes. He says he made some bad decisions and didn… [+1200 chars]"
 },
.....
]
```

### GET /news/[pk]

Returns the news article with ID [pk]
Response body template: **/news/5**

```
body: [
   {
      "id": 5,
      "comments": [
            {
               "id": 2,
               "comment": "Loved it!",
               "timestamp": "2024-04-10T08:37:09.723169Z",
               "user": 1,
               "article": 5
            }
      ],
      "source": "BBC News",
      "author": "https://www.facebook.com/bbcnews",
      "title": "Lizzo not quitting music, just 'negative energy'",
      "description": "The Grammy winner says: \"When I say I quit, I mean I quit giving any negative energy attention.\"",
      "url": "https://www.bbc.co.uk/news/world-us-canada-68716521",
      "publishedAt": "2024-04-02T22:50:16Z",
      "content": "US pop star Lizzo is not leaving the limelight anytime soon, she has assured her fans in a social media post.\r\nThe Grammy winner said last week she was \"quitting\" because she was fed up of being targ… [+1291 chars]"
   }
]
```

### GET /news/[pk]/bookmark

Bookmarks the article identified by [pk] for the current user.
Response body template: **/news/5/bookmark**

```
body: {
    "id": 1,
    "user": 1,
    "article": 5
}
```

### Query parameters:

The **/news** endpoint also accepts some specific query parameters for search and filter implementations:

- souce: Look for articles from a particular source
- author: Look for articles from a particular author
- q: Search based on space seperated keywords. Fields search are: title, description, content
- timestamp_before: Returns articles published before a given date
  timestamp_after: Returns articels published after a given date

Response body template: **/news?q=Apple%20cars&timestamp_after=2024-04-01**

```
body: [
    {
        "id": 127,
        "comments": [],
        "source": "Wired",
        "author": "Boone Ashworth",
        "title": "How an iPhone Powered by Google’s Gemini AI Might Work",
        "description": "Supercharged Siri. AI image editing. Smart “snapshots” of your day. We asked some experts to forecast how Apple might use Google’s Gemini platform to enable new AI-powered applications in iOS.",
        "url": "https://www.wired.com/story/apple-google-gemini-iphone/",
        "publishedAt": "2024-04-01T11:00:00Z",
        "content": "So, assuming the deal does go through, what might Gemini look like on the iPhone?\r\nFirst off, Gartenberg says it will likely manifest with a distinctly un-Apple label.\r\nIt would probably be something… [+3206 chars]"
    }
]
```

## Comments:

All users can post comments, view comments on all posts and delete any of their comments. Everytime a user comments on a post, they gain 10 karma points

### GET /comments:

Fetches all comments on all posts

Response body template: **/comments**

```
body: [
   ...
    {
        "id": 1,
        "comment": "This breaks my heart.",
        "timestamp": "2024-04-10T07:05:46.622545Z",
        "user": 1,
        "article": 1
    },
    {
        "id": 2,
        "comment": "Loved it!",
        "timestamp": "2024-04-10T08:37:09.723169Z",
        "user": 1,
        "article": 5
    },
    {
        "id": 3,
        "comment": "That is some good news",
        "timestamp": "2024-04-10T09:45:31.579940Z",
        "user": 2,
        "article": 9
    }
    ....
]
```

### GET /comments/by_user:

Fetches all comments posted by the current user

Response body template: **/comments/by_user**

```
body: [
   ....
    {
        "id": 1,
        "comment": "New commen",
        "timestamp": "2024-04-10T07:05:46.622545Z",
        "user": 1,
        "article": 1
    },
    {
        "id": 2,
        "comment": "Loved it!",
        "timestamp": "2024-04-10T08:37:09.723169Z",
        "user": 1,
        "article": 5
    },
    ....
]
```

### GET /comments/by_article?article_id=[pk]:

Fetches all comments posted for one particular article.

Response body template: **/comments/by_article?article_id=5:**

```
body: [
   ...
    {
        "id": 2,
        "comment": "Loved it!",
        "timestamp": "2024-04-10T08:37:09.723169Z",
        "user": 1,
        "article": 5
    }
    ...
]
```

### POST /comments:

Post of comment by the current user for a particular article

Request body template: **/comments**

```
body:
    {
        "comment": "Loved it!",
        "article": 5
    }
```

Response body template: **/comments**

```
body: [
   {
      "id": 8,
      "user": 1,
      "comment": "That's horrible",
      "timestamp": "2024-04-10T12:34:19.072816Z",
      "article": 10
   }
]
```

## Users:

This set of endpoints fetches the user profiles and allows users to edit it.

### GET /user:

Fetch the user profile
Response body template: **/user**

```
body: {
    "username": "rishbh",
    "first_name": "",
    "last_name": "",
    "email": "",
    "date_joined": "2024-04-09T21:16:34.520362Z",
    "karma": 70,
    "gender": "M",
    "pno": "",
    "comments": [
        {
            "id": 1,
            "user": 1,
            "comment": "New commen",
            "timestamp": "2024-04-10T07:05:46.622545Z",
            "article": 1
        },
        {
            "id": 2,
            "user": 1,
            "comment": "Loved it!",
            "timestamp": "2024-04-10T09:45:31.579940Z",
            "article": 9
        },
        {
            "id": 3,
            "user": 1,
            "comment": "That's horrible",
            "timestamp": "2024-04-10T12:22:00.655683Z",
            "article": 10
        },
    ],
    "bookmarks": [
        {
            "id": 1,
            "user": 1,
            "article": 5
        }
    ]
}
```

The profile response also includes all bookmarks and comments made by the user. This is for an effort to reduce API calls.

On making an account, the only required fields are username and password. However, the API provides a **PUT** method to save aditional information such as first name, last name, phone number, email.

### PUT /user:

Edit user profile. **The username field is mandatory** even if there is no update.

Request body template: **/user**

```
body: {
    "username": "rishbh102",
    "first_name": "Rishbh",
    "last_name": "Arora",
}
```

Response body template:

```
body: {
    "username": "rishbh",
    "first_name": "102",
    "last_name": "Rishbh",
    "email": "Arora",
    "date_joined": "2024-04-09T21:16:34.520362Z",
    "karma": 70,
    "gender": "M",
    "pno": "",
    "comments": [
        {
            "id": 1,
            "user": 1,
            "comment": "New commen",
            "timestamp": "2024-04-10T07:05:46.622545Z",
            "article": 1
        },
        {
            "id": 2,
            "user": 1,
            "comment": "Loved it!",
            "timestamp": "2024-04-10T09:45:31.579940Z",
            "article": 9
        },
        {
            "id": 3,
            "user": 1,
            "comment": "That's horrible",
            "timestamp": "2024-04-10T12:22:00.655683Z",
            "article": 10
        },
    ],
    "bookmarks": [
        {
            "id": 1,
            "user": 1,
            "article": 5
        }
    ]
}
```

# Setup

1. Clone the repository:
   Get the repo locally to setup the developement server by simply running `git clone https://github.com/rishbh-arora/jwtauth-django`

2. Installing dependencies:
   Install all required libraries and dependencies by running `pip install -r requirements.txt`

3. Configuring the environment variables:
   The connection string for the database must be stored in `path/to/base/directory/.env` as `MONGO_CONNETION_STRING=<YOUR_CONNECTION_STRING>`. In this case, the `.env` file should be in the same directory as `manage.py`

4. Create migrations:
   Make migration configurations for all models(database schemas) by running `python manage.py makemigrations`

5. Migrate to database:
   Run the migration using `python manage.py migrate`

6. Start server:
   Finally, start the server on local host using `python manage.py runserver`
