class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def discount(self, percent):
        """Return the new price after the discount (don't change self.price)."""
        return self.price * (100 - percent) /100

    def __str__(self):
        """Return text like: Phone (electronics) - Rs.25000"""
        return f"{self.name} ({self.category}) - Rs. {self.price}"

phone = Product("Phone", 25000, "electronics")
laptop = Product("Laptop", 80000, "electronics")
book = Product("Python Book", 1200, "books")

products = [phone, laptop, book]

for p in products:
    print(p, "->", p.discount(10))

class Cart:
    """A shopping cart that holds products and calculates the total."""
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        result = 0
        for item in self.items:
            result += item.price

        return result

class DigitalProduct(Product):
    def __init__(self, name, price, category, download_link):
        super().__init__(name, price, category)
        self.download_link = "https://ecommerce.com/ebook"

    def __str__(self):
        return f"{super().__str__()} [Download: {self.download_link}]"

cart = Cart()
cart.add(phone)
cart.add(book)
print(cart.total())
print(len(cart.items))
ebook = DigitalProduct("Python ebook", 500, "books", "https://ecommerce.com/ebook")
print(ebook)
print(ebook.download_link)
categories = set()
for p in products:
    categories.add(p.category)
print(categories)
grouped = {}
for p in products:
    if p.category not in grouped:
       grouped[p.category] = []
    grouped[p.category].append(p.name)
print(grouped)

def parse_price(text):
    try:
        price = float(text)
        if price < 0:
            raise ValueError("Price cannot be negative")
    except ValueError as e:
        print("Invalid price:", e)
        return None
    return price

print(parse_price("1500"))
print(parse_price("abc"))
print(parse_price("-50"))
