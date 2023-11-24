from random import randint

from lib.message import Message
from lib.states import States
from lib.constants import Constants


class Itai_Rodeh_Process:
    def __init__(self) -> None:
        """
        ID is the process identity.

        STATE ranges over {active, passive, leader}.

        ROUND represents the number of the current election round.
        """
        self.__id = self.generate_id()
        self.__state = States.ACTIVE
        self.__round = 1

        message = Message(self.__id, self.__round)
        Constants.fair_scheduler.put(message)

    def generate_id(self) -> int:
        return randint(1, Constants.number_of_ids)

    def run(self) -> None:
        message = Constants.fair_scheduler.get()
        match self.__state:
            case States.PASSIVE:
                message.hop += 1
                Constants.fair_scheduler.put(message)
                return
            case States.ACTIVE:
                if (
                    message.hop == Constants.number_of_processes
                    and message.bit == True
                ):
                    self.__state = States.LEADER
                elif (
                    message.hop == Constants.number_of_processes
                    and message.bit == False
                ):
                    self.__id = self.generate_id()
                    self.__round += 1
                    message = Message(self.__id, self.__round)
                    Constants.fair_scheduler.put(message)
                elif (
                    (message.get_id(), message.get_round()) == (self.__id, self.__round) 
                    and (message.hop < Constants.number_of_processes)
                ):
                    message.hop += 1
                    message.bit = False
                    Constants.fair_scheduler.put(message)
                elif (
                    (message.get_id(), message.get_round()) > (self.__id, self.__round)
                ):
                    self.__state = States.PASSIVE
                    message.hop += 1
                    Constants.fair_scheduler.put(message)
                elif (
                    (message.get_id(), message.get_round()) < (self.__id, self.__round)
                ):
                    pass
                return
            case States.LEADER:
                return
