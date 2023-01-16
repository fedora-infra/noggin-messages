from noggin_messages import MemberSponsorV1, UserCreateV1, UserUpdateV1
from fedora_messaging import message
import json


class TestSchema:
    """Unit tests for testing the noggin message schemas."""

    def test_member_sponsor_v1(self):
        """
        Test MemberSponsorV1

        The expected message here is:

        {
        "body": {
            "msg": {
            "agent": "dudemcpants",
            "group": "developers",
            "user": "testuser"
            }
        },
        "headers": {
            "fedora_messaging_schema": "noggin.group.member.sponsor.v1",
            "fedora_messaging_severity": 20,
            "sent-at": "2020-03-02T08:53:38+00:00"
        },
        "id": "c795df0d-3a95-47a9-85c4-7fabf3129ddf",
        "queue": null,
        "topic": "fas.group.member.sponsor"
        }

        """

        msg = MemberSponsorV1(
            {"msg": {"agent": "dudemcpants", "user": "testuser", "group": "developers"}}
        )
        msg.validate()

        assert msg.app_name == "fas"
        assert msg.agent_name == "dudemcpants"
        assert msg.usernames == ["dudemcpants", "testuser"]
        assert msg.agent_avatar == (
            "https://seccdn.libravatar.org/avatar/caa750e"
            "df4a11206831a58713cf9231b5b3227765887cbc765d4"
            "f8c5c55576a5?s=64&d=retro"
        )
        assert msg.groups == ["developers"]
        assert (
            msg.summary == "Sponsor dudemcpants added testuser to the groupdevelopers"
        )
        assert str(msg) == msg.summary

        msg_dump = json.loads(message.dumps(msg))
        assert msg_dump["body"]["msg"]["agent"] == "dudemcpants"
        assert msg_dump["body"]["msg"]["user"] == "testuser"
        assert msg_dump["body"]["msg"]["group"] == "developers"
        assert (
            msg_dump["headers"]["fedora_messaging_schema"]
            == "noggin.group.member.sponsor.v1"
        )
        assert msg_dump["topic"] == "fas.group.member.sponsor"

    def test_user_create_v1(self):
        """
        Test UserCreateV1

        The expected message here is:

        {
        "body": {
            "msg": {
            "agent": "dudemcpants",
            "user": "testuser"
            }
        },
        "headers": {
            "fedora_messaging_schema": "noggin.user.create.v1",
            "fedora_messaging_severity": 20,
            "sent-at": "2020-03-02T08:53:38+00:00"
        },
        "id": "c795df0d-3a95-47a9-85c4-7fabf3129ddf",
        "queue": null,
        "topic": "fas.user.create"
        }

        """

        msg = UserCreateV1({"msg": {"agent": "dudemcpants", "user": "testuser"}})
        msg.validate()

        assert msg.app_name == "fas"
        assert msg.agent_name == "dudemcpants"
        assert msg.usernames == ["dudemcpants", "testuser"]
        assert msg.agent_avatar == (
            "https://seccdn.libravatar.org/avatar/caa750e"
            "df4a11206831a58713cf9231b5b3227765887cbc765d4"
            "f8c5c55576a5?s=64&d=retro"
        )
        assert msg.groups == []
        assert msg.summary == "dudemcpants created a new Fedora Account for testuser"
        assert str(msg) == msg.summary

        msg_dump = json.loads(message.dumps(msg))
        assert msg_dump["body"]["msg"]["agent"] == "dudemcpants"
        assert msg_dump["body"]["msg"]["user"] == "testuser"
        assert msg_dump["headers"]["fedora_messaging_schema"] == "noggin.user.create.v1"
        assert msg_dump["topic"] == "fas.user.create"

        # the summary is different if agent == user, so lets test that too
        msg2 = UserCreateV1({"msg": {"agent": "dudemcpants", "user": "dudemcpants"}})
        msg2.validate()
        assert msg2.summary == "dudemcpants created a new Fedora Account"

    def test_user_update_v1(self):
        """
        Test UserUpdateV1

        The expected message here is:

        {
        "body": {
            "msg": {
            "agent": "dudemcpants",
            "user": "testuser",
            "fields": ["firstname", "lastname", "gpgkeyid"]
            }
        },
        "headers": {
            "fedora_messaging_schema": "noggin.user.update.v1",
            "fedora_messaging_severity": 20,
            "sent-at": "2020-03-02T08:53:38+00:00"
        },
        "id": "c795df0d-3a95-47a9-85c4-7fabf3129ddf",
        "queue": null,
        "topic": "fas.user.update"
        }

        """

        msg = UserUpdateV1(
            {
                "msg": {
                    "agent": "dudemcpants",
                    "user": "testuser",
                    "fields": ["firstname", "lastname", "gpgkeyid"],
                }
            }
        )
        msg.validate()

        assert msg.app_name == "fas"
        assert msg.agent_name == "dudemcpants"
        assert msg.usernames == ["dudemcpants", "testuser"]
        assert msg.agent_avatar == (
            "https://seccdn.libravatar.org/avatar/caa750e"
            "df4a11206831a58713cf9231b5b3227765887cbc765d4"
            "f8c5c55576a5?s=64&d=retro"
        )
        assert msg.groups == []
        assert (
            msg.summary == "dudemcpants edited 3 details of testuser's Fedora Account"
        )
        assert str(msg) == (
            "dudemcpants edited 3 details of testuser's Fedora Account\n"
            "\n"
            "Details changed:\n"
            "\n"
            "firstname\n"
            "lastname\n"
            "gpgkeyid "
        )

        msg_dump = json.loads(message.dumps(msg))
        assert msg_dump["body"]["msg"]["agent"] == "dudemcpants"
        assert msg_dump["body"]["msg"]["user"] == "testuser"
        assert msg_dump["body"]["msg"]["fields"] == [
            "firstname",
            "lastname",
            "gpgkeyid",
        ]
        assert msg_dump["headers"]["fedora_messaging_schema"] == "noggin.user.update.v1"
        assert msg_dump["topic"] == "fas.user.update"

        # the summary and __str__  is different if agent == user, so lets test that too
        msg2 = UserUpdateV1(
            {
                "msg": {
                    "agent": "dudemcpants",
                    "user": "dudemcpants",
                    "fields": ["firstname", "lastname"],
                }
            }
        )
        msg2.validate()
        assert msg2.summary == "dudemcpants edited 2 details of their Fedora Account"
        assert str(msg2) == (
            "dudemcpants edited 2 details of their Fedora Account\n"
            "\n"
            "Details changed:\n"
            "\n"
            "firstname\n"
            "lastname "
        )
