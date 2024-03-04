class Manager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.listeners = {}  # Dictionnary of string to list of function

    def add_listener(self, name, listener):
        listener_list = self.listeners.get(name)

        if listener_list is None:
            listener_list = []
            self.listeners[name] = listener_list

        if listener not in listener_list:
            listener_list.append(listener)

    def remove_listener(self, name, listener):
        listener_list = self.listeners.get(name)

        if listener_list is None:
            return

        try:
            listener_list.remove(listener)
        except ValueError:
            pass

    def trigger_event(self, name):
        listener_list = self.listeners.get(name)

        if listener_list is None:
            return

        for listener in listener_list:
            listener()
