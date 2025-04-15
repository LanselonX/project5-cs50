# Distinctiveness and Complexity:

This is a task management web application based on django. The project is designed to simplify the organization of personal and team tasks. This application allows you to manage teams and invite new members using unique links.

Unlike the task-related features seen in other projects such as Project 2 (Commerce) or Project 4 (Social Network), Notetaker integrates team-based functionality with real-time updates and role-specific task flows, elevating its complexity and scope. One of the core elements that makes Notetaker distinct is the team invitation system using UUID-based tokens, allowing users to join teams through secure, links. This mechanism involved implementing a custom Invitation model, token generation, expiration handling, and validation on the backend — a feature not seen in any course project example.

Another layer of complexity lies in the assignment and delegation of tasks within teams. The application supports enforces permissions, such as restricting who can delete a team. These features required careful management of user-to-task and user-to-team relationships, with logic that adapts depending on who performs an action.

On the frontend, the app uses asynchronous JavaScript (AJAX) to provide a seamless user experience: team task statuses are updated live, tasks can be marked as done or reassigned without full-page reloads, and image previews are dynamically displayed when uploading files. This interactive experience required building custom endpoints that respond with JSON data and coordinating Django views with JavaScript logic.

Notetaker is also built with scalability in mind: all views are paginated where needed, and the layout is fully responsive, ensuring usability on mobile devices. This goes beyond the design scope of earlier course projects. Overall, the combination of dynamic user roles, secure invitation flows, rich client-side interaction, and scalable architecture makes Notetaker both distinct and technically challenging.

### Unique Features

1. **Task Management** Users can create individual tasks, or team tasks, each team task has its own status to track the progress of the work

2. **Team Collaboration** The system allows users to form teams, add members, and assign tasks to specific team members. Assigned tasks will be displayed on the user's main page

3. **Invitation** Team leaders can create unique invitation links that make it easier to join a team and increase security.

## Project file structure

### 1. **models.py** – Defines data models:

- `User` – a custom model

- `Team` – a model that describes teams, their creators, and participants

- `Task` – a model for tasks with status support and the ability to attach images

- `Invitation` – a model for unique invitations using UUID

### 2. **views.py** Contains server logic for processing requests.

At the moment, this module includes **19 view functions**. Below is a brief description of each:

- `register` - function that processes new user registration, checks password confirmation, tracks duplicate usernames, and if successful, logs in the new user.

- `logout_view` - logs the user out of the system and directs him to the login form

- `login_view` - the function provides a form for entering login and password in order to get to the main page

- `index` - displays the main page with user tasks, both team and individual tasks

- `create_invitation` - a function that creates a unique link to join a team, _only the team leader can create it_

- `join_team` - function so that the user can join the team via a link

- `user_team` - display user's teams, achieved this effect thanks to the tool **Django ORM**, I also use **Django Pagination**

- `create` - creates a single task for the user

- `edit_task` - with this function the user can edit single tasks

- `mark_task_done` - marks a team task as done

- `delete_task` - removes single user tasks and team tasks

- `delete_team` - function to delete a team, _only the team leader can delete it_

- `leave_team` - the function is needed so that the user can exit the team, _the team leader cannot leave the team_

- `assign_task` - allows assigning a selected team task to a user

- `create_team_task` - creates a team task, _only team members can create such tasks_

- `team_detail` - a function that is needed to track team tasks: _task_todo_, _tasks_in_progress_, _tasks_done_

- `solo_task_detail` - serves to describe in detail a single user task

- `task_detail_api` - serves to describe the team's task in detail

- `create_team` - the function is needed to create a team

### 3. **urls.py** Defines routes including index:

- `/register`

- `/logout`

- `/login`

- `/create`

- `/create_team`

- `/user_team`

- `/create_invitation/<int:team_id>/`

- `/join_team/<uuid:token>/`

- `/team/<int:team_id>/create_task/`

- `/team/<int:team_id>/`

- `/team/<int:team_id>/task/<int:task_id>/`

- `/task/<int:task_id>/`

- `/team/<int:team_id>/task/<int:task_id>/assign/`

- `/task/<int:task_id>/mark_done/`

- `/task/<int:task_id>/delete/`

- `/team/<int:team_id>/leave/`

- `/task/<int:task_id>/edit`

- `/team/<int:team_id>/delete/`

### 4. **forms.py**

- `AddTasksForm` - Form for creating personal and team tasks. Uses ModelForm to automatically distribute fields based on the Task model. Widgets are customized to better display clients.

- `AddTeamForm` - Form for creating a team, includes `name` and `image` fields, styled with Bootstrap-like classes.

### 5. **Static files and scripts** Responsible for client logic, asynchronous requests and dynamic updating of the user interface

### **JavaScript**

There are 5 javascript files in my project

- `csrf.js` - JavaScript function that extracts CSRF from browser cookies

- `imgPreview.js` - also a JavaScript function that shows a preview of a photo

- `index.js` - opens a more detailed description of both team and single tasks. allows to delete single tasks

- `task_detail.js` - allows you to work more conveniently with team tasks, assign them to user, give them the value of a done task and delete them

- `teams.js` - function that allows to delete a team

### **styles**

there is only 1 static file here - `styles.css`, it is needed for more flexible work with styles

### **HTML**

there are **10 files** here for dynamic page generation

- `create_tasks.html` - page for displaying the form for creating a single task

- `create_team_task.html` - page for displaying the form for creating a team task

- `create_team.html` - page with form for creating a team

- `edit_task.html` - page with form for editing task

- `index.html` - main page with both single and team tasks

- `layout.html` - file is a **base template** used for structuring pages in the project.

- `login.html` - login form

- `register.html` - register form

- `task_detail.html` - The page displays team tasks

- `teams.html` - page displaying user team

## How to launch the application

1. **Clone the repository**

```bash
git clone <repo_url>
```

2. **Installing dependencies:**

```bash
pip install -r requirements.txt
```

3. **Apply migrations**

```bash
python manage.py makemigrations notetaker
```

```bash
python manage.py migrate
```

4. **Start the development server**

```bash
python manage.py runserver
```
