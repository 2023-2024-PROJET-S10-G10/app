# Higher priority = Higher number

class FAP:

    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def append(self, value, priority=0):
        self.elements.append(FAP.FAPElement(value, priority))

    def next(self):
        highestPriority = max([p.priority for p in self.elements])
        lastElement = [e for e in self.elements if e.priority == highestPriority][0]
        self.elements.remove(lastElement)
        return lastElement.value

    class FAPElement:
        def __init__(self, value, priority):
            self.value = value
            self.priority = priority

        def set(self, value, priority):
            self.value = value
            self.priority = priority
