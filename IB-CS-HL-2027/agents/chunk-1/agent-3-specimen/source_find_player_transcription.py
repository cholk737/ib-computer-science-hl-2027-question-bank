# Uploaded official specimen MS PDF84, printed22; indentation preserved. Known bug.
def find_player(self, name):
    temp = self.head
    found = False
    while temp != None:
        if temp.name == name:
            found = True
            print(temp.score)
            break
    else:
            temp = temp.next
    if found == False:
        print("Not found")
