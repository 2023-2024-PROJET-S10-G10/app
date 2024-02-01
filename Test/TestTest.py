from TestManager import TestManager

class AssertUT(TestManager):
    def assertTrue_validateTest(self):
        self.assertTrue(True)

    def assertFalse_validateTest(self):
        self.assertFalse(False)

    def assertEqual_validateTest(self):
        self.assertEqual(1, 1)

    def assertNotEqual_validateTest(self):
        self.assertNotEqual(1, 2)
