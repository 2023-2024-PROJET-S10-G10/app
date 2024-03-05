from Manager.Scheduler import Scheduler
from TestManager import TestManager


class insertJobUT(TestManager):

    def addElement_ElementAdded(self):
        s = Scheduler()
        j1 = "job1"
        j2 = "job2"
        j3 = "job3"
        j4 = "job4"

        s.insertJob(j1, "normal")
        s.insertJob(j2, "best_effort")
        s.insertJob(j3, "normal")
        s.insertJob(j4, "best_effort")

        self.assertEqual([e.value for e in s.normal.elements], [j1, j3])
        self.assertEqual([e.value for e in s.bestEffort.elements], [j2, j4])

    def wrongPriority_RaiseException(self):
        s = Scheduler()
        j = "job"

        try:
            s.insertJob(j, "Not a priority")
            self.assertTrue(False)  # Ce code ne doit pas être atteint
        except Exception as e:
            self.assertEqual(e.args[0], "Unknown priority : Not a priority")

class getNextJobUT(TestManager):
    def retrieveAllElements_emptyListAndJobsInPriorityOrder(self):
        s = Scheduler()
        j1 = "job1"
        j2 = "job2"
        j3 = "job3"
        j4 = "job4"

        s.insertJob(j1, "normal")
        s.insertJob(j2, "best_effort")
        s.insertJob(j3, "normal")
        s.insertJob(j4, "best_effort")

        self.assertEqual(s.getNextJob(), j1)
        self.assertEqual(s.getNextJob(), j3)
        self.assertEqual(s.getNextJob(), j2)
        self.assertEqual(s.getNextJob(), j4)

    def retrieveInEmptyList_ReturnNone(self):
        s = Scheduler()

        self.assertEqual(s.getNextJob(), None)
