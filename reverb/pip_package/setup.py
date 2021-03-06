# python3
# Copyright 2019 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Installs dm-reverb."""
import fnmatch
import os
import datetime
from setuptools import find_packages
from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.install import install as InstallCommandBase
import sys

import reverb_version


if '--release' in sys.argv:
  release = True
  sys.argv.remove('--release')
  version = reverb_version.__rel_version__
else:
  # Build a nightly package by default.
  release = False
  version = reverb_version.__dev_version__
  version += datetime.datetime.now().strftime('%Y%m%d')

if release:
  project_name = 'dm-reverb'
else:
  # Nightly releases use date-based versioning of the form
  # '0.0.1.dev20180305'
  project_name = 'dm-reverb-nightly'


class BinaryDistribution(Distribution):

  def has_ext_modules(self):
    return True


def find_files(pattern, root):
  """Return all the files matching pattern below root dir."""
  for dirpath, _, files in os.walk(root):
    for filename in fnmatch.filter(files, pattern):
      yield os.path.join(dirpath, filename)


class InstallCommand(InstallCommandBase):
  """Override the dir where the headers go."""

  def finalize_options(self):
    ret = super().finalize_options()
    # We need to set this manually because we are not using setuptools to
    # compile the shared libraries we are distributing.
    self.install_lib = self.install_platlib
    return ret


setup(
    name=project_name,
    # TODO(b/155888926): Improve how we determine version(s).
    version=version,
    description=('Reverb is an efficient and easy-to-use data storage and '
                 'transport system designed for machine learning research.'),
    long_description='',
    long_description_content_type='text/markdown',
    author='DeepMind',
    author_email='DeepMind <no-reply@google.com>',
    url='https://github.com/deepmind/reverb',
    license='Apache 2.0',
    packages=find_packages(),
    headers=list(find_files('*.proto', 'reverb')),
    include_package_data=True,
    install_requires=['dm-tree', 'portpicker'],
    distclass=BinaryDistribution,
    cmdclass={
        'install': InstallCommand,
    },
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='tensorflow deepmind reinforcement learning machine replay jax',
)
