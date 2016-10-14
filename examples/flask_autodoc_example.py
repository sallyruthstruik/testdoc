from json import dumps

from flask import Flask, redirect, request

from testdoc import Testdoc
from testdoc.configurator import BaseConfiguration
from testdoc.write_plugins.flask_autodoc import FlaskPlugin



app = Flask(__name__)
app.debug = True

class Configuration(BaseConfiguration):
    def should_write_doc(self, func):
        return app.debug

flaskPlugin = FlaskPlugin(app)

testdoc = Testdoc(Configuration(write_plugins=[
    flaskPlugin
]))


users = []
posts = []


class User(object):

    def __init__(self, username):
        self.username = username
        users.append(self)
        self.id = users.index(self)

    def __repr__(self):
        return dumps(self.__dict__)


class Post(object):

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        posts.append(self)
        self.id = posts.index(self)

    def __repr__(self):
        return dumps(self.__dict__)


u = User('acoomans')
Post('First post', 'This is the first awesome post', u)
Post('Second post', 'This is another even more awesome post', u)


@app.route('/')
@app.route('/posts')
@testdoc
def get_posts():
    """Return all posts."""
    return '%s' % posts


@app.route('/post/<int:id>')
@testdoc
def get_post(id):
    """Return the post for the given id."""
    return '%s' % posts[id]


@app.route('/post', methods=["POST"])
@testdoc
def post_post():
    """Create a new post.
    Form Data: title, content, authorid.
    """
    authorid = request.form.get('authorid', None)
    Post(request.form['title'],
         request.form['content'],
         users[authorid])
    return redirect("/posts")


@app.route('/users')
@testdoc
def get_users():
    """Return all users."""
    return '%s' % users


@app.route('/user/<int:id>')
@testdoc
def get_user(id):
    """Return the user for the given id."""
    return '%s' % users[id]


@app.route('/users', methods=['POST'])
@testdoc
def post_user(id):
    """Creates a new user.
    Form Data: username.
    """
    User(request.form['username'])
    redirect('/users')


@app.route('/admin', methods=['GET'])
@testdoc
def admin():
    """Admin interface."""
    return 'Admin interface'


@app.route('/doc')
def public_doc():
    return flaskPlugin.html()
#
#
# @app.route('/doc/private')
# def private_doc():
#     return auto.html(groups=['private'], title='Private Documentation')


if __name__ == '__main__':
    app.run()