# 🧊 冰箱管理大師 (Fridge Manager)

> 一個智能的冰箱物品管理系統，幫助你有效管理冰箱中的食物，減少浪費，提高生活品質！

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.2.2-green.svg)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.3.2-green.svg)](https://mongodb.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0.0-purple.svg)](https://getbootstrap.com)

## 📋 目錄

- [功能特色](#-功能特色)
- [技術棧](#-技術棧)
- [專案結構](#-專案結構)
- [安裝與運行](#-安裝與運行)
- [使用說明](#-使用說明)
- [API 文檔](#-api-文檔)
- [截圖展示](#-截圖展示)
- [開發者](#-開發者)
- [授權](#-授權)

## ✨ 功能特色

### 🎯 核心功能
- **📦 物品管理**: 新增、編輯、刪除冰箱物品
- **🔍 智能搜索**: 即時搜索物品名稱
- **📅 到期提醒**: 自動識別過期和即將過期的物品
- **🏷️ 分類管理**: 12種食物分類（蔬菜、水果、海鮮、肉類等）
- **📍 位置管理**: 冷藏、冷凍、室溫三種儲存位置
- **📊 數據統計**: 查看所有物品總覽

### 🎨 用戶體驗
- **響應式設計**: 適配各種螢幕尺寸
- **直觀界面**: 簡潔美觀的用戶界面
- **即時反饋**: AJAX 無刷新操作
- **圖標支持**: Font Awesome 圖標庫

## 🛠 技術棧

### 後端
- **Python 3.9+**: 主要程式語言
- **Flask 2.2.2**: Web 框架
- **PyMongo 4.3.2**: MongoDB 驅動
- **MongoDB**: NoSQL 資料庫

### 前端
- **HTML5**: 頁面結構
- **CSS3**: 樣式設計
- **JavaScript (ES6)**: 前端邏輯
- **jQuery 3.6.0**: DOM 操作
- **Bootstrap 5.0.0**: UI 框架
- **Font Awesome**: 圖標庫
- **Moment.js**: 日期處理

### 開發工具
- **虛擬環境**: Python venv
- **版本控制**: Git

## 📁 專案結構

```
fridgeManager/
├── app.py                 # Flask 主應用程式
├── README.MD             # 專案說明文檔
├── web.png              # 網站截圖
├── templates/
│   └── template.html     # 主頁面模板
├── static/
│   ├── index.js         # 前端 JavaScript
│   └── style/
│       └── index.css    # 樣式表
└── venv/                # Python 虛擬環境
```

## 🚀 安裝與運行

### 環境要求
- Python 3.9 或更高版本
- MongoDB 4.0 或更高版本
- Git

### 安裝步驟

1. **克隆專案**
   ```bash
   git clone <repository-url>
   cd fridgeManager
   ```

2. **創建虛擬環境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **安裝依賴**
   ```bash
   pip install flask pymongo flask-pymongo
   ```

4. **啟動 MongoDB**
   ```bash
   # 確保 MongoDB 服務正在運行
   mongod
   ```

5. **運行應用程式**
   ```bash
   python app.py
   ```

6. **訪問應用程式**
   打開瀏覽器訪問 `http://127.0.0.1:8080`

## 📖 使用說明

### 新增物品
1. 點擊「新增商品」按鈕
2. 填寫物品資訊：
   - 名稱：物品名稱
   - 到期日：選擇到期日期
   - 數量：物品數量
   - 位置：冷藏/冷凍/室溫
   - 類別：選擇對應的食物類別
3. 點擊「新增」完成

### 查看物品
- **全部商品**: 查看所有物品
- **尚在保存期限**: 查看未過期物品
- **已過期**: 查看已過期物品
- **按位置篩選**: 冷藏/冷凍/室溫
- **按類別篩選**: 12種食物分類
- **搜索功能**: 輸入關鍵字即時搜索

### 編輯/刪除物品
- 點擊物品旁的編輯按鈕進行修改
- 點擊刪除按鈕移除物品

## 🔌 API 文檔

### 端點列表

| 方法 | 端點 | 描述 | 參數 |
|------|------|------|------|
| GET | `/` | 主頁面 | - |
| POST | `/insert` | 新增物品 | itemName, itemDate, itemPlace, itemNum, itemType |
| POST | `/search` | 搜索物品 | text |
| POST | `/stateok/<time>` | 獲取未過期物品 | time (timestamp) |
| POST | `/statebad/<time>` | 獲取已過期物品 | time (timestamp) |
| POST | `/cold` | 獲取冷藏物品 | - |
| POST | `/frozer` | 獲取冷凍物品 | - |
| POST | `/tag/<tagName>` | 按類別獲取物品 | tagName |
| POST | `/total` | 獲取所有物品 | - |
| POST | `/delete/<_id>` | 刪除物品 | _id |
| POST | `/getone/<_id>` | 獲取單個物品 | _id |
| POST | `/edit/<_id>` | 編輯物品 | _id, itemName, itemDate, itemPlace, itemNum, itemType |

### 數據結構

```json
{
  "_id": "unique_id",
  "Name": "物品名稱",
  "ExpireDate": "2024-12-31T00:00:00.000Z",
  "Place": "cold|frozer|room",
  "Num": 1,
  "Type": "vegetable|fruit|seafood|meat|beverage|diary|egg|bread|frozen|sauce|snack|other"
}
```

## 📸 截圖展示

![Website Outlook](./web.png)

*冰箱管理大師主界面 - 簡潔直觀的設計，讓食物管理變得輕鬆愉快*

## 👨‍💻 開發者

**Alex87** - 國立中央大學資料庫系統期中專案

## 📄 授權

此專案僅供學習和研究使用。

---

<div align="center">

**⭐ 如果這個專案對你有幫助，請給個 Star！**

Made with ❤️ by Alex87

</div>