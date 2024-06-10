# tutoring-app
A web application built using Django, Django REST framework and Channels library with an addition of Vanilla JS. The application can be used by tutors of various subjects to manage lessons with their students and by people who are looking for a tutor.

# Running the app locally 

To run the app locally, start off by cloning the repository and create an virtual environment with the following command:
`
python -m venv venv
`

Then, switch to the location where the requirements.txt file is located and run the following command to install of the necessary dependencies:
`
pip install -r requirements.txt
`

Application uses the `Channesls` library which requires the use of Redis for the channel layer - before running the application, the Redis server must be running on a specific port. The easiest way to set it up is with Docker, specifically with [Docker Desktop]([https://duckduckgo.com](https://www.docker.com/products/docker-desktop/)). After it has been installed, you can start the Redis container with the following command: `docker run --rm -p 6379:6379 redis:7`

After that change the directory to where the `manage.py` file is located and run the app with the command: `python manage.py runserver`
