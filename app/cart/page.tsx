"use client"

import { useRouter } from "next/navigation"
import { useCart } from "../context/CartContext"
import { useEffect } from "react"

export default function CartPage() {
  const router = useRouter()
  const { items, updateQuantity, removeFromCart, clearCart, getTotalPrice } = useCart()

  const totalPrice = getTotalPrice()
  const deliveryFee = totalPrice >= 300000 ? 0 : 35000 // 300,000 so'mdan yuqori bo'lsa bepul
  const finalTotal = totalPrice + deliveryFee

  // So'm formatini yaratish
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("uz-UZ").format(price) + " so'm"
  }

  const handleCheckout = () => {
    if (items.length === 0) {
      return
    }

    // Telegram to'lov tizimiga ma'lumotlarni yuborish
    if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
      const tg = (window as any).Telegram.WebApp

      // Buyurtma ma'lumotlarini tayyorlash
      const orderData = {
        items: items,
        subtotal: totalPrice,
        delivery: deliveryFee,
        total: finalTotal,
        orderNumber: Math.floor(Math.random() * 1000000000),
      }

      // Telegram Bot'ga to'lov so'rovini yuborish
      tg.sendData(
        JSON.stringify({
          action: "initiate_payment",
          order: orderData,
        }),
      )

      // Telegram to'lov oynasini ochish uchun bot'ga signal
      tg.close()
    } else {
      // Agar Telegram Web App bo'lmasa, oddiy alert
      alert("Bu funksiya faqat Telegram Bot ichida ishlaydi!")
    }
  }

  useEffect(() => {
    // Telegram Web App sozlamalari
    if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
      const tg = (window as any).Telegram.WebApp

      if (items.length > 0) {
        tg.MainButton.setText(`${formatPrice(finalTotal)} TO'LASH`)
        tg.MainButton.show()
        tg.MainButton.onClick(handleCheckout)
      } else {
        tg.MainButton.hide()
      }

      return () => {
        tg.MainButton.offClick(handleCheckout)
      }
    }
  }, [items, finalTotal])

  if (items.length === 0) {
    return (
      <div className="container">
        <div className="header">
          <button className="back-btn" onClick={() => router.back()}>
            ←
          </button>
          <h1>Savat</h1>
          <div></div>
        </div>

        <div className="empty-cart">
          <div className="empty-cart-icon">🛒</div>
          <h2>Savat bo'sh</h2>
          <p>Mahsulot qo'shish uchun menyuga o'ting</p>
          <button className="menu-btn" onClick={() => router.push("/")}>
            Menyuga o'tish
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="header">
        <button className="back-btn" onClick={() => router.back()}>
          ←
        </button>
        <h1>Savat</h1>
        <button className="clear-btn" onClick={clearCart}>
          🗑
        </button>
      </div>

      <div className="cart-content">
        <div className="cart-items">
          {items.map((item) => (
            <div key={item.id} className="cart-item">
              <div className="item-info">
                <span className="item-emoji-large">{item.emoji}</span>
                <div className="item-details">
                  <h3>{item.name_uz}</h3>
                  <p className="item-price">{formatPrice(item.price)}</p>
                </div>
              </div>

              <div className="quantity-controls">
                <button className="quantity-btn" onClick={() => updateQuantity(item.id, item.quantity - 1)}>
                  −
                </button>
                <span className="quantity">{item.quantity}</span>
                <button className="quantity-btn" onClick={() => updateQuantity(item.id, item.quantity + 1)}>
                  +
                </button>
              </div>

              <div className="item-total">{formatPrice(item.price * item.quantity)}</div>

              <button className="remove-btn" onClick={() => removeFromCart(item.id)}>
                ✕
              </button>
            </div>
          ))}
        </div>

        <div className="cart-summary">
          <div className="summary-row">
            <span>Mahsulotlar:</span>
            <span>{formatPrice(totalPrice)}</span>
          </div>
          <div className="summary-row">
            <span>Yetkazib berish:</span>
            <span>{formatPrice(deliveryFee)}</span>
          </div>
          <div className="summary-row total">
            <span>Jami:</span>
            <span>{formatPrice(finalTotal)}</span>
          </div>
        </div>

        <button className="checkout-btn" onClick={handleCheckout}>
          {formatPrice(finalTotal)} TO'LASH
        </button>
      </div>
    </div>
  )
}
