from typing import List, TypedDict, Union, Literal
from typing_extensions import NotRequired
from enum import Enum


class Product(TypedDict):
    product_name: str
    product_price: float
    product_discount: Union[float, None]
    product_rating: Union[float, None]
    product_url: str
    product_image: str
    product_color: NotRequired[str]


ProductKey = Literal[
    "product_name",
    "product_price",
    "product_discount",
    "product_rating",
    "product_url",
    "product_image",
    "product_color"
]


class ProductVariants(TypedDict):
    base_name: str
    list_images: List[str]
    variants: List[Product]


class ProductSearchResult:
    is_last_page: bool
    products: List[Product]


class Websites(Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"
    AJIO = "ajio"


class SendMessageTo(Enum):
    TELEGRAM = "telegram"
    TWITTER = "twitter"


class ProductCategories(Enum):
    JEANS = "jeans"
    SHIRTS = "shirts"
    SHOES = "shoes"
    WATCHES = "watches"
    TSHIRTS = "tshirts"
