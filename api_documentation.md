## Database Schema Design

![reciprocity_db_diagram](https://github.com/user-attachments/assets/f1872345-b645-4831-8015-1db434e1d2af)

## USER AUTHENTICATION/AUTHORIZATION

### All endpoints that require authentication

All endpoints that require a current user to be logged in.

- Request: endpoints that require authentication
- Error Response: Require authentication

  - Status Code: 401
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Authentication required"
    }
    ```

### All endpoints that require proper authorization

All endpoints that require authentication and the current user does not have the
correct role(s) or permission(s).

- Request: endpoints that require proper authorization
- Error Response: Require proper authorization

  - Status Code: 403
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Forbidden"
    }
    ```

### Get the Current User

Returns the information about the current user that is logged in.

- Require Authentication: false
- Request

  - Method: GET
  - Route path: /api/session
  - Body: none

- Successful Response when there is a logged in user

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "user": {
        "bio": "I discovered my love for cooking by reading Anyone Can Cook by my idol, Auguste Gusteau.",
        "created_at": "2025-01-11T20:03:53.488461",
        "email": "remy@gasteaus.com",
        "first_name": "Demo",
        "id": 1,
        "location": "Paris, France",
        "profile_image_url": "https://static.wikia.nocookie.net/pixar/images/5/56/Ratatouille-remy2.jpg/revision/latest/top-crop/width/200/height/150?cb=20110512131040",
        "updated_at": "2025-01-11T20:03:53.488472",
        "username": "the_ratatouille"
      }
    }
    ```

- Successful Response when there is no logged in user

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "user": null
    }
    ```

### Log In a User

Logs in a current user with valid credentials and returns the current user's
information.

- Require Authentication: false
- Request

  - Method: POST
  - Route path: /api/session
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "email_or_username": "remy@gasteaus.com",
      "password": "password"
    }
    ```

    ```json
    {
      "email_or_username": "little_chef",
      "password": "password"
    }
    ```

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "bio": "I discovered my love for cooking by reading Anyone Can Cook by my idol, Auguste Gusteau.",
      "created_at": "2025-01-11T20:18:20.950811",
      "email": "remy@gasteaus.com",
      "first_name": "Demo",
      "id": 1,
      "location": "Paris, France",
      "profile_image_url": "https://static.wikia.nocookie.net/pixar/images/5/56/Ratatouille-remy2.jpg/revision/latest/top-crop/width/200/height/150?cb=20110512131040",
      "updated_at": "2025-01-11T20:18:20.950823",
      "username": "little_chef"
    }
    ```

- Error Response: Invalid credentials

  - Status Code: 401
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Invalid credentials"
    }
    ```

- Error response: Body validation errors

  - Status Code: 400
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "errors": {
        "email_or_username": "This field is required.",
        "password": "This field is required."
      },
      "message": "Bad Request"
    }
    ```

### Sign Up a User

Creates a new user, logs them in as the current user, and returns the current
user's information.

- Require Authentication: false
- Request

  - Method: POST
  - Route path: /api/users
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "email": "anton.ego@gourmand.com",
      "username": "ego",
      "first_name": "Anton",
      "password": "ratatouille"
    }
    ```

- Successful Response

  - Status Code: 201
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "bio": null,
      "created_at": "2025-01-11T20:39:28.688857",
      "email": "anton.ego@gourmand.com",
      "family_collection": {
        "created_at": "2025-01-11T20:39:28.691736",
        "description": "A collection of family recipes and memories.",
        "id": 9,
        "name": "FamilyRecipes",
        "updated_at": "2025-01-11T20:39:28.691745",
        "user_id": 6,
        "visibility": "public"
      },
      "first_name": "Anton",
      "id": 6,
      "location": null,
      "profile_image_url": null,
      "updated_at": "2025-01-11T20:39:28.688875",
      "username": "ego"
    }
    ```

