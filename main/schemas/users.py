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
    infection_accuracy = ms_fields.Int()
    use_privacy_data = ms_fields.Bool()
    tracking_save_duration = ms_fields.Float()
    bluetooth_save_duration = ms_fields.Int()
    data_save_duration = ms_fields.Int()
    phone = ms_fields.Str()
    zip_code = ms_fields.Str()
    registration_date_time = ms_fields.DateTime(default=datetime.datetime.now())

    class Meta:
        unknown = EXCLUDE


