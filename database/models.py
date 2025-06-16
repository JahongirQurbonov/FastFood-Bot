import aiosqlite
import asyncio
from datetime import datetime
import json

class Database:
    def __init__(self, db_path: str = "fastfood.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Users table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    telegram_id INTEGER UNIQUE,
                    username TEXT,
                    full_name TEXT,
                    phone TEXT,
                    language TEXT DEFAULT 'uz',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Menu items table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    name_uz TEXT NOT NULL,
                    price REAL NOT NULL,
                    emoji TEXT,
                    category TEXT,
                    description TEXT,
                    image_url TEXT,
                    is_available BOOLEAN DEFAULT 1
                )
            """)
            
            # Orders table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    order_number TEXT UNIQUE,
                    items TEXT,
                    total_amount REAL,
                    delivery_address TEXT,
                    phone TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
                )
            """)
            
            # Cart table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    item_id INTEGER,
                    quantity INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id),
                    FOREIGN KEY (item_id) REFERENCES menu_items (id)
                )
            """)
            
            await db.commit()
            await self.populate_menu()

    async def populate_menu(self):
        menu_items = [
            ("Cake", "Tort", 4.99, "🍰", "dessert", "Mazali tort", None),
            ("Burger", "Burger", 4.99, "🍔", "main", "Klassik burger", None),
            ("Fries", "Kartoshka fri", 1.49, "🍟", "side", "Qizil kartoshka", None),
            ("Hotdog", "Xot-dog", 3.49, "🌭", "main", "Issiq sosiska", None),
            ("Taco", "Tako", 3.99, "🌮", "main", "Meksika taomi", None),
            ("Pizza", "Pitsa", 7.99, "🍕", "main", "Italyan pitsasi", None),
            ("Donut", "Donut", 1.49, "🍩", "dessert", "Shirin donut", None),
            ("Popcorn", "Popkorn", 1.99, "🍿", "snack", "Kinodagi lazzat", None),
            ("Coke", "Kola", 1.49, "🥤", "drink", "Sovuq ichimlik", None),
            ("Icecream", "Muzqaymoq", 5.99, "🍦", "dessert", "Sovuq muzqaymoq", None),
            ("Cookie", "Pechene", 3.99, "🍪", "dessert", "Shirinlik", None),
            ("Flan", "Flan", 7.99, "🍮", "dessert", "Fransuz deserti", None)
        ]
        
        async with aiosqlite.connect(self.db_path) as db:
            for item in menu_items:
                await db.execute("""
                    INSERT OR IGNORE INTO menu_items 
                    (name, name_uz, price, emoji, category, description, image_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, item)
            await db.commit()

    async def add_user(self, telegram_id: int, username: str = None, full_name: str = None):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO users (telegram_id, username, full_name)
                VALUES (?, ?, ?)
            """, (telegram_id, username, full_name))
            await db.commit()

    async def get_menu_items(self):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT id, name, name_uz, price, emoji, category, description
                FROM menu_items WHERE is_available = 1
                ORDER BY category, name
            """)
            return await cursor.fetchall()

    async def add_to_cart(self, user_id: int, item_id: int, quantity: int = 1):
        async with aiosqlite.connect(self.db_path) as db:
            # Check if item already in cart
            cursor = await db.execute("""
                SELECT quantity FROM cart WHERE user_id = ? AND item_id = ?
            """, (user_id, item_id))
            existing = await cursor.fetchone()
            
            if existing:
                await db.execute("""
                    UPDATE cart SET quantity = quantity + ? 
                    WHERE user_id = ? AND item_id = ?
                """, (quantity, user_id, item_id))
            else:
                await db.execute("""
                    INSERT INTO cart (user_id, item_id, quantity)
                    VALUES (?, ?, ?)
                """, (user_id, item_id, quantity))
            await db.commit()

    async def get_cart(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT m.name_uz, m.price, m.emoji, c.quantity, m.id
                FROM cart c
                JOIN menu_items m ON c.item_id = m.id
                WHERE c.user_id = ?
            """, (user_id,))
            return await cursor.fetchall()

    async def clear_cart(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
            await db.commit()

    async def create_order(self, user_id: int, order_data: dict):
        import random
        order_number = f"#{random.randint(100000000, 999999999)}"
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO orders (user_id, order_number, items, total_amount, 
                                  delivery_address, phone, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, order_number, json.dumps(order_data['items']),
                order_data['total'], order_data.get('address', ''),
                order_data.get('phone', ''), 'pending'
            ))
            await db.commit()
            return order_number

# Global database instance
db = Database()
