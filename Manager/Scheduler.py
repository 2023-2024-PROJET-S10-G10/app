from Manager.FAP import FAP


class Scheduler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.normal = FAP()
        self.bestEffort = FAP()

    # Le priorité pourrait ne pas être nécessaire au fonctionnement normal de CiGri,
    # mais on se laisse la possibilité de la modifier en cas de besoin
    def insertJob(self, job, priority):
        if priority == "best_effort":
            self.bestEffort.append(job, 0)
        elif priority == "normal":
            self.normal.append(job, 0)
        else:
            raise Exception("Unknown priority : {}".format(priority))

    def getNextJob(self):
        if not self.normal.empty():
            return self.normal.next()

        if not self.bestEffort.empty():
            return self.bestEffort.next()

        return None
