import mongoengine as me


class ApiKeyModel(me.Document):
    discord_id = me.IntField(required=True, unique=True)
    api_key = me.StringField(required=True)

    meta = {"collection": "api_key"}
