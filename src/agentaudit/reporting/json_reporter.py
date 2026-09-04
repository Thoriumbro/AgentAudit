import json


class JSONReporter:
    """
    Saves execution traces and aggregate metrics as JSON.
    """

    def save(self, trace, path, metrics=None):
        output = {
            "trace": trace.to_dict(),
        }

        if metrics is not None:
            output["aggregate_metrics"] = metrics.__dict__

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                output,
                file,
                indent=4,
                ensure_ascii=False,
            )