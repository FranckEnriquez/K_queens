def print_board(individual):
    genotype = individual.genotype
    n = len(genotype)
    for i in range(0, n):
        text = ""
        for j in range(0, n):
            if genotype[j] == i:
                text += "[Q]"
            else:
                text += "[ ]"
        print(text)


def read_qap_entry_from_file(file_name):
    import os.path

    # Reading data from file_name
    data_file_name = file_name + ".dat.txt"
    if not os.path.isfile(data_file_name):
        raise Exception("File name: {} doesn't exists".format(data_file_name))

    # Reading file from path file_name
    f = open(data_file_name, "r")

    text = f.read()

    # Splitting file by rows
    text = text.split('\n')

    # Result variables n, matrix A and matrix B
    n = 0
    A = list()
    B = list()

    """
    "i" is a flag used to know what variable we are reading on text

    0: Reading "n"
    1: Reading matrix "A"
    2: Reading matrix "B"
    """
    i = 0
    # Start reading rows, from start to the end
    while len(text) != 0:
        # word makes its a row from the text, as a string
        word = text.pop(0)
        # Points to list A or B, depending on flag value
        current_list = A if i == 1 else B

        # When we reach a blank space, it means we have finished to read a certain variable
        if word == "":
            i += 1
        # Reading "n"
        elif i == 0:
            n = int(word)
        # Reading matrix "A" or "B"
        else:
            # Converting word to an array
            numbers = [int(i) for i in word.split()]
            # List used to accumulate numbers as a 1D array
            acc = list()

            # Read until we reach a blank space
            while word != "":
                # Appending numbers contained in row to acc
                acc += numbers
                # Reading new row
                word = text.pop(0)
                # If there are numbers left, continue reading
                numbers = [int(i) for i in word.split()] if word != "" else []
            # Making flag point to next variable to read
            i += 1
            # Converting acc from 1D array to an "n x n" array, store it on matrix A or B
            for i in range(n):
                current_list.append(acc[0:n])
                del acc[0:n]

    # Result of reading file
    result = {"A": A, "B": B, "n": n}

    # Reading solution for instance problem of file_name
    data_file_name = file_name + ".sln"
    if not os.path.isfile(data_file_name):
        # Solution file doesnt exists, returning data only
        return result

    # Reading file from path file_name
    f = open(data_file_name, "r")
    text = f.read()

    # Breaking text into words
    text = text.split()
    """
    First word is "n", second word is the value of
    objective function, the rest of the values are
    the array representing the solution
    """
    result["optimal_value"] = int(text[1])
    result["optimal_solution"] = [int(i) for i in text[2:]]

    # Result as a dictionary
    return result
