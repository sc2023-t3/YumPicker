from telegram import Location


class Restaurant:
    def __init__(self, name: str, open_now: bool, price_level: int, rating: float, vicinity: str, photo_reference: str,
                 location: Location):
        self.name: name = name
        self.open_now: bool = open_now
        self.price_level: int = price_level
        self.rating: float = rating
        self.vicinity: str = vicinity
        self.photo_reference: str = photo_reference
        self.location: Location = location

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            open_now=data["opening_hours"]["open_now"],
            price_level=data["price_level"],
            rating=data["rating"],
            vicinity=data["vicinity"],
            photo_reference=data["photos"][0]["photo_reference"],
            location=Location(data["geometry"]["location"]["lng"], data["geometry"]["location"]["lat"])
        )
