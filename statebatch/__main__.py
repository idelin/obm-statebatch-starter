import json
import sys
from . import Machine, StateError


def main():
    request = json.load(sys.stdin)
    try:
        machine = Machine(request["spec"], request.get("checkpoint"))
        result = machine.apply(request["events"], request["expected_version"])
    except StateError as error:
        json.dump({"error": error.code, "event_index": error.event_index}, sys.stdout)
        sys.stdout.write("\n")
        return 2
    json.dump(result, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
