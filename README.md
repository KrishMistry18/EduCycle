# 🎓 EduCycle - Student Marketplace Platform

A full-stack e-commerce platform built with Django REST Framework, featuring real-time communication, advanced search, and modern authentication. Designed for students to buy, sell, and exchange academic and hostel essentials within their campus community.

## ✨ **Key Features**

### 🔐 **Advanced Authentication & Security**
- **JWT Token Authentication** - Secure stateless authentication
- **OAuth2 Integration** - Google, GitHub login support
- **Two-Factor Authentication (2FA)** - SMS/Email verification
- **Rate Limiting** - Protection against brute force attacks
- **CSRF Protection** - Enhanced security headers
- **Password Strength Validation** - Real-time password strength meter

### 🔍 **Smart Search & Discovery**
- **Advanced Search** - Multi-field search with filters
- **Real-time Suggestions** - AI-powered autocomplete
- **Category Filtering** - Filter by item categories
- **Price Range Filtering** - Filter by price range
- **Search Analytics** - Track popular searches
- **Saved Searches** - Users can save search criteria

### 💬 **Real-time Communication**
- **WebSocket Integration** - Real-time chat between users
- **Live Notifications** - Instant message notifications
- **Online Status** - Show when sellers are online
- **Message Threading** - Organized conversations
- **File Sharing** - Share images in messages

### 🛒 **E-commerce Features**
- **Shopping Cart** - Add/remove items with quantity
- **Order Management** - Complete order lifecycle
- **Payment Integration** - Stripe payment processing
- **Escrow System** - Secure transactions
- **Order Tracking** - Real-time order status

### 📱 **Modern UI/UX**
- **Responsive Design** - Mobile-first approach
- **Dark Mode** - Toggle between light/dark themes
- **Progressive Web App (PWA)** - Offline functionality
- **Interactive Maps** - Show item locations
- **Image Gallery** - Multiple image support with zoom
- **Infinite Scroll** - Smooth pagination

### 📊 **Analytics & Insights**
- **User Analytics** - Track user behavior
- **Sales Analytics** - Revenue tracking and trends
- **Search Analytics** - Popular search terms
- **Performance Monitoring** - Real-time metrics
- **Admin Dashboard** - Comprehensive analytics panel

## 🛠 **Technology Stack**

### **Backend**
- **Django 5.2** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **Celery** - Background task processing
- **Elasticsearch** - Advanced search engine

### **Frontend**
- **React.js** - Modern frontend framework
- **Material-UI** - Professional component library
- **WebSocket** - Real-time communication
- **PWA** - Progressive web app features

### **DevOps & Deployment**
- **Docker** - Containerization
- **Docker Compose** - Multi-service orchestration
- **Nginx** - Reverse proxy and load balancer
- **Gunicorn** - WSGI server
- **AWS/Azure** - Cloud deployment ready

### **Security & Monitoring**
- **JWT Authentication** - Stateless authentication
- **OAuth2** - Third-party authentication
- **Rate Limiting** - API protection
- **HTTPS/SSL** - Secure communication
- **Security Headers** - XSS, CSRF protection

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (optional, SQLite for development)

### **Option 1: Docker (Recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/edicycle.git
cd edicycle

# Start all services
docker-compose up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
open http://localhost:8000
```

### **Option 2: Local Development**

```bash
# Clone the repository
git clone https://github.com/yourusername/edicycle.git
cd edicycle

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## 📚 **API Documentation**

### **Authentication**
```bash
# Get JWT token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token in requests
curl -H "Authorization: Bearer <your_token>" \
  http://localhost:8000/api/items/
```

### **Key Endpoints**
- `GET /api/items/` - List all items
- `POST /api/items/` - Create new item
- `GET /api/items/search/` - Advanced search
- `GET /api/profile/` - User profile
- `GET /api/my-cart/` - User's cart
- `POST /api/messages/` - Send message

## 🏗 **Architecture**

### **Database Schema**
```
User (Django Auth)
├── Item (Products)
│   ├── CartItem (Shopping Cart)
│   ├── OrderItem (Orders)
│   └── Message (Communication)
├── Cart (Shopping Cart)
├── Order (Orders)
└── Message (Communication)
```

### **Service Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │   Django App    │    │   PostgreSQL    │
│   (Port 80)     │◄──►│   (Port 8000)   │◄──►│   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐             │
         │              │     Redis       │             │
         │              │   (Port 6379)   │             │
         │              └─────────────────┘             │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Static Files  │    │   Cache/Session │    │   Data Storage  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📈 **Performance Metrics**

- **Response Time**: < 200ms average
- **Database Queries**: Optimized with select_related/prefetch_related
- **Caching**: Redis-based caching for frequently accessed data
- **Image Optimization**: Automatic image compression and resizing
- **CDN Ready**: Static files served via CDN

## 🔒 **Security Features**

- **JWT Authentication** - Secure token-based auth
- **Rate Limiting** - API protection (10 req/s for API, 5 req/min for login)
- **CSRF Protection** - Cross-site request forgery protection
- **XSS Protection** - Content Security Policy headers
- **SQL Injection Protection** - Django ORM protection
- **File Upload Security** - Validated file uploads
- **HTTPS Ready** - SSL/TLS encryption support

## 🧪 **Testing**

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report

# Run specific test
python manage.py test hub.tests.test_views
```

## 📊 **Monitoring & Analytics**

### **Application Metrics**
- Request/Response times
- Database query performance
- Memory usage
- Error rates

### **Business Metrics**
- User registration/engagement
- Item listing/sales
- Search patterns
- Revenue tracking

## 🚀 **Deployment**

### **Production Checklist**
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL certificates
- [ ] Configure database for production
- [ ] Set up monitoring and logging
- [ ] Configure backup system

### **AWS Deployment**
```bash
# Build Docker image
docker build -t edicycle .

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag edicycle:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/edicycle:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/edicycle:latest
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Django community for the excellent framework
- Django REST Framework for API development
- Material-UI for the beautiful components
- All contributors and testers

---

## 👤 Author
Built with ❤️ by Krish Mistry
- Email: mistrykrish2005@gmail.com
- GitHub: https://github.com/KrishMistry18
- LinkedIn: https://www.linkedin.com/in/krishmistry18
---

**Built with ❤️ by Krish Mistry** 
