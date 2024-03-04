from TestManager import TestManager
from Manager.Manager import Manager as ManagerToTest

cpt = [0]
cpt_2 = [0, 0]


def create_increaser(cpt):
    def increaser():
        cpt[0] += 1

    return increaser


def create_increaser_2(cpt_2, i):
    def increaser():
        cpt_2[i] += 1

    return increaser


class Manager(ManagerToTest):
    def __init__(self):
        self.reset_test()

    def reset_test(self):
        self.listeners = {}
        global cpt
        cpt = [0]
        cpt_2 = [0, 0]

    def add_listener(self, name):
        super().add_listener(name, create_increaser(cpt))

    def add_listener_method(self, name, method):
        super().add_listener(name, method)


class TestEventManager(TestManager):
    def singletonCheck(self):
        manager = Manager()
        manager2 = Manager()
        self.assertEqual(manager, manager2)

    def addTriggerRemove(self):
        manager = Manager()

        manager.add_listener("addTriggerRemove")
        manager.trigger_event("addTriggerRemove")
        self.assertEqual(cpt, [1])

    def multipleAddTriggerRemove(self):
        manager = Manager()

        f1 = create_increaser(cpt)
        f2 = create_increaser(cpt)
        f3 = create_increaser(cpt)

        manager.add_listener_method("multipleAddTriggerRemove", f1)
        manager.add_listener_method("multipleAddTriggerRemove", f2)
        manager.add_listener_method("multipleAddTriggerRemove", f3)

        for i in range(10):
            manager.trigger_event("multipleAddTriggerRemove")
            self.assertEqual(cpt, [3 * (i + 1)])

        manager.remove_listener("multipleAddTriggerRemove", f1)
        manager.trigger_event("multipleAddTriggerRemove")
        self.assertEqual(cpt, [3 * (i + 1) + 2])

        manager.remove_listener("multipleAddTriggerRemove", f2)
        manager.trigger_event("multipleAddTriggerRemove")
        self.assertEqual(cpt, [3 * (i + 1) + 3])

        manager.remove_listener("multipleAddTriggerRemove", f3)
        manager.trigger_event("multipleAddTriggerRemove")
        self.assertEqual(cpt, [3 * (i + 1) + 3])

    def uniqueListenerCheck(self):
        manager = Manager()

        f = create_increaser(cpt)

        manager.add_listener_method("uniqueListenerCheck", f)
        manager.add_listener_method("uniqueListenerCheck", f)

        manager.trigger_event("uniqueListenerCheck")
        self.assertEqual(cpt, [1])

        manager.remove_listener("uniqueListenerCheck", f)

        manager.trigger_event("uniqueListenerCheck")
        self.assertEqual(cpt, [1])

        manager.add_listener_method("uniqueListenerCheck", f)
        manager.add_listener_method("uniqueListenerCheck", f)

        manager.trigger_event("uniqueListenerCheck")
        self.assertEqual(cpt, [2])

        manager.remove_listener("uniqueListenerCheck", f)

        manager.trigger_event("uniqueListenerCheck")
        self.assertEqual(cpt, [2])

    def differentEventAndDifferentFunctionTrigger(self):
        manager = Manager()

        f1 = create_increaser_2(cpt_2, 0)
        f2 = create_increaser_2(cpt_2, 1)

        manager.add_listener_method("differentEventAndDifferentFunctionTrigger", f1)
        manager.add_listener_method("differentEventAndDifferentFunctionTrigger", f2)

        manager.add_listener_method("differentEventAndDifferentFunctionTrigger1", f1)

        manager.add_listener_method("differentEventAndDifferentFunctionTrigger2", f2)

        manager.trigger_event("differentEventAndDifferentFunctionTrigger")
        self.assertEqual(cpt_2, [1, 1])

        manager.trigger_event("differentEventAndDifferentFunctionTrigger1")
        self.assertEqual(cpt_2, [2, 1])

        manager.trigger_event("differentEventAndDifferentFunctionTrigger2")
        self.assertEqual(cpt_2, [2, 2])

        manager.remove_listener("differentEventAndDifferentFunctionTrigger", f1)
        manager.trigger_event("differentEventAndDifferentFunctionTrigger")
        self.assertEqual(cpt_2, [2, 3])

        manager.trigger_event("differentEventAndDifferentFunctionTrigger1")
        self.assertEqual(cpt_2, [3, 3])

        manager.add_listener_method("differentEventAndDifferentFunctionTrigger", f1)
        manager.trigger_event("differentEventAndDifferentFunctionTrigger")
        self.assertEqual(cpt_2, [4, 4])

    def removeNonExistingMethod(self):
        manager = Manager()

        f = create_increaser(cpt)

        manager.remove_listener("removeNonExistingMethod", f)
        manager.remove_listener("removeNonExistingMethod", f)

        manager.add_listener_method("removeNonExistingMethod", f)

        manager.remove_listener("removeNonExistingMethod", f)
        manager.remove_listener("removeNonExistingMethod", f)

    def triggerEventWithoutListener(self):
        manager = Manager()

        manager.trigger_event("triggerEventWithoutListener")
