from ctypes.wintypes import MSG
from time import sleep
from lib.const import MSG_TEMPLATE_BY_NAME, IMAGE_PATH
from lib.types import ProductVariants, SendMessageTo, Product
from ml_model.predict_deal import predict_deal
from typing import Optional
from os import path, makedirs
# Decorators


def retry(max_retry: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for retry_count in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retry_count < max_retry - 1:
                        sleep(1)
                        continue
                    raise  # Re-raise the last exception
            return None  # This line is actually unreachable
        return wrapper
    return decorator


def format_message(sendTo: SendMessageTo, product_name: str, product_price: str, product_discount: str, product_rating: str, product_url: str, product_discount_percentage: str) -> str:
    message = MSG_TEMPLATE_BY_NAME[sendTo].format(
        product_name=product_name,
        product_price=product_price,
        product_discount=product_discount,
        product_rating=product_rating,
        product_discount_percentage=product_discount_percentage,
        product_url=product_url
    )

    return message


class HelperFunctions:
    @staticmethod
    def short_url_with_affiliate_code(url: str) -> str:
        """
        Shorten the URL and add affiliate code to the URL
        """
        # Implementation for URL shortening
        return url

    @staticmethod
    def evaluate_products_with_ml(product: Optional[Product] = None) -> Optional[Product]:
        """
        Check if a product is a good deal using a machine learning model.
        Returns the product if it's a good deal, None otherwise.
        """
        if product is None:
            return None

        prediction_result = predict_deal(product)

        if prediction_result['prediction'] == 'Best Deal':
            return product

        return None

    @staticmethod
    def generate_message(sendTo: SendMessageTo, product: Product | ProductVariants) -> str:
        """
        Generate a message for the product
        """
        message = ""

        if isinstance(product, Product):
            product_name = product['product_name']
            product_price = product['product_price']
            product_discount = product['product_discount']
            product_rating = product['product_rating']
            product_url = product['product_url']
            product_discount_percentage = (
                product_price - product_discount) / product_price * 100

            message += format_message(
                sendTo,
                product_name,
                product_price,
                product_discount,
                product_rating,
                product_url,
                product_discount_percentage
            )

        elif isinstance(product, ProductVariants):
            product_name = product['base_product_name']
            product_price = product['variants'][0]['product_price']
            product_discount = product['variants'][0]['product_discount']
            product_discount_percentage = (
                product_price - product_discount) / product_price * 100
            product_average_rating = 0
            product_urls = ""

            for varient in product['variants']:
                product_average_rating += varient['product_rating']
                product_urls += f"{varient.get('product_color', "")} {varient['product_url']}\n"

            product_average_rating = product_average_rating / \
                len(product['variants'])

            message += format_message(
                sendTo,
                product_name,
                product_price,
                product_discount,
                product_average_rating,
                product_urls,
                product_discount_percentage
            )

        return message

    @staticmethod
    def save_image(url: str) -> str:
        pass
