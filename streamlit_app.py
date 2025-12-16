import streamlit as st
from collide_core import run_collide_demo


@st.cache_data(show_spinner=False)
def load_demo_results():
    """Run the demo consultation once and cache the result for the session."""
    return run_collide_demo()


st.set_page_config(page_title="COLLIDE AI Demo", page_icon="🤖", layout="wide")
st.title("COLLIDE AI – Brand Advisory Demo")
st.markdown("Click **Run Demo** to execute the consultation flow and view results.")

if st.button("Run Demo", type="primary"):
    with st.spinner("Running consultation..."):
        results = load_demo_results()

    assessment = results.get("assessment", {})
    report = results.get("report", {})

    st.success("Demo completed")

    cols = st.columns(3)
    cols[0].metric("Overall Score", f"{assessment.get('overall_score', 0):.1f}")
    cols[1].metric("Maturity Level", assessment.get("maturity_level", "N/A"))
    cols[2].metric("Top Priority", report.get("executive_summary", "").split("Immediate priorities:")[-1].strip())

    st.subheader("Assessment")
    st.json(assessment)

    st.subheader("Strategy")
    st.json(results.get("strategy", {}))

    st.subheader("Executive Summary")
    st.write(report.get("executive_summary", ""))
else:
    st.info("Press the button to start the demo.")
