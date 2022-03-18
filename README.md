# greenhands_backend
An open source, community service project to help people in need on 'need to know' basis


## Main Idea
This project divides users into three categories: Takers, Givers and Organizers.
therefore there are three paths.

### Takers Path:
1. Takers are not asked to fill in any data to use the application.
2. Takers can create an 'exchange point' to receive their needs (any point on the map).
3. Takers can attach any number of 'needs' to the exchange point.
4. Takers receive notification when the need is provided.
5. Takers can ask for organizers verification (to confirm their status).
6. Takers can report organizers abuse of the system (if any).

### Givers Path:
1. Givers are not asked to fill in any data to use the application.
2. Givers can see a map with taker's exchange points and the attached needs.
3. After providing a 'need', givers can notify takers.
4. Givers can contact organizers if they need a direct contact with takers. (like doctors).
5. Givers can report organizers abuse of the system (if any).

### Organizers Path:
With power comes responsibility, organizers are asked to vouch for takers and help givers reach real needs.
1. Organizers are asked to provide accurate details of themselves, and their account is activated manually by the admin after verifying their data and identity.
2. Organizers locations and data is always visible to both givers and takers.
3. Organizers receive verification requests from takers, and they are responsible for verifying or denying them.

# Backend Requirements:
1. Python 3.*
2. pip install -r requirements.txt

# Usage
After installing the required packages from previous step, all you need is to navigate to the project directory and type
python manage.py runserver

# Requests and Responses:
Api schema samples can be found on green_hands.postman_collection.json


# Related Projects:
* Backend: (on-going) https://github.com/saad4software/greenhands_backend
* Frontend: (on-going) https://github.com/saad4software/greenhands_frontend
* Mobile: (on-going) https://github.com/saad4software/greenhands_mobile
