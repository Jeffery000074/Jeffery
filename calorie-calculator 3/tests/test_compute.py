import os
from core.compute import Calculator, totals

def test_add_and_totals():
    c = Calculator(os.path.join("data", "foods.csv"))
    a = c.add(user_food="chicken breast", qty=100, unit="g")
    b = c.add(user_food="rice", qty=1, unit="cup")  # cooked rice override
    t = totals([a, b])
    assert t["kcal"] > 0
    assert t["protein_g"] > 0
