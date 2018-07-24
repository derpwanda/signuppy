import webapp2
import re

form = """
<form action="/" method="post">
    <label>
        Username:
        <input type="text" name="username" value="%(username)s"/>%(user_error)s
    </label>
    <br>
    <label>
        Password:
        <input type="password" name="password" value=""/>%(pswd_error)s
    </label>
    <br>
    <label>
        Verify Password:
        <input type="password" name="verify" value=""/>%(veri_error)s
    </label>
    <br>
    <label>
        Email (optional):
        <input type="text" name="email" value="%(email)s"/>%(email_error)s
    </label>
    <br>
    <input type="submit" value="submit"/>
</form>
"""
#    <div style="color:red">%(error)s</div>
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def val_username(username):
    return username and USER_RE.match(username)
        #validate password
PSWD_RE = re.compile(r"^.{3,20}$")
def val_password(password):
    return password and PSWD_RE.match(password)
        #validate email address
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def val_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):

    def write_form(self, user_error="", email_error="", pswd_error="",
        veri_error="", username="", password="", verify="", email=""):
        self.response.out.write(form % {"user_error": user_error,
                                        "email_error": email_error,
                                        "pswd_error": pswd_error,
                                        "veri_error": veri_error,
                                        "username": username,
                                        "password": password,
                                        "verify": verify,
                                        "email": email,
                                        })

    def get(self):
#        self.response.write(self.form)
        self.write_form()

    def post(self):
        error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        user_error, email_error, pswd_error, veri_error = "", "", "", "",

        if not val_username(username):
            user_error = "That's not a valid username. Try again."
            error = True

        if not val_password(password):
            pswd_error = "Please choose another password."
            error = True
        elif password != verify:
            veri_error = "Your passwords do not match. Please re-enter."
            error = True

        if not val_email(email):
            email_error = "That email is not valid. Try again."
            error = True

        self.write_form(user_error=user_error, email_error=email_error,
        pswd_error=pswd_error, veri_error=veri_error, username=username)

        if not error:
            self.redirect("/welcome?username=" + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome " + username + "!")

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', WelcomeHandler),
], debug=True)
