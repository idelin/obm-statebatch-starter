"""Basic region transition bookkeeping."""
import copy


class StateError(Exception):
    def __init__(self, code, event_index=None):
        self.code, self.event_index = code, event_index
        super().__init__(code)


class Machine:
    def __init__(self, spec, checkpoint=None):
        self.spec = copy.deepcopy(spec)
        self.current = copy.deepcopy(checkpoint) if checkpoint is not None else {
            "version": 0, "active": dict(spec["initial"]), "data": {}}

    def snapshot(self):
        return copy.deepcopy(self.current)

    def apply(self, events, expected_version):
        for event in events:
            self.current["active"][event["region"]] = event["target"]
        self.current["version"] += 1
        return {"snapshot": self.snapshot(), "trace": []}

    def fork(self):
        return Machine(self.spec, self.snapshot())
