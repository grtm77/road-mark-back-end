from extensions import db


class Datasets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table_name = db.Column(db.String(60))
    table_remark = db.Column(db.String(60))
    created_at = db.Column(db.Date)

    def asdict(self):
        return {
            'id': self.id,
            'table_name': self.table_name,
            'table_remark': self.table_remark,
            'created_at': self.created_at,
        }

