# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright 2019 igo95862

# This file is part of bubblejail.
# bubblejail is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# bubblejail is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with bubblejail.  If not, see <https://www.gnu.org/licenses/>.


from dataclasses import dataclass, field
from typing import FrozenSet, Optional, Tuple, Union


@dataclass
class BwrapConfigBase:
    arg_word: str = field(init=False)

    def to_args(self) -> Tuple[str, ...]:
        return (self.arg_word, )


@dataclass
class ReadOnlyBind(BwrapConfigBase):
    arg_word = '--ro-bind'
    source: str
    dest: Optional[str] = None

    def to_args(self) -> Tuple[str, str, str]:
        return (self.arg_word,
                self.source,
                self.dest if self.dest is not None else self.source)


@dataclass
class DirCreate(BwrapConfigBase):
    arg_word = '--dir'
    dest: str

    def to_args(self) -> Tuple[str, str]:
        return self.arg_word, self.dest


@dataclass
class Symlink(BwrapConfigBase):
    arg_word = '--symlink'
    source: str
    dest: str

    def to_args(self) -> Tuple[str, str, str]:
        return self.arg_word, self.source, self.dest


@dataclass
class FileTransfer:
    content: bytes
    dest: str


@dataclass
class EnvrimentalVar(BwrapConfigBase):
    arg_word = '--setenv'
    var_name: str
    var_value: str

    def to_args(self) -> Tuple[str, str, str]:
        return self.arg_word, self.var_name, self.var_value


@dataclass
class Bind(BwrapConfigBase):
    arg_word = '--bind'
    source: str
    dest: Optional[str] = None

    def to_args(self) -> Tuple[str, str, str]:
        return (self.arg_word,
                self.source,
                self.dest if self.dest is not None else self.source)


@dataclass
class DevBind(Bind):
    arg_word = '--dev-bind'


@dataclass
class BwrapConfig:
    binds: Tuple[Union[Bind, DevBind], ...] = tuple()
    read_only_binds: Tuple[ReadOnlyBind, ...] = tuple()
    dir_create: Tuple[DirCreate, ...] = tuple()
    symlinks: Tuple[Symlink, ...] = tuple()
    files: Tuple[FileTransfer, ...] = tuple()
    enviromental_variables: Tuple[EnvrimentalVar, ...] = tuple()
    env_no_unset: FrozenSet[str] = frozenset()
    extra_args: Tuple[str, ...] = tuple()
    share_network: bool = False
