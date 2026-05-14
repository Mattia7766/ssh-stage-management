import tornado.web
import tornado.escape

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_cookie = self.get_secure_cookie("user")
        if not user_cookie:
            return None
        return tornado.escape.json_decode(user_cookie)

    def write_json(self, data, status=200):
        self.set_status(status)
        self.set_header("Content-Type", "application/json")
        self.write(tornado.escape.json_encode(data))