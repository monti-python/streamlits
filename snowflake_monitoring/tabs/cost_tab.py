import streamlit as st
import altair as alt

def display_cost_tab(cost_data, selected_schema):
    st.header("Materialization Costs")
    st.markdown("Overview of compute costs associated with materializing data models in the schema.")
    
    if not cost_data.empty:
        col1, col2 = st.columns([2,1])
        with col1:
            st.subheader("Cost per Data Model")
            cost_chart = alt.Chart(cost_data).mark_bar().encode(
                x=alt.X('Data Model:N', sort='-y'),
                y=alt.Y('Materialization Cost (Credits):Q', title='Cost (Credits)'),
                tooltip=['Data Model', 'Materialization Cost (Credits)', 'Last Run']
            ).properties(
                title=f"Materialization Costs for {selected_schema}"
            )
            st.altair_chart(cost_chart, use_container_width=True)
        
        with col2:
            total_cost = cost_data['Materialization Cost (Credits)'].sum()
            st.metric("Total Estimated Cost (Last Run Cycle)", f"{total_cost:.2f} Credits")
            most_expensive = cost_data.loc[cost_data['Materialization Cost (Credits)'].idxmax()]
            st.markdown(f"""
            **Most Expensive Model:**
            - **Name:** {most_expensive['Data Model']}
            - **Cost:** {most_expensive['Materialization Cost (Credits)']} Credits
            """)
            st.markdown("---")
            st.subheader("Recent Materializations")
            st.dataframe(cost_data[['Data Model', 'Last Run', 'Materialization Cost (Credits)']].sort_values(by="Last Run", ascending=False), height=200)

    else:
        st.warning("No cost data available.")
