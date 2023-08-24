from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, RadioField, TextAreaField
from wtforms.validators import InputRequired, Optional, NumberRange, URL


class AddCupcakeForm(FlaskForm):
    """Form for adding new cupcakes"""

    flavor = StringField("Flavor", validators=[
        InputRequired(message="Name cannot be blank")])
    size = RadioField("Size", choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")],  validators=[
        InputRequired()])
    rating = FloatField("Rating", validators=[
        InputRequired(message="Rating cannot be blank"), NumberRange(min=0, max=10)])
    image = TextAreaField("Image URL", validators=[
        Optional(), URL(require_tld=True)])
