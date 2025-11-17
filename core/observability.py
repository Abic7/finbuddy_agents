import time

class Tracer:
    """
    Tracks execution time of each agent/tool call.
    """

    def trace(self, label, fn, *args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f"[TRACE] {label} took {round(end - start, 3)}s")
        return result


class Logger:
    def log(self, msg):
        print(f"[LOG] {msg}")
