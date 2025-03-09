1. **Clone the repository:**
    ```bash
    git clone 
    cd SoiDayGanKet
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required packages:**
   ```bash
    pip install django
   ```
   
5. **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Start the development server:**
    ```bash
    python manage.py runserver
    ```
