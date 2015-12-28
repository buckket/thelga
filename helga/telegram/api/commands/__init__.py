from helga.telegram.api.types import Type, InputFile, String, Boolean, Integer, Update, Structure, User, Descriptor, \
    File


class TelegramCommand(Structure):
    """ TelegramCommand base structure

    if you implement a new command you need to overwrite at least:
    __command__ and parse_result

    """

    __command__ = None  # command (or method) string see telegram botapi for available commands
    __method__ = 'get'  # HTTP-Method (get or post)

    def get_params(self):
        """ Returns a dict with URL-Query parameters for this command
        :return: dict
        """
        return {k: v.cls.get_value(getattr(self, k)) for k, v in self.__class__.__dict__.items() if
                (isinstance(v, Descriptor) and isinstance(v.cls, Type) and v.cls.target == 'params')}

    def get_data(self):
        """ Returns a dict with Formdata elements for this command
        :return: dict
        """
        return {k: v.cls.get_value(getattr(self, k)) for k, v in self.__class__.__dict__.items() if
                (isinstance(v, Descriptor) and isinstance(v.cls, Type) and v.cls.target == 'data')}

    def parse_result(self, result):
        return result

    @property
    def method(self):
        return self.__method__

    @property
    def command(self):
        return self.__command__


class GetMe(TelegramCommand):
    """ Command structure for the getMe command

    see https://core.telegram.org/bots/api#getme
    """
    __command__ = 'getMe'

    def parse_result(self, result):
        """ Parses the Result of the getMe Command

        :param result: dict
        :return: helga.telegram.api.types.User
        """
        return User(**result)


class SendMessage(TelegramCommand):
    """ Command structure for the sendMessage command

    see https://core.telegram.org/bots/api#sendmessage
    """
    __command__ = 'sendMessage'
    __method__ = 'post'

    chat_id = String()
    text = String()
    parse_mode = String()
    disable_web_page_preview = Boolean()
    reply_to_message_id = Integer()


class ForwardMessage(TelegramCommand):
    """ Command structure for the forwardMessage command

    see https://core.telegram.org/bots/api#forwardmessage
    """
    __command__ = 'forwardMessage'
    __method__ = 'post'

    chat_id = String()
    from_chat_id = String()
    message_id = Integer()


class SendPhoto(TelegramCommand):
    """ Command structure for the sendPhoto command

    see https://core.telegram.org/bots/api#sendphoto
    """
    __command__ = 'sendPhoto'
    __method__ = 'post'

    chat_id = String()
    photo = InputFile()


class GetUpdates(TelegramCommand):
    """ Command structure for the getUpdates command

    see https://core.telegram.org/bots/api#getupdates
    """
    __command__ = 'getUpdates'
    __method__ = 'get'
    timeout = Integer()
    limit = Integer()
    offset = Integer()

    def parse_result(self, result):
        updates = []
        for item in result:
            update = Update(**item)
            updates.append(update)
        return updates


class GetFile(TelegramCommand):
    """ Command structure for the getFile command

    see https://core.telegram.org/bots/api#getfile
    """
    __command__ = 'getFile'
    __method__ = 'get'

    file_id = String()

    def parse_result(self, result):
        return File(**result)
