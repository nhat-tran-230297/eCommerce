


class Basket():
    """
    A base Basket class, providing some default behaviors
    """

    def __init__(self, request):
        self.session = request.session
        
        if 'basket' not in request.session:
            basket = self.session['basket'] = {'basket_quantity': 0}
        else:
            basket = self.session['basket']

        self.basket = basket
    

    def add(self, product, product_quantity):
        """
        Add and update user's basket session data
        """

        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'quantity': int(product_quantity)}
        else:
            self.basket[product_id]['quantity'] += product_quantity

        self.basket['basket_quantity'] += product_quantity

        self.session.modified = True


    def __len__(self):
        """
        Get the basket data and count the total quantity
        """
        return self.basket['basket_quantity']

