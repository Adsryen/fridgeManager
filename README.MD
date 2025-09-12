# 🧊 Fridge Manager

> An intelligent fridge inventory management system that helps you effectively manage food items in your refrigerator, reduce waste, and improve your quality of life!

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.2.2-green.svg)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.3.2-green.svg)](https://mongodb.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0.0-purple.svg)](https://getbootstrap.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 Core Functionality
- **📦 Item Management**: Add, edit, and delete fridge items
- **🔍 Smart Search**: Real-time search by item name
- **📅 Expiry Tracking**: Automatically identify expired and soon-to-expire items
- **🏷️ Category Management**: 12 food categories (vegetables, fruits, seafood, meat, etc.)
- **📍 Location Management**: Three storage locations (refrigerator, freezer, room temperature)
- **📊 Data Overview**: View all items at a glance

### 🎨 User Experience
- **Responsive Design**: Adapts to various screen sizes
- **Intuitive Interface**: Clean and beautiful user interface
- **Real-time Feedback**: AJAX-powered seamless operations
- **Icon Support**: Font Awesome icon library

## 🛠 Tech Stack

### Backend
- **Python 3.9+**: Primary programming language
- **Flask 2.2.2**: Web framework
- **PyMongo 4.3.2**: MongoDB driver
- **MongoDB**: NoSQL database

### Frontend
- **HTML5**: Page structure
- **CSS3**: Styling
- **JavaScript (ES6)**: Frontend logic
- **jQuery 3.6.0**: DOM manipulation
- **Bootstrap 5.0.0**: UI framework
- **Font Awesome**: Icon library
- **Moment.js**: Date handling

### Development Tools
- **Virtual Environment**: Python venv
- **Version Control**: Git

## 📁 Project Structure

```
fridgeManager/
├── app.py                 # Flask main application
├── README.MD             # Project documentation
├── web.png              # Website screenshot
├── requirements.txt      # Python dependencies
├── pytest.ini           # Pytest configuration
├── run_tests.py          # Test runner script
├── test_basic.py         # Basic test validation
├── templates/
│   └── template.html     # Main page template
├── static/
│   ├── index.js         # Frontend JavaScript
│   └── style/
│       └── index.css    # Stylesheet
├── tests/                # Test suite
│   ├── __init__.py
│   ├── conftest.py      # Pytest fixtures
│   ├── test_app.py      # Unit tests
│   ├── test_database.py # Integration tests
│   └── test_pytest.py   # Pytest tests
└── venv/                # Python virtual environment
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- MongoDB 4.0 or higher
- Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd fridgeManager
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start MongoDB**
   ```bash
   # Ensure MongoDB service is running
   mongod
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   Open your browser and visit `http://127.0.0.1:8080`

## 📖 Usage Guide

### Adding Items
1. Click the "Add Item" button
2. Fill in the item information:
   - **Name**: Item name
   - **Expiry Date**: Select expiration date
   - **Quantity**: Number of items
   - **Location**: Refrigerator/Freezer/Room temperature
   - **Category**: Select appropriate food category
3. Click "Add" to complete

### Viewing Items
- **All Items**: View all items
- **Not Expired**: View items within expiry date
- **Expired**: View expired items
- **Filter by Location**: Refrigerator/Freezer/Room temperature
- **Filter by Category**: 12 food categories
- **Search Function**: Real-time search by keyword

### Editing/Deleting Items
- Click the edit button next to an item to modify
- Click the delete button to remove items

## 🔌 API Documentation

### Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/` | Main page | - |
| POST | `/insert` | Add item | itemName, itemDate, itemPlace, itemNum, itemType |
| POST | `/search` | Search items | text |
| POST | `/stateok/<time>` | Get non-expired items | time (timestamp) |
| POST | `/statebad/<time>` | Get expired items | time (timestamp) |
| POST | `/cold` | Get refrigerated items | - |
| POST | `/frozer` | Get frozen items | - |
| POST | `/tag/<tagName>` | Get items by category | tagName |
| POST | `/total` | Get all items | - |
| POST | `/delete/<_id>` | Delete item | _id |
| POST | `/getone/<_id>` | Get single item | _id |
| POST | `/edit/<_id>` | Edit item | _id, itemName, itemDate, itemPlace, itemNum, itemType |

### Data Structure

```json
{
  "_id": "unique_id",
  "Name": "Item Name",
  "ExpireDate": "2024-12-31T00:00:00.000Z",
  "Place": "cold|frozer|room",
  "Num": 1,
  "Type": "vegetable|fruit|seafood|meat|beverage|diary|egg|bread|frozen|sauce|snack|other"
}
```

## 📸 Screenshots

![Website Outlook](./web.png)

*Fridge Manager Main Interface - Clean and intuitive design that makes food management easy and enjoyable*

## 🧪 Testing

This project includes a comprehensive testing framework:

### Test Types
- **Unit Tests**: Flask routes and individual functions
- **Integration Tests**: Database operations and API endpoints
- **Pytest Tests**: Modern testing with fixtures and mocking
- **Basic Tests**: Core functionality validation

### Running Tests
```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --type unittest
python run_tests.py --type pytest
python run_tests.py --type coverage

# Run basic validation
python test_basic.py
```

### Test Coverage
- ✅ Flask application startup and routing
- ✅ Database connection and CRUD operations
- ✅ JSON encoding with ObjectId support
- ✅ All API endpoints (insert, search, filter, delete, edit)
- ✅ Error handling and edge cases


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Educational Use**: This project was created as part of a National Central University Database Systems midterm project and is intended for educational and research purposes.

---

<div align="center">

**⭐ If this project helps you, please give it a Star!**

Made with ❤️ by hill0106

</div>