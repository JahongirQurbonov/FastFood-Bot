// Telegram WebApp utilities with error handling
export const telegramUtils = {
  // Check if running in Telegram WebApp
  isAvailable: () => {
    try {
      return (
        typeof window !== "undefined" &&
        window.Telegram &&
        window.Telegram.WebApp &&
        typeof window.Telegram.WebApp === "object"
      )
    } catch (err) {
      console.error("Error checking Telegram availability:", err)
      return false
    }
  },

  // Get Telegram WebApp instance
  getWebApp: () => {
    try {
      return window.Telegram?.WebApp || null
    } catch (err) {
      console.error("Error getting WebApp:", err)
      return null
    }
  },

  // Initialize WebApp safely
  init: () => {
    try {
      const tg = telegramUtils.getWebApp()
      if (tg && typeof tg.ready === "function") {
        tg.ready()

        if (typeof tg.expand === "function") {
          tg.expand()
        }

        if (typeof tg.setHeaderColor === "function") {
          tg.setHeaderColor("#1e3c72")
        }

        if (typeof tg.setBackgroundColor === "function") {
          tg.setBackgroundColor("#1e3c72")
        }

        return tg
      }
      return null
    } catch (err) {
      console.error("Error initializing WebApp:", err)
      return null
    }
  },

  // Send data safely
  sendData: (data) => {
    try {
      const tg = telegramUtils.getWebApp()
      if (tg && typeof tg.sendData === "function") {
        const dataString = typeof data === "string" ? data : JSON.stringify(data)
        tg.sendData(dataString)
        return true
      }
      return false
    } catch (err) {
      console.error("Error sending data:", err)
      return false
    }
  },

  // Trigger haptic feedback safely
  hapticFeedback: (type = "light") => {
    try {
      const tg = telegramUtils.getWebApp()
      if (tg && tg.HapticFeedback && typeof tg.HapticFeedback.impactOccurred === "function") {
        tg.HapticFeedback.impactOccurred(type)
      }
    } catch (err) {
      console.error("Error with haptic feedback:", err)
    }
  },

  // Get user data safely
  getUserData: () => {
    try {
      const tg = telegramUtils.getWebApp()
      return tg?.initDataUnsafe?.user || null
    } catch (err) {
      console.error("Error getting user data:", err)
      return null
    }
  },

  // Close WebApp safely
  close: () => {
    try {
      const tg = telegramUtils.getWebApp()
      if (tg && typeof tg.close === "function") {
        tg.close()
      }
    } catch (err) {
      console.error("Error closing WebApp:", err)
    }
  },
}