- Error response: User already exists with the specified email or username

  - Status Code: 500
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "errors": {
        "email": "Email address is already in use.",
        "username": "Username is already in use."
      },
      "message": "Invalid Request"
    }
    ```

- Error response: Body validation errors

  - Status Code: 400
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "errors": {
        "email": "Invalid email address.",
        "password": "Field must be at least 6 characters long.",
        "username": "This field is required."
      },
      "message": "Invalid Request"
    }
    ```

### Edit User Profile

Returns the updated information about the current user.

- Require Authentication: false
- Request

  - Method: PUT
  - Route path: /api/session/edit
  - Body: none

- Successful Response when there is a logged in user

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "first_name": "Remy",
      "location": "San Francisco, CA",
      "bio": "I discovered my love for cooking by reading Anyone Can Cook by my idol, Auguste Gusteau and was a secret chef at Gatsteau's.I am now the exec chef and found of La Ratatouille.",
      "profile_image_url": "https://www.toonarific.com/wp-content/uploads/2024/10/Alfredo-Linguini-Ratatouille.jpg"
    }
    ```

- Successful Response when there is no logged in user

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "User profile updated successfully",
      "user": {
        "bio": "I discovered my love for cooking by reading Anyone Can Cook by my idol, Auguste Gusteau and was a secret chef at Gatsteau's.I am now the exec chef and found of La Ratatouille.",
        "created_at": "2025-01-11T20:18:20.950811",
        "email": "remy@gasteaus.com",
        "first_name": "Remy",
        "id": 1,
        "location": "San Francisco, CA",
        "profile_image_url": "https://www.toonarific.com/wp-content/uploads/2024/10/Alfredo-Linguini-Ratatouille.jpg",
        "updated_at": "2025-01-11T20:58:04.963705",
        "username": "little_chef"
      }
    }
    ```

- Error Response: If you ARE NOT the profile owner.

  - Status Code: 403
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
  {
    "message": "Only the profile owner can make changes to these details."
  }

    ```

## RECIPES

### Get all RECIPES

Returns all the recipes.

- Require Authentication: false
- Request

  - Method: GET
  - Route path: /api/recipes
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "recipes": []
    }
    ```

### Get all recipes owned by the Current User

Returns all the recipes owned (created) by the current user.

- Require Authentication: true
- Request

  - Method: GET
  - Route path: /api/recipes/current
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

```json
{
  "recipes": [
    {
      "id": 1,
      "name": "Burger Haven",
      "yield": 4,
      "prep_time": 15,
      "cook_time": 10,
      "total_time": 25,
      "short_description": "Juicy gourmet burgers and hand-cut fries.",
      "cuisine": "American",
      "difficulty": "Medium",
      "description": "A delicious gourmet burger served with crispy hand-cut fries.",
      "ingredients": "Beef patties, lettuce, tomato, cheese, burger buns, fries",
      "instructions": "Grill the beef patties, toast the buns, assemble the burger with cheese, lettuce, and tomato.",
      "tags": "burger, gourmet, American",
      "image_url": "https://example.com/images/burger.jpg",
      "owner_id": 1,
      "visibility": "Public",
      "created_at": "2024-12-16T10:00:00Z",
      "updated_at": "2024-12-16T10:00:00Z"
    },
    {
      "id": 2,
      "name": "Veggie Stir-Fry",
      "yield": 2,
      "prep_time": 10,
      "cook_time": 15,
      "total_time": 25,
      "short_description": "A healthy and flavorful stir-fry with mixed veggies.",
      "cuisine": "Asian",
      "difficulty": "Easy",
      "description": "Stir-fried mixed vegetables in a savory sauce served over rice.",
      "ingredients": "Broccoli, bell peppers, carrots, soy sauce, sesame oil, rice",
      "instructions": "Stir-fry the vegetables in sesame oil, add soy sauce, and serve over rice.",
      "tags": "vegetarian, stir-fry, healthy",
      "image_url": "https://example.com/images/veggie-stirfry.jpg",
      "owner_id": 2,
      "visibility": "Public",
      "created_at": "2024-12-16T11:00:00Z",
      "updated_at": "2024-12-16T11:00:00Z"
    }
  ]
}
```

