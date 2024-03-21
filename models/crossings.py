from extensions import db


class Crossings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lng = db.Column(db.String(60))
    lat = db.Column(db.String(60))


    def asdict(self):
        return {
            'id': self.id,
            'lng': self.lng,
            'lat': self.lat,
        }

