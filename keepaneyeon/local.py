import os
import os.path
import shutil
import errno

class LocalStorage():
    def __init__(self, path):
        self.path = path

    def path_for_name(self, name):
        """
        Return full file path for the named file.
        """
        return os.path.join(self.path, name)

    def exists(self, name):
        """
        Determine whether the named file exists.
        """
        return os.path.isfile(self.path_for_name(name))

    @staticmethod
    def ensure_directory(path):
        directory = os.path.dirname(path)
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def store_from_filename(self, name, filename):
        """
        Store given filename under the provided name.
        """
        path = self.path_for_name(name)
        self.ensure_directory(path)
        return shutil.copyfile(filename, path)

    def store_from_string(self, name, string):
        """
        Store given string under the provided name.
        """
        path = self.path_for_name(name)
        self.ensure_directory(path)
        with open(path, 'wb') as f:
            f.write(string)
