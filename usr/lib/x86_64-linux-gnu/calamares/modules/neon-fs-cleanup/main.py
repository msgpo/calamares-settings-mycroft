# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Harald Sitter <sitter@kde.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of
# the License or any later version accepted by the membership of
# KDE e.V. (or its successor approved by the membership of KDE
# e.V.), which shall act as a proxy defined in Section 14 of
# version 3 of the license.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil

import libcalamares
from libcalamares.utils import check_target_env_call

def run():
    """ Cleaning up filesystem tools (must run after packages cleanup) """

    optional_filesystems = {
        'btrfs': 'btrfs-tools',
        'jfs': 'jfsutils',
        'reiserfs': 'reiserfsprogs',
        'xfs': 'xfsprogs'
    }

    partitions = libcalamares.globalstorage.value('partitions')

    # Drop all actually used filesystems from the optional dict.
    for partition in partitions:
        fs = partition['fs']
        if fs in optional_filesystems.keys():
            del optional_filesystems[fs]

    pkgs = list(optional_filesystems.values())
    if len(pkgs) > 0:
        check_target_env_call(["apt-get", "--purge", "-q", "-y",
                               "remove"] + pkgs)
        check_target_env_call(["apt-get", "--purge", "-q", "-y",
                               "autoremove"])

    return None
