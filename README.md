## ---- EVENT MANAGEGEMENT SYSTE ----####

This is an event management system developed solely using django and django rest framework (DRF).
The system is designed for users to register, login then manage their events according to their wishes.
they can perfrom CRUD operation such as

1. POST
2. GET
3. RETRIVE
4. UPDATE
5. DELETE events
   The users must first register there accounts using this endpoint

### ---- END POINT FOR USER REGISTRATION ----####

    api/users/register/

### TEST DATA

  {
    "email": "johndoe@gmail.com",
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "0701234190",
    "bio": "Upcoming organizer",
    "password": "John@200"
  }
  # OR
  {
    "email": "janesmith@gmail.com",
    "username": "jane_smith",
    "first_name": "Jane",
    "last_name": "Smith",
    "phone_number": "0712345678",
    "bio": "Passionate about creating memorable events",
    "password": "Jane@200"
  }
  # OR USE THIS ---->
  {
    "email": "michaelowiti@gmail.com",
    "username": "mike_owiti",
    "first_name": "Michael",
    "last_name": "Owiti",
    "phone_number": "0721987654",
    "bio": "Tech enthusiast and part-time event organizer",
    "password": "Mike@200"
  }
Then they can login using this endpoint

### --- END POINT FOR LOGING IN ---###

api/users/login/

### --- TEST DATA ---

{
"email":"johndoe@gmail.com",
"password":"John@200"
}

Once logged in the API authentication's JWT will provide access and refresh token which can be used in postman to POST/RETRIEVE/UPDATE/DELETE events.
The users can post an event using the endpoint bellow.

### ---- END POINT TO POST AN EVENT ---###

/api/events/list/

### --- TEST-DATA ----### ->

{
"organizer": 15,
"name": "Weekend Yoga Retreat",
"category": "others",
"description": "Relax and rejuvenate with a weekend of yoga and meditation.",
"start_date": "2025-09-19",
"end_date": "2025-09-21",
"start_time": "06:00:00",
"end_time": "18:00:00",
"capacity": 70,
"status": "upcoming",
"is_paid": true,
"price": "180.00",
"is_public": true,
"location": "Naivasha, Kenya"
},
  {
    "organizer": 15,
    "name": "Weekend Yoga Retreat",
    "category": "others",
    "description": "Relax and rejuvenate with a weekend of yoga and meditation.",
    "start_date": "2025-09-19",
    "end_date": "2025-09-21",
    "start_time": "06:00:00",
    "end_time": "18:00:00",
    "capacity": 70,
    "status": "upcoming",
    "is_paid": true,
    "price": "180.00",
    "is_public": true,
    "location": "Naivasha, Kenya"
  },
  {
    "organizer": 15,
    "name": "Tech Innovators Conference 2025",
    "category": "conference",
    "description": "A gathering of the brightest minds in technology and innovation.",
    "start_date": "2025-10-10",
    "end_date": "2025-10-12",
    "start_time": "09:00:00",
    "end_time": "17:00:00",
    "capacity": 300,
    "status": "upcoming",
    "is_paid": true,
    "price": "500.00",
    "is_public": true,
    "location": "KICC, Nairobi, Kenya"
  },
  {
    "organizer": 15,
    "name": "Art & Culture Festival",
    "category": "festival",
    "description": "Celebrate African heritage with art exhibitions, music, and dance.",
    "start_date": "2025-11-22",
    "end_date": "2025-11-24",
    "start_time": "10:00:00",
    "end_time": "22:00:00",
    "capacity": 500,
    "status": "upcoming",
    "is_paid": false,
    "price": "0.00",
    "is_public": true,
    "location": "Uhuru Gardens, Nairobi, Kenya"
  },
  {
    "organizer": 15,
    "name": "Startup Pitch Night",
    "category": "business",
    "description": "An evening where startups pitch their innovative ideas to investors.",
    "start_date": "2025-12-05",
    "end_date": "2025-12-05",
    "start_time": "17:00:00",
    "end_time": "21:00:00",
    "capacity": 100,
    "status": "upcoming",
    "is_paid": false,
    "price": "0.00",
    "is_public": true,
    "location": "iHub, Nairobi, Kenya"
  }


The logged in user can retrieve a single event using the API endpoint bellow

### --- ENDPOINT TO RETRIEVE AN EVENT ---

api/events/pk/ (Replace the pk with the primary key of an event)
for example the enpoint:
api/events/10/ will retrieve event with the primary key 10.

Once the retrieval is succesful, the authenticated/logged in user can either delete or update the event.

### IN ADDITION TO PERFORMING CRUD OPERATIONS THE AUTHENTICATED USERS CAN PERFORM OTHER OPERATIONS

For example: 
1. They can list all events 
2. They can post a comment 
4. They can book events 
5. They can like an event 
6. They can filter events based on parameters such as upcomming, cancelled, completed, organizer, dates etc

All these operations can be performed following these ENDPOINTS

### ENDPOINT TO LIST ALL EVENTS

    api/events/list

### ENDPOINT TO POST A COMMENT

    /api/events/33/post/comments/

### TEST DATA ------>

{
"comment":"Wow a must attend event."
}

### TEST DATA

{
"comment":"Testing posting of comments"
}

### ENDPOINT FOR BOOKING AN EVENT

api/events/pk/book/

### ---TEST DATA ---###

{
"event":33,
"user":8
}

### ---- ENPOINT TO FILTERING AN EVENT ---

    api/events/filter/?status=upcoming

    This endpoint will filter all the upcoming events. A user can use the filter button provided by the DRF to filter data based on the filter fields available.

### --- ENDPOINT TO LIKING AN EVENT ---

    /api/events/33/like/ (replace 33 with the primary key of the event you have posted)

    Once on that endpoint, click post and you should get a message stating event liked succesfully.
    The same endpoint can be used to unlike, click on it and there should be a message indicating event unliked succesfully.
    Alternatively
    -------------
    You can visit this endpoint to unlike an event:

    /api/events/33/unlike/

    This endpoint is only dedicated to deleting the like placed on an event.
