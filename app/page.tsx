"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Toaster } from "@/components/ui/toaster"
import { useToast } from "@/components/ui/use-toast"
import { ShoppingCart, Plus, Minus, MapPin, Phone, Clock, Star } from "lucide-react"

interface MenuItem {
  id: string
  name: string
  description: string
  price: number
  image: string
  category: string
  rating?: number
}

interface CartItem extends MenuItem {
  quantity: number
}

const menuItems: MenuItem[] = [
  {
    id: "1",
    name: "Big Burger",
    description: "Katta burger go'sht, pomidor, salat va maxsus sous bilan",
    price: 25000,
    image: "🍔",
    category: "Burgerlar",
    rating: 4.8,
  },
  {
    id: "2",
    name: "Cheese Burger",
    description: "Pishloqli burger go'sht va pishloq bilan",
    price: 22000,
    image: "🍔",
    category: "Burgerlar",
    rating: 4.6,
  },
  {
    id: "3",
    name: "Chicken Burger",
    description: "Tovuq go'shti bilan burger",
    price: 20000,
    image: "🍔",
    category: "Burgerlar",
    rating: 4.5,
  },
  {
    id: "4",
    name: "Pizza Margherita",
    description: "Klassik pizza pomidor va pishloq bilan",
    price: 35000,
    image: "🍕",
    category: "Pizzalar",
    rating: 4.7,
  },
  {
    id: "5",
    name: "Pepperoni Pizza",
    description: "Pizza pepperoni va pishloq bilan",
    price: 40000,
    image: "🍕",
    category: "Pizzalar",
    rating: 4.9,
  },
  {
    id: "6",
    name: "Vegetarian Pizza",
    description: "Sabzavotli pizza",
    price: 32000,
    image: "🍕",
    category: "Pizzalar",
    rating: 4.4,
  },
  {
    id: "7",
    name: "French Fries",
    description: "Qizil kartoshka fri",
    price: 12000,
    image: "🍟",
    category: "Garnirlar",
    rating: 4.3,
  },
  {
    id: "8",
    name: "Onion Rings",
    description: "Piyoz halqalari",
    price: 10000,
    image: "🧅",
    category: "Garnirlar",
    rating: 4.2,
  },
  {
    id: "9",
    name: "Coca Cola",
    description: "Sovuq ichimlik 0.5L",
    price: 8000,
    image: "🥤",
    category: "Ichimliklar",
    rating: 4.1,
  },
  {
    id: "10",
    name: "Pepsi",
    description: "Sovuq ichimlik 0.5L",
    price: 8000,
    image: "🥤",
    category: "Ichimliklar",
    rating: 4.0,
  },
  {
    id: "11",
    name: "Orange Juice",
    description: "Apelsin sharbati",
    price: 12000,
    image: "🧃",
    category: "Ichimliklar",
    rating: 4.5,
  },
]

const categories = ["Barchasi", "Burgerlar", "Pizzalar", "Garnirlar", "Ichimliklar"]

