from app.models import ProductInDb, ResourceInDb
from app.models.resource import ResourceObjectType
from tests.utils import random_string

class TestModels:
    def test_create_model(self, db):
        product = ProductInDb.create("HAHA", "haha")

        db.add(product)
        db.commit()
        db.refresh(product)

        assert product.name == "HAHA"
        assert product.slug == "haha"
        assert product.created_at != None

    def test_create_model_with_relationship(self, db):
        product = ProductInDb.create("HAHA", "haha")
        db.add(product)
        db.flush()

        resources = [
            ResourceInDb.create(
                random_string(), 
                random_string() + ".pdf", 
                ResourceObjectType.PRODUCT,
                product.id
            ) for _ in range(5)
        ]
        db.add_all(resources)
        db.commit()

        assert len(product.resources) == 5
