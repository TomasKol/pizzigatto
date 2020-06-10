def cartTotal(items):
  totalPrice = 0
  for item in items:
    item.priceForAmount = item.amount * item.price_unit
    totalPrice += item.priceForAmount
  return totalPrice