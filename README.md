# FastAPI CRUD with PostgreSQL and SQLAlchemy

A complete CRUD (Create, Read, Update, Delete) API built with FastAPI, using PostgreSQL database with SQLAlchemy ORM. Features intelligent gap-filling to reuse deleted IDs and sequential display options.

## 🚀 Features

- **Full CRUD Operations** - Create, Read, Update, Delete items
- **PostgreSQL Integration** - Production-ready database
- **Gap-Filling Logic** - Automatically reuses deleted IDs
- **Sequential Display** - Optional continuous numbering
- **Auto-Documentation** - Interactive API docs
- **Clean Architecture** - Separated models, schemas, and CRUD functions

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Git (for cloning)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aaditya3333/Task3--CRUD-with-FastApi-and-SQLALCHEMY.git
   cd Task3--CRUD-with-FastApi-and-SQLALCHEMY
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE your_database_name;
   ```

5. **Configure database connection**
   - Open `main.py`
   - Update the database URL:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/your_database_name"
   ```

## 🚀 Running the Application

1. **Start the server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. **Access the application**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## 📚 API Endpoints

### Standard Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/items/` | Create a new item |
| `GET` | `/items/` | List all items (sorted by ID) |
| `GET` | `/items/{id}` | Get a specific item |
| `PUT` | `/items/{id}` | Update an existing item |
| `DELETE` | `/items/{id}` | Delete an item |

### Special Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/items/sequential/` | List items with continuous display numbering |

## 📝 Request/Response Examples

### Create Item
```bash
POST /items/
Content-Type: application/json

{
    "name": "Example Item",
    "description": "This is a test item",
    "price": 100
}
```

### Response
```json
{
    "id": 1,
    "name": "Example Item",
    "description": "This is a test item",
    "price": 100
}
```

### Sequential Display Response
```json
[
    {
        "display_id": 1,
        "id": 1,
        "name": "Example Item",
        "description": "This is a test item",
        "price": 100
    },
    {
        "display_id": 2,
        "id": 3,
        "name": "Another Item",
        "description": "Description here",
        "price": 200
    }
]
```

## 🎯 Key Features Explained

### Gap-Filling Logic
When you delete an item (e.g., ID 3) and create a new item, the system automatically:
1. Finds the first available ID (3)
2. Assigns it to the new item
3. Maintains continuous ID sequence

### Sequential Display
The `/items/sequential/` endpoint provides:
- `display_id`: Continuous numbering (1, 2, 3, 4...)
- `id`: Actual database ID (may have gaps)
- Perfect for UI display purposes

## 🗄️ Database Schema

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    price INTEGER NOT NULL
);
```

## 🔧 Configuration

### Database URL Format
```python
# PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/database_name"

# Other supported databases:
# MySQL: "mysql+pymysql://user:password@localhost/dbname"
# SQLite: "sqlite:///./test.db"
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check credentials in database URL
   - Ensure database exists

2. **Module Import Errors**
   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change port: `uvicorn main:app --port 8001`

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`

---

**Built with ❤️ using FastAPI, SQLAlchemy, and PostgreSQL**
