# 🧊 Fridge Manager

> An intelligent fridge inventory management system that helps you effectively manage food items in your refrigerator, reduce waste, and improve your quality of life!

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)](https://www.sqlite.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0.0-purple.svg)](https://getbootstrap.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

English | [中文](./README.md)

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [License](#license)

## About

This project is a secondary development based on [hill0106/fridgeManager](https://github.com/hill0106/fridgeManager), adding multi-user support and user authentication system on top of the original features.

**Original Project**: hill0106/fridgeManager - Fridge Manager

**Major Improvements**:
- ✅ Multi-user support - Each user manages their own fridge independently
- ✅ User authentication system - Registration, login, password encryption
- ✅ Data isolation - Complete user data separation
- ✅ Database optimization - Changed from MongoDB to SQLite for lighter weight
- ✅ Performance improvement - Added database indexes
- ✅ Privacy protection - Database files not committed to Git

## ✨ Features

### 🎯 Core Functionality
- **👤 User System**: Registration, login, multi-user data isolation
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
- **Python 3.12+**: Primary programming language
- **Flask 3.1.0**: Web framework
- **SQLite 3**: Lightweight database (no additional installation required)

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

## 🚀 Quick Start

### Prerequisites
- Python 3.12 or higher
- Git

### Windows Users (Recommended)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Adsryen/fridgeManager.git
   cd fridgeManager
   ```

2. **One-Click Setup**
   ```bash
   # Double-click to run
   setup.bat
   ```

3. **Start Application**
   ```bash
   # Double-click to run
   start.bat
   ```

4. **Access Application**
   
   Open your browser and visit `http://127.0.0.1:8080`

### Linux/Mac Users

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Adsryen/fridgeManager.git
   cd fridgeManager
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python app.py
   ```

5. **Access Application**
   
   Open your browser and visit `http://127.0.0.1:8080`

## 📖 Usage Guide

### First Time Use
1. Visit `http://127.0.0.1:8080`
2. Click "Register" to create an account
3. Fill in username, email, password (at least 6 characters)
4. Automatically logged in after successful registration

### Adding Items
1. Click the "Add Item" button
2. Fill in item information:
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
- **Filter by Location**: Refrigerator/Freezer
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
| GET/POST | `/register` | User registration | username, email, password |
| GET/POST | `/login` | User login | username, password |
| GET | `/logout` | User logout | - |
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
  "user_id": "user_id",
  "Name": "Item Name",
  "ExpireDate": "2024-12-31T00:00:00.000Z",
  "Place": "cold|frozer|room",
  "Num": 1,
  "Type": "vegetable|fruit|seafood|meat|beverage|diary|egg|bread|frozen|sauce|snack|other"
}
```

## 📁 Project Structure

```
fridgeManager/
├── app.py                 # Flask main application
├── auth.py                # User authentication module
├── README.md              # Project documentation (Chinese)
├── README_EN.md           # Project documentation (English)
├── requirements.txt       # Python dependencies
├── setup.bat              # Windows setup script
├── start.bat              # Windows start script
├── migrate_add_user_id.py # Data migration script
├── data/                  # Database directory (not committed to Git)
├── templates/             # HTML templates
│   ├── template.html      # Main page template
│   ├── login.html         # Login page
│   └── register.html      # Registration page
├── static/                # Static resources
│   ├── index.js           # Frontend JavaScript
│   └── style/
│       └── index.css      # Stylesheet
└── tests/                 # Test suite
    ├── conftest.py        # Pytest configuration
    ├── test_app.py        # Unit tests
    └── test_database.py   # Integration tests
```

## 🧪 Testing

This project includes a comprehensive testing framework:

### Test Types
- **Unit Tests**: Flask routes and individual functions
- **Integration Tests**: Database operations and API endpoints
- **Pytest Tests**: Modern testing with fixtures and mocking

### Running Tests
```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --type unittest
python run_tests.py --type pytest
python run_tests.py --type coverage
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Educational Use**: This project is a secondary development based on a National Central University Database Systems midterm project and is intended for educational and research purposes.

**Original Project Credits**: Thanks to [hill0106](https://github.com/hill0106) for creating the original project.

---

<div align="center">

**⭐ If this project helps you, please give it a Star!**

Original Project: [hill0106/fridgeManager](https://github.com/hill0106/fridgeManager)

Secondary Development: [Adsryen](https://github.com/Adsryen)

</div>
