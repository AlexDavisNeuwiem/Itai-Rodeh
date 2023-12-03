class MessageQueue:

    def __init__(self):
        self.queue = []
        self.last_seen = -1

    def add_message(self, message):
        self.queue.append(message)

    def get_new_message(self):
        self.last_seen += 1
        return self.queue[self.last_seen]

    def empty(self):
        return self.last_seen + 1 == len(self.queue)
