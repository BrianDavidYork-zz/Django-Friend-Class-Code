DJANGO FRIEND CLASS CODE

This project contains code for a (minimal) user model and Friendship model that can be applied to any project where Friendship relationships are needed.  Included are views that allow the user to add friends, delete friends, show all of the a particular user's friends, and confirm friendships.  The views output is JSON, and in practice the JSON being returned would be passed to user-facing front-end code.  Included is an Auth Token authentication scheme, which provides security and allows django to access the User through Auth Tokens when that user makes requests.

NEEDED:
django
django_rest_framework

AUTHOR:
Brian York
