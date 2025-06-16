"use client"

import { useState } from "react"
import { motion } from "framer-motion"

const ProductCard = ({ product, lang, onAddToCart, formatPrice, getText, index }) => {
  const [isAdding, setIsAdding] = useState(false)

  const handleAdd = async () => {
    try {
      setIsAdding(true)
      onAddToCart(product)

      // Add haptic feedback if available
      if (window.Telegram?.WebApp?.HapticFeedback?.impactOccurred) {
        window.Telegram.WebApp.HapticFeedback.impactOccurred("light")
      }

      setTimeout(() => setIsAdding(false), 300)
    } catch (err) {
      console.error("Error adding product:", err)
      setIsAdding(false)
    }
  }

  const handleBuy = () => {
    try {
      onAddToCart(product)
    } catch (err) {
      console.error("Error buying product:", err)
    }
  }

  // Safe property access
  const productName = product?.name?.[lang] || product?.name?.uz || "Unknown"
  const productPrice = product?.price || 0
  const productEmoji = product?.emoji || "🍽️"
  const isNew = product?.isNew || false

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: (index || 0) * 0.1 }}
      className="product-card"
    >
      <div className="product-emoji">
        {productEmoji}
        {isNew && <span className="new-badge">NEW</span>}
      </div>

      <div className="product-info">
        <h3 className="product-name">
          {productName} • {formatPrice(productPrice)} {getText("sum")}
        </h3>
      </div>

      <div className="product-actions">
        {isNew ? (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="buy-button"
            onClick={handleBuy}
          >
            {getText("buy")}
          </motion.button>
        ) : (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`add-button ${isAdding ? "adding" : ""}`}
            onClick={handleAdd}
            disabled={isAdding}
          >
            {isAdding ? "✓" : getText("add")}
          </motion.button>
        )}
      </div>
    </motion.div>
  )
}

export default ProductCard
