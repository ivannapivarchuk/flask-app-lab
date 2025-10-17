import unittest
from app import create_app

class ProductBlueprintTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_product_list(self):
        response = self.client.get("/products/list")
        self.assertEqual(response.status_code, 200)
        text = response.data.decode("utf-8")
        self.assertIn("Ноутбук", text)
        self.assertIn("Мишка", text)
        self.assertIn("Клавіатура", text)

if __name__ == "__main__":
    unittest.main()
