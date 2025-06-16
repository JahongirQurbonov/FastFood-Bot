import type React from "react"
import "./globals.css"
import type { Metadata } from "next"
import { CartProvider } from "./context/CartContext"

export const metadata: Metadata = {
  title: "Durger King - FastFood",
  description: "Telegram FastFood Bot Web App",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="uz">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
      </head>
      <body>
        <CartProvider>{children}</CartProvider>
      </body>
    </html>
  )
}
