import mongoengine as me


class TestimoniModel(me.Document):
    rating = me.IntField(required=True)
    description = me.StringField(required=True)
    created_at = me.IntField(required=True)
    url_testimoni = me.StringField(required=False)

    user = me.ReferenceField("UserModel", reverse_delete_rule=me.CASCADE)

    meta = {"collection": "testimoni"}
