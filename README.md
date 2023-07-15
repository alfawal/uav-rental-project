# UAV (Unmanned Aerial Vehicle) Rental Project

## Requirements

- Docker Engine >=18.02.0 (Check with `docker --version`)
- Docker Compose

## Running the project

I do assume that you know the first couple of steps, but I did mention them anyway.

1. Clone the repository
```bash
git clone https://github.com/alfawal/uav-rental-project.git
```

2. Change directory to the project directory
```bash
cd uav-rental-project
```

4. Build it
```bash
python3 docker.py build
```

5. Run it
```bash
python3 docker.py run
```

6. Run the migrations
```bash
python3 docker.py migrate
```

8. Seed the database
```bash
python3 docker.py seed
```
You'll receive 3 users (1 admin, 2 customers) in your terminal.
Each of the customers has different rental history. They cannot access each other's history but the admin.


*The frontend is not ready (I was/still relocating).*


9. Open your browser and go to `http://localhost:8000/api-auth/login` to login (if you prefer DRF's browsable UI).

10. Use the API routes and have a look at the source code!

## API Routes

### Authentication

JWT Authentication is used for the API routes.

Obtain a token:

`POST` `http://localhost:8000/api/token`

```json
{
    "username": "admin",
    "password": "admin"
}
```

Refresh a token:

`POST` `http://localhost:8000/api/token/refresh/`

```json
{
    "refresh": "your_refresh_token"
}
```
### Users
List the users:

`GET` `http://localhost:8000/api/users/`

- Permissions:
    - Only authenticated users can access.
    - Admins can access all users.
    - Customers can access only themselves.

- Ordering fields (`-` for descending order):
    - `id`
    - `username`
    - `email`

- Filterset fields:
    - `is_active`: boolean
    - `is_superuser`: boolean
    - `is_staff`: boolean
    - `is_customer`: boolean

Retrieve a user:

`GET` `http://localhost:8000/api/users/{user_pk}`

- Permissions:
    - Only authenticated users can access.
    - Admins can access all users.
    - Users can access only themselves.


### UAVs

List the UAVs:

`GET` `http://localhost:8000/api/uavs/`

- Permissions:
    - Only authenticated users can access.

- Ordering fields (`-` for descending order):
    - `created_at`
    - `updated_at`
    - `weight`
    - `daily_price`

- Filterset fields:
    - `is_rented`: boolean
    - `brand`: string
    - `model`: string
    - `weight`: float
    - `weight_min`: float
    - `weight_max`: float
    - `category`: string
    - `description`: string
    - `daily_price`: float
    - `daily_price_min`: float
    - `daily_price_max`: float
    - `created_at`: datetime
    - `created_at_before`: datetime
    - `created_at_after`: datetime
    - `updated_at`: datetime
    - `updated_at_before`: datetime
    - `updated_at_after`: datetime

Retrieve a UAV:

`GET` `http://localhost:8000/api/uavs/{uav_pk}`

- Permissions:
    - Only authenticated users can access.

Create a UAV:

`POST` `http://localhost:8000/api/uavs/`

- Permissions:
    - Only authenticated users can access.
    - Only admins can create UAVs.

- Example request body:

```json
{
    "brand": "DJI",
    "model": "Mavic Air 2",
    "weight": 570,
    "category": "Consumer",
    "description": "The Mavic Air 2 is a drone that offers a perfect balance of power and portability. It is equipped with a 1/2-inch image sensor for 48MP photos and 4K/60fps videos and a max flight time of 34 minutes.",
    "daily_price": 100,
    "photo": (BINARY),
    "data": {
        "max_speed": 68.4,
    }
}
```

Update a UAV:

`PUT` `http://localhost:8000/api/uavs/{uav_pk}`

- Permissions:
    - Only authenticated users can access.
    - Only admins can update UAVs.

- Example request body:

```json
{
    "brand": "DJI",
    "model": "Mavic Air 2",
    "weight": 570,
    "category": "Consumer",
    "description": "The Mavic Air 2 is a drone that offers a perfect balance of power and portability. It is equipped with a 1/2-inch image sensor for 48MP photos and 4K/60fps videos and a max flight time of 34 minutes.",
    "daily_price": 100,
    "photo": (BINARY),
    "data": {
        "max_speed": 68.4,
    }
}
```

Delete a UAV:

`DELETE` `http://localhost:8000/api/uavs/{uav_pk}`

- Permissions:
    - Only authenticated users can access.
    - Only admins can delete UAVs.

### Rentals

List the rentals under a specific UAV/User (All if admin, only owned by self if not):

`GET` `http://localhost:8000/api/uavs/{uav_pk}/rentals/`

`GET` `http://localhost:8000/api/users/{user_pk}/rentals/`

- Permissions:
    - Only authenticated users can access.
    - Admins can access all rentals.
    - Customers can access only their own rentals.

- Ordering fields (`-` for descending order):
    - `created_at`
    - `updated_at`
    - `start_date`
    - `end_date`

Retrieve a rental:

`GET` `http://localhost:8000/api/uavs/{uav_pk}/rentals/{rental_pk}`

- Permissions:
    - Only authenticated users can access.
    - Admins can access all rentals.
    - Customers can access only their own rentals.

Create a rental only authenticated users:

`POST` `http://localhost:8000/api/uavs/{uav_pk}/rentals/`

- Permissions:
    - Only authenticated users can access.

- Example request body:

```json
{
    "start_date": "2021-01-01",
    "end_date": "2021-01-02"
}
```

Update a rental:

`PUT` `http://localhost:8000/api/uavs/{uav_pk}/rentals/{rental_pk}`

- Permissions:
    - Only authenticated users can access.
    - Admins can update all rentals.
    - Customers can update only their own rentals.

- Example request body:

```json
{
    "start_date": "2021-01-01",
    "end_date": "2021-01-02"
}
```

Delete a rental:

`DELETE` `http://localhost:8000/api/uavs/{uav_pk}/rentals/{rental_pk}`

- Permissions:
    - Only authenticated users can access.
    - Admins can delete all rentals.
    - Customers can delete only their own rentals.
