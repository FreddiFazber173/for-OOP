class MenuItem:
    def init(self, name, base_price):
        self.name = name
        self.base_price = base_price

    def calculatePrice(self):
        raise NotImplementedError("Этот метод должен быть переопределен в дочернем классе!")


class Pizza(MenuItem):
    def init(self, name, base_price, size):
        super().init(name, base_price)
        self.size = size

    def calculatePrice(self):
        if self.size == "большая":
            return self.base_price * 1.3
        return self.base_price


class Drink(MenuItem):
    def init(self, name, base_price, is_ice):
        super().init(name, base_price)
        self.is_ice = is_ice

    def calculatePrice(self):
        return self.base_price

    def getName(self):
        if self.is_ice:
            return self.name + " со льдом"
        return self.name


class ComboSet(MenuItem):
    def init(self, name, items):
        super().init(name, 0)
        self.items = items

    def calculatePrice(self):
        summa = 0
        for item in self.items:
            summa += item.calculatePrice()
        return summa * 0.85


class Order:
    def init(self):
        self.__items = []
        self.__status = "создан"
        self.__all_statuses = ["создан", "готовится", "в пути", "доставлен"]

    def getStatus(self):
        return self.__status

    def nextStep(self):
        current_index = self.all_statuses.index(self.status)
        if current_index < len(self.__all_statuses) - 1:
            self.status = self.all_statuses[current_index + 1]
            print("Статус заказа изменился:", self.__status)
        else:
            print("Заказ уже доставлен!")

    def addItem(self, item):
        if self.__status != "создан":
            raise ValueError("Нельзя добавлять товары, заказ уже в работе!")
        
        self.__items.append(item)
        real_name = item.getName() if hasattr(item, "getName") else item.name
        print("Добавлено в заказ:", real_name)

    def getTotalCost(self):
        total = 0
        for item in self.__items:
            total += item.calculatePrice()
        return total

    def pay(self, paymentMethod):
        summa = self.getTotalCost()
        if summa == 0:
            print("Корзина пустая!")
            return
        paymentMethod.collectPayment(summa)


class PaymentStrategy:
    def collectPayment(self, amount):
        raise NotImplementedError("Метод оплаты должен быть реализован!")


class CardPayment(PaymentStrategy):
    def init(self, cardNumber, expiryDate, cvv):
        self.cardNumber = cardNumber
        self.expiryDate = expiryDate
        self.cvv = cvv

    def collectPayment(self, amount):
        if "/" not in self.expiryDate:
            print("Ошибка: неверный формат срока действия карты!")
            return
        print("С вашей карты списано:", amount, "руб.")


class CashPayment(PaymentStrategy):
    def collectPayment(self, amount):
        print("Надо отдать курьеру наличными:", amount, "руб.")


if __name__ == "__main__":
    p1 = Pizza("Маргарита", 500, "средняя")
    p2 = Pizza("Пепперони", 600, "большая")
    drink = Drink("Кола", 150, True)
    
    combo = ComboSet("Студенческий обед", [p1, drink])

    my_order = Order()
    my_order.addItem(p2)
    my_order.addItem(combo)

    print("Сумма заказа:", my_order.getTotalCost())

    my_order.nextStep()

    try:
        my_order.addItem(drink)
    except Exception as e:
        print("Не получилось добавить:", e)

    my_order.nextStep()
    my_order.nextStep()

    pay = CardPayment("1234567890123456", "12/28", "777")
    my_order.pay(pay)