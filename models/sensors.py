from extensions import db


class Sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lng = db.Column(db.String(60))
    lat = db.Column(db.String(60))
    group = db.Column(db.Integer)
    group_number = db.Column(db.Integer)

    def asdict(self):
        return {
            'id': self.id,
            'lng': self.lng,
            'lat': self.lat,
            'group': self.group,
            'group_number': self.group_number,
        }

