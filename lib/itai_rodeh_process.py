from multiprocessing import Queue
from random import randint

from lib.message import Message
from lib.states import States


class Itai_Rodeh_Process:
    def __init__(self, number_of_ids: int, number_of_processes: int) -> None:
        """
        N é o número total de processos

        K é o número total de IDs disponíveis

        ID é a identidade do processo (os IDs podem repetir)

        STATE varia entre {ACTIVE, PASSIVE, LEADER}

        ROUND representa o número do round de eleição atual

        Cada processo possui sua MESSAGE QUEUE

        Todo processo envia uma mensagem para o próximo do ciclo
        """
        self.__number_of_ids = number_of_ids
        self.__number_of_processes = number_of_processes

        self.__id = self.generate_id()
        self.__state = States.ACTIVE
        self.__round = 1

        self.message_queue = Queue()

    def generate_id(self) -> int:
        """
        o valor do ID é gerado aleatoriamente
        """
        return randint(1, self.__number_of_ids)
    
    def send_message(self, message: Message) -> None:
        """
        Inserindo a mensagem na MESSAGE QUEUE do processo
        seguinte no ciclo
        """
        self.__next_process.message_queue.put(message)

    def run(self, next_process) -> None:
        """
        Enviando a primeira mensagem para o processo adjacente
        """
        self.__next_process = next_process
        message = Message(self.__id, self.__round)
        self.send_message(message)

        """
        A execução só termina quando todo processo estiver no estado PASSIVE
        ou ter sido eleito como líder e quando não restarem mais mensagens na
        MESSAGE QUEUE

        O comportamento dos processos está descrito no Tópico 2.1 do artigo
        da pasta DATA
        """
        while(True):
            if not self.message_queue.empty():
                message = self.message_queue.get()
                print(f"O processo {self.__id} recebeu a mensagem ({message.get_id()}, {message.get_round()}, {message.hop}, {message.bit})", flush=True)
            else:
                continue

            match self.__state:
                case States.PASSIVE:
                    message.hop += 1
                    self.send_message(message)
                    if message.get_round() == -1:
                        if self.message_queue.empty():
                            return
                        else:
                            print("ERROR: Message Queue not empty!", flush=True)
                            return
                case States.ACTIVE:
                    if message.get_round() == -1:
                        print("ERROR: Active process found", flush=True)
                        return
                    if (
                        message.hop == self.__number_of_processes
                        and message.bit == True
                    ):
                        self.__state = States.LEADER
                        print("Eu sou o Líder", flush=True)
                        message = Message(self.__id, -1)
                        self.send_message(message)
                    elif (
                        message.hop == self.__number_of_processes
                        and message.bit == False
                    ):
                        self.__id = self.generate_id()
                        self.__round += 1
                        message = Message(self.__id, self.__round)
                        self.send_message(message)
                    elif (
                        (message.get_id(), message.get_round()) == (self.__id, self.__round) 
                        and (message.hop < self.__number_of_processes)
                    ):
                        message.hop += 1
                        message.bit = False
                        self.send_message(message)
                    elif (
                        (message.get_id(), message.get_round()) > (self.__id, self.__round)
                    ):
                        self.__state = States.PASSIVE
                        message.hop += 1
                        self.send_message(message)
                    elif (
                        (message.get_id(), message.get_round()) < (self.__id, self.__round)
                    ):
                        pass
                case States.LEADER:
                    if self.message_queue.empty():
                        return
                    else:
                        print("ERROR: Message Queue not empty!", flush=True)
                        return
