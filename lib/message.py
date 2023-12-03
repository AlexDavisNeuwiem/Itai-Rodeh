class Message:
    def __init__(self, id: int, round: int) -> None:
        """
        Os valores de ID e ROUND são obtidos do processo que originou
        a mensagem

        HOP é um contador inicializado em 1 e é incrementado toda vez
        que um processo repassa a mensagem

        BIT é um booleano inicializado como true e que recebe o valor
        false quando a mensagem visita um processo com o mesmo ID que
        seu emissor
        """
        self.__id = id
        self.__round = round
        self.hop = 1
        self.bit = True

    def get_id(self) -> int:
        return self.__id

    def get_round(self) -> int:
        return self.__round

    @staticmethod
    def from_tuple(message_tuple: tuple) -> "Message":
        message = Message(message_tuple[0], message_tuple[1])
        message.hop = message_tuple[2]
        message.bit = message_tuple[3]
        return message

    @staticmethod
    def to_tuple(message: "Message") -> tuple:
        return message.get_id(), message.get_round(), message.hop, message.bit
