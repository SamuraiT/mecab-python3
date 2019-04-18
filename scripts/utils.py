# Utility routines used by the scripts in this directory.
# These scripts need to work correctly with Python 2.7 and 3.4
# as well as newer versions; in particular, subprocess.run cannot
# be used, and we need fallbacks for shlex.quote and os.cpu_count.

import hashlib
import locale
import os
import subprocess
import sys
import tempfile

__all__ = [
    "get_parallel_jobs",
    "sh_quote", "log_cmd", "run", "run_output",
    "activate_venv", "chdir", "mkdir_p", "setenv", "symlink", "touch",
    "Downloadable"
]

OUTPUT_ENCODING = locale.getpreferredencoding(True)


#
# Intuit the available parallelism
#
def get_parallel_jobs():
    def _get_parallel_jobs():
        try:
            return max(len(os.sched_getaffinity(0)), 1)
        except Exception:
            pass

        try:
            return os.cpu_count() or 1
        except Exception:
            pass

        try:
            from multiprocessing import cpu_count
            return cpu_count() or 1
        except Exception:
            pass

        return 1

    global _parallel_jobs
    try:
        return _parallel_jobs
    except NameError:
        _parallel_jobs = pj = _get_parallel_jobs()
        return pj


#
# Running subprocesses
#
try:
    from shlex import quote as sh_quote
except ImportError:
    from pipes import quote as sh_quote


def log_cmd(argv):
    sys.stderr.write("+ " + " ".join(sh_quote(arg) for arg in argv) + "\n")
    sys.stderr.flush()


def run(*argv):
    log_cmd(argv)
    try:
        subprocess.check_call(argv)

    except subprocess.CalledProcessError as e:
        if e.returncode > 0:
            sys.stderr.write("* {}: exit {}\n".format(
                sh_quote(argv[0]), e.returncode))
        else:
            sys.stderr.write("* {}: signal {}\n".format(
                sh_quote(argv[0]), -e.returncode))
        sys.exit(1)

    except OSError as e:
        sys.stderr.write("* {}: {}\n".format(sh_quote(argv[0]), e.strerror))
        sys.exit(1)

    except Exception as e:
        sys.stderr.write("* {}: {}\n".format(sh_quote(argv[0]), str(e)))
        sys.exit(1)


def run_output(*argv):
    sys.stderr.write("+ $(" + " ".join(sh_quote(arg) for arg in argv) + ") = ")
    sys.stderr.flush()
    raw_output = b''
    try:
        raw_output = subprocess.check_output(argv)
        output = raw_output.decode(OUTPUT_ENCODING).strip()
        if "\n" in output:
            sys.stderr.write('"""\n' + output + '\n"""\n')
        else:
            sys.stderr.write(sh_quote(output) + "\n")
        return output

    except subprocess.CalledProcessError as e:
        if e.returncode > 0:
            sys.stderr.write("*\n* {}: exit {}\n".format(
                sh_quote(argv[0]), e.returncode))
        else:
            sys.stderr.write("*\n* {}: signal {}\n".format(
                sh_quote(argv[0]), -e.returncode))
        sys.exit(1)

    except OSError as e:
        sys.stderr.write("*\n* {}: {}\n".format(sh_quote(argv[0]), e.strerror))
        sys.exit(1)

    except Exception as e:
        sys.stderr.write("*\n* {}: decoding subprocess output: {}\n"
                         "* raw output: {!r}\n"
                         .format(sh_quote(argv[0]), str(e), raw_output))
        sys.exit(1)

#
# Things that don't require spawning a subprocess or wouldn't work in
# a subprocess.
#


def activate_venv(venv_dir):
    # This does approximately what ". ${venv_dir}/bin/activate" would do
    # if this were a shell script.  The major difference is that we make
    # no provision for deactivating the venv again, because nobody needs
    # that at the moment.  We also don't dink with PS1.
    venv_dir = os.path.abspath(venv_dir)
    if os.path.isfile(os.path.join(venv_dir, "bin", "activate")):
        bin_dir = "bin"
    elif os.path.isfile(os.path.join(venv_dir, "Scripts", "activate")):
        bin_dir = "Scripts"
    else:
        sys.stderr.write("* {!r} does not appear to be a virtualenv"
                         .format(venv_dir))
        sys.exit(1)

    os.environ["VIRTUAL_ENV"] = venv_dir
    os.environ["PATH"] = (
        os.path.join(venv_dir, bin_dir)
        + os.pathsep + os.environ["PATH"]
    )
    os.environ.pop("PYTHONHOME", None)

    # https://bugs.python.org/issue22490
    os.environ.pop("__PYVENV_LAUNCHER__", None)

    log_cmd(["activate_venv", venv_dir])


def chdir(dest):
    log_cmd(["cd", dest])
    try:
        os.chdir(dest)
    except OSError as e:
        sys.stderr.write("* cd: {}: {}\n".format(sh_quote(dest), e.strerror))
        sys.exit(1)


def mkdir_p(dir):
    log_cmd(["mkdir", "-p", dir])
    # In 2.7, os.makedirs does not have the exist_ok parameter.
    if os.path.isdir(dir):
        return
    try:
        os.makedirs(dir)
    except OSError as e:
        if hasattr(e, 'filename'):
            sys.stderr.write("* mkdir: {}: {}\n".format(
                sh_quote(e.filename), e.strerror))
        else:
            sys.stderr.write("* mkdir: {}: {}\n".format(
                sh_quote(dir), e.strerror))
        sys.exit(1)


def setenv(key, value):
    log_cmd(["export", "{}={}".format(key, value)])
    os.environ[key] = value


def symlink(src, dest):
    log_cmd(["ln", "-s", src, dest])
    try:
        os.symlink(src, dest)
    except OSError as e:
        if hasattr(e, 'filename'):
            sys.stderr.write("* ln: {}: {}\n".format(
                sh_quote(e.filename), e.strerror))
        else:
            sys.stderr.write("* ln: {}: {}\n".format(
                sh_quote(dest), e.strerror))
        sys.exit(1)


def touch(path):
    log_cmd(["touch", path])
    try:
        os.utime(path, None)
    except OSError as e:
        sys.stderr.write("* touch: {}: {}\n".format(
            sh_quote(path), e.strerror))
        sys.exit(1)

#
# Downloading tarballs
#


class Downloadable(object):
    def __init__(self, name, url, hash, unpacked_name=None):
        self.name = name
        self.url  = url
        self.hash = hash
        self.unpacked_name = unpacked_name

    def retrieve(self, destdir="."):
        fd = None
        tfname = None
        try:
            (fd, tfname) = tempfile.mkstemp(prefix=self.name + ".",
                                            dir=destdir)
            run("curl", "-L", "-o", tfname, self.url)

            h = hashlib.sha256()
            while True:
                blk = os.read(fd, 8192)
                if not blk:
                    break
                h.update(blk)

            digest = h.hexdigest()
            if digest != self.hash:
                sys.stderr.write("* SHA256 mismatch for {}:\n"
                                 "*  expected {}\n"
                                 "*       got {}\n"
                                 .format(self.url, self.hash, digest))
                sys.exit(1)

            os.close(fd)
            fd = None
            os.rename(tfname, os.path.join(destdir, self.name))
            return

        except:  # noqa: E722: bare except used intentionally, with reraise
            if fd is not None:
                os.close(fd)
            if tfname is not None:
                os.unlink(tfname)
            raise
