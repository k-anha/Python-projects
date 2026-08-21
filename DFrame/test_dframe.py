import unittest

import numpy as np

from dam import DFrame


class DFrameTests(unittest.TestCase):
    def test_supported_inputs_have_consistent_shape(self):
        self.assertEqual(DFrame([[1, 2], [3, 4]], ["a", "b"]).shape, (2, 2))
        self.assertEqual(DFrame({"a": [1, 2], "b": [3, 4]}).shape, (2, 2))
        self.assertEqual(
            DFrame([{"a": 1}, {"a": 2, "b": 3}]).columns,
            ["a", "b"],
        )

    def test_selection_filter_and_assign(self):
        frame = DFrame({"name": ["a", "b", "c"], "score": [3, 1, 2]})
        self.assertEqual(frame["score"].tolist(), [3, 1, 2])
        self.assertEqual(frame.filter(frame["score"] > 1)["name"].tolist(), ["a", "c"])
        self.assertEqual(frame.assign(double=lambda item: item["score"] * 2)["double"].tolist(), [6, 2, 4])

    def test_missing_values_sorting_and_summary(self):
        frame = DFrame({"value": [3, np.nan, 1]})
        self.assertEqual(frame.dropna()["value"].tolist(), [3.0, 1.0])
        self.assertEqual(frame.fillna(0)["value"].tolist(), [3.0, 0.0, 1.0])
        self.assertEqual(frame.sort_values("value")["value"].tolist(), [1, 3, np.nan])
        self.assertEqual(frame.describe()["value"]["count"], 2.0)


if __name__ == "__main__":
    unittest.main()