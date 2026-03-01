# Django Trello Clone
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Alpine.js](https://img.shields.io/badge/alpine.js-%238BC0D0.svg?style=for-the-badge&logo=alpine.js&logoColor=white) 
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) 
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

A functional Kanban-style project management application built with Django. This project replicates core Trello features, focusing on user experience, data persistence, and real-time interaction.

## Key Features

### Board & Task Management
* **Dynamic Kanban Boards:** Create multiple boards with customizable lists.
* **Interactive Drag & Drop:** Move tasks between lists and reorder lists using **SortableJS** with instant database persistence via AJAX.
* **Task Details:** Rich task cards with descriptions, checklists, and priority levels.
* **Soft Delete (Archive):** Archive tasks instead of permanent deletion to prevent data loss, with a dedicated Archive View for restoration.

### xCollaboration & Permissions
* **Member Invitations:** Board owners can invite other registered users to collaborate.
* **Role-Based Access:** Granular permissions ensure only authorized members can edit tasks or manage labels.
* **Activity Logging:** Track changes (edits, moves, comments) to keep the team informed.

### Advanced UX & UI
* **Real-time Search:** Instant task filtering by title using **Alpine.js** (zero-latency).
* **Label System:** Create custom color-coded labels to categorize tasks.
* **Priority Indicators:** Visual cues (pulses) for high-priority tasks.
* **Smart Counters:** List task counts update dynamically as cards are moved.

##  Technical Stack
* **Backend:** Django (Python) - Custom User models, Signals for activity logging, and QuerySet optimization.
* **Frontend:** Tailwind CSS (Modern, responsive UI), Alpine.js (Lightweight reactivity).
* **Database:** PostgreSQL (Production) / SQLite (Development).
* **Interactions:** SortableJS for smooth drag-and-drop UX.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Retunse/Project-Management-App.git
   cd trello-clone
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install dependencies**
    ```bash
   Install dependencies
   ```
4. **Run migrations**
    ```bash
   python manage.py makemigrations
   python manage.py migrate
    ```
5. **Start the development server**
    ```bash
   python manage.py runserver
   ```
   
## Project Structure

* **models.py**: Core logic for Boards, Lists, Tasks, Labels, and ActivityLogs.

* **views.py**: Business logic, including custom AJAX endpoints for drag-and-drop persistence.

* **templates/**: Responsive UI built with Tailwind CSS and Alpine.js.