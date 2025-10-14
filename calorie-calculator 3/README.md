# Calorie Calculator (Streamlit)

A lightweight Streamlit app to log foods, convert household measures to grams, and compute daily calories & macros.

## Features
- Alias matching (e.g. "鸡胸肉", "chicken breast", "鸡里脊" → Chicken breast)
- Unit conversion for common measures (g, cup, tbsp, tsp, slice, piece) with sensible defaults
- Macro totals (kcal / protein / fat / carbs)
- Daily target & remaining balance
- CSV diary export

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Layout
```
calorie-calculator/
  app.py
  core/
    __init__.py
    foods.py
    units.py
    compute.py
  data/foods.csv
  tests/test_compute.py
  requirements.txt
  README.md
```

## Notes
- Food data are sample values per 100 g; you can expand `data/foods.csv` with more rows.
- Unit conversions are approximations aimed at convenience, not clinical use.
- This is an educational prototype.