### Get details of a Recipe from an id

Returns the details of a recipe specified by its id.

- Require Authentication: false
- Request

  - Method: GET
  - Route path: /api/recipes/:recipe_id
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

  ```json
  {
    "recipe": {
      "id": 1,
      "owner_id": 1,
      "name": "Burger Haven",
      "yield": 4,
      "prep_time": 15,
      "cook_time": 10,
      "total_time": 25,
      "short_description": "Juicy gourmet burgers and hand-cut fries.",
      "cuisine": "American",
      "difficulty": "Medium",
      "description": "A delicious gourmet burger served with crispy hand-cut fries.",
      "ingredients": "Beef patties, lettuce, tomato, cheese, burger buns, fries",
      "instructions": "Grill the beef patties, toast the buns, assemble the burger with cheese, lettuce, and tomato.",
      "tags": "burger, gourmet, American",
      "image_url": "https://example.com/images/burger.jpg",
      "owner_id": 1,
      "visibility": "Public",
      "created_at": "2024-12-16T10:00:00Z",
      "updated_at": "2024-12-16T10:00:00Z"
    }
  }
  ```

- Error response: Couldn't find a Recipe with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe couldn't be found"
    }
    ```

### Create a Recipe

Creates and returns a new recipe.

- Require Authentication: true
- Request

  - Method: POST
  - Route path: /api/recipes
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "name": "Spaghetti Bolognese",
      "yield": 4,
      "prep_time": 15,
      "cook_time": 45,
      "total_time": 60,
      "short_description": "Classic Italian pasta with a rich meat sauce",
      "cuisine": "Italian",
      "difficulty": "Medium",
      "description": "A hearty and comforting spaghetti dish.",
      "ingredients": "Spaghetti, Ground beef, Onion, Tomato, Garlic, Olive oil, Herbs",
      "instructions": [
        "1. Brown beef.",
        "2. Add onions and garlic.",
        "3. Simmer with tomatoes."
      ],
      "tags": "Italian, Pasta, Dinner",
      "image_url": "https://example.com/spaghetti.jpg",
      "owner_id": 1,
      "visibility": "Public"
    }
    ```

- Successful Response

  - Status Code: 201
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "name": "Spaghetti Bolognese",
      "yield": 4,
      "prep_time": 15,
      "cook_time": 45,
      "total_time": 60,
      "short_description": "Classic Italian pasta with a rich meat sauce",
      "cuisine": "Italian",
      "difficulty": "Medium",
      "description": "A hearty and comforting spaghetti dish.",
      "ingredients": "Spaghetti, Ground beef, Onion, Tomato, Garlic, Olive oil, Herbs",
      "instructions": [
        "1. Brown beef.",
        "2. Add onions and garlic.",
        "3. Simmer with tomatoes."
      ],
      "tags": "Italian, Pasta, Dinner",
      "image_url": "https://example.com/spaghetti.jpg",
      "owner_id": 1,
      "visibility": "Public",
      "created_at": "2025-01-01 10:15:00",
      "deleted_at": "2025-01-07 10:15:00"
    }
    ```

- Error Response: Body validation errors

  - Status Code: 400
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "name": "Name must be less than 50 characters.",
        "yield": "Servings yield is required.",
        "prep_time": "Prep time in minutes is required.",
        "cooking_time": "Cooking time in minutes is required.",
        "total_time": "Total time in minutes is required.",
        "email": "Valid email required.",
        "phone_number": "Valid phone number required.",
        "cuisine": "Cuisine must be selected from list."
      }
    }
    ```

### Add an Image to a Recipe based on the Recipe's id

Create and return a new image for a recipe specified by id.

