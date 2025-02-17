# Pizzigatto - the pizza project

This is my submission of the cs50w project 3 - Pizza - https://docs.cs50.net/web/2020/x/projects/3/project3.html

Screencast: https://youtu.be/muswxcWX_lM

# Description
Pizzigatto is a restaurant e-shop featuring menu-management section for the staff.
The django project is divided into three apps: Accounts (dealing with user accounts), Menu (dealing with the restaurant menu and its handling) and Orders (dealing with the shopping process). 
For the flexibility of the menu I decided to design the models in a very simple fashion, where we have only two classes to represent non-pizzas: MealType and MenuItem. This allows for a fully customizable menu that a restaurant manager (staff user) can make any changes to without using django admin (because, do we really want the restarant people to use django admin?). For the pizzas, there is paradoxically no need to have a Pizza class, since the point of the restaurant's system is that every pizza is custom-designed by the guests. Therefore we only need to handle the set of Toppings and enable price handling for all the possible combinations of (1) pizza forms, (2) pizza size and (3) combination of toppings. The prices are handled by only one instance of a Price class, which is not deletable outside of django admin, thus cannot be messed up incidentally by the staff user.
The personal touch took me more than half of the time I spent working on this, but I couldn't allow myself submitting the project without the 'management section' that allows for the abovementioned menu customizability. More precisely, by the customizability I mean that new meal types can by created, edited, hidden from the menu or deleted; and the same goes for menu items and toppings - all of this using our own interface.

# Side note
If you are about the clone and try out, there is a superuser created for you (credentials: superuser/password1234).  
