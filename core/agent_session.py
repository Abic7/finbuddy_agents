class AgentSession:
    """
    Manages session state, allowing agents to maintain continuity.
    """

    def __init__(self):
        self.state = {}
        self.log_messages = []

    def set(self, key, value):
        self.state[key] = value

    def get(self, key, default=None):
        return self.state.get(key, default)

    def log(self, message):
        self.log_messages.append(message)
        print(f"[SESSION LOG] {message}")
