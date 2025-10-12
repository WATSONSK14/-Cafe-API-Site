# ☕ Kafe API Sitesi

Modern ve kullanıcı dostu bir kafe keşif platformu. Kullanıcılar kafe ekleyebilir, arayabilir ve filtreleyebilir.

## 🌟 Özellikler

- **Kafe Keşfi**: Dünya çapında kafeleri keşfedin
- **Akıllı Filtreleme**: Ülke, konum, fiyat ve özelliklere göre filtreleme
- **Kullanıcı Paneli**: Kendi kafelerinizi yönetin
- **REST API**: Tam entegre API desteği
- **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- **Güvenli Kimlik Doğrulama**: JWT tabanlı API key sistemi

## 🚀 Canlı Demo

**Site:** [https://cafe-api-site.onrender.com](https://cafe-api-site.onrender.com)

## 🛠️ Teknolojiler

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **API**: RESTful API with JWT Authentication
- **Deployment**: Render.com

## 📋 Gereksinimler

### Python Paketleri
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

### Sistem Gereksinimleri
- Python 3.11+
- SQLite3 (Development)
- PostgreSQL (Production - Opsiyonel)

## 🚀 Kurulum

### 1. Repository'yi Klonlayın
```bash
git clone https://github.com/WATSONSK14/cafe-api-site.git
cd cafe-api-site
```

### 2. Virtual Environment Oluşturun
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Dependencies Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Ayarlayın
`.env` dosyası oluşturun:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
FERNET_KEY=your-fernet-key-here
DATABASE_URL=sqlite:///cafes.db
```

### 5. Uygulamayı Çalıştırın
```bash
python main.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## 📚 API Dokümantasyonu

### Base URL
```
https://cafe-api-site.onrender.com/v1
```

### Authentication
API key gerektiren endpoint'ler için `X-API-KEY` header'ı kullanın.

---

## 👤 Kullanıcı İşlemleri

### Kullanıcı Kaydı
**Endpoint:** `POST /v1/users`

**API Key Gerekli:** ❌ Hayır

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

**Hata Durumları:**
- `400`: Geçersiz veri
- `409`: Kullanıcı zaten mevcut

---

## ☕ Kafe İşlemleri

### Kafe Ekleme
**Endpoint:** `POST /v1/cafes/{username}`

**API Key Gerekli:** ✅ Evet

**Headers:**
```
Content-Type: application/json
X-API-KEY: your-api-key-here
```

**Required Fields:**
- `name` (string): Kafe adı
- `location` (string): Konum bilgisi
- `country` (string): Ülke
- `coffee_price` (float): Kahve fiyatı

**Optional Fields:**
- `img_url` (string): Kafe fotoğrafı URL'i
- `map_url` (string): Harita linki
- `has_wifi` (boolean): WiFi var mı? (default: false)
- `has_toilet` (boolean): Tuvalet var mı? (default: false)
- `has_sockets` (boolean): Priz var mı? (default: false)
- `can_take_calls` (boolean): Telefon konuşması yapılabilir mi? (default: false)

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

**Hata Durumları:**
- `401`: Geçersiz API key
- `400`: Geçersiz veri
- `404`: Kullanıcı bulunamadı

### Tüm Kafeleri Listele
**Endpoint:** `GET /v1/cafes`

**API Key Gerekli:** ❌ Hayır

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

### Kullanıcının Kafelerini Listele
**Endpoint:** `GET /v1/cafes/{username}`

**API Key Gerekli:** ✅ Evet

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

### Kafe Güncelleme
**Endpoint:** `PUT /v1/cafes/{username}/{cafe_id}`

**API Key Gerekli:** ✅ Evet

**Headers:**
```
Content-Type: application/json
X-API-KEY: your-api-key-here
```

**Request Body:** (Kafe ekleme ile aynı format)

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

### Kafe Silme
**Endpoint:** `DELETE /v1/cafes/{username}/{cafe_id}`

**API Key Gerekli:** ✅ Evet

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

## 🔐 API Key Yönetimi

### API Key Alma
Kullanıcı kaydı sırasında otomatik olarak API key oluşturulur ve response'da döndürülür.

### API Key Kullanımı
API key gerektiren endpoint'lerde `X-API-KEY` header'ı ile gönderin:

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

## 🌐 Web Arayüzü

### Ana Sayfa
- **URL:** `/`
- **Özellikler:** Kafe showcase, filtreleme, arama

### Kullanıcı Paneli
- **URL:** `/panel`
- **Özellikler:** İstatistikler, API key yönetimi

### Kafelerim
- **URL:** `/kafelerim`
- **Özellikler:** Kendi kafelerinizi yönetin

### Kafe Ekleme
- **URL:** `/kafe-ekle`
- **Özellikler:** Yeni kafe ekleme formu

---

## 🚀 Deployment

### Render.com ile Deploy

1. **Repository'yi GitHub'a push edin**
2. **Render.com'da yeni Web Service oluşturun**
3. **Environment Variables ekleyin:**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   FERNET_KEY=your-fernet-key
   ```
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `python main.py`

### Environment Variables

**Production için gerekli:**
- `FLASK_ENV=production`
- `SECRET_KEY`: Flask güvenlik anahtarı
- `FERNET_KEY`: API key şifreleme anahtarı
- `DATABASE_URL`: PostgreSQL URL (opsiyonel)

---

## 📝 Örnek Kullanım

### Python ile API Kullanımı

```python
import requests

# Base URL
BASE_URL = "https://cafe-api-site.onrender.com/v1"

# Kullanıcı kaydı
user_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

response = requests.post(f"{BASE_URL}/users", json=user_data)
print(response.json())

# API Key al
api_key = response.json()["user"].split("API-KEY: ")[1]

# Kafe ekleme
headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

cafe_data = {
    "name": "Test Cafe",
    "location": "İstanbul, Türkiye",
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

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

## 👨‍💻 Geliştirici

**WATSONSK14**
- GitHub: [@WATSONSK14](https://github.com/WATSONSK14)
- Portfolio: [cafe-api-site.onrender.com](https://cafe-api-site.onrender.com)

---

## 🎯 Gelecek Özellikler

- [ ] Kafe yorumları ve puanlama
- [ ] Kullanıcı profilleri
- [ ] Kafe favorileme sistemi
- [ ] Mobil uygulama
- [ ] Real-time bildirimler
- [ ] Kafe fotoğraf yükleme
- [ ] Harita entegrasyonu
- [ ] Sosyal medya paylaşımı

---

**☕ En iyi kafeleri keşfedin ve paylaşın!**