- Require Authentication: true
- Require proper authorization: Recipe must belong to the current user
- Request

  - Method: POST
  - Route path: /api/recipes/:recipe_id/images
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "recipe_id": 1,
      "owner_id": 1,
      "url": "image.url",
      "preview": true
    }
    ```

- Successful Response

  - Status Code: 201
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "id": 1,
      "url": "image.url",
      "preview": true
    }
    ```

- Error response: Couldn't find a Recipe with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe couldn't be found"
    }
    ```

### Edit a Recipe

Updates and returns an existing recipe.

- Require Authentication: true
- Require proper authorization: Recipe must belong to the current user
- Request

  - Method: PUT
  - Route path: /api/recipes/:recipe_id
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "name": "Vegan Vibes Stir-Fry",
      "yield": 4,
      "prep_time": 10,
      "cook_time": 15,
      "total_time": 25,
      "short_description": "My dad's healthy and flavorful stir-fry with mixed veggies.",
      "cuisine": "Asian",
      "difficulty": "Easy",
      "description": "Stir-fried mixed vegetables in a savory sauce served over rice.",
      "ingredients": "Broccoli, bell peppers, carrots, soy sauce, sesame oil, rice",
      "instructions": "Stir-fry the vegetables in sesame oil, add soy sauce, and serve over rice.",
      "tags": "vegetarian, stir-fry, healthy",
      "image_url": "https://example.com/images/veggie-stirfry.jpg",
      "visibility": "Public"
    }
    ```

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "id": "5",
      "owner_id": "1",
      "name": "Vegan Vibes Stir-Fry",
      "yield": 4,
      "prep_time": 10,
      "cook_time": 15,
      "total_time": 25,
      "short_description": "A healthy and flavorful stir-fry with mixed veggies.",
      "cuisine": "Asian",
      "difficulty": "Easy",
      "description": "Stir-fried mixed vegetables in a savory sauce served over rice.",
      "ingredients": "Broccoli, bell peppers, carrots, soy sauce, sesame oil, rice",
      "instructions": "Stir-fry the vegetables in sesame oil, add soy sauce, and serve over rice.",
      "tags": "vegetarian, stir-fry, healthy",
      "image_url": "https://example.com/images/veggie-stirfry.jpg",
      "visibility": "Public",
      "created_at": "2024-12-16T12:00:00Z",
      "updated_at": "2024-12-16T12:30:00Z"
    }
    ```

- Error Response: Body validation errors

  - Status Code: 400
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Bad Request",
      "errors": {
        "name": "Name must be less than 100 characters",
        "description": "Description must be at least 30 characters",
        "ingredients": "Ingredients are required",
        "instructions": "Instructions must be provided"
      }
    }
    ```

- Error response: Couldn't find a Recipe with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe couldn't be found"
    }
    ```

### Delete a Recipe

Deletes an existing recipe.

- Require Authentication: true
- Require proper authorization: Recipe must belong to the current user
- Request

  - Method: DELETE
  - Route path: /api/recipes/:recipe_id
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

- Error response: Couldn't find a Recipe with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe couldn't be found"
    }
    ```

## REVIEWS

### Get all Reviews of the Current User

Returns all the reviews written by the current user.

- Require Authentication: true
- Request

  - Method: GET
  - Route path: /api/reviews/current
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "Reviews": [
        {
          "id": 1,
          "user_id": 1,
          "recipe_id": 1,
          "review": "This was an awesome recipe!",
          "stars": 5,
          "created_at": "2024-11-19 20:39:36",
          "updated_at": "2024-11-19 20:39:36",
          "User": {
            "id": 1,
            "first_name": "River",
            "last_name": "Tam"
          },
          "Recipe": {
            "id": 1,
            "owner_id": 1,
            "name": "Burger Haven",
            "address": "123 Burger Lane",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "cuisine": "Burger",
            "price_point": 2,
            "price_range": "$11 - $30"
          },
          "Images": [
            {
              "id": 1,
              "url": "image url"
            }
          ]
        }
      ]
    }
    ```

### Get all Reviews by a Recipe's id

Returns all the reviews that belong to a recipe specified by id.

- Require Authentication: false
- Request

  - Method: GET
  - Route path: /api/recipes/:recipe_id/reviews
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "Reviews": [
        {
          "id": 1,
          "user_id": 1,
          "recipe_id": 1,
          "review": "This was an awesome recipe!",
          "stars": 5,
          "created_at": "2024-11-19 20:39:36",
          "updated_at": "2024-11-19 20:39:36",
          "User": {
            "id": 1,
            "first_name": "River",
            "last_name": "Tam"
          },
          "Images": [
            {
              "id": 1,
              "url": "image url"
            }
          ]
        }
      ]
    }
    ```

