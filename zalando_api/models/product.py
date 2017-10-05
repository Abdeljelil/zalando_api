from decimal import Decimal


class ProductModel:

    def __init__(self, row, index):

        self.id = None
        self.name = None
        self.image_url = None
        self.price = None
        self.brand = None
        self.index = index

        for field, value in row.items():
            # Convert Decimal to float
            if isinstance(value, Decimal):
                value = float(value)
            setattr(self, field, value)

    def to_dict(self):
        """
        convert fields to dict
        """
        r = dict(
            id=self.id,
            name=self.name,
            image_url=self.image_url,
            price=self.price,
            brand=self.brand,
            index=self.index
        )
        return r
