<div align="center">

# ♻️ EduCycle

### Student Marketplace Platform

[![Live Demo](https://img.shields.io/badge/🔗%20Live%20Demo-edu--cycle.vercel.app-blue?style=for-the-badge)](https://edu-cycle-five.vercel.app/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*Buy, sell, and swap textbooks, lab equipment, and academic essentials — within your campus community.*

</div>

---

## Features

- **Marketplace** — Browse, search, and filter items by category and price
- **Sell Items** — List items with images, description, and asking price
- **Shopping Cart** — Add items and check out in one flow
- **Order Management** — Track purchases and sales history
- **Messaging** — Contact sellers directly from any listing
- **AI Chatbot** — Built-in assistant for platform help and item discovery
- **Authentication** — Register, login, JWT API support
- **User Profiles** — Manage your listings and order history
- **Payments** — Stripe + Razorpay + Cash on Delivery
- **Notifications** — Real-time alerts for orders and messages
- **Reviews** — Rate and review items after purchase
- **Dark Mode** — Toggle between light and dark themes
- **Responsive** — Fully functional on mobile and desktop

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2, Django REST Framework |
| Database | Supabase (PostgreSQL) / Firebase Realtime DB |
| Media Storage | Firebase Storage (GCP) |
| Auth | JWT (djangorestframework-simplejwt) |
| Payments | Stripe + Razorpay |
| Static Files | WhiteNoise |
| Deployment | Vercel |

---

## Getting Started

### Prerequisites

- Python 3.11+

### 1. Clone the repository

```bash
git clone https://github.com/KrishMistry18/EduCycle.git
cd EduCycle
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your values
```

For local development, leave `DATABASE_URL` empty — the app uses SQLite automatically.

### 4. Run migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Project Structure

```
EduCycle/
├── EduCycle/               # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py             # Auto-migrates on first request
├── hub/                    # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── api_views.py        # REST API viewsets
│   ├── serializers.py
│   ├── chatbot.py          # AI assistant logic
│   ├── payment_views.py    # Stripe / Razorpay handlers
│   └── templates/hub/      # HTML templates
├── media/                  # Uploaded item images
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── vercel.json
```

---

## Deploy to Vercel

### 1. Set up Supabase

Go to [supabase.com](https://supabase.com) → New Project → **Settings → Database → URI** and copy your connection string.

### 2. Import to Vercel

Import `KrishMistry18/EduCycle` into a new Vercel project. Vercel auto-detects Django ✅

### 3. Add environment variables

| Key | Value |
|---|---|
| `SECRET_KEY` | A long random string (50+ chars) |
| `DEBUG` | `False` |
| `DATABASE_URL` | Your Supabase connection string |
| `USE_FIREBASE_STORAGE` | `True` |
| `FIREBASE_CREDENTIALS_JSON` | Minified JSON string of your Firebase Service Account key |

### 4. Deploy

Click **Deploy**. Vercel installs dependencies, starts the WSGI app, and auto-runs migrations on first request.

---

## API Endpoints

Base URL: `/api/`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/token/` | Get JWT token |
| `POST` | `/api/token/refresh/` | Refresh JWT token |
| `GET` | `/api/items/` | List all items |
| `POST` | `/api/items/` | Create item |
| `GET` | `/api/items/{id}/` | Item details |
| `GET` | `/api/items/?search=query` | Search items |
| `GET` | `/api/my-cart/` | Get cart |
| `POST` | `/api/cart/checkout/` | Place order |
| `GET` | `/api/orders/` | List orders |
| `GET` | `/api/notifications/` | Get notifications |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: add your feature"`
4. Push and open a Pull Request

---

## License

MIT — see `LICENSE` for details.

---

<div align="center">

*Built with ❤️ for students, by a student — [Krish Mistry](https://github.com/KrishMistry18)*

</div>
