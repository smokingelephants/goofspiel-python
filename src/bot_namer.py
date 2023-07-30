Name = str


class BotNamer(object):
    def next_name(self) -> Name:
        raise NotImplementedError


class NumberedNamer(object):
    def __init__(self):
        self.counter = 1
        super().__init__()

    def next_name(self) -> Name:
        name = f"Bot #{self.counter}"
        self.counter += 1
        return name


default = NumberedNamer
