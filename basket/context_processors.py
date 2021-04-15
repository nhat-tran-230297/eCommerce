from .basket import Basket


def basket(request) -> dict:
    return {'basket_context_processor': Basket(request)}
