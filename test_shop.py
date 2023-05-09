"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(0) == True, 'Ожидается True, так как количество продукта больше запрашиваемого'
        assert product.check_quantity(1000) == True, 'Ожидается True, так как количество продукта больше запрашиваемого'
        assert product.check_quantity(1001) == False, 'Ожидается False, так как количество продукта меньше запрашиваемого'

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(0)
        assert product.quantity == 1000, 'Некорректно вычисляется количество после покупки продуктов = 0шт'

        product.buy(100)
        assert product.quantity == 900, 'Некорректно вычисляется количество после покупки продуктов = 100шт'

        product.buy(900)
        assert product.quantity == 0, 'Некорректно вычисляется количество после покупки продуктов = 900шт'

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        try:
            product.buy(1001)
        except:
            ValueError
            print('Продуктов не хватает')


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        assert len(cart.products) == 0, 'Корзина не пуста'

        cart.add_product(product)
        assert len(cart.products) == 1, 'В корзине должен находиться один одноименный товар'

        cart.add_product(product, 10)
        assert cart.products[product] == 11, 'Ошибка подсчета количества в корзине при дополнении продукта'
        assert len(cart.products) == 1, 'Ошибка проверки количества типов продуктов в корзине'


    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 2)
        assert cart.products[product] == 3, 'Ошибка вычисления количества, после удаления N-ного количества шт. продукта'
        cart.remove_product(product)
        assert len(cart.products) == 0, ' Удаление всего количества продукта, если количество не указано'
        cart.add_product(product, 10)
        cart.remove_product(product, 10)
        assert cart.products[product] == 0, 'Ошибка удаления всго количества продукта'
        cart.add_product(product, 15)
        cart.remove_product(product, 20)
        assert len(cart.products) == 0, 'Если указаное количество больше чем в корзине, то удаляется вся позиция'


    def test_clear(self,  cart, product):
        cart.add_product(product, 20)
        cart.clear()
        assert len(cart.products) == 0, 'Ошибка при очистки корзины'


    def test_get_total_price(self, cart, product):
        assert cart.get_total_price() == 0, 'Цена равна 0, так как в корзине нет товаров'
        cart.add_product(product)
        assert cart.get_total_price() == 100, 'Ошибка вычисления стоимости товара в корзине'
        cart.add_product(product, 50)
        assert cart.get_total_price() == 5100, 'Ошибка вычисления стоимости товара в корзине'


    def test_buy_product(self, cart, product):
        cart.add_product(product, 5)
        cart.buy()
        assert len(cart.products) == 0, 'Удаление товара из корзины после покупки'


    def test_product_buy_more_than_available(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            assert cart.buy(), 'Ожидаемый тип ошибки: ValueError'