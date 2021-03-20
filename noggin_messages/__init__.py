from fedora_messaging import message


class MemberSponsorV1(message.Message):
    """The message sent when a user is added to a group by a sponsor"""

    topic = "fas.group.member.sponsor"
    body_schema = {
        "id": "http://fedoraproject.org/message-schema/noggin",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when a user is added to a group by a sponsor",
        "type": "object",
        "required": ["msg"],
        "properties": {
            "msg": {
                "required": ["agent", "user", "group"],
                "description": "the contents of the event",
                "type": "object",
                "properties": {
                    "agent": {"type": "string"},
                    "user": {"type": "string"},
                    "group": {"type": "string"},
                },
            }
        },
    }


class UserCreateV1(message.Message):
    """The message sent when a user is created"""

    topic = "fas.user.create"
    body_schema = {
        "id": "http://fedoraproject.org/message-schema/noggin",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when a user is created",
        "type": "object",
        "required": ["msg"],
        "properties": {
            "msg": {
                "required": ["agent", "user"],
                "description": "the contents of the event",
                "type": "object",
                "properties": {
                    "agent": {"type": "string"},
                    "user": {"type": "string"},
                },
            }
        },
    }


class UserUpdateV1(message.Message):
    """The message sent when a user is updated"""

    topic = "fas.user.update"
    body_schema = {
        "id": "http://fedoraproject.org/message-schema/noggin",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when a user is updated",
        "type": "object",
        "required": ["msg"],
        "properties": {
            "msg": {
                "required": ["agent", "user", "fields"],
                "description": "the contents of the event",
                "type": "object",
                "properties": {
                    "agent": {"type": "string"},
                    "user": {"type": "string"},
                    "fields": {
                        "type": "array",
                        "contains": {
                            "type": "string",
                        },
                    },
                },
            },
        },
    }
