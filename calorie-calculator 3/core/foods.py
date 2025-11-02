from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd
from pathlib import Path

@dataclass(frozen=True)
class FoodItem:
    key: str
    display_name: str
    kcal_per_100g: float
    protein_g_per_100g: float
    fat_g_per_100g: float
    carbs_g_per_100g: float
    piece_weight_g: Optional[float] = None  # optional average piece weight

def normalize(s: str) -> str:
    return " ".join(s.strip().lower().replace("，", ",").replace("、", ",").split())

from typing import Union, Tuple

def load_foods(csv_path: 'Union[str, Path]') -> 'Tuple[Dict[str, FoodItem], Dict[str, str]]':
    """
    Returns:
      foods: dict[food_key] -> FoodItem
      alias_index: dict[alias_normalized] -> food_key
    """
    df = pd.read_csv(csv_path)
    foods: Dict[str, FoodItem] = {}
    alias_index: Dict[str, str] = {}
    for _, r in df.iterrows():
        item = FoodItem(
            key=str(r["food_key"]),
            display_name=str(r["display_name"]),
            kcal_per_100g=float(r["kcal_per_100g"]),
            protein_g_per_100g=float(r["protein_g_per_100g"]),
            fat_g_per_100g=float(r["fat_g_per_100g"]),
            carbs_g_per_100g=float(r["carbs_g_per_100g"]),
            piece_weight_g=float(r["piece_weight_g"]) if not pd.isna(r["piece_weight_g"]) else None,
        )
        foods[item.key] = item
        # aliases
        aliases: List[str] = []
        raw_aliases = str(r.get("aliases", "") or "")
        for token in raw_aliases.split(";"):
            t = normalize(token)
            if t:
                aliases.append(t)
        # include display_name & key as aliases
        aliases.extend([normalize(item.display_name), normalize(item.key)])
        for a in aliases:
            alias_index[a] = item.key
    return foods, alias_index
