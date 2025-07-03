# LRU Cache with GUI, Theme Support, and Database Integration

This project is an advanced implementation of an **LRU (Least Recently Used) Cache** using **Python**, which features:
- A user-friendly **Tkinter GUI**
- **SQLite database** integration for persistent storage
- **Hit/Miss statistics tracking**
- Support for **light/dark themes**
- And an efficient **O(1) time complexity** for `get()` and `put()` operations

> Developed as an Open-Ended Lab project for the **Data Structures and Algorithms (CS-218)** course.

What is an LRU Cache?

An LRU Cache (Least Recently Used) is a data structure that stores a fixed number of key-value pairs. When it reaches capacity, it **evicts the least recently accessed item** to make room for new ones. This project efficiently implements an LRU cache using:
- A **doubly linked list** to track usage order
- A **dictionary** for O(1) lookup and updates

FEATURES OF THE PROJECT:
- `get()` and `put()` operations with **O(1)** time complexity
- Live updates and cache visualization through the GUI
- 🧪 Testing Buttons
  - **Fill Cache with 50 Keys**
  - **Retrieve Odd Keys**
  - **Put Primes from 1 to 100**
  - **Show Miss/Hit Rate**
- Highlights **MRU** (Most Recently Used) and **LRU** (Least Recently Used) items
- 🌙 Theme Support:
  - Toggle between **Light Mode** and **Dark Mode**
  - Maintains accessibility, readability, and consistent styling
- 💾 Persistent Storage (SQLite)
  - Automatically loads cache from a local SQLite database (`cache.db`)
  - Option to save the current cache state
  - Option to clear/reset the database
- 📊 Performance Monitoring and tracking
  - Total accesses
  - Hits and misses
  - Hit ratio and miss ratio

 
TECHNOLOGIES USED:
- **Python 3**
- **Tkinter** and **ttk** (GUI)
- **sqlite3** (Database)


HOW TO RUN?<br>
Option 1: Using Python Directly<br>
python lru_cache.py<br><br>

Option 2: Using Virtual Environment<br>
Create virtual environment using:<br>
python -m venv venv<br>

Activate virtual environment by:<br>
venv\Scripts\activate  # On Windows<br>
source venv/bin/activate  # On macOS/Linux<br><br>

Run the app,<br>
python lru_cache.py<br><br>

Option 3: Run with IDEs or your preferred code editors<br>

  
