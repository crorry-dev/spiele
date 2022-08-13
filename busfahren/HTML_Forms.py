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

    # Zeiterfassung 
    zeiterfassung_zeit_von = DateField("Von", format="%Y-%m-%d", default=datetime.datetime.now(), render_kw={"style": "width:200px"})
    zeiterfassung_zeit_von_time = TimeField("", format="%H:%M", default=datetime.datetime.now(), render_kw={"style": "width:200px"})
    zeiterfassung_zeit_bis = DateField("Bis", format="%Y-%m-%d", default=datetime.datetime.now(), render_kw={"style": "width:200px"})
    zeiterfassung_zeit_bis_time = TimeField("", format="%H:%M", default=datetime.datetime.now(), render_kw={"style": "width:200px"})
    zeiterfassung_zeit_job = SelectField("Tätigkeit", choices=["Trainings-Leistung", "Co-Trainings-Leistung", "Wettkampfrichter"], render_kw={"style": "width:200px"})

    # Reisekosten 
    reisekosten_ort_von = StringField("Start Ort", render_kw={"style": "width:400px; background-color: #ebeced"})
    reisekosten_ort_bis = StringField("Ziel Ort", render_kw={"style": "width:400px; background-color: #ebeced"})
    reisekosten_ort_km = StringField("Anzahl Kilometer hin- und zurück als Ganze Zahl angeben", render_kw={"style": "width:100px; background-color: #ebeced"})
    reisekosten_zeit_von = DateField("Von", format="%Y-%m-%d", default=datetime.datetime.now(), render_kw={"style": "width:200px; background-color: #ebeced"})
    reisekosten_zeit_bis = DateField("Bis", format="%Y-%m-%d", default=datetime.datetime.now(), render_kw={"style": "width:200px; background-color: #ebeced"})
    reisekosten_ort_person_1 = StringField("Mitgefahrene Person 1", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_2 = StringField("Mitgefahrene Person 2", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_3 = StringField("Mitgefahrene Person 3", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_4 = StringField("Mitgefahrene Person 4", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_5 = StringField("Mitgefahrene Person 5", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_6 = StringField("Mitgefahrene Person 6", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_7 = StringField("Mitgefahrene Person 7", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_8 = StringField("Mitgefahrene Person 8", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_9 = StringField("Mitgefahrene Person 9", render_kw={"style": "width:50%; background-color: #ebeced"})
    reisekosten_ort_person_10 = StringField("Mitgefahrene Person 10", render_kw={"style": "width:50%; background-color: #ebeced"})
    
