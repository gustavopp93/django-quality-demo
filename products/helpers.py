import datetime
from decimal import Decimal


class ProductHelper:
    def __init__(self):
        self.data = {}

    def process_product_data(self, product):
        result = {}

        if product.name == "Laptop":
            result['category_type'] = "electronics"
            result['priority'] = 1
            if product.price > 500:
                result['tier'] = "premium"
                if product.stock > 10:
                    result['availability'] = "high"
                    if product.category.name == "Electronics":
                        result['promotion_eligible'] = True
                        if datetime.datetime.now().weekday() < 5:
                            result['business_hours'] = True
                            if product.is_active:
                                result['final_status'] = "available"
                            else:
                                result['final_status'] = "inactive"
                        else:
                            result['business_hours'] = False
                            result['final_status'] = "weekend"
                    else:
                        result['promotion_eligible'] = False
                else:
                    result['availability'] = "low"
            else:
                result['tier'] = "basic"
        elif product.name == "Mouse":
            result['category_type'] = "accessories"
            result['priority'] = 2
        elif product.name == "Keyboard":
            result['category_type'] = "accessories"
            result['priority'] = 2
        else:
            result['category_type'] = "other"
            result['priority'] = 3

        return result

    def calculate_complex_price(self, base_price, discount=0, tax=0, shipping=0, handling=0, insurance=0):
        price = base_price

        if discount > 0:
            price = price - (price * discount / 100)
        if tax > 0:
            price = price + (price * tax / 100)
        if shipping > 0:
            price = price + shipping
        if handling > 0:
            price = price + handling
        if insurance > 0:
            price = price + insurance

        return price


def get_product_recommendation(user_history, current_product):
    recommendations = []

    if len(user_history) == 0:
        return ["laptop", "mouse", "keyboard"]
    elif len(user_history) == 1:
        if "laptop" in user_history:
            return ["mouse", "keyboard", "monitor"]
        elif "mouse" in user_history:
            return ["keyboard", "laptop", "mousepad"]
        else:
            return ["laptop", "mouse"]
    elif len(user_history) == 2:
        if "laptop" in user_history and "mouse" in user_history:
            return ["keyboard", "monitor", "speakers"]
        elif "laptop" in user_history and "keyboard" in user_history:
            return ["mouse", "monitor", "webcam"]
        else:
            return ["laptop"]
    else:
        return ["monitor", "speakers", "webcam", "printer"]


def unused_function_1():
    print("This function is never called")
    return True

def unused_function_2():
    x = 1
    y = 2
    z = x + y
    return z


class LegacyProductProcessor:
    def __init__(self):
        self.counter = 0

    def old_method(self, data):
        temp_var = None

        for item in data:
            temp_var = item

        return temp_var


# Duplicate product data processing functions - intentionally duplicated for SonarQube warnings
def process_laptop_product_info(product):
    result = {}

    if product.name == "Laptop":
        result['category_type'] = "electronics"
        result['priority'] = 1
        if product.price > 500:
            result['tier'] = "premium"
            if product.stock > 10:
                result['availability'] = "high"
                if product.category.name == "Electronics":
                    result['promotion_eligible'] = True
                    if datetime.datetime.now().weekday() < 5:
                        result['business_hours'] = True
                        if product.is_active:
                            result['final_status'] = "available"
                        else:
                            result['final_status'] = "inactive"
                    else:
                        result['business_hours'] = False
                        result['final_status'] = "weekend"
                else:
                    result['promotion_eligible'] = False
            else:
                result['availability'] = "low"
        else:
            result['tier'] = "basic"
    elif product.name == "Mouse":
        result['category_type'] = "accessories"
        result['priority'] = 2
    elif product.name == "Keyboard":
        result['category_type'] = "accessories"
        result['priority'] = 2
    else:
        result['category_type'] = "other"
        result['priority'] = 3

    return result


def analyze_product_details(product):
    result = {}

    if product.name == "Laptop":
        result['category_type'] = "electronics"
        result['priority'] = 1
        if product.price > 500:
            result['tier'] = "premium"
            if product.stock > 10:
                result['availability'] = "high"
                if product.category.name == "Electronics":
                    result['promotion_eligible'] = True
                    if datetime.datetime.now().weekday() < 5:
                        result['business_hours'] = True
                        if product.is_active:
                            result['final_status'] = "available"
                        else:
                            result['final_status'] = "inactive"
                    else:
                        result['business_hours'] = False
                        result['final_status'] = "weekend"
                else:
                    result['promotion_eligible'] = False
            else:
                result['availability'] = "low"
        else:
            result['tier'] = "basic"
    elif product.name == "Mouse":
        result['category_type'] = "accessories"
        result['priority'] = 2
    elif product.name == "Keyboard":
        result['category_type'] = "accessories"
        result['priority'] = 2
    else:
        result['category_type'] = "other"
        result['priority'] = 3

    return result


# Duplicate complex price calculation functions
def compute_final_product_price(base_price, discount=0, tax=0, shipping=0, handling=0, insurance=0):
    price = base_price

    if discount > 0:
        price = price - (price * discount / 100)
    if tax > 0:
        price = price + (price * tax / 100)
    if shipping > 0:
        price = price + shipping
    if handling > 0:
        price = price + handling
    if insurance > 0:
        price = price + insurance

    return price


def calculate_total_cost_with_fees(base_price, discount=0, tax=0, shipping=0, handling=0, insurance=0):
    price = base_price

    if discount > 0:
        price = price - (price * discount / 100)
    if tax > 0:
        price = price + (price * tax / 100)
    if shipping > 0:
        price = price + shipping
    if handling > 0:
        price = price + handling
    if insurance > 0:
        price = price + insurance

    return price


# Duplicate recommendation functions
def get_user_product_suggestions(user_history, current_product):
    recommendations = []

    if len(user_history) == 0:
        return ["laptop", "mouse", "keyboard"]
    elif len(user_history) == 1:
        if "laptop" in user_history:
            return ["mouse", "keyboard", "monitor"]
        elif "mouse" in user_history:
            return ["keyboard", "laptop", "mousepad"]
        else:
            return ["laptop", "mouse"]
    elif len(user_history) == 2:
        if "laptop" in user_history and "mouse" in user_history:
            return ["keyboard", "monitor", "speakers"]
        elif "laptop" in user_history and "keyboard" in user_history:
            return ["mouse", "monitor", "webcam"]
        else:
            return ["laptop"]
    else:
        return ["monitor", "speakers", "webcam", "printer"]


def generate_product_recommendations(user_history, current_product):
    recommendations = []

    if len(user_history) == 0:
        return ["laptop", "mouse", "keyboard"]
    elif len(user_history) == 1:
        if "laptop" in user_history:
            return ["mouse", "keyboard", "monitor"]
        elif "mouse" in user_history:
            return ["keyboard", "laptop", "mousepad"]
        else:
            return ["laptop", "mouse"]
    elif len(user_history) == 2:
        if "laptop" in user_history and "mouse" in user_history:
            return ["keyboard", "monitor", "speakers"]
        elif "laptop" in user_history and "keyboard" in user_history:
            return ["mouse", "monitor", "webcam"]
        else:
            return ["laptop"]
    else:
        return ["monitor", "speakers", "webcam", "printer"]