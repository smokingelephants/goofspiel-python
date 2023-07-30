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


class AliceBenjamin(object):
    _ALL_NAMES = [
        "Alice",
        "Benjamin",
        "Chen",
        "Diana",
        "Ethan",
        "Fatima",
        "Gabriela",
        "Harold",
        "Isabella",
        "Jack",
        "Kofi",
        "Lily",
        "Miguel",
        "Natalia",
        "Olivia",
        "Patrick",
        "Qi",
        "Rafael",
        "Sarah",
        "Thomas",
        "Uma",
        "Victoria",
        "William",
        "Xiao",
        "Yasmin",
        "Zara",
    ]
    
    def __init__(self):
        self.counter = 0
        super().__init__()

    def next_name(self) -> Name:
        name = self._ALL_NAMES[self.counter%26]
        self.counter += 1
        return name


default = NumberedNamer