export default function FastFoodApp() {
  const [cart, setCart] = useState<CartItem[]>([])
  const [selectedCategory, setSelectedCategory] = useState("Barchasi")
  const [showCheckout, setShowCheckout] = useState(false)
  const [customerInfo, setCustomerInfo] = useState({
    phone: "",
    address: "",
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { toast } = useToast()

  // Telegram WebApp integration
  const tg = typeof window !== "undefined" ? (window as any).Telegram?.WebApp : null

  useEffect(() => {
    if (tg) {
      tg.ready()
      tg.expand()
      tg.MainButton.hide()

      // Set theme colors
      tg.setHeaderColor("#f97316")
      tg.setBackgroundColor("#fed7aa")
    }
  }, [tg])

  const filteredItems =
    selectedCategory === "Barchasi" ? menuItems : menuItems.filter((item) => item.category === selectedCategory)

  const addToCart = (item: MenuItem) => {
    setCart((prev) => {
      const existing = prev.find((cartItem) => cartItem.id === item.id)
      if (existing) {
        return prev.map((cartItem) =>
          cartItem.id === item.id ? { ...cartItem, quantity: cartItem.quantity + 1 } : cartItem,
        )
      }
      return [...prev, { ...item, quantity: 1 }]
    })

    toast({
      title: "Savatga qo'shildi",
      description: `${item.name} savatga qo'shildi`,
    })

    // Haptic feedback
    if (tg) {
      tg.HapticFeedback.impactOccurred("light")
    }
  }

  const removeFromCart = (itemId: string) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.id === itemId)
      if (existing && existing.quantity > 1) {
        return prev.map((item) => (item.id === itemId ? { ...item, quantity: item.quantity - 1 } : item))
      }
      return prev.filter((item) => item.id !== itemId)
    })

    if (tg) {
      tg.HapticFeedback.impactOccurred("light")
    }
  }

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + item.price * item.quantity, 0)
  }

  const getTotalItems = () => {
    return cart.reduce((total, item) => total + item.quantity, 0)
  }

  const handleCheckout = async () => {
    if (!customerInfo.phone || !customerInfo.address) {
      toast({
        title: "Xatolik",
        description: "Telefon va manzil kiritilishi shart",
        variant: "destructive",
      })
      return
    }

    if (cart.length === 0) {
      toast({
        title: "Xatolik",
        description: "Savat bo'sh",
        variant: "destructive",
      })
      return
    }

    setIsSubmitting(true)

    try {
      const orderData = {
        items: cart,
        totalAmount: getTotalPrice(),
        customerInfo,
        orderDate: new Date().toISOString(),
      }

      if (tg) {
        tg.sendData(JSON.stringify(orderData))

        toast({
          title: "Buyurtma yuborildi!",
          description: "Tez orada siz bilan bog'lanamiz",
        })

        // Haptic feedback
        tg.HapticFeedback.notificationOccurred("success")

        setTimeout(() => {
          tg.close()
        }, 2000)
      } else {
        console.log("Order data:", orderData)
        toast({
          title: "Test rejimida",
          description: "Buyurtma ma'lumotlari konsolga yuborildi",
        })
      }
    } catch (error) {
      toast({
        title: "Xatolik yuz berdi",
        description: "Iltimos qaytadan urinib ko'ring",
        variant: "destructive",
      })

      if (tg) {
        tg.HapticFeedback.notificationOccurred("error")
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  if (showCheckout) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-400 to-red-600 p-4">
        <div className="max-w-md mx-auto">
          <div className="flex items-center justify-between mb-6">
            <Button variant="ghost" onClick={() => setShowCheckout(false)} className="text-white hover:bg-white/20">
              ← Orqaga
            </Button>
            <h1 className="text-2xl font-bold text-white">Buyurtma</h1>
            <div></div>
          </div>

          <Card className="mb-4">
            <CardContent className="p-4">
              <h2 className="text-lg font-semibold mb-4">Buyurtma tafsilotlari</h2>
              {cart.map((item) => (
                <div key={item.id} className="flex justify-between items-center py-2 border-b last:border-b-0">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">{item.image}</span>
                    <div>
                      <p className="font-medium">{item.name}</p>
                      <p className="text-sm text-gray-600">x{item.quantity}</p>
                    </div>
                  </div>
                  <p className="font-semibold">{(item.price * item.quantity).toLocaleString()} so'm</p>
                </div>
              ))}
              <div className="flex justify-between items-center pt-4 border-t font-bold text-lg">
                <span>Jami:</span>
                <span>{getTotalPrice().toLocaleString()} so'm</span>
              </div>
            </CardContent>
          </Card>

          <Card className="mb-4">
            <CardContent className="p-4 space-y-4">
              <h2 className="text-lg font-semibold">Aloqa ma'lumotlari</h2>

              <div>
                <label className="block text-sm font-medium mb-1">
                  <Phone className="inline w-4 h-4 mr-1" />
                  Telefon raqami
                </label>
                <Input
                  type="tel"
                  placeholder="+998 90 123 45 67"
                  value={customerInfo.phone}
                  onChange={(e) => setCustomerInfo((prev) => ({ ...prev, phone: e.target.value }))}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">
                  <MapPin className="inline w-4 h-4 mr-1" />
                  Yetkazib berish manzili
                </label>
                <Textarea
                  placeholder="To'liq manzilni kiriting..."
                  value={customerInfo.address}
                  onChange={(e) => setCustomerInfo((prev) => ({ ...prev, address: e.target.value }))}
                  className="min-h-[80px]"
                  required
                />
              </div>

              <Button
                onClick={handleCheckout}
                className="w-full bg-green-500 hover:bg-green-600 text-white py-6 text-lg"
                disabled={isSubmitting}
              >
                {isSubmitting ? "Yuborilmoqda..." : "Buyurtma berish"}
              </Button>
            </CardContent>
          </Card>
        </div>
        <Toaster />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-400 to-red-600">
      {/* Header */}
      <div className="bg-white/10 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-md mx-auto p-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">FastFood</h1>
              <p className="text-white/80 text-sm">Tez va mazali</p>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-white" />
              <span className="text-white text-sm">24/7</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-md mx-auto p-4">
        {/* Categories */}
        <div className="flex space-x-2 mb-6 overflow-x-auto pb-2">
          {categories.map((category) => (
            <Button
              key={category}
              variant={selectedCategory === category ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedCategory(category)}
              className={`whitespace-nowrap ${
                selectedCategory === category
                  ? "bg-white text-orange-600 hover:bg-white/90"
                  : "bg-white/20 text-white border-white/30 hover:bg-white/30"
              }`}
            >
              {category}
            </Button>
          ))}
        </div>

        {/* Menu Items */}
        <div className="space-y-4 mb-20">
          {filteredItems.map((item) => {
            const cartItem = cart.find((cartItem) => cartItem.id === item.id)
            const quantity = cartItem?.quantity || 0

            return (
              <Card key={item.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center space-x-4">
                    <div className="text-4xl">{item.image}</div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <h3 className="font-semibold text-lg">{item.name}</h3>
                        {item.rating && (
                          <div className="flex items-center">
                            <Star className="w-4 h-4 text-yellow-400 fill-current" />
                            <span className="text-sm text-gray-600 ml-1">{item.rating}</span>
                          </div>
                        )}
                      </div>
                      <p className="text-gray-600 text-sm mb-2">{item.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-lg font-bold text-orange-600">{item.price.toLocaleString()} so'm</span>
                        <div className="flex items-center space-x-2">
                          {quantity > 0 && (
                            <>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => removeFromCart(item.id)}
                                className="w-8 h-8 p-0"
                              >
                                <Minus className="w-4 h-4" />
                              </Button>
                              <Badge variant="secondary" className="px-3">
                                {quantity}
                              </Badge>
                            </>
                          )}
                          <Button
                            size="sm"
                            onClick={() => addToCart(item)}
                            className="w-8 h-8 p-0 bg-orange-500 hover:bg-orange-600"
                          >
                            <Plus className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Cart Button */}
        {cart.length > 0 && (
          <div className="fixed bottom-4 left-4 right-4 max-w-md mx-auto">
            <Button
              onClick={() => setShowCheckout(true)}
              className="w-full bg-green-500 hover:bg-green-600 text-white py-4 text-lg shadow-lg"
            >
              <ShoppingCart className="w-5 h-5 mr-2" />
              Savat ({getTotalItems()}) - {getTotalPrice().toLocaleString()} so'm
            </Button>
          </div>
        )}
      </div>

      <Toaster />
    </div>
  )
}
