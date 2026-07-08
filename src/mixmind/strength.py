"""
Compressive-strength model.

A gradient-boosting regressor trained on the public UCI Concrete Compressive
Strength dataset (Yeh 1998, 1030 real lab tests). Held-out R2 ~= 0.91.

Honest boundary: the UCI data is wet-cast concrete; dry-cast pavers differ, so
we treat predictions as directional, not certified. We predict directions — we
do not certify mixes.

The mix dict (cement/slag/sand/chips/water kg/m3) maps onto the dataset's 8
features; `age` (days) lets us read early (demould, ~2 d) vs 28-day strength.
"""
from __future__ import annotations
from dataclasses import dataclass

# heavy deps (pandas / sklearn / ucimlrepo) are imported lazily inside methods
# so the package imports on any machine.

FEATURES = ["Cement", "Blast Furnace Slag", "Fly Ash", "Water",
            "Superplasticizer", "Coarse Aggregate", "Fine Aggregate", "Age"]


@dataclass
class Metrics:
    r2: float
    mae: float


class StrengthModel:
    def __init__(self) -> None:
        self.gbm = None
        self.metrics: Metrics | None = None

    def train(self, seed: int = 42) -> Metrics:
        from ucimlrepo import fetch_ucirepo
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import r2_score, mean_absolute_error
        ds = fetch_ucirepo(id=165)              # Concrete Compressive Strength
        X, y = ds.data.features, ds.data.targets.values.ravel()
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=seed)
        self.gbm = GradientBoostingRegressor(
            n_estimators=400, max_depth=3, learning_rate=0.05, random_state=seed)
        self.gbm.fit(Xtr, ytr)
        pred = self.gbm.predict(Xte)
        self.metrics = Metrics(round(float(r2_score(yte, pred)), 3),
                               round(float(mean_absolute_error(yte, pred)), 2))
        return self.metrics

    def predict(self, mix: dict[str, float], age: int) -> float:
        if self.gbm is None:
            raise RuntimeError("call train() first")
        import pandas as pd
        row = {
            "Cement": mix["cement"], "Blast Furnace Slag": mix["slag"], "Fly Ash": 0,
            "Water": mix["water"], "Superplasticizer": mix.get("plasticizer", 3),
            "Coarse Aggregate": mix["chips"], "Fine Aggregate": mix["sand"], "Age": age,
        }
        return round(float(self.gbm.predict(pd.DataFrame([row])[FEATURES])[0]), 1)
