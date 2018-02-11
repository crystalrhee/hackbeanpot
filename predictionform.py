"""
Flask form to take in text passages and model name, and return predicted
pro/con value.
"""
from wtforms import Form, TextAreaField, validators, SelectField


class PredictionForm(Form):
    """
    Form containing textarea for text passage input and select for model choice.
    """
    name = TextAreaField('Text', validators=[validators.required()])
    choices = SelectField('Model', choices=[("gun_control", "Gun Control"),
                                            ("death_penalty", "Death Penalty"),
                                            ("climate_change", "Climate Change"),
                                            ("illegal_immigration", "Illegal Immigration"),
                                            ("abortion_right", "Abortion")])
