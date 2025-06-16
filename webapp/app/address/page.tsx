"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"

export default function AddressPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    address: "",
    apartment: "",
    city: "",
    region: "",
    district: "",
    postalCode: "",
    fullName: "",
    phone: "",
    saveInfo: true,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Telegram Bot'ga ma'lumotlarni yuborish
    if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
      const tg = (window as any).Telegram.WebApp
      tg.sendData(
        JSON.stringify({
          action: "submit_address",
          address: formData,
        }),
      )
      tg.close()
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  return (
    <div className="address-form">
      <div className="form-header">
        <button className="back-btn" onClick={() => router.back()}>
          ←
        </button>
        <h1>Yetkazib berish axboroti</h1>
        <button className="back-btn">✓</button>
      </div>

      <form className="form-content" onSubmit={handleSubmit}>
        <div className="form-section">
          <h3 className="section-title">Yetkazib berish manzili</h3>

          <div className="form-group">
            <label className="form-label">Manzil 1 (ko'cha)</label>
            <input
              type="text"
              name="address"
              className="form-input"
              value={formData.address}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Manzil 2 (Ko'cha)</label>
            <input
              type="text"
              name="apartment"
              className="form-input"
              value={formData.apartment}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Shahar</label>
            <input
              type="text"
              name="city"
              className="form-input"
              value={formData.city}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Viloyat</label>
            <input
              type="text"
              name="region"
              className="form-input"
              value={formData.region}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Mamlakat</label>
            <input
              type="text"
              name="district"
              className="form-input"
              value={formData.district}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Pochta indeksi</label>
            <input
              type="text"
              name="postalCode"
              className="form-input"
              value={formData.postalCode}
              onChange={handleInputChange}
            />
          </div>
        </div>

        <div className="form-section">
          <h3 className="section-title">Qabul qiluvchi</h3>

          <div className="form-group">
            <label className="form-label">To'liq ismi</label>
            <input
              type="text"
              name="fullName"
              className="form-input"
              value={formData.fullName}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Telefon raqami</label>
            <div className="phone-input">
              <input type="text" className="country-code" value="+998" readOnly />
              <input
                type="tel"
                name="phone"
                className="form-input"
                placeholder="-- -------"
                value={formData.phone}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
        </div>

        <div className="toggle-section">
          <div className="toggle-info">
            <h4>Yetkazish ma'lumotlarini saqlash</h4>
            <p className="toggle-desc">
              Yetkazib berish ma'lumotlaringizni kelgusida foydalanish uchun saqlashingiz mumkin.
            </p>
          </div>
          <div
            className="toggle-switch"
            onClick={() => setFormData((prev) => ({ ...prev, saveInfo: !prev.saveInfo }))}
            style={{
              background: formData.saveInfo ? "#4A90E2" : "#666",
              transform: formData.saveInfo ? "none" : "scaleX(-1)",
            }}
          ></div>
        </div>

        <button type="submit" className="submit-button">
          Tasdiqlash
        </button>
      </form>
    </div>
  )
}
