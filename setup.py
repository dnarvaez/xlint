#!/usr/bin/env python3
# Copyright 2013 Daniel Narvaez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import stat
import subprocess
import tarfile
import urllib.request

base_dir = os.path.abspath(os.path.dirname(__file__))


def install_node():
    version = "0.8.21"

    url = "http://nodejs.org/dist/v%s/node-v%s.tar.gz" % (version, version)

    f = urllib.request.urlopen(url)
    with tarfile.open(fileobj=f, mode="r:gz") as tar:
        tar.extractall(base_dir)

    prefix_dir = os.path.join(base_dir, "linters", "node")
    source_dir = os.path.join(base_dir, "node-v%s" % version)

    try:
        try:
            shutil.rmtree(prefix_dir)
        except OSError:
            pass

        os.chdir(source_dir)

        subprocess.check_call(["./configure", "--prefix", prefix_dir]) 
        subprocess.check_call(["make"]) 
        subprocess.check_call(["make", "install"]) 

        subprocess.check_call([os.path.join(prefix_dir, "bin", "npm"),
                               "-g", "install", "jshint"])
    finally:
        shutil.rmtree(source_dir)


def create_virtualenv():
    version = "1.8.4"

    url = "https://pypi.python.org/packages/source/v/" \
          "virtualenv/virtualenv-%s.tar.gz" % version

    f = urllib.request.urlopen(url)
    with tarfile.open(fileobj=f, mode="r:gz") as tar:
        tar.extractall(base_dir)

    source_dir = os.path.join(base_dir, "virtualenv-%s" % version)
    env_dir = os.path.join(base_dir, "linters", "python")

    try:
        try:
            shutil.rmtree(env_dir)
        except OSError:
            pass

        subprocess.check_call(["python3",
                               os.path.join(source_dir, "virtualenv.py"),
                               env_dir])
    finally:
        shutil.rmtree(source_dir)

    bin_dir = os.path.join(env_dir, "bin")

    subprocess.check_call([os.path.join(bin_dir, "pip"), "install",
                           "pep8", "pyflakes"])

def download_html5check():
    url = "http://about.validator.nu/html5check.py"

    dest_path = os.path.join(base_dir, "linters", "python", "bin",
                             "html5check.py")

    request = urllib.request.urlopen(url)
    with open(dest_path, "wb") as f:
        f.write(request.read())

    os.chmod(dest_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


def main():
    create_virtualenv()
    download_html5check()
    install_node()


main()
