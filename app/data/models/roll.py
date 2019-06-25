from app.data import db
from app.data.models import Base


class Roll(Base):
    __tablename__ = "roll"

    time = db.Column(db.DateTime, default=datetime.now())
    class_id = db.Column(db.Integer)
    roll = db.relationship("Roll_Student", backref="roll", lazy="dynamic")
    linked_rfid = db.relationship("Station", back_populates="linked_roll_rel")

    def __repr__(self):
        return "<Roll object Student: {} is in Class: {}>".format(
            self.student_id,
            self.class_id,
        )
