# 📝 Description

This project is a backend application for a travel booking platform. It has been enhanced with asynchronous background processing using Celery and RabbitMQ to handle tasks like sending email notifications. This ensures the main application remains responsive and provides a better user experience.

<br>

# 🎯 Objective

The primary objective of this version was to:
- Implement an email notification system for booking confirmations.
- Integrate Celery with RabbitMQ to send emails asynchronously.
- Enhance performance by offloading time-consuming tasks from the main request-response cycle.

<br>

# ✨ Features

- **Celery & RabbitMQ Integration:** Configured to handle background tasks, improving application responsiveness.
- **Asynchronous Email Notifications:** A shared task to send booking confirmation emails is triggered upon booking creation, without blocking the user.
- **Database Models:** Three core models—`Listing`, `Booking`, and `Review`—represent travel listings, user bookings, and user reviews.
- **Django REST Framework Serializers:** Serializers are implemented to convert model instances into JSON format, providing a structured way to interact with the data via an API.
- **Database Seeder:** A custom management command (`seed`) is available to quickly populate the database with a large amount of realistic, fake data for development and testing purposes.
- **Environment Variables:** Sensitive configurations are managed using a `.env` file, following best practices for production-ready applications.

<br>

# 🛠️ Technologies Used

- Python 3
- Django
- Django REST Framework
- Celery
- RabbitMQ (as the message broker)
- Faker (for generating fake data)
- python-decouple (for managing environment variables)
- mysqlclient (MySQL database connector)

<br>

# 🚀 Setup and Installation

Follow these steps to get the project up and running on your local machine.

<br>

1. **Clone the Repository:**
```bash
git clone https://github.com/frankiewilson1/alx_travel_app_0x03.git
cd alx_travel_app_0x03/alx_travel_app
```

<br>

2. **Create a Virtual Environment:**
```bash
python3 -m venv env
source env/bin/activate # On Windows, use: env\Scripts\activate
```

<br>

3. **Install Dependencies:**
Install all required Python packages, including `celery`, `pika`, and `python-decouple`.
```bash
pip install -r requirements.txt
```

<br>

4. **Configure Environment Variables:**
Create a file named `.env` in the project root directory (`alx_travel_app/`) and add your database and Celery configurations.
```
# Django SECRET_KEY
SECRET_KEY=your_secret_key_here

# MySQL Database Configuration
DATABASE_URL=mysql://alx_user:12345@localhost:3306/alxtravelapp_db
DATABASE_NAME=alxtravelapp_db
DATABASE_USER=alx_user
DATABASE_PASSWORD=12345
DATABASE_HOST=localhost
DATABASE_PORT=3306

# Celery Configuration
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
```

<br>

5. **Run Migrations:**
Apply the database schema to your MySQL database.
```bash
python manage.py makemigrations
python manage.py migrate
```

<br>

# 📋 Usage

<br>

## Running Background Services

You need to run a RabbitMQ server and a Celery worker in separate terminals to handle the asynchronous tasks.

### Start RabbitMQ:
Ensure RabbitMQ is running on your system.

### Start the Celery Worker:
This command starts the worker, which listens for and executes tasks from the message broker.
```bash
celery -A alx_travel_app worker -l info
```

### Start the Django Server:
```bash
python manage.py runserver
```

When a new booking is created via the API, a confirmation email task will be sent to the Celery worker, which will process and send the email in the background without blocking the API response.

<br>

## Seeding the Database

After setting up the project, you can use the custom seed command to populate your database with fake data.

### To seed with default values:
```bash
python manage.py seed
```

### To clear existing data and seed with custom values:
```bash
python manage.py seed --clear --num_listings 50 --num_users 10
```

<br>

# 🧑‍💻 Author

Frank Williams Ugwu - [GitHub Profile](https://github.com/your-username)

