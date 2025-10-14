from __future__ import annotations
from typing import Dict, Optional

def normalize_unit(u: str) -> str:
    u = (u or "").strip().lower()
    mapping = {
        "g": "g", "gram": "g", "grams": "g",
        "kg": "kg",
        "cup": "cup", "cups": "cup", 
        "tbsp": "tbsp", "tablespoon": "tbsp", "tablespoons": "tbsp",
        "tsp": "tsp", "teaspoon": "tsp", "teaspoons": "tsp",
        "slice": "slice", "slices": "slice", 
        "piece": "piece", "pieces": "piece",
    }
    return mapping.get(u, u)

class UnitConverter:
    """Simple, pragmatic unit converter.
    - 'g' and 'kg' are exact by definition
    - cup/tbsp/tsp use water-like density defaults unless food-specific override is provided
    - slice/piece can use food-specific defaults (piece_weight_g in FoodItem)
    """
    def __init__(self):
        # Defaults (approximate)
        self.default_g_per_cup = 240.0
        self.default_g_per_tbsp = 15.0
        self.default_g_per_tsp = 5.0
        # Food-specific overrides (if known)
        self.food_overrides_g_per_cup: Dict[str, float] = {
            "rice_cooked": 195.0,
            "oats_dry": 90.0,
            "milk": 245.0,
        }

    def to_grams(self, *, unit: str, qty: float, food_key: str, piece_weight_g: 'Optional[float]') -> float:
        u = normalize_unit(unit)
        if qty < 0:
            raise ValueError("Quantity must be non-negative")
        if u in ("g", ""):
            return qty
        if u == "kg":
            return qty * 1000.0
        if u == "cup":
            g_per_cup = self.food_overrides_g_per_cup.get(food_key, self.default_g_per_cup)
            return qty * g_per_cup
        if u == "tbsp":
            return qty * self.default_g_per_tbsp
        if u == "tsp":
            return qty * self.default_g_per_tsp
        if u in ("slice", "piece"):
            if piece_weight_g is None:
                # fallback
                piece_weight_g = 30.0
            return qty * piece_weight_g
        raise ValueError(f"Unsupported unit: {unit!r}")
