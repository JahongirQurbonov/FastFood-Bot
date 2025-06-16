"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"

interface OrderItem {
  id: number
  name_uz: string
  price: number
  emoji: string
  quantity: number
}

interface OrderData {
  items: OrderItem[]
  total: number
  orderNumber: number
}

export default function CheckoutPage() {
  const router = useRouter()
  const [orderData, setOrderData] = useState<OrderData | null>(null)

  useEffect(() => {
    const savedOrder = localStorage.getItem("currentOrder")
    if (savedOrder) {
      setOrderData(JSON.parse(savedOrder))
    }
  }, [])

  const handlePayment = () => {
    // Telegram to'lov tizimiga o'tish
    if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
      const tg = (window as any).Telegram.WebApp

      // Telegram Bot'ga to'lov ma'lumotlarini yuborish
      tg.sendData(
        JSON.stringify({
          action: "initiate_payment",
          order: orderData,
          amount: orderData?.total || 0,
        }),
      )

      // Telegram to'lov oynasini ochish
      tg.close()
    } else {
      // Test uchun address sahifasiga o'tish
      router.push("/address")
    }
  }

  if (!orderData) {
    return <div>Loading...</div>
  }

  const deliveryFee = orderData.total >= 25 ? 0 : 0
  const finalTotal = orderData.total + deliveryFee

  return (
    <div className="checkout-container">
      <div className="header">
        <button className="back-btn" onClick={() => router.back()}>
          ←
        </button>
        <h1>Test To'lash</h1>
        <div></div>
      </div>

      <div className="order-header">
        <div className="order-icon">🍔</div>
        <div className="order-number">Order #{orderData.orderNumber}</div>
        <div className="order-subtitle">Perfect lunch from Durger King.</div>
        <div className="restaurant-name">Durger King</div>
      </div>

      <div className="order-details">
        {orderData.items.map((item, index) => (
          <div key={index} className="order-item">
            <div className="item-info">
              <span className="item-emoji-small">{item.emoji}</span>
              <div className="item-details">
                <h4>
                  {item.name_uz} x{item.quantity}
                </h4>
              </div>
            </div>
            <div className="item-price-large">{(item.price * item.quantity).toFixed(2)} US$</div>
          </div>
        ))}

        <div className="order-item">
          <div className="item-info">
            <div className="item-details">
              <h4>Free Delivery</h4>
            </div>
          </div>
          <div className="item-price-large">{deliveryFee.toFixed(2)} US$</div>
        </div>

        <div className="total-section">
          <div className="total-row total-final">
            <span>Jami</span>
            <span>{finalTotal.toFixed(2)} US$</span>
          </div>
        </div>
      </div>

      <button className="pay-button" onClick={handlePayment}>
        {finalTotal.toFixed(2)} US$ TO'LASH
      </button>
    </div>
  )
}
