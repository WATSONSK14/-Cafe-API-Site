# ☕ Cafe API Website

A full-stack web application for discovering and sharing cafes around the world. Built with Flask, SQLAlchemy, and Bootstrap.

## 🌟 Features

- **User Authentication** - Register, login, and user management
- **Cafe Management** - Add, edit, delete, and view cafes
- **Global Database** - Cafes from 5 different countries
- **Advanced Filtering** - Filter by country, location, price, and amenities
- **Search Functionality** - Find cafes by name or location
- **Responsive Design** - Mobile-friendly interface
- **REST API** - Full API endpoints for cafe data
- **Security** - CSRF protection, user permissions, encrypted API keys

## 🚀 Tech Stack

- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend:** Bootstrap 5, Custom CSS, JavaScript
- **Database:** SQLite (Development), PostgreSQL (Production)
- **Security:** Werkzeug, Cryptography (Fernet)
- **Icons:** Font Awesome

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd coffe-api-site
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV` - Environment (development/production)
- `SECRET_KEY` - Flask secret key
- `FERNET_KEY` - Encryption key for API keys
- `DATABASE_URL` - Database connection string

### Default Configuration

- **Development:** SQLite database
- **Production:** PostgreSQL database
- **Testing:** In-memory SQLite database

## 🌍 Database

The application includes a pre-populated database with:

- **25 Cafes** from 5 countries
- **5 Test Users** (test1-test5)
- **Real Data** - Actual cafe information with images and maps

### Countries Included:
- 🇬🇧 United Kingdom (London)
- 🇹🇷 Turkey (Istanbul)
- 🇮🇹 Italy (Venice, Rome, Florence, Padua, Milan)
- 🇫🇷 France (Paris)
- 🇯🇵 Japan (Tokyo)

## 🔌 API Endpoints

### User Management
- `POST /v1/users` - Create new user
- `GET /v1/users/<username>` - Get user info

### Cafe Management
- `GET /v1/cafes` - Get all cafes
- `POST /v1/cafes/<username>` - Add new cafe
- `PATCH /v1/cafes/<cafe_id>` - Update cafe
- `DELETE /v1/cafes/<cafe_id>` - Delete cafe

### Authentication
All API endpoints require `X-API-KEY` header with user's API key.

## 🎨 Frontend Features

- **Responsive Design** - Works on all devices
- **Modern UI** - Bootstrap 5 with custom styling
- **Interactive Filters** - Country, location, price, amenities
- **Search Functionality** - Real-time cafe search
- **User Dashboard** - Personal cafe management
- **Flash Messages** - User feedback and notifications

## 🚀 Deployment

### Render.com Deployment

1. **Connect GitHub repository**
2. **Set environment variables:**
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
   - `FERNET_KEY=your-fernet-key`
   - `DATABASE_URL=postgresql://...`
3. **Deploy automatically**

### Heroku Deployment

1. **Create Procfile:**
   ```
   web: python main.py
   ```
2. **Set environment variables**
3. **Deploy with Git**

## 🔒 Security Features

- **CSRF Protection** - All forms protected
- **User Authentication** - Secure login system
- **API Key Encryption** - Fernet encryption for API keys
- **Input Validation** - WTF forms with validation
- **SQL Injection Protection** - SQLAlchemy ORM

## 📱 Mobile Support

- **Responsive Design** - Mobile-first approach
- **Touch-Friendly** - Optimized for touch devices
- **Fast Loading** - Optimized images and assets

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**WATSONSK14** - Full-Stack Developer
- GitHub: [@WATSONSK14](https://github.com/WATSONSK14)
- Portfolio: [Your Portfolio](https://your-portfolio.com)

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap team for the amazing framework
- Unsplash for beautiful cafe images
- Font Awesome for the icon library

---

**Made with ❤️ and ☕**
