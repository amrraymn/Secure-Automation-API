from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError, fields, validates_schema


db = SQLAlchemy()
ma = Marshmallow()


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(25), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=True)
    source = db.Column(db.String(50), nullable=False, default="whatsapp")
    status = db.Column(db.String(30), nullable=False, default="new")
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = db.relationship("Order", back_populates="lead", cascade="all, delete-orphan", lazy="dynamic")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"), nullable=False, index=True)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    due_amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="open")
    due_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    lead = db.relationship("Lead", back_populates="orders")
    payments = db.relationship("Payment", back_populates="order", cascade="all, delete-orphan", lazy="dynamic")


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    method = db.Column(db.String(30), nullable=False, default="cash")
    notes = db.Column(db.Text, nullable=True)
    paid_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    order = db.relationship("Order", back_populates="payments")


class LeadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lead
        load_instance = False
        ordered = True
        include_fk = True


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = False
        ordered = True
        include_fk = True

    total_amount = fields.Decimal(as_string=True, required=True)
    due_amount = fields.Decimal(as_string=True, required=True)

    @validates_schema
    def validate_amounts(self, data, **kwargs):
        total_amount = data.get("total_amount")
        due_amount = data.get("due_amount")
        if total_amount is not None and total_amount <= Decimal("0"):
            raise ValidationError("`total_amount` must be greater than 0.", field_name="total_amount")
        if due_amount is not None and due_amount < Decimal("0"):
            raise ValidationError("`due_amount` cannot be negative.", field_name="due_amount")
        if total_amount is not None and due_amount is not None and due_amount > total_amount:
            raise ValidationError("`due_amount` cannot be greater than `total_amount`.", field_name="due_amount")


class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        load_instance = False
        ordered = True
        include_fk = True

    amount = fields.Decimal(as_string=True, required=True)

    @validates_schema
    def validate_amount(self, data, **kwargs):
        amount = data.get("amount")
        if amount is not None and amount <= Decimal("0"):
            raise ValidationError("`amount` must be greater than 0.", field_name="amount")

