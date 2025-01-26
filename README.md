# How to use this project

After you have cloned this repository, you must follow the following steps to set up the project:

1. Install Python 3.12 by downloading it from the official Python website: https://www.python.org/downloads/ or upgrade your current Python version.
2. Install virtualenv by running this command in your terminal: `pip install virtualenv`
3. Create a virtual environment by running this command in your terminal: `virtualenv venv` (or any other name you choose)
4. Activate the virtual environment by running this command in your terminal: `source venv/bin/activate` (or the equivalent command for your operating system)
5. Install all the dependencies required by the project by running this command in your terminal: `pip install -r requirements.txt`
6. Create a `.env` file in the root directory of the project and add your environment variables. For example, you can use the following variables:

        DEBUG=True
        SECRET_KEY=django-insecure-default-key-change-me
        DATABASE_URL=sqlite:///db.sqlite3
        ALLOWED_HOSTS=localhost,127.0.0.1

7. Run the following commands in your terminal to create the database tables and apply any pending migrations:

        python manage.py migrate
        python manage.py createsuperuser

8. Finally, run the following command in your terminal to start the Django development server:

        python manage.py runserver

9. Open the following URL in your web browser: `http://localhost:8000` (or the IP address and port number you specified in your `ALLOWED_HOSTS` environment variable)

