# ☕ Cafe API Site

A modern and user-friendly cafe discovery platform. Users can add, search, and filter cafes from around the world.

## 🌟 Features

- **Cafe Discovery**: Explore cafes worldwide
- **Smart Filtering**: Filter by country, location, price, and amenities
- **User Panel**: Manage your own cafes
- **REST API**: Full integrated API support
- **Responsive Design**: Mobile and desktop compatible
- **Secure Authentication**: JWT-based API key system

## 🚀 Live Demo

**Website:** [https://cafe-api-site.onrender.com](https://cafe-api-site.onrender.com)

## 🛠️ Technologies

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **API**: RESTful API with JWT Authentication
- **Deployment**: Render.com

## 📋 Requirements

### Python Packages
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Flask-WTF==1.1.1
Werkzeug==2.3.7
cryptography==41.0.4
requests==2.31.0
python-dotenv==1.0.0
email-validator==2.1.0
```

### System Requirements
- Python 3.11+
- SQLite3 (Development)
- PostgreSQL (Production - Optional)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/WATSONSK14/cafe-api-site.git
cd cafe-api-site
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create `.env` file:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
FERNET_KEY=your-fernet-key-here
DATABASE_URL=sqlite:///cafes.db
```

### 5. Run the Application
```bash
python main.py
```

The application will run at `http://localhost:5000`.

## 📚 API Documentation

### Base URL
```
https://cafe-api-site.onrender.com/v1
```

### Authentication
For endpoints requiring API key, use `X-API-KEY` header.

---

## 👤 User Operations

### User Registration
**Endpoint:** `POST /v1/users`

**API Key Required:** ❌ No

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "string (required)",
    "email": "string (required, valid email)",
    "password": "string (required, min 6 characters)"
}
```

**Response (201):**
```json
{
    "message": "User created successfully",
    "user": "Username: testuser, API-KEY: abc123def456..."
}
```

**Error Cases:**
- `400`: Invalid data
- `409`: User already exists

---

## ☕ Cafe Operations

### Add Cafe
**Endpoint:** `POST /v1/cafes/{username}`

**API Key Required:** ✅ Yes

**Headers:**
```
Content-Type: application/json
X-API-KEY: your-api-key-here
```

**Required Fields:**
- `name` (string): Cafe name
- `location` (string): Location information
- `country` (string): Country
- `coffee_price` (float): Coffee price

**Optional Fields:**
- `img_url` (string): Cafe photo URL
- `map_url` (string): Map link
- `has_wifi` (boolean): Has WiFi? (default: false)
- `has_toilet` (boolean): Has toilet? (default: false)
- `has_sockets` (boolean): Has power sockets? (default: false)
- `can_take_calls` (boolean): Can make phone calls? (default: false)

**Request Body:**
```json
{
    "name": "Starbucks Kadıköy",
    "location": "Kadıköy, İstanbul",
    "country": "Turkey",
    "coffee_price": 25.50,
    "img_url": "https://example.com/cafe.jpg",
    "map_url": "https://maps.google.com/...",
    "has_wifi": true,
    "has_toilet": true,
    "has_sockets": true,
    "can_take_calls": false
}
```

**Response (200):**
```json
{
    "message": "Cafe added successfully",
    "cafe": {
        "id": 1,
        "name": "Starbucks Kadıköy",
        "location": "Kadıköy, İstanbul",
        "country": "Turkey",
        "coffee_price": 25.50,
        "has_wifi": true,
        "has_toilet": true,
        "has_sockets": true,
        "can_take_calls": false
    }
}
```

**Error Cases:**
- `401`: Invalid API key
- `400`: Invalid data
- `404`: User not found

### List All Cafes
**Endpoint:** `GET /v1/cafes`

**API Key Required:** ❌ No

**Response (200):**
```json
{
    "cafes": [
        {
            "id": 1,
            "name": "Starbucks Kadıköy",
            "location": "Kadıköy, İstanbul",
            "country": "Turkey",
            "coffee_price": 25.50,
            "has_wifi": true,
            "has_toilet": true,
            "has_sockets": true,
            "can_take_calls": false
        }
    ]
}
```

### List User's Cafes
**Endpoint:** `GET /v1/cafes/{username}`

**API Key Required:** ✅ Yes

**Headers:**
```
X-API-KEY: your-api-key-here
```

**Response (200):**
```json
{
    "cafes": [
        {
            "id": 1,
            "name": "Starbucks Kadıköy",
            "location": "Kadıköy, İstanbul",
            "country": "Turkey",
            "coffee_price": 25.50,
            "has_wifi": true,
            "has_toilet": true,
            "has_sockets": true,
            "can_take_calls": false
        }
    ]
}
```

### Update Cafe
**Endpoint:** `PUT /v1/cafes/{username}/{cafe_id}`

**API Key Required:** ✅ Yes

**Headers:**
```
Content-Type: application/json
X-API-KEY: your-api-key-here
```

**Request Body:** (Same format as add cafe)

**Response (200):**
```json
{
    "message": "Cafe updated successfully",
    "cafe": {
        "id": 1,
        "name": "Starbucks Kadıköy Updated",
        "location": "Kadıköy, İstanbul",
        "country": "Turkey",
        "coffee_price": 30.00,
        "has_wifi": true,
        "has_toilet": true,
        "has_sockets": true,
        "can_take_calls": false
    }
}
```

### Delete Cafe
**Endpoint:** `DELETE /v1/cafes/{username}/{cafe_id}`

**API Key Required:** ✅ Yes

**Headers:**
```
X-API-KEY: your-api-key-here
```

**Response (200):**
```json
{
    "message": "Cafe deleted successfully"
}
```

---

## 🔐 API Key Management

### Getting API Key
API key is automatically generated during user registration and returned in the response.

### Using API Key
Send API key with `X-API-KEY` header for endpoints that require it:

```python
import requests

