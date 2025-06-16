from database.db import SessionLocal
from database.models import Order, OrderItem, Product, User as DBUser
from typing import List, Dict
import uuid

class OrderManager:
    @staticmethod
    def create_order(user_id: int, items: List[Dict], delivery_address: str, phone: str) -> Order:
        db = SessionLocal()
        try:
            # Calculate total amount
            total_amount = 0
            order_items = []
            
            for item in items:
                product = db.query(Product).filter(Product.id == item['product_id']).first()
                if product:
                    item_total = product.price * item['quantity']
                    total_amount += item_total
                    
                    order_items.append(OrderItem(
                        product_id=product.id,
                        quantity=item['quantity'],
                        price=product.price
                    ))
            
            # Create order
            order = Order(
                user_id=user_id,
                total_amount=total_amount,
                delivery_address=delivery_address,
                phone=phone,
                items=order_items
            )
            
            db.add(order)
            db.commit()
            db.refresh(order)
            
            return order
        finally:
            db.close()
    
    @staticmethod
    def get_user_orders(user_id: int) -> List[Order]:
        db = SessionLocal()
        try:
            user = db.query(DBUser).filter(DBUser.telegram_id == user_id).first()
            if user:
                return db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()
            return []
        finally:
            db.close()
    
    @staticmethod
    def update_order_status(order_id: int, status: str, payment_id: str = None):
        db = SessionLocal()
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                order.status = status
                if payment_id:
                    order.payment_id = payment_id
                db.commit()
        finally:
            db.close()
