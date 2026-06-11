import streamlit as st
from person import get_person_data, get_person_object_by_full_name
from ekgdata import EKGdata

def run_dashboard():
    st.set_page_config(page_title="EKG Dashboard", layout="wide")

    st.title("EKG Dashboard")
    st.markdown("---")

    persons = get_person_data()

    selected_name = st.selectbox("Select Patient", [person.get_full_name() for person in persons])
    person = get_person_object_by_full_name(selected_name)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image(person.get_image(), width=200)

    with col2:
        st.subheader(person.get_full_name())

        col_age, col_hr = st.columns(2)
        with col_age:
            st.metric("Age", f"{person.calc_age()} years")
        with col_hr:
            st.metric("Max Heart Rate", f"{person.calc_max_heart_rate()} bpm")

    st.markdown("---")

    if person.ekg_tests:
        st.subheader("EKG Analysis")

        ekg = EKGdata(person.ekg_tests[0])
        ekg.find_peaks()

        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("Current Heart Rate", f"{ekg.estimate_hr()} bpm")

        st.plotly_chart(ekg.plot_time_series(), use_container_width=True)
    else:
        st.info("No EKG data available for this patient")
