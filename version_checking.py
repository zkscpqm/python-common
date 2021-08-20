import sys


class PythonVersion:
    """
    This is an ugly but robust way to compare python versions. Do not add types to this class or any other
    PY3+ flavour.
    """

    def __init__(self, major, minor=0, revision=0):
        self.major = major
        self.minor = minor
        self.revision = revision

    @classmethod
    def from_tuple(cls, ver):
        return PythonVersion(ver[0], ver[1], ver[2])

    def as_tuple(self):
        return self.major, self.minor, self.revision

    @classmethod
    def _convert_other(cls, other):
        if isinstance(other, cls):
            return other.as_tuple()

        elif isinstance(other, tuple):
            return other

        raise TypeError("PythonVersion can only be compared to PythonVersion, tuple.")

    def __eq__(self, other):
        other = self._convert_other(other)
        return self.as_tuple() == other

    def __lt__(self, other):
        other = self._convert_other(other)
        return self.as_tuple() < other

    def __gt__(self, other):
        other = self._convert_other(other)
        return self.as_tuple() > other

    def __le__(self, other):
        other = self._convert_other(other)
        return self.as_tuple() <= other

    def __ge__(self, other):
        other = self._convert_other(other)
        return self.as_tuple() >= other

    def __ne__(self, other):
        other = self._convert_other(other)
        return self.as_tuple() != other

    def __str__(self):
        return "PythonVersion(%s, %s, %s)" % (self.major, self.minor, self.revision)


def get_current_version():
    return PythonVersion.from_tuple(sys.version_info)


def _assert_py_version(required):
    if get_current_version() < required:
        raise DinosaurException(required)


class DinosaurException(Exception):

    def __init__(self, required):
        self.required = required

    def __str__(self):
        msg = "Your python version is older than the Queen of England. If you want to do what you're trying to do," \
              "please come out of the stone ages and join civilized society.\nRequired: %s\nActual: %s" % (
                  self.required,
                  get_current_version()
              )
        return msg
