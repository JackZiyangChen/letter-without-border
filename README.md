# Letters without Borders

### A Quick Note
This project is intended to be a finished and improved version of my project at the 2022 Annual HackNYU Hackathon. The idea of this project and the original version of the project that I repurposed from belong to the original authors, which I have listed in the "Authors" section. The original version of the code will be stored in the "stab/0.0.2-violet-functional" branch. 

## Authors
* Jack Chen
* Jack Lee
* Johnathan Zhou
* Brian Zou

## Project Description
Letters without Borders, named after the famous nonprofit "Doctors without Borders," is an online anonymous messaging application. This application works similar to the "message in a bottle" app on WeChat. In Letters Without Borders, users can post letters anonymously and read/respond to other people's letters.

The hope for this project is to promote positivity through anonymity. Oftentimes in our lives, a lot of us have no outlets to share our inner thoughts and feelings. Letters Without Borders provide an easy and quick way to jog down random thoughts to share with others across the internet. Our ultimate hope is to improve the mental health of users who use our site, even just for a litte.

## Architecture Overview
Flask is the main framework of the project. It allows for easier wiring of
the front end and the back end, along with the database.

## Running the project
Go to http://letterswithoutborders.herokuapp.com

If you want to run the project locally, feel free to use a local git terminal to download the project. To configure the project, please run "main.py" and follow the instructions of localhost in your terminal. Alternatively, you can right click the index.html file under HackNYU2022/website/templates/index.html and open in a browser of their choice.

For security reasons, I chose to exclude the .env file in my commit. Please reconfigure the project yourself with the following parameters:
* SECRET_KEY
* LOCAL_DB_URL
* FLASK_APP=main.py
* DEBUG

## Prerequisites
Before you begin, ensure you have met the following requirements:
* You have Python 3 installed
* You have imported the flask libraries and SQLAlchemy 
* You have enabled javascript

(Note: comments on specific imports located in the __init__.py file - 
installation can be done through pip in the terminal/command prompt)

## SQL Database
Databse is handled through PostgreSQL database, powered by Heroku and AWS. 

## Contacts
If you have any questions regarding the project, you can locate
us at:
* zc2398@nyu.edu (Jack Chen)
* jl12734@nyu.edu (Jack Lee)
* qz2190@nyu.edu (Johnathan Zhou)
* bz2193@nyu.edu (Brian Zou)


















