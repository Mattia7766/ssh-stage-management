import tornado.escape
import bcrypt

from backend.handlers.base import BaseHandler
from backend.db.db import db_interface

class RegisterHandler(BaseHandler):
    async def post(self):
        body = tornado.escape.json_decode(self.request.body)
        email = body.get("email", "").strip()
        password = body.get("password", "")

        if not email or not password:
            return self.write_json({"error": "Email e password obbligatorie"}, 400)

        existing = await db_interface.get_user_by_email(email)
        if existing:
            return self.write_json({"error": "Utente già registrato"}, 400)

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        await db_interface.create_user(email, hashed)

        return self.write_json({"message": "Registrazione completata"}, 201)

class LoginHandler(BaseHandler):
    async def post(self):
        body = tornado.escape.json_decode(self.request.body)
        email = body.get("email", "").strip()
        password = body.get("password", "")

        ruolo = await db_interface.check_user(email)

        user = await db_interface.get_user_by_email(email)
        if not user:
            return self.write_json({"error": "Credenziali errate"}, 401)

        if not bcrypt.checkpw(password.encode(), user["password"]):
            return self.write_json({"error": "Credenziali errate"}, 401)

        user_data = {
            "id": str(user["_id"]),
            "email": user["email"]
        }

        self.set_secure_cookie("user", tornado.escape.json_encode(user_data))
        return self.write_json({"message": "Login effettuato", "user": user_data, "ruolo": ruolo})

class LogoutHandler(BaseHandler):
    async def post(self):
        self.clear_cookie("user")
        return self.write_json({"message": "Logout effettuato"})
