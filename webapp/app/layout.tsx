import type React from "react"
import "./globals.css"
import type { Metadata } from "next"

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
      <body>{children}</body>
    </html>
  )
}
