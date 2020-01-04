import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
#create admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
#flask security, the storage of users, roles
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import view
from posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/blog') #registration posts app(blueprint)
###  Admin  ####
from models import *
#integration Admin and Flask Security
from flask_security import current_user
from flask import redirect, url_for, request
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwargs):
        #localhost/admin/
        return redirect(url_for('security.login', next=request.url))

#Point to admin panel to use our class-constructors
#Allows our to change slug at the moment creating or editing Post from admin Panel
class BaseModelView(ModelView):
    def on_model_change(self, form, model , is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

#class constrains allow to models POst and Tag in AdminPanel
class AdminView(AdminMixin, ModelView):
    pass

#class constrains allow to AdminPanel at all
from flask_admin import AdminIndexView
class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags', 'image']

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']

admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session)) #before was ModelView instead of AdminView --->PostAdminView
admin.add_view(TagAdminView(Tag, db.session))
## flask security ##
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

if __name__ == '__main__':
    app.run()