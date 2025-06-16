"use client"
import { motion } from "framer-motion"

const Cart = ({ cart, lang, onUpdateItem, onBack, onOrder, formatPrice, getText, getTotalAmount }) => {
  const getBackText = () => {
    const texts = {
      uz: "Orqaga",
      ru: "Назад",
      en: "Back",
    }
    return texts[lang] || "Back"
  }

  const getEmptyCartText = () => {
    const texts = {
      uz: "Savat bo'sh",
      ru: "Корзина пуста",
      en: "Cart is empty",
    }
    return texts[lang] || "Cart is empty"
  }

  if (cart.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, x: 100 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -100 }}
        className="cart-view"
      >
        <div className="cart-header">
          <button className="back-button" onClick={onBack}>
            ← {getBackText()}
          </button>
          <h2>{getText("cart")}</h2>
        </div>

        <div className="empty-cart">
          <div className="empty-cart-icon">🛒</div>
          <p>{getEmptyCartText()}</p>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="cart-view"
    >
      <div className="cart-header">
        <button className="back-button" onClick={onBack}>
          ← {getBackText()}
        </button>
        <h2>{getText("cart")}</h2>
      </div>

      <div className="cart-items">
        {cart.map((item) => (
          <div key={item.id} className="cart-item">
            <div className="item-info">
              <span className="item-emoji">{item.emoji}</span>
              <div>
                <h4>{item.name[lang]}</h4>
                <p>
                  {formatPrice(item.price)} {getText("sum")}
                </p>
              </div>
            </div>

            <div className="quantity-controls">
              <button onClick={() => onUpdateItem(item.id, item.quantity - 1)} className="quantity-btn">
                -
              </button>
              <span className="quantity">{item.quantity}</span>
              <button onClick={() => onUpdateItem(item.id, item.quantity + 1)} className="quantity-btn">
                +
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="cart-footer">
        <div className="total">
          {getText("total")}: {formatPrice(getTotalAmount())} {getText("sum")}
        </div>
        <button className="order-button" onClick={onOrder}>
          {getText("order")}
        </button>
      </div>
    </motion.div>
  )
}

export default Cart
