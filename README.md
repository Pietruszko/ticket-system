## 🛠 Installation

### Backend

Clone the repository:

```bash
git clone https://github.com/Pietruszko/ticket-system.git
cd ticket-backend
```

#### Create virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Environment variables

Copy the example environment file and adjust:

```bash
cp .env.example .env
```

#### Apply migrations

```bash
python manage.py migrate
```

#### Run development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`.

#### Run tests

```bash
pytest
```

---

### Frontend

A minimal Angular frontend is included with a login view only. It connects to the backend via CORS.

To run it:

```bash
cd ticket-frontend
npm install
ng serve
```

The app will be available at `http://localhost:4200/`.

**Note**: Only the login functionality is implemented. The app expects the backend running at `http://localhost:8000/`.

---

