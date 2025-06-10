import streamlit as st
import altair as alt

def display_governance_tab(governance_data, selected_schema):
    st.header("Data Governance Status")
    st.markdown("Documentation and ownership of data models.")

    if not governance_data.empty:
        total_models = len(governance_data)
        documented_models = governance_data['Has Documentation'].sum()
        documentation_percentage = (documented_models / total_models) * 100 if total_models > 0 else 0

        st.metric("Documentation Coverage", f"{documentation_percentage:.1f}%", 
                  help=f"{documented_models} out of {total_models} models have descriptions/comments.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Documentation Status")
            status_counts = governance_data['Has Documentation'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            status_counts['Status'] = status_counts['Status'].map({True: 'Documented', False: 'Not Documented'})
            
            pie_chart = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Status", type="nominal"),
                tooltip=['Status', 'Count']
            ).properties(title="Model Documentation Breakdown")
            st.altair_chart(pie_chart, use_container_width=True)

        with col2:
            st.subheader("Models Missing Documentation")
            missing_docs = governance_data[~governance_data['Has Documentation']]
            if not missing_docs.empty:
                st.dataframe(missing_docs[['Data Model', 'Owner']], height=280)
            else:
                st.success("All models are documented!")
        
        st.markdown("---")
        st.subheader("Data Model Owners (Sample)")
        st.dataframe(governance_data[['Data Model', 'Owner']].sample(min(5, len(governance_data))), height=200)

    else:
        st.warning("No governance data available.")
