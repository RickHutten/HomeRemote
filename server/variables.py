from ast import literal_eval
from threading import Lock

class ServerVariables:

    # Declaring constants
    PLAYING = 0
    PAUSED = 1
    STOPPED = 2

    lock = Lock()  # Thread lock for accessing the file
    glob = dict()  # Global dictionary holding all variables

    def __init__(self):
        self.filename = "./data/server_variables"
        # If the file does not exist, make a new one
        try:
            # Try to read the file
            open(self.filename, "r").close()
        except IOError:
            # File does not exist, create new and dont fill global variable
            open(self.filename, "w").close()
            return

        # Now that a file is present, fill global variable with variables
        f = open(self.filename, "r")
        for line in f:
            linesplit = line.split("=")
            # Get key and values from file
            key = linesplit[0].strip()
            value = literal_eval(linesplit[1].strip())
            # Save in global variable
            self.glob[key] = value

    def get(self, key, default):
        if self.contains(key):
            return self.glob[key]
        else:
            return default

    def put(self, key, value, writeToFile=True):
        # Check if the key and value are of the correct types
        if type(key) != str:
            raise TypeError(
                "First argument should be string not of type: " + str(
                    type(key)))
        if type(value) not in [int, float, str, list, dict, tuple, bool,
                               type(None)]:
            raise TypeError(
                "Value type not supported: " + str(type(value)))

        # Save variable in global
        key = key.strip()
        self.glob[key] = value

        if not writeToFile:
                # Don't write the key and value to file
                return

        # Write key to file
        self.lock.acquire()  # Acquire lock
        try:
            # Check if key already exists
            f = open(self.filename, "r")
            for i, line in enumerate(f):
                linesplit = line.split("=")
                if linesplit[0].strip() == key:
                    # Key already exists
                    f.close()
                    line_no = i
                    break
            else:
                # Key does not exists
                f.close()
                # Append to file
                f = open(self.filename, "a")
                if type(value) == str:
                    f.write(key + " = '" + str(value) + "'\n")
                else:
                    f.write(key + " = " + str(value) + "\n")
                f.close()
                return  # Finally will be called where the lock will be released
            # Key already exists
            f = open(self.filename, "r")
            lines = f.readlines()
            if type(value) == str:
                lines[line_no] = key + " = '" + str(value) + "'\n"
            else:
                lines[line_no] = key + " = " + str(value) + "\n"
            f.close()
            # Overwrite new lines to file
            f = open(self.filename, "w")
            f.writelines(lines)
            f.close()
        finally:
            # Release lock
            self.lock.release()

    def contains(self, key):
        # Returns whether the key exists in the varible
        if type(key) != str:
            raise TypeError(
                "Argument should be string not of type: " + str(type(key)))
        return key in self.glob.keys()

    def get_from_file(self, key, default):
        ### Should not be used any more! ###
        # Reads file and returns it's value
        self.lock.acquire()
        try:
            if type(key) != str:
                raise TypeError(
                    "Argument should be string not of type: " + str(type(key)))
            key = key.strip()
            f = open(self.filename, "r")
            for line in f:
                linesplit = line.split("=")
                if linesplit[0].strip() == key:
                    f.close()
                    # Finally will be called where the lock will be released
                    return literal_eval(linesplit[1].strip())
            # Key not found, return default value
            f.close()
        finally:
            self.lock.release()
        return default

    def contains_in_file(self, key):
        ### Should not be used any more! ###
        # Return True/False if file contains key
        if type(key) != str:
            raise TypeError(
                "Argument should be string not of type: " + str(type(key)))
        key = key.strip()
        f = open(self.filename, "r")
        for line in f:
            if line.split("=")[0].strip() == key:
                f.close()
                return True
        f.close()
        return False
