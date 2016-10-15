################
# evoSim
# Copyright © 2016 Elias F. Domingos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#################


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


@unique
class FourActions(AbstractActions):
    CnI = 0
    DnI = 1
    CI = 2
    DI = 3


def action_factory(args):
    def factory():
        pass

    return factory
