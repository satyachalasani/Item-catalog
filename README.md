# Udacity Full-Stack Nanodegree

# Project 4 : Item Catalog

This is a python module that creates a website and JSON API for a list of Book Sections. Each Book Section displays their Books and also provides user authentication using Google. 

Registered users will have ability to edit and delete their own items. This application uses Flask,SQL Alchemy, JQuery,CSS, Javascript, and OAuth2 to create Item catalog website.

### Installation 
1.virtualBox 

2.Vagrant 

3.python 2.7


### Setting up OAuth 2.0

You will need to signup for a google account and set up a client id.
Visit **_http://console.developers.google.com_** for google setup.

## How to Run

ensure you have Python, Vagrant and VirtualBox installed. This project uses a pre-congfigured Vagrant virtual machine which has the Flask server installed.

$ cd vagrant

$ vagrant up

$ vagrant ssh

Within the virtual machine change in to the shared directory by running

$ cd /vagrant/catalog/catalogproject-final

$ python project.py

> Then navigate to localhost:5000 on your favorite browser.

> Once you are done, terminate the web server using _CTRL+C_ in the terminal running.oooo..
