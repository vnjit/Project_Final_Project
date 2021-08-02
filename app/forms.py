from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class SignupForm(FlaskForm):
    """Sign up for a user account."""
    name = StringField(
        'Name',
        [DataRequired()]
    )
    email = StringField(
        "Email",
        [
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        "Password",
        [
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirmPassword = PasswordField(
        "Confirm Your Password",
        [
            EqualTo(password, message="Passwords must match.")
        ]
    )
    submit = SubmitField("Register")

    class LoginForm(FlaskForm):
        """User Log-in Form."""
        email = StringField(
            "Email",
            [
                Email(message='Enter a valid email.'),
                DataRequired()
            ]
        )
        password = PasswordField(
            "Password",
            [
                DataRequired(message="Please enter a password."),
            ]
        )
        submit = SubmitField("Login In")

