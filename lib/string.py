def cleanJSON(string):
    # Replaces "\\/" in strings with "/", f*cking JSON...
    s = ""
    for i in range(len(string)-1):
        if not (string[i] == "\\" and string[i+1] == "/"):
            s += string[i]	    
    return s + string[-1]
