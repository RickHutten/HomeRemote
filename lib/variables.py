from ast import literal_eval

class ServerVariables():
    def __init__(self):
        self.filename = "./data/server_variables"
        # If the file does not exist, make a new one
        try:
            # No errors if it exists
            f = open(self.filename, "r")
            f.close()
        except IOError:
            # File does not exist
            f = open(self.filename, "w")
            f.close()

    def get(self, key):
        if type(key) != type(""):
            raise ValueError("Argument should be string not of type: " + str(type(key)))
        key = key.strip()
        f = open(self.filename, "r")
        for line in f:
            linesplit = line.split("=")
            if linesplit[0].strip() == key:
                f.close()
                return literal_eval(linesplit[1].strip())
        # Item not found
        f.close()
        raise LookupError("Item not found: " + key)

    def put(self, key, value):
        # Puts variable in file. Overwrites if already present.
        if type(key) != type(""):
            raise ValueError("First argument should be string not of type: " + str(type(key)))
        if type(value) not in [int, float, str, list, dict, tuple, bool, type(None)]:
            raise ValueError("Value type not supported: " + str(type(value)))
        key = key.strip()
        # Check if key already exists
        f = open(self.filename, "r")
        for i, line in enumerate(f):
            linesplit = line.split("=")
            if linesplit[0].strip() == key:
                # Line already exists
                f.close()
                line_no = i
                break
        else:
            # Line does not exists
            f.close()
            # Append to file
            f = open(self.filename, "a")
            if type(value) == type(""):
                f.write(key + " = '" + str(value) + "'\n")
            else:
                f.write(key + " = " + str(value) + "\n")
            f.close()
            return
        # Line already exists
        f = open(self.filename, "r")
        lines = f.readlines()
        if type(value) == type(""):
            lines[line_no] = key + " = '" + str(value) + "'\n"
        else:
            lines[line_no] = key + " = " + str(value) + "\n"
        f.close()
        f = open(self.filename, "w")
        f.writelines(lines)
        f.close()

    def contains(self, key):
        # Return True/False if file contains key
        if type(key) != type(""):
            raise ValueError("Argument should be string not of type: " + str(type(key)))
        key = key.strip()
        f = open(self.filename, "r")
        for line in f:
            if line.split("=")[0].strip() == key:
                f.close()
                return True
        f.close()
        return False
