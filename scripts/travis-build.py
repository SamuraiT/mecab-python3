#! /usr/bin/env python

import os
import sys

from utils import activate_venv, mkdir_p, setenv, run, run_output
from build_requirements import SWIG

#
# Driver: tox
# currently only supports Ubuntu 16.04LTS (xenial), which is the
# most up-to-date Linux environment available via Travis, and
# installing many Pythons into it is straightforward
#


def tox_ubuntu_install_buildreqs(MECAB):
    run("sudo", "add-apt-repository", "-y", "ppa:deadsnakes/ppa")
    run("sudo", "apt-get", "-y", "update")

    packages = [
        "python2.7-dev", "python3.5-dev", "python3.6-dev",
        "python3.7-dev", "tox", "swig"
    ]
    if MECAB == "system":
        packages.append("libmecab-dev")
        packages.append("mecab-ipadic-utf8")

    run("sudo", "apt-get", "-y", "install", *packages)


def tox_build(MECAB, TRAVIS_OS):

    if TRAVIS_OS != "linux":
        sys.stderr.write("Operating system {!r} not supported by tox mode\n"
                         .format(TRAVIS_OS))
        sys.exit(1)

    DISTRO = run_output("lsb_release", "-s", "-c")
    if DISTRO != "xenial":
        sys.stderr.write("Unrecognized Linux distribution: {}\n"
                         .format(DISTRO))
        sys.exit(1)

    tox_ubuntu_install_buildreqs(MECAB)

    for snake in ("python2.7", "python3.5", "python3.6", "python3.7"):
        run(snake, "--version")

    if MECAB == "system":
        run("mecab-config", "--version")

    run_output("tox", "--version")
    run("tox", "-vvv")

#
# Driver: cibuildwheel
#


def cibuildwheel_ubuntu_install_buildreqs():
    run("sudo", "apt-get", "-y", "update")
    run("sudo", "apt-get", "-y", "install", "virtualenv")


def cibuildwheel_ubuntu_prep_swig():
    SWIG.retrieve("build")


def cibuildwheel_ubuntu_prep_dictionary():
    try:
        with open("/etc/mecabrc", "rt") as fp:
            for line in fp:
                if line.startswith("dicdir"):
                    _, _, dicdir = line.partition("=")
                    dicdir = dicdir.strip()
                    break
            else:
                raise ValueError("no 'dicdir' line found")

    except (OSError, IOError) as e:
        sys.stderr.write("* /etc/mecabrc: {}\n", e.strerror())
        sys.exit(1)

    except Exception as e:
        sys.stderr.write("* /etc/mecabrc: {}\n", str(e))
        sys.exit(1)

    # dicdir may be a symlink, force resolution
    run("cp", "-a", dicdir+"/.", "build/dic")


def cibuildwheel_osx_install_buildreqs():
    # don't waste time on "cleanup"
    os.environ.pop("HOMEBREW_INSTALL_CLEANUP", None)
    os.environ["HOMEBREW_NO_INSTALL_CLEANUP"] = "yes"

    # TODO: All calls to brew can probably be removed
    run("brew", "update")
    run("brew", "--version")
    run("brew", "install", "swig")
    run("pip3", "install", "virtualenv")


def cibuildwheel_build(MECAB, TRAVIS_OS):

    if MECAB != "bundled":
        sys.stderr.write("cibuildwheel mode only supports bundled libmecab")
        sys.exit(1)

    if TRAVIS_OS == "linux":
        DISTRO = run_output("lsb_release", "-s", "-c")
        if DISTRO != "xenial":
            sys.stderr.write("Unrecognized Linux distribution: {}\n"
                             .format(DISTRO))
            sys.exit(1)

        mkdir_p("build")
        cibuildwheel_ubuntu_install_buildreqs()
        cibuildwheel_ubuntu_prep_swig()

    elif TRAVIS_OS == "osx":
        mkdir_p("build")
        cibuildwheel_osx_install_buildreqs()

    else:
        sys.stderr.write("Operating system {!r} not yet supported by "
                         "cibuildwheel mode\n"
                         .format(TRAVIS_OS))
        sys.exit(1)

    # The easiest way to install cibuildwheel is with pip, and pip
    # really wants to be working inside a virtualenv.
    run("virtualenv", "--version")
    run("python3", "--version")
    run("virtualenv", "-p", "python3", "build/venv")
    activate_venv("build/venv")

    run("pip", "install", "cibuildwheel")

    # environment variables to control cibuildwheel
    TEST_REQUIRES = "pytest"
    if MECAB == "bundled":
        TEST_REQUIRES += " unidic-lite"

    S = setenv
    S("CIBW_ENVIRONMENT", "MECAB_DICDIR=build/dic BUNDLE_LIBMECAB=true")
    S("CIBW_BEFORE_BUILD", "{project}/scripts/cibw-prepare-"+TRAVIS_OS+".py")
    S("CIBW_TEST_COMMAND", "pytest {project}/test/")
    S("CIBW_TEST_REQUIRES", TEST_REQUIRES)
    S("CIBW_BUILD_VERBOSITY", "3")

    run("cibuildwheel", "--output-dir", "wheelhouse")


def main():
    if not os.path.isfile("setup.py"):
        sys.stderr.write("setup.py missing - where is the package?\n")
        sys.exit(1)

    MECAB     = os.environ.get("MECAB", "<not set>")
    DRIVER    = os.environ.get("DRIVER", "<not set>")
    TRAVIS_OS = os.environ.get("TRAVIS_OS_NAME", "<not set>")

    if MECAB == "bundled":
        os.environ["BUNDLE_LIBMECAB"] = "true"
    elif MECAB == "system":
        os.environ.pop("BUNDLE_LIBMECAB", None)
    else:
        sys.stderr.write("Unrecognized MECAB value: {}\n".format(MECAB))
        sys.exit(1)

    if DRIVER == "tox":
        tox_build(MECAB, TRAVIS_OS)

    elif DRIVER == "cibuildwheel":
        cibuildwheel_build(MECAB, TRAVIS_OS)

    else:
        sys.stderr.write("Unrecognized DRIVER value: {}\n".format(DRIVER))
        sys.exit(1)


if __name__ == "__main__":
    main()
