1. **Clone the repository:**
    ```bash
    git clone https://github.com/PhucNgo5903/SoiDayGanKet.git
    cd SoiDayGanKet
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install the required packages:**
   ```bash
    pip install -r requirements.txt
   ```
   
5. **Run database migrations:**
    ```bash
    python manage.py migrate app
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Start the development server:**
    ```bash
    python manage.py runserver
    ```
