import attr


# TODO: Bid and Card should kinda match...
Bid = int
# TODO: Consider making this a strong type
Card = int


# TOOD: Move to another file
class GoofErrors(Exception):
    """Any error that's specific to this program's code."""

    pass

