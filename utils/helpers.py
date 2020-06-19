# capitlises every space divided word in a string
def capitalizeId(_id):
    capNameList = list(
        map(lambda substring: substring[0].upper() + substring[1:], _id.split(" "))
    )
    return " ".join(capNameList)
