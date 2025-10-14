from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional, Union
from .foods import FoodItem, load_foods, normalize as norm_food
from .units import UnitConverter, normalize_unit
import pandas as pd
from pathlib import Path

@dataclass
class ConsumedItem:
    food_key: str
    display_name: str
    qty: float
    unit: str
    grams: float
    kcal: float
    protein_g: float
    fat_g: float
    carbs_g: float

def resolve_food(user_text: str, alias_index: Dict[str, str]) -> Optional[str]:
    key = alias_index.get(norm_food(user_text))
    return key

def compute_macros(item: FoodItem, grams: float) -> Tuple[float, float, float, float]:
    factor = grams / 100.0
    kcal = item.kcal_per_100g * factor
    p = item.protein_g_per_100g * factor
    f = item.fat_g_per_100g * factor
    c = item.carbs_g_per_100g * factor
    return kcal, p, f, c

class Calculator:
    def __init__(self, csv_path: Union[str, Path]):
        self.foods, self.alias_index = load_foods(csv_path)
        self.units = UnitConverter()

    def list_foods(self) -> List[str]:
        return [f.display_name for f in self.foods.values()]

    def add(self, *, user_food: str, qty: float, unit: str) -> ConsumedItem:
        if qty is None or qty == "":
            raise ValueError("Quantity is required")
        qty = float(qty)
        key = resolve_food(user_food, self.alias_index)
        if key is None:
            raise KeyError(f"Unknown food: {user_food!r}")
        item = self.foods[key]
        grams = self.units.to_grams(unit=unit, qty=qty, food_key=key, piece_weight_g=item.piece_weight_g)
        kcal, p, f, c = compute_macros(item, grams)
        return ConsumedItem(
            food_key=key,
            display_name=item.display_name,
            qty=qty,
            unit=normalize_unit(unit),
            grams=grams,
            kcal=kcal,
            protein_g=p,
            fat_g=f,
            carbs_g=c,
        )

def totals(consumed: List[ConsumedItem]) -> Dict[str, float]:
    out = {"grams": 0.0, "kcal": 0.0, "protein_g": 0.0, "fat_g": 0.0, "carbs_g": 0.0}
    for x in consumed:
        out["grams"] += x.grams
        out["kcal"] += x.kcal
        out["protein_g"] += x.protein_g
        out["fat_g"] += x.fat_g
        out["carbs_g"] += x.carbs_g
    return out

def to_dataframe(consumed: List[ConsumedItem]) -> pd.DataFrame:
    return pd.DataFrame([asdict(x) for x in consumed])

def export_diary(consumed: List[ConsumedItem], path: str | Path, date_str: str):
    df = to_dataframe(consumed)
    df.insert(0, "date", date_str)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
