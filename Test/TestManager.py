import json
import traceback
from datetime import datetime


class TestManager:
    _instance = None
    subclasses = []
    stats = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        TestManager.subclasses.append(cls)

    # Singleton pattern so that test subclasses all reference the same TestManager
    def __new__(cls, debugLevel):
        cls._debug = debugLevel
        if cls._instance is None:
            cls._instance = super(TestManager, cls).__new__(cls)
        return cls._instance

    def debug(self, level, *args):
        if level <= self._debug:
            print(*args)

    @staticmethod
    def assertTrue(boolean):
        if not boolean:
            raise AssertionError("Assert Failed")

    @staticmethod
    def assertFalse(boolean):
        if boolean:
            raise AssertionError("Assert Failed")

    @staticmethod
    def assertEqual(value, expected):
        if value != expected:
            raise AssertionError(
                "Assert Failed : Expected : {}, got : {}".format(
                    expected, value
                )
            )

    @staticmethod
    def assertNotEqual(value, expected):
        if value == expected:
            raise AssertionError(
                "Assert Failed : Not Expected : {}, got : {}".format(
                    expected, value
                )
            )

    # Run all referenced tests
    def start(self):
        for classToTest in self.subclasses:
            passed, n_passed, tests = self.testClass(classToTest)
            subclassStats = {
                "method_name": classToTest.__name__,
                "passed": passed,
                "n_passed": n_passed,
                "tests": tests,
            }

            self.stats.append(subclassStats)
        return self.summary()

    def testClass(self, classToTest):
        testsStats = []
        success = True
        tests = [
            nom
            for nom, attribute in classToTest.__dict__.items()
            if callable(attribute) and not nom.startswith("__")
        ]
        n_passed = 0
        for test in tests:
            passed, details = self.runTest(getattr(classToTest, test))
            if passed:
                n_passed += 1
            success = success and passed
            testStats = {
                "test_name": test,
                "passed": passed,
                "details": details,
            }
            testsStats.append(testStats)

        return success, n_passed, testsStats

    def runTest(self, test):
        try:
            test(self)
            return True, "Success"
        except AssertionError:
            return False, 'Failed "' + "\n".join(
                ["\t" + a for a in traceback.format_exc().split("\n")]
            )
        except Exception:
            return (
                False,
                'Exception raised "'
                + "\n".join(
                    ["\t" + a for a in traceback.format_exc().split("\n")]
                ).split("Test/")[-1],
            )

    def summary(self):
        with open(
            "Logs/"
            + datetime.now().strftime("%Y-%m-%d_%H-%M-%S").split(".")[0]
            + ".json",
            "w",
        ) as log:
            json.dump(self.stats, log, indent=2)

        totalMethods = len(self.stats)
        passedMethods = 0
        totalTests = 0
        passedTests = 0
        for methods in self.stats:
            totalTests += len(methods["tests"])
            if methods["passed"]:
                color = "\033[92m"
                debugLevel = 2
                passedMethods += 1
            else:
                debugLevel = 1
                color = "\033[91m"
            self.debug(
                debugLevel,
                f"\n{color + methods['method_name']} {methods['n_passed']}/{len(methods['tests'])} \033[0m",
            )

            for test in methods["tests"]:
                if test["passed"]:
                    color = "\033[92m"
                    debugLevel = 2
                    passedTests += 1
                else:
                    debugLevel = 1
                    color = "\033[91m"
                self.debug(
                    debugLevel,
                    "\t" + color + test["test_name"],
                    test["details"] + "\033[0m",
                )

        if totalTests == 0:
            self.debug(0, "No test found")
            exit(1)
        self.debug(
            0,
            "\n" + ("Success" if passedMethods == totalMethods else "Failed"),
        )
        self.debug(
            0,
            f"Total Passed Tests: {passedTests}/{totalTests} {100 * passedTests / totalTests:.1f}%",
        )
        self.debug(
            0,
            f"Total Passed Methods: {passedMethods}/{totalMethods} {100 * passedMethods / totalMethods:.1f}%",
        )

        return passedMethods == totalMethods
