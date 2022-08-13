#-*- charset: utf-8 -*-
from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, validators, SelectField, DateTimeField, widgets, SelectMultipleField
from wtforms.widgets.core import TextInput
from wtforms.fields import DateField, EmailField, TelField
from wtforms_components import TimeField
from wtforms.validators import DataRequired
import datetime

class Form(Form):

    # defaults
    text_input = TextAreaField("", [validators.Length(min=1, max=9999)], render_kw={"style":"width: 75%; height: 25%; font-size: 48px;"})
    text_input_guest = TextAreaField("", [validators.Length(min=1, max=9999)], render_kw={"style":"width: 75%; height: 25%; font-size: 48px;"})
    string_input = StringField("", [validators.Length(min=1, max=9999)])
    string_input_password = PasswordField("Passwort", [validators.Length(min=1, max=9999)])
    select_input = SelectField("", choices=[])
    datetime_input = DateField("DatePicker", format="%Y-%m-%d", default=datetime.datetime.now())
    checkbox_input = BooleanField('True/False', render_kw={"style":"width: 15px; height: 15px;"})

    # login 
    login_email = StringField("Email Adresse", [validators.Length(min=1, max=9999)], render_kw={"style":"margin:0 auto; width: 75%; font-size: 20px;"})
    login_password = PasswordField("Passwort", [validators.Length(min=1, max=9999)], render_kw={"style":"margin:0 auto; width: 75%; font-size: 20px;"})

    #register
    register_firstname = StringField("Vorname", [validators.Length(min=1, max=9999)], render_kw={"style":"margin:0 auto; width: 75%; font-size: 20px;"})
    register_name = StringField("Nachname", [validators.Length(min=1, max=9999)], render_kw={"style":"margin:0 auto; width: 75%; font-size: 20px;"})
    register_telephone = StringField("Telefonnummer", [validators.Length(min=1, max=9999)], render_kw={"style":"margin:0 auto; width: 75%; font-size: 20px;"})
    register_email = StringField("Email Adresse", [validators.Length(min=1, max=9999)], render_kw={"style":"margin:0 auto; width: 75%; font-size: 20px;"})
    register_password = PasswordField("Passwort", [validators.Length(min=1, max=9999)], render_kw={"style":"margin:0 auto; width: 75%; font-size: 20px;"})
    register_confirm_password = PasswordField("Passwort bestätigen", [validators.Length(min=1, max=9999)], render_kw={"style":"margin:0 auto; width: 75%; font-size: 20px;"})
    select_abteilung = SelectField("Abteilung", choices=["faustball", "badminton", "basketball", "judo", "leichtathletik", "volleyball"])
    
    # contact-page
    contact_name = StringField("Ihr Vor- und Nachname", [validators.Length(min=1, max=9999)], render_kw={"style": "width: 75%; font-size: 20px;"})
    contact_title = StringField("Titel Ihrer Anfrage", [validators.Length(min=1, max=9999)], render_kw={"style": "width: 75%; font-size: 20px;"})
    contact_contact = StringField("Ihre Telefonnummer oder Email Adresse", [validators.Length(min=1, max=9999)], render_kw={"style": "width: 75%; font-size: 20px;"})
    contact_text = TextAreaField("Beschreibung Ihrer Anfrage", [validators.Length(min=1, max=9999)], render_kw={"style": "width: 75%; height: 40%; font-size: 20px;"})

    # Busfahren Lobby
    busfahren_nickname = StringField("Nickname", [validators.Length(min=1, max=9999)], render_kw={"style": "width: 50%; font-size: 20px;"})
    