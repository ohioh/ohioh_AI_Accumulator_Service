import datetime

from marshmallow import Schema, EXCLUDE
import marshmallow.fields as ms_fields



class UserSchema(Schema):
    _id = ms_fields.Str()
    first_name = ms_fields.Str()
    last_name = ms_fields.Str()
    age = ms_fields.Int()
    country=ms_fields.Str()
    is_infected = ms_fields.Bool()
    infection_accuracy = ms_fields.Float()
    user_privacy_data = ms_fields.Bool()
    tracking_save_duration = ms_fields.Float()
    bluetooth_save_duration = ms_fields.Float()
    data_save_duration = ms_fields.Float()
    phone = ms_fields.Int()
    zip_code = ms_fields.Int()
    registration_date_time = ms_fields.DateTime()

    #BluettihEncouter
    encounter_user_id = ms_fields.Str()
    bluetooth_date_time = ms_fields.DateTime()

    #Location
    location_id = ms_fields.Str()
    latitude = ms_fields.Float()
    departure = ms_fields.Bool()
    location_date_time = ms_fields.DateTime()
    splitted = ms_fields.Bool()
    accuracy = ms_fields.Float()
    location_type = ms_fields.Float()
    longitude = ms_fields.Float()
    speed = ms_fields.Float()
    arrival = ms_fields.Bool()

    class Meta:
        unknown = EXCLUDE


