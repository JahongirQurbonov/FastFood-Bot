"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { telegramUtils } from "../utils/telegram"

const OrderForm = ({ cart, lang, onBack, formatPrice, getText, getTotalAmount, isTelegramApp }) => {
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    address: "",
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState("")

  const getBackText = () => {
    const texts = {
      uz: "Orqaga",
      ru: "Назад",
      en: "Back",
    }
    return texts[lang] || "Back"
  }

  const getSummaryText = () => {
    const texts = {
      uz: "xulosasi",
      ru: "резюме",
      en: "summary",
    }
    return texts[lang] || "summary"
  }

  const validateForm = () => {
    if (!formData.name.trim()) {
      setError(lang === "uz" ? "Ism kiritilmagan" : lang === "ru" ? "Имя не введено" : "Name is required")
      return false
    }
    if (!formData.phone.trim()) {
      setError(lang === "uz" ? "Telefon kiritilmagan" : lang === "ru" ? "Телефон не введен" : "Phone is required")
      return false
    }
    if (!formData.address.trim()) {
      setError(lang === "uz" ? "Manzil kiritilmagan" : lang === "ru" ? "Адрес не введен" : "Address is required")
      return false
    }
    setError("")
    return true
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    setIsSubmitting(true)

    try {
      // Prepare order data
      const orderData = {
        items: cart.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
          name: item.name?.[lang] || item.name?.uz || "Unknown",
          price: item.price || 0,
        })),
        total_amount: getTotalAmount(),
        customer: {
          name: formData.name.trim(),
          phone: formData.phone.trim(),
          address: formData.address.trim(),
        },
      }

      // Send data back to Telegram bot if available
      if (isTelegramApp) {
        const success = telegramUtils.sendData(orderData)
        if (success) {
          // Success - Telegram will handle the rest
          return
        }
      }

      // Fallback for testing outside Telegram
      console.log("Order data:", orderData)
      alert(
        `Order submitted!\n\nTotal: ${formatPrice(getTotalAmount())} sum\nItems: ${cart.length}\n\n(This is a demo outside Telegram)`,
      )
    } catch (error) {
      console.error("Error submitting order:", error)
      setError(
        lang === "uz"
          ? "Buyurtma yuborishda xatolik"
          : lang === "ru"
            ? "Ошибка при отправке заказа"
            : "Error submitting order",
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleInputChange = (field, value) => {
    try {
      setFormData((prev) => ({ ...prev, [field]: value }))
      if (error) setError("") // Clear error when user starts typing
    } catch (err) {
      console.error("Error updating form:", err)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="order-form"
    >
      <div className="form-header">
        <button className="back-button" onClick={onBack}>
          ← {getBackText()}
        </button>
        <h2>{getText("order")}</h2>
      </div>

      {error && <div className="error-message">❌ {error}</div>}

      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>{lang === "uz" ? "Ism" : lang === "ru" ? "Имя" : "Name"}</label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => handleInputChange("name", e.target.value)}
            required
            placeholder={lang === "uz" ? "Ismingizni kiriting" : lang === "ru" ? "Введите ваше имя" : "Enter your name"}
          />
        </div>

        <div className="form-group">
          <label>{lang === "uz" ? "Telefon" : lang === "ru" ? "Телефон" : "Phone"}</label>
          <input
            type="tel"
            value={formData.phone}
            onChange={(e) => handleInputChange("phone", e.target.value)}
            required
            placeholder="+998 90 123 45 67"
          />
        </div>

        <div className="form-group">
          <label>{lang === "uz" ? "Manzil" : lang === "ru" ? "Адрес" : "Address"}</label>
          <textarea
            value={formData.address}
            onChange={(e) => handleInputChange("address", e.target.value)}
            required
            placeholder={
              lang === "uz"
                ? "Yetkazib berish manzilini kiriting"
                : lang === "ru"
                  ? "Введите адрес доставки"
                  : "Enter delivery address"
            }
          />
        </div>

        <div className="order-summary">
          <h3>
            {getText("order")} {getSummaryText()}
          </h3>
          {cart.map((item) => (
            <div key={item.id} className="summary-item">
              <span>
                {item.emoji || "🍽️"} {item.name?.[lang] || item.name?.uz || "Unknown"} x{item.quantity || 1}
              </span>
              <span>
                {formatPrice((item.price || 0) * (item.quantity || 1))} {getText("sum")}
              </span>
            </div>
          ))}
          <div className="summary-total">
            <strong>
              {getText("total")}: {formatPrice(getTotalAmount())} {getText("sum")}
            </strong>
          </div>
        </div>

        <button type="submit" className="submit-button" disabled={isSubmitting}>
          {isSubmitting
            ? lang === "uz"
              ? "Yuborilmoqda..."
              : lang === "ru"
                ? "Отправляется..."
                : "Submitting..."
            : lang === "uz"
              ? "Buyurtma berish"
              : lang === "ru"
                ? "Заказать"
                : "Place Order"}
        </button>
      </form>
    </motion.div>
  )
}

export default OrderForm
