from ast import literal_eval

class ServerVariables():
    def __init__(self):
        self.filename = "./data/server_variables"
        # If the file does not exist, make a new one
        try:
            # Try to read the file
            open(self.filename, "r").close()
        except IOError:
            # File does not exist, create new
            open(self.filename, "w").close()

    def get(self, key):
        if type(key) != str:
            raise ValueError("Argument should be string not of type: " + str(type(key)))
        key = key.strip()
        f = open(self.filename, "r")
        for line in f:
            linesplit = line.split("=")
            if linesplit[0].strip() == key:
                f.close()
                return literal_eval(linesplit[1].strip())
        # Key not found
        f.close()
        raise LookupError("Key not found: " + key)

    def put(self, key, value):
        # Puts key with corresponding value in file. Overwrites if already present.
        if type(key) != str:
            raise ValueError("First argument should be string not of type: " + str(type(key)))
        if type(value) not in [int, float, str, list, dict, tuple, bool, type(None)]:
            raise ValueError("Value type not supported: " + str(type(value)))
        key = key.strip()
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
            return
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

    def contains(self, key):
        # Return True/False if file contains key
        if type(key) != str:
            raise ValueError("Argument should be string not of type: " + str(type(key)))
        key = key.strip()
        f = open(self.filename, "r")
        for line in f:
            if line.split("=")[0].strip() == key:
                f.close()
                return True
        f.close()
        return False