- Error response: Couldn't find a Recipe with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe couldn't be found"
    }
    ```

### Create a Review for a Recipe based on the Recipe's id

Create and return a new review for a recipe specified by id.

- Require Authentication: true
- Request

  - Method: POST
  - Route path: /api/recipes/:recipe_id/reviews
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "review": "This was an awesome recipe!",
      "stars": 5
    }
    ```

- Successful Response

  - Status Code: 201
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "id": 1,
      "user_id": 1,
      "recipe_id": 1,
      "review": "This was an awesome recipe!",
      "stars": 5,
      "created_at": "2024-11-19 20:39:36",
      "updated_at": "2024-11-19 20:39:36"
    }
    ```

- Error Response: Body validation errors

  - Status Code: 400
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "review": "Review text is required",
        "stars": "Stars must be an integer from 1 to 5"
      }
    }
    ```

- Error response: Couldn't find a Recipe with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe couldn't be found"
    }
    ```

- Error response: Review from the current user already exists for the Recipe

  - Status Code: 500
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "User already has a review for this recipe"
    }
    ```

### Add an Image to a Review based on the Review's id

Create and return a new image for a review specified by id.

- Require Authentication: true
- Require proper authorization: Review must belong to the current user
- Request

  - Method: POST
  - Route path: /api/reviews/:reviewId/images
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "url": "image url"
    }
    ```

- Successful Response

  - Status Code: 201
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "id": 1,
      "url": "image url"
    }
    ```

- Error response: Couldn't find a Review with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Review couldn't be found"
    }
    ```

- Error response: Cannot add any more images because there is a maximum of 10
  images per resource

  - Status Code: 403
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Maximum number of images for this resource was reached"
    }
    ```

### Edit a Review

Update and return an existing review.

- Require Authentication: true
- Require proper authorization: Review must belong to the current user
- Request

  - Method: PUT
  - Route path: /api/reviews/:reviewId
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "review": "This was an awesome recipe!",
      "stars": 5
    }
    ```

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "id": 1,
      "user_id": 1,
      "recipe_id": 1,
      "review": "This was an awesome recipe!",
      "stars": 5,
      "created_at": "2024-11-19 20:39:36",
      "updated_at": "2024-11-20 10:06:40"
    }
    ```

- Error Response: Body validation errors

  - Status Code: 400
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "review": "Review text is required",
        "stars": "Stars must be an integer from 1 to 5"
      }
    }
    ```

- Error response: Couldn't find a Review with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Review couldn't be found"
    }
    ```

### Delete a Review

Delete an existing review.

- Require Authentication: true
- Require proper authorization: Review must belong to the current user
- Request

  - Method: DELETE
  - Route path: /api/reviews/:reviewId
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

- Error response: Couldn't find a Review with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Review couldn't be found"
    }
    ```

## RESERVATIONS

### Get all of the Current User's Reservations

Return all the reservations that the current user has made.

- Require Authentication: true
- Request

  - Method: GET
  - Route path: /api/reservations/current
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "Reservations": [
        {
          "id": 1,
          "recipe_id": 1,
          "Recipe": {
            "id": 1,
            "name": "Burger Haven",
            "address": "123 Burger Lane",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "email": "contact@burgerhaven.com",
            "phone_number": "212-555-6789",
            "website": "https://www.burgerhaven.com"
          },
          "first_name": "John",
          "last_name": "Smith",
          "date": "2024-11-19",
          "start_time": "06:00 PM",
          "party_size": 5,
          "created_at": "2024-11-19 20:39:36",
          "updated_at": "2024-11-19 20:39:36"
        }
      ]
    }
    ```

