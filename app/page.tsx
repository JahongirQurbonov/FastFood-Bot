"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useCart } from "./context/CartContext"

interface MenuItem {
  id: number
  name: string
  name_uz: string
  price: number
  emoji: string
  category: string
  isNew?: boolean
  animationClass: string
}

// Narxlarni so'mga o'zgartirdik va animatsiya klasslari qo'shdik
const menuItems: MenuItem[] = [
  {
    id: 1,
    name: "Cake",
    name_uz: "Tort",
    price: 60000,
    emoji: "🍰",
    category: "dessert",
    isNew: true,
    animationClass: "animate-cake",
  },
  {
    id: 2,
    name: "Burger",
    name_uz: "Burger",
    price: 60000,
    emoji: "🍔",
    category: "main",
    animationClass: "animate-burger",
  },
  {
    id: 3,
    name: "Fries",
    name_uz: "Kartoshka fri",
    price: 18000,
    emoji: "🍟",
    category: "side",
    animationClass: "animate-fries",
  },
  {
    id: 4,
    name: "Hotdog",
    name_uz: "Xot-dog",
    price: 42000,
    emoji: "🌭",
    category: "main",
    animationClass: "animate-hotdog",
  },
  { id: 5, name: "Taco", name_uz: "Tako", price: 48000, emoji: "🌮", category: "main", animationClass: "animate-taco" },
  {
    id: 6,
    name: "Pizza",
    name_uz: "Pitsa",
    price: 96000,
    emoji: "🍕",
    category: "main",
    animationClass: "animate-pizza",
  },
  {
    id: 7,
    name: "Donut",
    name_uz: "Donut",
    price: 18000,
    emoji: "🍩",
    category: "dessert",
    animationClass: "animate-donut",
  },
  {
    id: 8,
    name: "Popcorn",
    name_uz: "Popkorn",
    price: 24000,
    emoji: "🍿",
    category: "snack",
    animationClass: "animate-popcorn",
  },
  {
    id: 9,
    name: "Coke",
    name_uz: "Kola",
    price: 18000,
    emoji: "🥤",
    category: "drink",
    animationClass: "animate-drink",
  },
  {
    id: 10,
    name: "Icecream",
    name_uz: "Muzqaymoq",
    price: 72000,
    emoji: "🍦",
    category: "dessert",
    animationClass: "animate-icecream",
  },
  {
    id: 11,
    name: "Cookie",
    name_uz: "Pechene",
    price: 48000,
    emoji: "🍪",
    category: "dessert",
    animationClass: "animate-cookie",
  },
  {
    id: 12,
    name: "Flan",
    name_uz: "Flan",
    price: 96000,
    emoji: "🍮",
    category: "dessert",
    animationClass: "animate-flan",
  },
]

export default function Page() {
  const router = useRouter()
  const { addToCart, getTotalItems } = useCart()

  const triggerAnimation = (itemId: number) => {
    const emojiElement = document.querySelector(`[data-item-id="${itemId}"] .item-emoji`)
    const item = menuItems.find((item) => item.id === itemId)

    if (emojiElement && item) {
      // Eski animatsiyani olib tashlash
      emojiElement.className = "item-emoji"

      // Yangi animatsiyani qo'shish
      setTimeout(() => {
        emojiElement.classList.add(item.animationClass)
      }, 10)

      // Animatsiyani tozalash
      setTimeout(() => {
        emojiElement.classList.remove(item.animationClass)
      }, 1000)
    }
  }

  const handleAddToCart = (item: MenuItem) => {
    // Animatsiyani ishga tushirish
    triggerAnimation(item.id)

    // Savatga qo'shish
    setTimeout(() => {
      addToCart({
        id: item.id,
        name: item.name,
        name_uz: item.name_uz,
        price: item.price,
        emoji: item.emoji,
      })
    }, 300)

    // Telegram Web App API orqali ma'lumot yuborish
    if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
      const tg = (window as any).Telegram.WebApp
      tg.HapticFeedback.impactOccurred("light")
    }
  }

  const buyNow = (item: MenuItem) => {
    // Animatsiyani ishga tushirish
    triggerAnimation(item.id)

    // Savatni tozalash va mahsulotni qo'shish
    setTimeout(() => {
      addToCart({
        id: item.id,
        name: item.name,
        name_uz: item.name_uz,
        price: item.price,
        emoji: item.emoji,
      })

      // To'g'ridan-to'g'ri savatga o'tish
      router.push("/cart")
    }, 500)
  }

  const goToCart = () => {
    router.push("/cart")
  }

  useEffect(() => {
    // Telegram Web App ni sozlash
    if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
      const tg = (window as any).Telegram.WebApp
      tg.ready()
      tg.expand()
      tg.MainButton.hide()
    }
  }, [])

  const totalItems = getTotalItems()

  // So'm formatini yaratish
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("uz-UZ").format(price) + " so'm"
  }

  return (
    <div className="container">
      <div className="header">
        <button className="back-btn">✕</button>
        <h1>Durger King</h1>
        <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
          <button className="cart-btn" onClick={goToCart}>
            🛒{totalItems > 0 && <span className="cart-badge">{totalItems}</span>}
          </button>
          <button className="back-btn">⌄</button>
          <button className="back-btn">⋮</button>
        </div>
      </div>

      <div className="menu-grid">
        {menuItems.map((item, index) => (
          <div key={item.id} className="menu-item" data-item-id={item.id} style={{ position: "relative" }}>
            {item.isNew && <span className="new-badge">NEW</span>}
            <span className="item-emoji">{item.emoji}</span>
            <div className="item-name">{item.name_uz}</div>
            <div className="item-price">{formatPrice(item.price)}</div>
            <button
              className={`item-button ${index === 0 ? "buy-btn" : "add-btn"}`}
              onClick={() => (index === 0 ? buyNow(item) : handleAddToCart(item))}
            >
              {index === 0 ? "BUY" : "ADD"}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
