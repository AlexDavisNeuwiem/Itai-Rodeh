from random import randint

from lib.message import Message
from lib.utils import Constants, States


class Process:
    def __init__(self) -> None:
        """
        ID is the process identity.

        STATE ranges over {active, passive, leader}.

        ROUND represents the number of the current election round.
        """
        self.id = self.generate_id()
        self.state = States.ACTIVE
        self.round = 1

        message = Message(self.id, self.round)
        self.send_message(message)

    def generate_id(self) -> int:
        return randint(1, Constants.K)

    def send_message(self, message: Message) -> Message:
        match self.state:
            case States.PASSIVE:
                message.hop += 1
                return message
            case States.ACTIVE:
                return  # IMPLEMENTAR
            case States.LEADER:
                return

    def receive_message(self, message: Message) -> None:
        match self.state:
            case States.PASSIVE:
                self.send_message(message)
                return
            case States.ACTIVE:
                if message.hop == Constants.N and message.bit == True:
                    self.state = States.LEADER
                elif message.hop == Constants.N and message.bit == False:
                    self.id = self.generate_id()
                    self.round = message.round + 1
                    self.send_message()  # IMPLEMENTAR
                elif (message.id, message.round) == (self.id, self.round) and (
                    message.hop < Constants.N
                ):
                    pass
                elif (message.id, message.round) > (self.id, self.round):
                    self.state = States.PASSIVE
                    self.send_message(message)
                elif (message.id, message.round) < (self.id, self.round):
                    pass  # IMPLEMENTAR
                return
            case States.LEADER:
                return
