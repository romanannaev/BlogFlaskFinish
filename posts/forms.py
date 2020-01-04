from wtforms import Form, StringField, TextAreaField, FileField
from wtforms.validators import InputRequired

class PostForm(Form):
    title = StringField('Title', [InputRequired()])
    body = TextAreaField('Body')
    image = FileField('Image')
    