### Get all Reservations for a Recipe based on the Recipe's id

Return all the reservations for a recipe specified by id.

- Require Authentication: true
- Request

  - Method: GET
  - Route path: /api/recipes/:recipe_id/reservations
  - Body: none

- Successful Response: If you ARE NOT the owner of the recipe.

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "Reservations": [
        {
          "recipe_id": 1,
          "date": "2024-11-19",
          "start_time": "06:00 PM",
          "party_size": 5
        }
      ]
    }
    ```

- Successful Response: If you ARE the owner of the recipe.

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "Reservations": [
        {
          "User": {
            "id": 2,
            "first_name": "River",
            "last_name": "Tam"
          },
          "id": 1,
          "recipe_id": 1,
          "first_name": "John",
          "last_name": "Smith",
          "date": "2024-11-19",
          "start_time": "06:00 PM",
          "party_size": 5,
          "created_at": "2024-11-19 20:39:36",
          "updated_at": "2024-11-19 20:39:36"
        }
      ]
    }
    ```

- Error Response: If you ARE NOT the owner and NOT the reserver.

  - Status Code: 403
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "You are not authorized"
    }
    ```

- Error response: Couldn't find a Recipe with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe couldn't be found"
    }
    ```

### Create a Reservation from a Recipe based on the Recipe's id

Create and return a new reservation from a recipe specified by id.

- Require Authentication: true
- Require proper authorization: Recipe must NOT belong to the current user
- Request

  - Method: POST
  - Route path: /api/recipes/:recipe_id/reservations
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "date": "2024-11-19",
      "start_time": "06:00 PM",
      "party_size": 5
    }
    ```

- Successful Response

  - Status Code: 201
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "id": 1,
      "recipe_id": 1,
      "user_id": 2,
      "date": "2024-11-19",
      "start_time": "06:00 PM",
      "part_size": 5,
      "created_at": "2024-11-19 20:39:36",
      "updated_at": "2024-11-19 20:39:36"
    }
    ```

- Error response: Body validation errors

  - Status Code: 400
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "date": "Reservation date cannot be in the past",
        "start_time": "Start time must be within business hours",
        "party_size": "Please indicate your party size"
      }
    }
    ```

- Error response: Couldn't find a Recipe with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe couldn't be found"
    }
    ```

- Error response: Reservation conflict

  - Status Code: 403
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Sorry no more availability",
      "errors": {
        "startdate": "Start date conflicts with an existing reservation",
        "start_time": "Start time must be within business hours"
      }
    }
    ```

### Edit a Reservation

Update and return an existing reservation.

- Require Authentication: true
- Require proper authorization: Reservation must belong to the current user
- Request

  - Method: PUT
  - Route path: /api/reservations/:reservationId
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "sate": "2024-11-19",
      "start_time": "07:00 PM",
      "party_size": 5
    }
    ```

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "id": 1,
      "recipe_id": 1,
      "first_name": "John",
      "last_name": "Smith",
      "date": "2024-11-19",
      "start_time": "07:00 PM",
      "party_size": 5,
      "created_at": "2024-11-19 20:39:36",
      "updated_at": "2024-11-20 10:06:40"
    }
    ```

- Error response: Body validation errors

  - Status Code: 400
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "date": "Reservation date cannot be in the past",
        "start_time": "Start time must be within business hours",
        "party_size": "Please indicate your party size"
      }
    }
    ```

