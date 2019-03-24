#! /usr/bin/env python

import os
import sys

from utils import run, run_output

def install_dead_snakes_ubuntu():
    run("sudo", "add-apt-repository", "-y", "ppa:deadsnakes/ppa")
    run("sudo", "apt-get", "-y", "update")

    run("sudo", "apt-get", "-y", "install",
        "python2.7-dev", "python3.4-dev", "python3.5-dev",
        "python3.6-dev", "python3.7-dev")

def install_buildreqs_ubuntu(MECAB):
    install_dead_snakes_ubuntu()

    packages = ["tox", "swig", "mecab-ipadic-utf8"]
    if MECAB == "system":
        packages.append("libmecab-dev")

    run("sudo", "apt-get", "-y", "install", *packages)

def smoke_test():
    for snake in ("python2.7", "python3.4",
                  "python3.5", "python3.6", "python3.7"):
        run(snake, "--version")
    try:
        run("mecab-config", "--version")
    except SystemExit:
        pass

def run_tox_builds():
    run_output("tox", "--version")
    run("tox", "-vvv")

def main():
    MECAB     = os.environ.get("MECAB", "<not set>")
    DRIVER    = os.environ.get("DRIVER", "<not set>")
    TRAVIS_OS = os.environ.get("TRAVIS_OS_NAME", "<not set>")

    if DRIVER != "tox":
        sys.stderr.write("Unrecognized DRIVER value: {}\n".format(DRIVER))
        sys.exit(1)

    if MECAB == "bundled":
        os.environ["BUNDLE_LIBMECAB"] = "true"
    elif MECAB == "system":
        if "BUNDLE_LIBMECAB" in os.environ:
            del os.environ["BUNDLE_LIBMECAB"]
    else:
        sys.stderr.write("Unrecognized MECAB value: {}\n".format(MECAB))
        sys.exit(1)

    if TRAVIS_OS == "linux":
        DISTRO = run_output("lsb_release", "-s", "-c")
        if DISTRO == "xenial":
            install_buildreqs_ubuntu(MECAB)
        else:
            sys.stderr.write("Unrecognized Linux distribution: {}\n"
                             .format(DISTRO))
            sys.exit(1)

    else:
        sys.stderr.write("Unrecognized TRAVIS_OS_NAME value: {}\n"
                         .format(TRAVIS_OS))
        sys.exit(1)

    smoke_test()
    run_tox_builds()

if __name__ == "__main__":
    main()
