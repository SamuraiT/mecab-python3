#! /opt/python/cp37-cp37m/bin/python3.7

# invoked with CIBW_BEFORE_BUILD="{project}/scripts/cibw-prepare-linux.py"
#
# expects to be run inside the manylinux1 Docker image, which is the
# ancient CentOS 5.11 distribution; many mod cons are not available;
# however, a comprehensive set of Pythons is available in /opt, hence
# the unusual shebang line above.
#
# expects the outer environment to have downloaded a SWIG source tarball
# and placed it at {project}/build/${SWIG.name}.

import sys
from os import path, getcwd
from utils import run, chdir, get_parallel_jobs
from build_requirements import SWIG


def main():
    chdir(path.dirname(path.dirname(path.abspath(__file__))))
    if not path.isfile("setup.py") or not path.isdir("build"):
        sys.stderr.write("* Failed to locate build directory\n")
        sys.stderr.write("* __file__={!r} cwd={!r}\n".format(
            __file__, getcwd()))
        run("ls", "-l")
        sys.exit(1)

    # Don't rebuild swig if it's already been built.
    if path.isfile("/usr/local/bin/swig"):
        sys.stderr.write("SWIG has already been built and installed.\n")
        sys.stderr.flush()
        return

    chdir("build")
    run("tar", "zxf", SWIG.name)
    chdir(SWIG.unpacked_name)

    run("./configure", "--without-maximum-compile-warnings",
        "--without-pcre", "--without-alllang",
        "--with-python=/opt/python/cp27-cp27mu/bin/python",
        "--with-python3=/opt/python/cp37-cp37m/bin/python3")

    run("make", "-j{}".format(get_parallel_jobs()))
    run("make", "install")


if __name__ == "__main__":
    main()
