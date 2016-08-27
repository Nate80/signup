#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

form = """
<!DOCTYPE html>
<html>
    <head>
        <title>Signup Homework</title>
    </head>

    <body>
        <form method = "post">
            <h1>Sign Up</h1>
            <label><b>USER NAME:</b>
                <input type="text" name="username" value="%(username)s"
                            style="height: 20px; width: 200px">&nbsp;<div style="color: red">%(username_error)s</div>
            </label>
            <br>
            <label><b>PASSWORD:</b>
                <input type="password" name="password"
                    <style="height: 20px; width: 200px">&nbsp;<div style="color: red">%(password_error)s</div>
            </label>
            <br>
            <label><b>VERIFY PASSWORD:</b>
                <input type="password" name="password2"
                    style="height: 20px; width: 200px">&nbsp;<div style="color: red">%(password2_error)s</div>
            </label>
            <br>
            <label><b>EMAIL</b>
                <input type="email" name="email" value="%(email)s"
                        style="height: 20px; width: 200px">&nbsp;<div style="color: red">%(email_error)s</div>
            </label>
            <br>
            <p><input type="submit" value="Submit"></p>
        </form>
    </body>

    <footer>
    </footer>
</html>
"""

def escape_html(s):
    return cgi.escape(s, quote=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_name(name):
    return name and USER_RE.match(name)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)


class MainSignUpHandler(webapp2.RequestHandler):

    def write_form(self, username="", email="", username_error="", password_error="", password2_error="", email_error=""):
        self.response.out.write(form % {"username": username,
                                        "email": email,
                                        "username_error": username_error,
                                        "password_error": password_error,
                                        "password2_error": password2_error,
                                        "email_error": email_error})
    def get(self):
        self.write_form()

    def post(self):
        user_name = self.request.get('username')
        user_password = self.request.get('password')
        user_password2 = self.request.get('password2')
        user_email = self.request.get('email')

        username = escape_html(user_name)
        password = escape_html(user_password)
        password2 = escape_html(user_password2)
        email = escape_html(user_email)

        username_error = ""
        password_error = ""
        password2_error = ""
        email_error = ""

        if not username or not valid_name(username):
            username_error = "Invalid username"
        if email and not valid_email(email):
            email_error = "Not a valid email address."
        if not password:
            password_error = "Password Required."
        if not password2:
            password2_error = "Verification required."
        if not valid_password(password):
            password_error = "Please enter a valid password."
        if not valid_password(password2):
            password2_error = "Please enter a valid password."
        if password != password2:
            password_error = "Passwords are not the same."


        if username_error or password_error or password2_error or email_error:
            self.write_form(username, email, username_error, password_error, password2_error, email_error)

        else:
            self.redirect('/welcome?username='+username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write("Welcome " + username + "!")


app = webapp2.WSGIApplication([
    ('/', MainSignUpHandler),
    ('/welcome', Welcome)
], debug=True)
