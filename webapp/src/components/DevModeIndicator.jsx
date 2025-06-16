"use client"

const DevModeIndicator = ({ isTelegramApp, lang }) => {
  if (isTelegramApp) return null

  const texts = {
    uz: "🔧 Ishlab chiqish rejimi - Telegram tashqarisida ishlamoqda",
    ru: "🔧 Режим разработки - работает вне Telegram",
    en: "🔧 Development mode - running outside Telegram",
  }

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        background: "#ff9800",
        color: "white",
        padding: "8px",
        textAlign: "center",
        fontSize: "12px",
        zIndex: 1000,
        boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
      }}
    >
      {texts[lang]}
    </div>
  )
}

export default DevModeIndicator
