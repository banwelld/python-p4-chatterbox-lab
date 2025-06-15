from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = [m.to_dict() for m in Message.query.order_by(Message.created_at).all()]
        return make_response(messages, 200)
    
    if request.method == "POST":
        new_msg = Message(
            body=request.json.get("body"),
            username=request.json.get("username"),
            created_at=request.json.get("created_at"),
            updated_at=request.json.get("updated_at"),
        )
        db.session.add(new_msg)
        db.session.commit()
        
        new_msg_dict = new_msg.to_dict()
        
        return make_response(new_msg_dict, 201)
        


@app.route('/messages/<int:id>', methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    
    if not message:
        response_body = {"msg": f"Message with ID {id} does not exist."}
        return make_response(response_body, 404)
    
    if request.method == "GET":
        message = Message.query.filter_by(id=id).first()
        msg_dict = message.to_dict()
        return make_response(msg_dict, 200)
    
    if request.method == "PATCH":
        for attr, value in request.json.items():
            setattr(message, attr, value)
        db.session.commit()
        
        updated_msg = message.to_dict()
        
        return make_response(updated_msg, 200)
    
    if request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        
        response_body = {}
        
        return make_response(response_body, 204)


if __name__ == '__main__':
    app.run(port=4000)