- Error response: Couldn't find a Reservation with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Reservation couldn't be found"
    }
    ```

- Error response: Can't edit a reservation that's past the end date

  - Status Code: 403
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Past reservations can't be modified"
    }
    ```

- Error response: Reservation conflict

  - Status Code: 403
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Sorry no more availability",
      "errors": {
        "startdate": "Start date conflicts with an existing reservation",
        "enddate": "End date conflicts with an existing reservation"
      }
    }
    ```

### Delete a Reservation

Delete an existing reservation.

- Require Authentication: true
- Require proper authorization: Reservation must belong to the current user or the
  Recipe must belong to the current user
- Request

  - Method: DELETE
  - Route path: /api/reservations/:reservationId
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

- Error response: Couldn't find a Reservation with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Reservation couldn't be found"
    }
    ```

- Error response: Reservations that have been started can't be deleted

  - Status Code: 403
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Reservations that have been started can't be deleted"
    }
    ```

## IMAGES

### Delete a Recipe Image

Delete an existing image for a Recipe.

- Require Authentication: true
- Require proper authorization: Recipe must belong to the current user
- Request

  - Method: DELETE
  - Route path: /api/recipe-images/:imageId
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

- Error response: Couldn't find a Recipe Image with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Recipe Image couldn't be found"
    }
    ```

### Delete a Review Image

Delete an existing image for a Review.

- Require Authentication: true
- Require proper authorization: Review must belong to the current user
- Request

  - Method: DELETE
  - Route path: /api/review-images/:imageId
  - Body: none

- Successful Response

  - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

- Error response: Couldn't find a Review Image with the specified id

  - Status Code: 404
  - Headers:
    - Content-Type: application/json
  - Body:

    ```json
    {
      "message": "Review Image couldn't be found"
    }
    ```

## Get All Recipes (with Query Filters)

This endpoint allows users to retrieve recipes filtered by query parameters such as collection, cuisine type, location, and other criteria.

- Require Authentication: false
- Request
  - Method: GET
  - Route Path: /api/recipes
- Query Parameters:

  - page (integer): Page number, default is 1, minimum is 1.
  - size (integer): Number of recipes per page, default is 20, minimum is 1, maximum is 20.
  - cuisine (string, optional): Type of cuisine (e.g., "Italian", "Mexican").
  - collection price_point (integer, optional): Price point from 1 to 5.
  - location: City where the recipe is located (e.g., "New York").
  - avg_rating (float, optional): Average rating filter for the recipes.
  - Successful Response
    - Status Code: 200
  - Headers:
    - Content-Type: application/json
  - Body:
    ```json
    {
      "name": "Spaghetti Bolognese",
      "yield": 4,
      "prep_time": 15,
      "cook_time": 45,
      "total_time": 60,
      "short_description": "Classic Italian pasta with a rich meat sauce",
      "cuisine": "Italian",
      "difficulty": "Medium",
      "description": "A hearty and comforting spaghetti dish.",
      "ingredients": "Spaghetti, Ground beef, Onion, Tomato, Garlic, Olive oil, Herbs",
      "instructions": [
        "1. Brown beef.",
        "2. Add onions and garlic.",
        "3. Simmer with tomatoes."
      ],
      "tags": "Italian, Pasta, Dinner",
      "image_url": "https://example.com/spaghetti.jpg",
      "owner_id": 1,
      "visibility": "Public",
      "created_at": "2025-01-01 10:15:00",
      "deleted_at": "2025-01-07 10:15:00"
    }
    ```

- Error Response: Query Parameter Validation Errors
  If the query parameters are invalid, the API will return the following error response:
- Status Code: 400
- Headers:
  - Content-Type: application/json
- Body:

  ```json
  {
    "message": "Bad Request",
    "errors": {
      "page": "Page must be greater than or equal to 1",
      "size": "Size must be between 1 and 20",
      "minPrice": "Minimum price must be greater than or equal to 0",
      "maxPrice": "Maximum price must be greater than or equal to 0"
    }
  }
  ```
