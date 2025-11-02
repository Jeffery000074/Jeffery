import streamlit as st
import pandas as pd
from datetime import date
from core.compute import Calculator, totals, to_dataframe, export_diary

st.set_page_config(page_title="Calorie Calculator", page_icon="🍎", layout="centered")

@st.cache_data
def get_calculator():
    return Calculator("data/foods.csv")

calc = get_calculator()

st.title("🍎 Calorie Calculator")
st.caption("Alias matching • Unit conversion • Macro totals • CSV export")

with st.sidebar:
    st.subheader("🎯 Daily target (kcal)")
    target_kcal = st.number_input("Target", min_value=0, value=2000, step=50)
    st.write("---")
    st.markdown("**Tip:** chicken breast")

# Session state
if "items" not in st.session_state:
    st.session_state["items"] = []

st.subheader("Add food")
c1, c2, c3, c4 = st.columns([2,1,1,1])
with c1:
    user_food = st.text_input("Food (name or alias)", placeholder="e.g., chicken breast / rice")
with c2:
    qty = st.number_input("Qty", min_value=0.0, value=1.0, step=0.5, format="%.2f")
with c3:
    unit = st.selectbox("Unit", ["g", "kg", "cup", "tbsp", "tsp", "slice", "piece"], index=0)
with c4:
    st.write("")
    st.write("")
    if st.button("➕ Add"):
        try:
            item = calc.add(user_food=user_food, qty=qty, unit=unit)
            st.session_state["items"].append(item)
        except KeyError as e:
            st.error(str(e))
        except ValueError as e:
            st.error(str(e))

# Items table
items_df = to_dataframe(st.session_state["items"]) if st.session_state["items"] else pd.DataFrame(columns=["display_name","qty","unit","grams","kcal","protein_g","fat_g","carbs_g"])
if not items_df.empty:
    st.subheader("Today's log")
    st.dataframe(items_df[["display_name","qty","unit","grams","kcal","protein_g","fat_g","carbs_g"]], use_container_width=True)

    # Totals & balance
    t = totals(st.session_state["items"])
    st.metric("Total kcal", f"{t['kcal']:.0f}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Protein (g)", f"{t['protein_g']:.1f}")
    c2.metric("Fat (g)", f"{t['fat_g']:.1f}")
    c3.metric("Carbs (g)", f"{t['carbs_g']:.1f}")
    st.progress(min(t['kcal']/target_kcal, 1.0) if target_kcal>0 else 0.0, text=f"{t['kcal']:.0f} / {target_kcal} kcal")    

    # Export
    st.write("---")
    cc1, cc2, cc3 = st.columns([1,1,1])
    with cc1:
        if st.button("🧹 Clear"):
            st.session_state["items"] = []
            st.experimental_rerun()
    with cc2:
        filename = f"diary_{date.today().isoformat()}.csv"
        csv_bytes = items_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download table CSV", data=csv_bytes, file_name=filename, mime="text/csv")
    with cc3:
        if st.button("💾 Save diary to file"):
            export_diary(st.session_state["items"], path=f"diary/{date.today().isoformat()}.csv", date_str=date.today().isoformat())
            st.success("Saved to diary/")
else:
    st.info("Add your first food above to see totals.")
