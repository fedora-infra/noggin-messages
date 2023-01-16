from fedora_messaging import message
from fedora_messaging.schema_utils import user_avatar_url


class NogginMessage(message.Message):
    @property
    def app_name(self):
        """
        Return the name of the application that generated the message.

        Returns:
            the name of the application (fas)
        """
        return "fas"

    @property
    def agent_name(self):
        """Return the agent's username for this message.

        Returns:
            The agent's username, or None if the msg has no agent key.
        """
        return self.body["msg"]["agent"]

    @property
    def user_name(self):
        """Return the username for this message.

        Returns:
            The username this message is about
        """
        return self.body["msg"]["user"]

    @property
    def agent_avatar(self):
        """
        Return a URL to the avatar of the user who caused the action.

        Returns:
            The URL to the user's avatar, or None if username is None.
        """
        return user_avatar_url(self.agent_name)

    @property
    def usernames(self):
        """
        List of users affected by the action that generated this message.

        Returns:
            A list of affected usernames.
        """
        users = [self.agent_name, self.user_name]
        users.sort()
        return users

    def __str__(self):
        """
        Return a human-readable representation of this message.

        This should provide a detailed representation of the message, much like the body
        of an email.

        Returns:
            A human readable representation of this message.
        """
        return self.summary


class MemberSponsorV1(NogginMessage):
    """The message sent when a user is added to a group by a sponsor"""

    @property
    def groups(self):
        """
        List of groups affected by the action that generated this message.

        Returns:
            A list of affected groups.
        """
        return [self.body["msg"]["group"]]

    @property
    def summary(self):
        """
        Return a short, human-readable representation of this message.

        This should provide a short summary of the message, much like the subject line
        of an email.

        Returns:
            A summary for this message.
        """
        return (
            f"Sponsor {self.agent_name} added {self.user_name} to the group"
            f"{self.groups[0]}"
        )

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


class UserCreateV1(NogginMessage):
    """The message sent when a user is created"""

    @property
    def summary(self):
        """
        Return a short, human-readable representation of this message.

        This should provide a short summary of the message, much like the subject line
        of an email.

        Returns:
            A summary for this message.
        """

        if self.user_name == self.agent_name:
            return f"{self.agent_name} created a new Fedora Account"
        else:
            return (
                f"{self.agent_name} created a new Fedora Account for {self.user_name}"
            )

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


class UserUpdateV1(NogginMessage):
    """The message sent when a user is updated"""

    @property
    def summary(self):
        """
        Return a short, human-readable representation of this message.

        This should provide a short summary of the message, much like the subject line
        of an email.

        Returns:
            A summary for this message.
        """

        if self.user_name == self.agent_name:
            return (
                f"{self.agent_name} edited {len(self.body['msg']['fields'])} details of "
                "their Fedora Account"
            )
        else:
            return (
                f"{self.agent_name} edited {len(self.body['msg']['fields'])} details of "
                f"{self.user_name}'s Fedora Account"
            )

    def __str__(self):
        """
        Return a human-readable representation of this message.

        This should provide a detailed representation of the message, much like the body
        of an email.

        Returns:
            A human readable representation of this message.
        """
        new_line = "\n"
        return (
            f"{self.summary}\n\n"
            f"Details changed:\n\n"
            f"{new_line.join([item for item in self.body['msg']['fields']])} "
        )

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
