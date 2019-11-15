import webapp2
import password
import MySQLdb
import random

def get_conn():
    conn = MySQLdb.connect(unix_socket = password.SQL_HOST,
        user = password.SQL_USER,
        passwd = password.SQL_PASSWD,
        db = "customers")
    return conn

def increment():
    return"""
    <html>
    <center>
    <title>Increment</title>
    <body>
    <h1>Increment Value</h1><hr>
    <form action="/increment" method="get">
    Click Me to increment my current value by one<br> 
    <input type="submit">
    </form>
    </body>
    </center>
    </html>
    """)


def create_username_form():
    return("""
    <html>
    <center>
    <title>New User</title>
    <body>
    <h1>Create a New Username</h1><hr>
    <form action="/add_user" method="get">
    Create a new User Name: <input type="text" name="username"><br>
    <input type="submit">
    </form>
    </body>
    </center>
    </html>
    """)

class MainPage(webapp2.RequestHandler):
    def get(self):
        cookieId = self.request.cookies.get("cookie_name")
        conn = get_conn()
        cursor = conn.cursor()
        if cookieId == None:
            id = "%032x" % random.getrandbits(128)
            self.response.set_cookie("cookie_name", id, max_age=1800)
            cursor.execute("INSERT INTO sessions(id) VALUES(%s)", (id,))
            cursor.close()
            conn.commit()
            self.response.write(create_username_form())
        else:
            cursor.execute("SELECT user_name FROM sessions WHERE id=%s", (cookieID,))
            username = cursor.fetchall()[0]
            if username != "":
                self.response.write(increment())
            else:
                self.response.write(create_username_form())

class Increment(webapp2.RequestHandler):
    def get(self):
        cookieId = self.request.get("cookie_name")
        user_name = self.request.get("username")
        conn = get_conn()
        cursor = conn.get_cursor()
        cursor.execute("SELECT count FROM users WHERE user_name=%s", (user_name,))
        curr = cursor.fetchall()[0]
        cursor.execute("UPDATE users SET count = %s WHERE user_name = %s", (curr + 1, user_name))

class Add_User(webapp2.RequestHandler):
    def get(self):
        cookieId = self.request.cookies.get("cookie_name")
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE sessions SET user_name=%s WHERE id=%s", (user_name, cookieID))

app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/increment", Increment),
    ("/add_user", Add_User)
], debug=True)
