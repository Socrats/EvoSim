from enum import Enum, unique


@unique
class AbstractActions(Enum):
    def next_action(self):
        pass


@unique
class TwoActions(AbstractActions):
    cooperate = 0
    defect = 1


@unique
class ThreeActions(AbstractActions):
    cooperate = 0
    defect = 1
    inspect = 2


def action_factory(args):
    def factory():
        pass

    return factory
