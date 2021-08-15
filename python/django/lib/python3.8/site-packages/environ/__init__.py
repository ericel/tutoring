# This file is part of the django-environ-2.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (C) 2013-2021 Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The top-level module for django-environ-2 package.

This module tracks the version of the package as well as the base
package info used by various functions within django-environ-2.

Modules:

    compat
    environ

Classes:

    Env
    NoValue
    Path

Misc variables:

    __copyright__
    __version__
    __license__
    __author__
    __author_email__
    __maintainer__
    __maintainer_email__
    __url__
    __description__
    logger
    DJANGO_POSTGRES
    REDIS_DRIVER

Refer to the `documentation <https://django-environ-2.readthedocs.io/>`_
for details on the use of this package.
"""

from .environ import *


__copyright__ = 'Copyright (C) 2021 Serghei Iakovlev'
__version__ = '2.1.0'
__license__ = 'MIT'
__author__ = 'Daniele Faraglia'
__author_email__ = 'daniele.faraglia@gmail.com'
__maintainer__ = 'Serghei Iakovlev'
__maintainer_email__ = 'egrep@protonmail.ch'
__url__ = 'https://django-environ-2.readthedocs.io'
__description__ = 'Configure Django made easy.'
