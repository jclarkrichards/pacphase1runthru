class Stack(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        if len(self.items) > 0:
            return False
        return True

    def length(self):
        return len(self.items)

    def clear(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) > 0:
            removedItem = self.items.pop(len(self.items)-1)
            return removedItem
        return None

    def peek(self):
        if len(self.items) > 0:
            return self.items[len(self.items)-1]
        return None
