
# Item Catalog

The Live version of project can be found at <a href="http://zdburrage.pythonanywhere.com">This Link</a>

## Project Overview

To Develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items as well as CRUD categories that they created.

## Why This Project?

Modern web applications perform a variety of functions and provide amazing features and utilities to their users; but deep down, it’s really all just creating, reading, updating and deleting data. In this project, you’ll combine your knowledge of building dynamic websites with persistent data storage to create a web application that provides a compelling service to your users.

## How to Run?
### PreRequisites

Python ~2.7

Vagrant

VirtualBox

## Setup Project:
1. Install Vagrant and VirtualBox

2. Download or Clone <a href="https://github.com/udacity/fullstack-nanodegree-vm">fullstack-nanodegree-vm repository.</a>

3. Find the catalog folder and replace it with the content of this current repository, by either downloading or cloning it from Here.

4. Launch the Vagrant VM using command:

   $ vagrant up
  
5. Run your application within the VM

   $ python /vagrant/catalog database_setup.py (This will create your database and tables)
  
   $ python /vagrant/catalog/application.py
  
6. Access and test your application by visiting http://0.0.0.0:5000.
