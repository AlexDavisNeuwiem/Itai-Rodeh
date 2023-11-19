class Message:
    def __init__(self, id: int, round: int) -> None:
        """
        The values of ID and ROUND are taken from the process that sends the message.

        HOP is a counter that initially has the value one, and which is increased by
        one every time it is passed on by a process.

        BIT is a bit that initially is true, and which is set to false when it visits
        a process that has the same identity but that is not its originator.
        """
        self.id = id
        self.round = round
        self.hop = 0  # Talvez precise ser inicializado com 0
        self.bit = True
