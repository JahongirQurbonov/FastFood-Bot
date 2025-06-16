"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"

interface MenuItem {
  id: number
  name: string
  name_uz: string
  price: number
  emoji: string
  category: string
  isNew?: boolean
}

const menuItems: MenuItem[] = [
  { id: 1, name: "Cake", name_uz: "Cake", price: 4.99, emoji: "🍰", category: "dessert", isNew: true },
  { id: 2, name: "Burger", name_uz: "Burger", price: 4.99, emoji: "🍔", category: "main" },
  { id: 3, name: "Fries", name_uz: "Fries", price: 1.49, emoji: "🍟", category: "side" },
  { id: 4, name: "Hotdog", name_uz: "Hotdog", price: 3.49, emoji: "🌭", category: "main" },
  { id: 5, name: "Taco", name_uz: "Taco", price: 3.99, emoji: "🌮", category: "main" },
  { id: 6, name: "Pizza", name_uz: "Pizza", price: 7.99, emoji: "🍕", category: "main" },
  { id: 7, name: "Donut", name_uz: "Donut", price: 1.49, emoji: "🍩", category: "dessert" },
  { id: 8, name: "Popcorn", name_uz: "Popcorn", price: 1.99, emoji: "🍿", category: "snack" },
  { id: 9, name: "Coke", name_uz: "Coke", price: 1.49, emoji: "🥤", category: "drink" },
  { id: 10, name: "Icecream", name_uz: "Icecream", price: 5.99, emoji: "🍦", category: "dessert" },
  { id: 11, name: "Cookie", name_uz: "Cookie", price: 3.99, emoji: "🍪", category: "dessert" },
  { id: 12, name: "Flan", name_uz: "Flan", price: 7.99, emoji: "🍮", category: "dessert" },
]

export default function MenuPage() {
  const router = useRouter()
  const [cart, setCart] = useState<{ [key: number]: number }>({})

  const addToCart = (itemId: number) => {
    setCart((prev) => ({
      ...prev,
      [itemId]: (prev[itemId] || 0) + 1,
    }))

    // Telegram Web App API orqali ma'lumot yuborish
    if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
      const tg = (window as any).Telegram.WebApp
      tg.sendData(
        JSON.stringify({
          action: "add_to_cart",
          item_id: itemId,
          cart: cart,
        }),
      )
    }
  }

  const buyNow = (item: MenuItem) => {
    // To'g'ridan-to'g'ri checkout sahifasiga o'tish
    const orderData = {
      items: [{ ...item, quantity: 1 }],
      total: item.price,
      orderNumber: Math.floor(Math.random() * 1000000000),
    }

    localStorage.setItem("currentOrder", JSON.stringify(orderData))
    router.push("/checkout")
  }

  useEffect(() => {
    // Telegram Web App ni sozlash
    if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
      const tg = (window as any).Telegram.WebApp
      tg.ready()
      tg.expand()
    }
  }, [])

  return (
    <div className="container">
      <div className="header">
        <button className="back-btn">✕</button>
        <h1>Durger King</h1>
        <div style={{ display: "flex", gap: "10px" }}>
          <button className="back-btn">⌄</button>
          <button className="back-btn">⋮</button>
        </div>
      </div>

      <div className="menu-grid">
        {menuItems.map((item, index) => (
          <div key={item.id} className="menu-item" style={{ position: "relative" }}>
            {item.isNew && <span className="new-badge">NEW</span>}
            <span className="item-emoji">{item.emoji}</span>
            <div className="item-name">{item.name_uz}</div>
            <div className="item-price">${item.price}</div>
            <button
              className={`item-button ${index === 0 ? "buy-btn" : "add-btn"}`}
              onClick={() => (index === 0 ? buyNow(item) : addToCart(item.id))}
            >
              {index === 0 ? "BUY" : "ADD"}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
