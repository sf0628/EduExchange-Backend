# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

# EduShare Hub

## Description

For our final project, we created a student sharing platform called EduShare Hub, designed to alleviate the financial burden on college students while fostering a collaborative and sustainable academic community. EduShare Hub facilitates the exchange of educational resources such as textbooks, lecture notes, and lab materials, specifically targeting the Northeastern student community. By addressing the challenges of high educational expenses and material wastage, EduShare Hub promotes sustainability and collaborative learning. Through its user-friendly interface, students can effortlessly find, share, or swap the materials they need, creating a stronger, more resourceful, and interconnected academic community.

## Team Information

**Team Name:** EduExchange

**Team Members and Contact Information:**

- Nozomi Kaneda: kaneda.n@northeastern.edu
- Sanjana Singhania: singhania.sa@northeastern.edu
- Sophia Fu: fu.so@northeastern.edu
- Rhea Kallely: kallely.r@northeastern.edu

## Setting Up the Project
**Important** - you need Docker Desktop installed
 ## How to setup and start the containers

To set up the project, follow these steps:

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 

## Accessing the AppSmith Tool

Once the containers are running, you can access the AppSmith tool by following these steps:

1. Open a web browser.
2. Navigate to the following URL: [http://localhost:8080/applications](http://localhost:8080/applications).
   - Note: Replace `8080` with the port number if you've configured a different port in the `docker-compose.yml` file.

## Additional Notes

- Ensure that the necessary SQL files are executed to set up the database schema and populate initial data.
- For any issues or inquiries, please contact the team members listed above.

## Demo
- Demo located at following URL (sorry in advance for the poor quality): [https://youtu.be/_TPQKjX5T2U]

