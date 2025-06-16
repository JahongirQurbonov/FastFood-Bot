from database.db import SessionLocal, create_tables
from database.models import Category, Product

def seed_database():
    create_tables()
    
    db = SessionLocal()
    try:
        # Create categories
        categories_data = [
            {"name_uz": "Asosiy taomlar", "name_ru": "Основные блюда", "name_en": "Main Dishes"},
            {"name_uz": "Ichimliklar", "name_ru": "Напитки", "name_en": "Beverages"},
            {"name_uz": "Shirinliklar", "name_ru": "Десерты", "name_en": "Desserts"}
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            categories.append(category)
        
        db.commit()
        
        # Create products
        products_data = [
            {
                "name_uz": "Burger", "name_ru": "Бургер", "name_en": "Burger",
                "description_uz": "Mazali burger", "description_ru": "Вкусный бургер", "description_en": "Delicious burger",
                "price": 25000, "emoji": "🍔", "category_id": categories[0].id
            },
            {
                "name_uz": "Pizza", "name_ru": "Пицца", "name_en": "Pizza",
                "description_uz": "Issiq pizza", "description_ru": "Горячая пицца", "description_en": "Hot pizza",
                "price": 45000, "emoji": "🍕", "category_id": categories[0].id
            },
            {
                "name_uz": "Fri", "name_ru": "Картофель фри", "name_en": "French Fries",
                "description_uz": "Qovurilgan kartoshka", "description_ru": "Жареный картофель", "description_en": "Fried potatoes",
                "price": 12000, "emoji": "🍟", "category_id": categories[0].id
            },
            {
                "name_uz": "Kola", "name_ru": "Кола", "name_en": "Cola",
                "description_uz": "Sovuq kola", "description_ru": "Холодная кола", "description_en": "Cold cola",
                "price": 8000, "emoji": "🥤", "category_id": categories[1].id
            },
            {
                "name_uz": "Tort", "name_ru": "Торт", "name_en": "Cake",
                "description_uz": "Shirin tort", "description_ru": "Сладкий торт", "description_en": "Sweet cake",
                "price": 15000, "emoji": "🍰", "category_id": categories[2].id, "is_new": True
            }
        ]
        
        for prod_data in products_data:
            product = Product(**prod_data)
            db.add(product)
        
        db.commit()
        print("Database seeded successfully!")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
