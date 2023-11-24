# Project "PhotoSHAKE" from team "Snake Shake"

<p align="center">
   <img src="https://img.shields.io/badge/Language-Python-9cf">
   <img src="https://img.shields.io/badge/FastAPI-0.95.1-brightgreen">
   <img src="https://img.shields.io/badge/SQLAlchemy-2.0-orange">
   <img src="https://img.shields.io/badge/Pytest-7.3.0-informational">
   <img src="https://img.shields.io/badge/License-MIT-yellow">
</p>

## About ✨

#### PhotoShake 
PhotoShake is a web application that allows users to create an account, upload posts with photos, use hashtags and leave comments. The application is built using the FastAPI framework and uses SQLAlchemy as the database ORM.

## Deployment
- [Live PhotoShake](https://goit-py-web-14-team-project-group-4.fly.dev/docs)


## Installation 💻
To run this project, follow these steps:

1. Clone this repository to your local machine.
2. Install poetry by command ''' pip install poetry '''
3. Activate virtual environment by command ''' poetry shell '''
4. Install the required packages by running ''' poetry install '''
5. Create a virtual environment file in the root of the project based on env.example.
6. Create a database according to the requirements of env.example.
7. Start the creation of tables in the database with the command in the terminal while being at the root of the project ''' alembic upgrade head '''
8. Run the application with the command in the terminal while being at the root of the project ''' python3 main.py '''
9. All further actions in the application are carried out according to the link ''' http://localhost:8000/docs#/ '''


## Usage 💠
This project exposes many endpoints through a REST API. To access these APIs, use any API client, such as Postman or cURL. The API documentation can be found at [documentation](https://github.com/ValeraRishniak/goit_py_web_14_team_project_group_4/blob/main/docs/_build/html/index.html).


## Developers:

<div align="">
  <a href="https://github.com/ValeraRishniak">Team Lead Valerii Rishniak</a><br>
  <a href="https://github.com/Vikka777">Scrum master Viktoriia Piatkovska</a><br>
  <a href="https://github.com/Topsya">Developer Anton Mescheryakov</a><br>
  <a href="https://github.com/VladyslavBon">Developer Vladyslav Bondarenko</a><br>
</div>


## License 🔱
Project "PhotoShake" is distributed under the MIT license.
