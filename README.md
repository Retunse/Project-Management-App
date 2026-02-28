# Django Trello Clone

A functional Kanban-style project management application built with Django. This project replicates core Trello features, focusing on user experience, data persistence, and real-time interaction.

## Key Features

* **User Authentication:** Secure signup and login system. Users have private access to their own boards.
* **Dynamic Boards & Lists:** Create, edit, and delete multiple boards and lists.
* **Task Management:**
    * Inline card creation for faster workflow.
    * Detailed task views with descriptions and priority levels.
    * Custom labeling system with a dedicated color picker.
* **Drag & Drop UI:** Interactive task reordering and moving between lists using SortableJS. Position and list assignments are persisted in the database via AJAX.
* **Activity Feed:** A dedicated sidebar that logs all major user actions (adding/moving tasks, renaming lists, etc.) providing a full audit trail for each board.

## Tech Stack

* **Backend:** Django (Python)
* **Frontend:** Tailwind CSS, Alpine.js
* **Database:** SQLite
* **Interactivity:** SortableJS & Fetch API



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