"use client"

import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import ProductCard from "./components/ProductCard"
import Cart from "./components/Cart"
import OrderForm from "./components/OrderForm"
import DevModeIndicator from "./components/DevModeIndicator"
import { telegramUtils } from "./utils/telegram"
import "./App.css"

function App() {
  const [products, setProducts] = useState([])
  const [cart, setCart] = useState([])
  const [currentView, setCurrentView] = useState("menu") // menu, cart, order
  const [loading, setLoading] = useState(true)
  const [lang, setLang] = useState("uz")
  const [isTelegramApp, setIsTelegramApp] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    try {
      // Check if running in Telegram WebApp
      const isTelegram = telegramUtils.isAvailable()
      setIsTelegramApp(isTelegram)

      if (isTelegram) {
        telegramUtils.init()
      }

      // Get language from URL params
      const urlParams = new URLSearchParams(window.location.search)
      const langParam = urlParams.get("lang") || "uz"
      setLang(langParam)

      // Load products
      loadProducts()
    } catch (err) {
      console.error("Initialization error:", err)
      setError("Ilovani ishga tushirishda xatolik")
      setLoading(false)
    }
  }, [])

  const loadProducts = async () => {
    try {
      // Mock data - in real app, fetch from API
      const mockProducts = [
        {
          id: 1,
          name: { uz: "Tort", ru: "Торт", en: "Cake" },
          price: 15000,
          emoji: "🍰",
          isNew: true,
        },
        {
          id: 2,
          name: { uz: "Burger", ru: "Бургер", en: "Burger" },
          price: 25000,
          emoji: "🍔",
        },
        {
          id: 3,
          name: { uz: "Fri", ru: "Картофель фри", en: "Fries" },
          price: 12000,
          emoji: "🍟",
        },
        {
          id: 4,
          name: { uz: "Hot-dog", ru: "Хот-дог", en: "Hotdog" },
          price: 18000,
          emoji: "🌭",
        },
        {
          id: 5,
          name: { uz: "Tako", ru: "Тако", en: "Taco" },
          price: 20000,
          emoji: "🌮",
        },
        {
          id: 6,
          name: { uz: "Pizza", ru: "Пицца", en: "Pizza" },
          price: 45000,
          emoji: "🍕",
        },
        {
          id: 7,
          name: { uz: "Donut", ru: "Пончик", en: "Donut" },
          price: 8000,
          emoji: "🍩",
        },
        {
          id: 8,
          name: { uz: "Popkorn", ru: "Попкорн", en: "Popcorn" },
          price: 10000,
          emoji: "🍿",
        },
        {
          id: 9,
          name: { uz: "Kola", ru: "Кола", en: "Coke" },
          price: 8000,
          emoji: "🥤",
        },
        {
          id: 10,
          name: { uz: "Muzqaymoq", ru: "Мороженое", en: "Ice cream" },
          price: 12000,
          emoji: "🍦",
        },
        {
          id: 11,
          name: { uz: "Kukie", ru: "Печенье", en: "Cookie" },
          price: 6000,
          emoji: "🍪",
        },
        {
          id: 12,
          name: { uz: "Flan", ru: "Флан", en: "Flan" },
          price: 18000,
          emoji: "🍮",
        },
      ]

      setProducts(mockProducts)
      setLoading(false)
    } catch (err) {
      console.error("Error loading products:", err)
      setError("Mahsulotlarni yuklashda xatolik")
      setLoading(false)
    }
  }

  const addToCart = (product, quantity = 1) => {
    try {
      if (!product || !product.id) {
        console.error("Invalid product:", product)
        return
      }

      setCart((prevCart) => {
        const existingItem = prevCart.find((item) => item.id === product.id)
        if (existingItem) {
          return prevCart.map((item) =>
            item.id === product.id ? { ...item, quantity: item.quantity + quantity } : item,
          )
        }
        return [...prevCart, { ...product, quantity }]
      })

      // Haptic feedback
      telegramUtils.hapticFeedback("light")
    } catch (err) {
      console.error("Error adding to cart:", err)
    }
  }

  const updateCartItem = (productId, quantity) => {
    try {
      if (quantity <= 0) {
        setCart((prevCart) => prevCart.filter((item) => item.id !== productId))
      } else {
        setCart((prevCart) => prevCart.map((item) => (item.id === productId ? { ...item, quantity } : item)))
      }
    } catch (err) {
      console.error("Error updating cart:", err)
    }
  }

  const getTotalAmount = () => {
    try {
      return cart.reduce((total, item) => {
        const price = Number(item.price) || 0
        const quantity = Number(item.quantity) || 0
        return total + price * quantity
      }, 0)
    } catch (err) {
      console.error("Error calculating total:", err)
      return 0
    }
  }

  const formatPrice = (price) => {
    try {
      const numPrice = Number(price) || 0
      return new Intl.NumberFormat("uz-UZ").format(numPrice)
    } catch (err) {
      console.error("Error formatting price:", err)
      return "0"
    }
  }

  const getText = (key) => {
    try {
      const texts = {
        uz: {
          title: "Durger King",
          buy: "SOTIB OLISH",
          add: "QO'SHISH",
          cart: "Savat",
          total: "Jami",
          order: "Buyurtma berish",
          sum: "so'm",
          error: "Xatolik yuz berdi",
          loading: "Yuklanmoqda...",
        },
        ru: {
          title: "Durger King",
          buy: "КУПИТЬ",
          add: "ДОБАВИТЬ",
          cart: "Корзина",
          total: "Итого",
          order: "Заказать",
          sum: "сум",
          error: "Произошла ошибка",
          loading: "Загрузка...",
        },
        en: {
          title: "Durger King",
          buy: "BUY",
          add: "ADD",
          cart: "Cart",
          total: "Total",
          order: "Order",
          sum: "sum",
          error: "An error occurred",
          loading: "Loading...",
        },
      }
      return texts[lang]?.[key] || key
    } catch (err) {
      console.error("Error getting text:", err)
      return key
    }
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-content">
          <h2>❌ {getText("error")}</h2>
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>
            {lang === "uz" ? "Qayta yuklash" : lang === "ru" ? "Перезагрузить" : "Reload"}
          </button>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>{getText("loading")}</p>
      </div>
    )
  }

  return (
    <div className="app">
      <DevModeIndicator isTelegramApp={isTelegramApp} lang={lang} />

      <header className="header" style={{ marginTop: isTelegramApp ? 0 : "40px" }}>
        <div className="header-content">
          <h1>{getText("title")}</h1>
          {cart.length > 0 && (
            <button className="cart-button" onClick={() => setCurrentView("cart")}>
              {getText("cart")} ({cart.length})
            </button>
          )}
        </div>
      </header>

      <AnimatePresence mode="wait">
        {currentView === "menu" && (
          <motion.div
            key="menu"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="products-grid"
          >
            {products.map((product, index) => (
              <ProductCard
                key={product.id}
                product={product}
                lang={lang}
                onAddToCart={addToCart}
                formatPrice={formatPrice}
                getText={getText}
                index={index}
              />
            ))}
          </motion.div>
        )}

        {currentView === "cart" && (
          <Cart
            cart={cart}
            lang={lang}
            onUpdateItem={updateCartItem}
            onBack={() => setCurrentView("menu")}
            onOrder={() => setCurrentView("order")}
            formatPrice={formatPrice}
            getText={getText}
            getTotalAmount={getTotalAmount}
          />
        )}

        {currentView === "order" && (
          <OrderForm
            cart={cart}
            lang={lang}
            onBack={() => setCurrentView("cart")}
            formatPrice={formatPrice}
            getText={getText}
            getTotalAmount={getTotalAmount}
            isTelegramApp={isTelegramApp}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

export default App
