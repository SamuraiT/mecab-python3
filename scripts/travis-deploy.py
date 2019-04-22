#! /usr/bin/env python3

from glob import glob
from os import environ
from sys import stderr, exit

from utils import run, activate_venv


def do_deployment(tag, os):
    # Check whether there is anything to deploy.
    # We expect built wheels in the "wheelhouse" directory.
    wheels = glob("wheelhouse/*-{}-*.whl".format(tag))
    if not wheels:
        stderr.write("No wheels to deploy for tag '{}'??\n".format(tag))
        run("ls", "-l", "wheelhouse")
        exit(1)

    activate_venv("build/venv")
    run("pip", "install", "twine")

    # If this is the Linux build, also generate an sdist tarball;
    # cibuildwheel does not do this for us.
    if os == "linux":
        run("python", "setup.py", "sdist")
        sdists = glob("dist/*-{}.tar.gz".format(tag))
        if sdists:
            run("twine", "check", *sdists)
            wheels.extend(sdists)
        else:
            stderr.write("No sdist to deploy for tag '{}'??\n".format(tag))
            run("ls", "-l", "dist")
            exit(1)

    # Twine will pick up the username, password, and repo URL from the
    # environment.
    run("twine", "upload", "--verbose", "--disable-progress-bar", *wheels)


def main():
    # Only run deployment if we're a tagged release, not a pull
    # request, used cibuildwheel to do the builds, and all necessary
    # Twine parameters are set.
    build_driver   = environ.get("DRIVER", "")
    travis_os      = environ.get("TRAVIS_OS_NAME", "")
    travis_branch  = environ.get("TRAVIS_BRANCH", "")
    travis_tag     = environ.get("TRAVIS_TAG", "")
    travis_pr      = environ.get("TRAVIS_PULL_REQUEST", "")
    twine_user     = environ.get("TWINE_USERNAME", "")
    twine_password = environ.get("TWINE_PASSWORD", "")
    twine_repo     = environ.get("TWINE_REPOSITORY_URL", "")

    stderr.write("Deployment-related environment variables:\n"
                 "DRIVER               = {!r}\n"
                 "TRAVIS_OS_NAME       = {!r}\n"
                 "TRAVIS_BRANCH        = {!r}\n"
                 "TRAVIS_TAG           = {!r}\n"
                 "TRAVIS_PULL_REQUEST  = {!r}\n"
                 "TWINE_USERNAME       = {!r}\n"
                 "TWINE_PASSWORD       = {}\n"
                 "TWINE_REPOSITORY_URL = {!r}\n"
                 "\n".format(
                     build_driver, travis_os,
                     travis_branch, travis_tag, travis_pr,
                     twine_user, "[REDACTED]" if twine_password else "''",
                     twine_repo
                 ))

    if not (build_driver == "cibuildwheel"
            and travis_tag
            and travis_tag == travis_branch
            and travis_pr in ("", "false")
            and twine_user and twine_password):
        stderr.write("No deployment for this build.\n")
        exit(0)

    do_deployment(travis_tag, travis_os)


if __name__ == "__main__":
    main()
