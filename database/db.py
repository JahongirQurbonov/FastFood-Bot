import sqlite3
import logging
from typing import Optional, List, Dict, Any
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "fastfood_bot.db"):
        self.db_path = db_path
        
    def get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[tuple]]:
        """Execute a query and return results."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Database error: {e}")
            return None

def create_tables():
    """Create all necessary database tables."""
    db = Database()
    
    # Users table
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language_code TEXT DEFAULT 'uz',
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Orders table
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            items TEXT NOT NULL,
            total_amount INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            payment_status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    
    # Menu items table
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT,
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert default menu items
    insert_default_menu_items()
    
    logger.info("Database tables created successfully!")

def insert_default_menu_items():
    """Insert default menu items."""
    db = Database()
    
    # Check if menu items already exist
    existing = db.execute_query("SELECT COUNT(*) FROM menu_items")
    if existing and existing[0][0] > 0:
        return
    
    default_items = [
        ("Big Burger", "Katta burger go'sht, pomidor, salat va maxsus sous bilan", 25000, "Burgerlar", "🍔"),
        ("Cheese Burger", "Pishloqli burger go'sht va pishloq bilan", 22000, "Burgerlar", "🍔"),
        ("Chicken Burger", "Tovuq go'shti bilan burger", 20000, "Burgerlar", "🍔"),
        ("Pizza Margherita", "Klassik pizza pomidor va pishloq bilan", 35000, "Pizzalar", "🍕"),
        ("Pepperoni Pizza", "Pizza pepperoni va pishloq bilan", 40000, "Pizzalar", "🍕"),
        ("Vegetarian Pizza", "Sabzavotli pizza", 32000, "Pizzalar", "🍕"),
        ("French Fries", "Qizil kartoshka fri", 12000, "Garnirlar", "🍟"),
        ("Onion Rings", "Piyoz halqalari", 10000, "Garnirlar", "🧅"),
        ("Coca Cola", "Sovuq ichimlik 0.5L", 8000, "Ichimliklar", "🥤"),
        ("Pepsi", "Sovuq ichimlik 0.5L", 8000, "Ichimliklar", "🥤"),
        ("Orange Juice", "Apelsin sharbati", 12000, "Ichimliklar", "🧃"),
    ]
    
    for item in default_items:
        db.execute_query("""
            INSERT INTO menu_items (name, description, price, category, image_url)
            VALUES (?, ?, ?, ?, ?)
        """, item)
    
    logger.info("Default menu items inserted!")

class OrderManager:
    def __init__(self):
        self.db = Database()
    
    def save_order(self, user_id: int, user_name: str, phone: str, 
                   address: str, items: List[Dict], total_amount: int) -> int:
        """Save new order to database."""
        result = self.db.execute_query("""
            INSERT INTO orders (user_id, user_name, phone, address, items, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, user_name, phone, address, json.dumps(items), total_amount))
        
        # Get the last inserted order ID
        order_result = self.db.execute_query(
            "SELECT id FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (user_id,)
        )
        order_id = order_result[0][0] if order_result else 0
        
        logger.info(f"Order {order_id} saved for user {user_id}")
        return order_id
    
    def get_orders(self, status: Optional[str] = None) -> List[tuple]:
        """Get orders from database."""
        if status:
            return self.db.execute_query(
                "SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC", 
                (status,)
            ) or []
        return self.db.execute_query("SELECT * FROM orders ORDER BY created_at DESC") or []
    
    def update_order_status(self, order_id: int, status: str):
        """Update order status."""
        self.db.execute_query(
            "UPDATE orders SET status = ? WHERE id = ?", 
            (status, order_id)
        )
        logger.info(f"Order {order_id} status updated to {status}")
    
    def get_order_by_id(self, order_id: int) -> Optional[tuple]:
        """Get order by ID."""
        result = self.db.execute_query("SELECT * FROM orders WHERE id = ?", (order_id,))
        return result[0] if result else None

class UserManager:
    def __init__(self):
        self.db = Database()
    
    def save_user(self, user_id: int, username: str = None, first_name: str = None, 
                  last_name: str = None, language_code: str = 'uz'):
        """Save or update user in database."""
        try:
            self.db.execute_query("""
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, last_name, language_code)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, language_code))
        except Exception as e:
            logger.error(f"Error saving user {user_id}: {e}")
    
    def get_user(self, user_id: int) -> Optional[tuple]:
        """Get user by ID."""
        result = self.db.execute_query("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return result[0] if result else None