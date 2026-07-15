import streamlit as st

st.set_page_config(page_title="EHI Assessment", layout="centered")
st.title("Electrolyte Health Index")
st.caption("Assess and monitor the condition of phosphate-based nickel stripping solution across cycles.")

with st.form("inputs"):
    st.subheader("Solution parameters")
    col1, col2 = st.columns(2)
    with col1:
        fresh_phos = st.number_input("Fresh phosphate (mg/kg)", value=8542.5)
        fresh_ph   = st.number_input("Fresh pH", value=4.367, format="%.3f")
        phosphate  = st.number_input("Current phosphate (mg/L)", value=3937.5)
    with col2:
        ph         = st.number_input("Current pH", value=6.741, format="%.3f")
        time_taken = st.number_input("Time taken (min)", value=46)
    submitted = st.form_submit_button("Run assessment")

if submitted:
    crit_phos  = fresh_phos * 0.475
    crit_ph    = fresh_ph + 2.21

    def clamp(v): return max(0.0, min(1.0, v))
    phos_score = clamp((phosphate - crit_phos) / (fresh_phos - crit_phos))
    ph_score   = clamp((crit_ph - ph) / (crit_ph - fresh_ph))

    hi = (0.65 * phos_score + 0.35 * ph_score) * 100

    def get_decision(hi, t):
        if hi >= 50:              return "Continue operation"
        if t >= 40:               return "Unsuitable for use. Send for further processing"
        if hi >= 20 and t >= 30:  return "Regeneration recommended"
        if hi >= 20 and t < 30:   return "Continue with monitoring"
        if hi < 20 and t >= 30:   return "Regeneration recommended"
        return "Continue with monitoring"

    decision = get_decision(hi, time_taken)

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("HI score",        f"{hi:.1f}")
    m2.metric("Phosphate score", f"{phos_score:.3f}")
    m3.metric("pH score",        f"{ph_score:.3f}")

    colour = {"Continue operation": "green",
              "Continue with monitoring": "blue",
              "Regeneration recommended": "orange",
              "Unsuitable for use. Send for further processing": "red"}[decision]
    st.markdown(f"### :{colour}[{decision}]")

    with st.expander("Show intermediate values"):
        st.write(f"Critical phosphate: {crit_phos:.2f} mg/kg")
        st.write(f"Critical pH: {crit_ph:.3f}")
        import streamlit as st

st.title("EN‑AL6061 Condition Assessment")
st.write("Welcome! This app analyzes EN stripping solution conditions based on input parameters.")
