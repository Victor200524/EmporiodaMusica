# Tests for the tools. They use the real CSV files and do not call the LLM.

from emporio_agent.data_loader import normalize
from emporio_agent.tools import (
    get_active_promotions,
    get_order_status,
    get_product_details,
    list_categories,
    search_products,
)


def test_normalize_removes_accents():
    assert normalize("Violão Elétrico ") == "violao eletrico"


def test_search_by_name_without_accents():
    result = search_products(query="takamine gd20")
    assert result["total_found"] == 1
    assert result["products"][0]["price_brl"] == 2199.0


def test_search_by_category_and_max_price():
    result = search_products(category="violoes", max_price=1000)
    assert result["total_found"] > 0
    for product in result["products"]:
        assert product["category"] == "Violões"
        assert product["price_brl"] <= 1000
        assert product["stock_quantity"] > 0


def test_search_hides_discontinued_unless_asked():
    assert search_products(query="Shelby SN-7C")["total_found"] == 0
    result = search_products(query="Shelby SN-7C", only_available=False)
    assert result["products"][0]["status"] == "discontinued"


def test_active_promotion_final_price():
    # Taylor 110e: 5999 with 8% off
    product = search_products(query="Taylor 110e")["products"][0]
    assert product["discount_percent"] == 8
    assert product["final_price_brl"] == 5519.08


def test_product_details_show_expired_promotions():
    details = get_product_details(95)
    assert "promotion" not in details
    assert details["expired_promotions"] == ["Oferta Especial"]


def test_product_details_not_found():
    assert "error" in get_product_details(999)


def test_list_categories():
    assert len(list_categories()["categories"]) == 9


def test_active_promotions_by_category():
    promotions = get_active_promotions("Ukuleles")["promotions"]
    assert len(promotions) == 2


def test_order_status_with_email_or_phone():
    by_email = get_order_status(8, "AnaCarol.Ferreira@coldmail.com")
    by_phone = get_order_status(8, "67 99654-7821")
    assert by_email["status"] == "shipped"
    assert by_phone["tracking_code"] == "BRJL5544332BR"


def test_order_status_wrong_contact_is_blocked():
    assert "error" in get_order_status(8, "someone@else.com")
    assert "error" in get_order_status(999, "someone@else.com")
