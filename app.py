from __future__ import annotations
from flask import request
from decimal import Decimal
from datetime import datetime
from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .config import Config
from .models import Lead, LeadSchema, Order, OrderSchema, Payment, PaymentSchema, db, ma


lead_schema = LeadSchema()
leads_schema = LeadSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)


def _json_error(message: str, status_code: int = 400):
    return jsonify({"ok": False, "error": message}), status_code


def _read_json() -> dict:
    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidationError("Request body must be valid JSON.")
    return payload


def _read_pagination() -> tuple[int, int]:
    try:
        page = int(request.args.get("page", "1"))
        per_page = int(request.args.get("per_page", "20"))
    except ValueError as exc:
        raise ValidationError({"pagination": ["`page` and `per_page` must be integers."]}) from exc
    if page < 1:
        raise ValidationError({"page": ["`page` must be >= 1."]})
    if per_page < 1 or per_page > 200:
        raise ValidationError({"per_page": ["`per_page` must be between 1 and 200."]})
    return page, per_page


def _update_order_status(order: Order) -> None:
    if order.due_amount <= Decimal("0"):
        order.status = "paid"
        order.due_amount = Decimal("0.00")
    elif order.due_amount < order.total_amount:
        order.status = "partial"
    else:
        order.status = "open"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        details = exc.messages if isinstance(exc.messages, dict) else {"message": exc.messages}
        return jsonify({"ok": False, "error": "Validation error", "details": details}), 400

    @app.errorhandler(404)
    def handle_not_found(_exc):
        return _json_error("Resource not found.", 404)

    @app.get("/health")
    def health():
        return jsonify({"ok": True, "status": "healthy"})

    @app.post("/api/leads")
    def create_lead():
        payload = _read_json()
        data = lead_schema.load(payload)
        lead = Lead(**data)
        db.session.add(lead)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return _json_error("Lead phone already exists.", 409)
        return jsonify({"ok": True, "lead": lead_schema.dump(lead)}), 201

    @app.get("/api/leads") 
    def list_leads():

    
        with open("security_logs.txt", "a") as f:
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            user_ip = request.remote_addr
            token_used = request.args.get('token', 'NO_TOKEN')
            status_val = request.args.get('status', 'NONE')
        
    
            f.write(f"[{now}] IP: {user_ip} | Token: {token_used} | Status: {status_val}\n")
        
        if request.args.get('token') != 'YOUR_TOKEN_HERE':
         return {"ok": False, "error": "Unauthorized: Invalid Security Token"}, 403
      


        status = request.args.get("status")
        allowed_statuses = ["new", "active", "closed", None] 
    
        if status not in allowed_statuses: 
         return {"ok": False, "error": "Security Alert: Invalid Input Detected!"}, 400
        page, per_page = _read_pagination()
        source = request.args.get("source")

        query = Lead.query
        if status:
            query = query.filter(Lead.status == status)
        if source:
            query = query.filter(Lead.source == source)

        paginated = query.order_by(Lead.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return jsonify(
            {
                "ok": True,
                "count": len(paginated.items),
                "total": paginated.total,
                "page": page,
                "per_page": per_page,
                "pages": paginated.pages,
                "leads": leads_schema.dump(paginated.items),
            }
        )

    @app.get("/api/leads/<int:lead_id>")
    def get_lead(lead_id: int):
        lead = Lead.query.get_or_404(lead_id)
        return jsonify({"ok": True, "lead": lead_schema.dump(lead)})

    @app.put("/api/leads/<int:lead_id>")
    @app.patch("/api/leads/<int:lead_id>")
    def update_lead(lead_id: int):
        lead = Lead.query.get_or_404(lead_id)
        payload = _read_json()
        data = lead_schema.load(payload, partial=True)
        for key, value in data.items():
            setattr(lead, key, value)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return _json_error("Lead phone already exists.", 409)
        return jsonify({"ok": True, "lead": lead_schema.dump(lead)})

    @app.delete("/api/leads/<int:lead_id>")
    def delete_lead(lead_id: int):
        lead = Lead.query.get_or_404(lead_id)
        db.session.delete(lead)
        db.session.commit()
        return jsonify({"ok": True, "message": "Lead deleted."})

    @app.post("/api/orders")
    def create_order():
        payload = _read_json()
        data = order_schema.load(payload)
        lead = Lead.query.get(data["lead_id"])
        if not lead:
            return _json_error("Lead not found.", 404)
        order = Order(**data)
        _update_order_status(order)
        db.session.add(order)
        db.session.commit()
        return jsonify({"ok": True, "order": order_schema.dump(order)}), 201

    @app.get("/api/orders")
    def list_orders():
        page, per_page = _read_pagination()
        status = request.args.get("status")
        lead_id = request.args.get("lead_id")

        query = Order.query
        if status:
            query = query.filter(Order.status == status)
        if lead_id:
            try:
                query = query.filter(Order.lead_id == int(lead_id))
            except ValueError as exc:
                raise ValidationError({"lead_id": ["`lead_id` must be an integer."]}) from exc

        paginated = query.order_by(Order.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return jsonify(
            {
                "ok": True,
                "count": len(paginated.items),
                "total": paginated.total,
                "page": page,
                "per_page": per_page,
                "pages": paginated.pages,
                "orders": orders_schema.dump(paginated.items),
            }
        )

    @app.get("/api/orders/<int:order_id>")
    def get_order(order_id: int):
        order = Order.query.get_or_404(order_id)
        return jsonify({"ok": True, "order": order_schema.dump(order)})

    @app.put("/api/orders/<int:order_id>")
    @app.patch("/api/orders/<int:order_id>")
    def update_order(order_id: int):
        order = Order.query.get_or_404(order_id)
        payload = _read_json()
        data = order_schema.load(payload, partial=True)
        if "lead_id" in data:
            lead = Lead.query.get(data["lead_id"])
            if not lead:
                return _json_error("Lead not found.", 404)
        for key, value in data.items():
            setattr(order, key, value)
        _update_order_status(order)
        db.session.commit()
        return jsonify({"ok": True, "order": order_schema.dump(order)})

    @app.delete("/api/orders/<int:order_id>")
    def delete_order(order_id: int):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({"ok": True, "message": "Order deleted."})

    @app.post("/api/payments")
    def create_payment():
        payload = _read_json()
        data = payment_schema.load(payload)
        order = Order.query.get(data["order_id"])
        if not order:
            return _json_error("Order not found.", 404)
        if Decimal(str(data["amount"])) > Decimal(str(order.due_amount)):
            return _json_error("Payment amount exceeds order due amount.", 400)

        payment = Payment(**data)
        order.due_amount = Decimal(str(order.due_amount)) - Decimal(str(payment.amount))
        _update_order_status(order)

        db.session.add(payment)
        db.session.commit()
        return jsonify({"ok": True, "payment": payment_schema.dump(payment)}), 201

    @app.get("/api/payments")
    def list_payments():
        page, per_page = _read_pagination()
        order_id = request.args.get("order_id")
        method = request.args.get("method")

        query = Payment.query
        if order_id:
            try:
                query = query.filter(Payment.order_id == int(order_id))
            except ValueError as exc:
                raise ValidationError({"order_id": ["`order_id` must be an integer."]}) from exc
        if method:
            query = query.filter(Payment.method == method)

        paginated = query.order_by(Payment.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return jsonify(
            {
                "ok": True,
                "count": len(paginated.items),
                "total": paginated.total,
                "page": page,
                "per_page": per_page,
                "pages": paginated.pages,
                "payments": payments_schema.dump(paginated.items),
            }
        )

    @app.get("/api/payments/<int:payment_id>")
    def get_payment(payment_id: int):
        payment = Payment.query.get_or_404(payment_id)
        return jsonify({"ok": True, "payment": payment_schema.dump(payment)})

    @app.put("/api/payments/<int:payment_id>")
    @app.patch("/api/payments/<int:payment_id>")
    def update_payment(payment_id: int):
        payment = Payment.query.get_or_404(payment_id)
        payload = _read_json()
        data = payment_schema.load(payload, partial=True)

        original_order = payment.order
        original_amount = Decimal(str(payment.amount))

        for key, value in data.items():
            setattr(payment, key, value)

        target_order = Order.query.get(payment.order_id)
        if not target_order:
            db.session.rollback()
            return _json_error("Order not found.", 404)

        if original_order.id == target_order.id:
            restored_due = Decimal(str(target_order.due_amount)) + original_amount
            new_due = restored_due - Decimal(str(payment.amount))
            if new_due < 0:
                db.session.rollback()
                return _json_error("Payment amount exceeds order due amount.", 400)
            target_order.due_amount = new_due
            _update_order_status(target_order)
        else:
            original_order.due_amount = Decimal(str(original_order.due_amount)) + original_amount
            _update_order_status(original_order)
            if Decimal(str(payment.amount)) > Decimal(str(target_order.due_amount)):
                db.session.rollback()
                return _json_error("Payment amount exceeds order due amount.", 400)
            target_order.due_amount = Decimal(str(target_order.due_amount)) - Decimal(str(payment.amount))
            _update_order_status(target_order)

        db.session.commit()
        return jsonify({"ok": True, "payment": payment_schema.dump(payment)})

    @app.delete("/api/payments/<int:payment_id>")
    def delete_payment(payment_id: int):
        payment = Payment.query.get_or_404(payment_id)
        order = payment.order
        order.due_amount = Decimal(str(order.due_amount)) + Decimal(str(payment.amount))
        _update_order_status(order)
        db.session.delete(payment)
        db.session.commit()
        return jsonify({"ok": True, "message": "Payment deleted."})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8010, debug=False)