headers = {
    'X-API-KEY': 'your-api-key-here',
    'Content-Type': 'application/json'
}

response = requests.post(
    'https://cafe-api-site.onrender.com/v1/cafes/username',
    headers=headers,
    json=cafe_data
)
```

---

## 🌐 Web Interface

### Homepage
- **URL:** `/`
- **Features:** Cafe showcase, filtering, search

### User Panel
- **URL:** `/panel`
- **Features:** Statistics, API key management

### My Cafes
- **URL:** `/kafelerim`
- **Features:** Manage your own cafes

### Add Cafe
- **URL:** `/kafe-ekle`
- **Features:** Add new cafe form

---

## 🚀 Deployment

### Deploy with Render.com

1. **Push repository to GitHub**
2. **Create new Web Service on Render.com**
3. **Add Environment Variables:**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   FERNET_KEY=your-fernet-key
   ```
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `python main.py`

### Environment Variables

**Required for Production:**
- `FLASK_ENV=production`
- `SECRET_KEY`: Flask security key
- `FERNET_KEY`: API key encryption key
- `DATABASE_URL`: PostgreSQL URL (optional)

---

## 📝 Usage Examples

### Python API Usage

```python
import requests

# Base URL
BASE_URL = "https://cafe-api-site.onrender.com/v1"

# User registration
user_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

response = requests.post(f"{BASE_URL}/users", json=user_data)
print(response.json())

# Get API Key
api_key = response.json()["user"].split("API-KEY: ")[1]

# Add cafe
headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

cafe_data = {
    "name": "Test Cafe",
    "location": "Istanbul, Turkey",
    "country": "Turkey",
    "coffee_price": 25.50,
    "has_wifi": True,
    "has_toilet": True
}

response = requests.post(
    f"{BASE_URL}/cafes/testuser",
    headers=headers,
    json=cafe_data
)
print(response.json())
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Developer

**WATSONSK14**
- GitHub: [@WATSONSK14](https://github.com/WATSONSK14)
- Portfolio: [cafe-api-site.onrender.com](https://cafe-api-site.onrender.com)

---

## 🎯 Future Features

- [ ] Cafe reviews and ratings
- [ ] User profiles
- [ ] Cafe favoriting system
- [ ] Mobile application
- [ ] Real-time notifications
- [ ] Cafe photo upload
- [ ] Map integration
- [ ] Social media sharing

---

**☕ Discover and share the best cafes!**
