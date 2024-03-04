from Manager.FAP import FAP
from TestManager import TestManager

class appendUT(TestManager):

    def addElement_ElementAddedAtTheEnd(self):
        fap = FAP()
        e1 = "test1"
        e2 = "test2"
        e3 = "test3"

        fap.append(e1)
        fap.append(e2)
        fap.append(e3)

        self.assertEqual([e.value for e in fap.elements], [e1, e2, e3])


class nextUT(TestManager):
    def getElement_ElementsRecoveredInTheCorrectOrder(self):
        fap = FAP()
        e1 = "test1"
        e2 = "test2"
        e3 = "test3"

        fap.append(e1)
        fap.append(e2)
        fap.append(e3)

        self.assertEqual(fap.next(), e1)
        self.assertEqual(fap.next(), e2)
        self.assertEqual(fap.next(), e3)

    def getElementWithHighestPriority_ElementsRecoveredInTheCorrectOrder(self):
        fap = FAP()
        e1 = "test1"
        e2 = "test2"
        e3 = "test3"
        e4 = "test4"

        fap.append(e1, 1)
        fap.append(e2, -1)
        fap.append(e3, 3)
        fap.append(e4, 1)

        self.assertEqual(fap.next(), e3)
        self.assertEqual(fap.next(), e1)
        self.assertEqual(fap.next(), e4)
        self.assertEqual(fap.next(), e2)
