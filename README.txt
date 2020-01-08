DJANGO FRIEND CLASS CODE

This project contains code for a (minimal) User model and Friend model, with methods, that can be used with any project where Friendship relationships are needed.
Included are views that allow the user to add friends, delete friends, show all of the a particular user's friends, and confirm friendships.
The views output is JSON, and in practice the JSON being returned would be passed to user-facing front-end code.

A friend request is sent by maing a POST request to /friend/<username>
A friend request is confirmed by making a PUT request to /friend/<username>
A user's list of friendships can be seen by maing a GET request to /friend/<username>
A friendship or friend request can be deleted by making a DELETE request to /friends/<username>

In all cases above, <username> is the username of the friend you are establishing/deleting a frienship with.  Django Rest-Framework's AuthTokens allows users to be identified with every request they make.


PACKAGES NEEDED:
django
django_rest_framework

AUTHOR:
Brian York
