import streamlit as st
from person import get_person_data, get_person_object_by_full_name
from ekgdata import EKGdata

def run_dashboard():
    st.title("EKG Dashboard")

    persons = get_person_data()
    
    selected_names = st.selectbox("Select a person", [person.get_full_name() for person in persons])

    person = get_person_object_by_full_name(selected_names)

    st.image(person.get_image(), width=200)

    st.write(f"Alter: {person.get_age()}" | Max HR: {person.calc_max_heart_rate()} bpm")
             
    if person.ekg_tests:
       
        ekg_test = EKGdata(person.ekg_tests[0])
        ekg.find_peaks()
        st.write(f"Herzfrequenz: {ekg.get_heart_rate()} bpm")
        st.plotly_chart(ekg.plot:_ekg_data(),
                        use_container_width=True)



    
    


