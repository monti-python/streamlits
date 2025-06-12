import streamlit as st
import altair as alt
import pandas as pd # Import pandas

def display_cost_tab(cost_data, selected_schema):
    st.header("Data Model Materialization Costs")
    st.markdown("Overview of compute costs associated with materializing and maintaining data models in the schema. This includes single-shot materializations and costs over time for incremental models and materialized views.")
    
    if not cost_data.empty and 'Last Run' in cost_data.columns:
        # Ensure 'Last Run' is datetime
        cost_data['Last Run'] = pd.to_datetime(cost_data['Last Run'])
        cost_data['Month-Year'] = cost_data['Last Run'].dt.strftime('%Y-%m')
        
        available_months = sorted(cost_data['Month-Year'].unique(), reverse=True)
        
        if not available_months:
            st.warning("No month data available to select.")
            return

        selected_month_year = st.selectbox("Select Month:", available_months, key="cost_month_selector")
        
        # Filter data based on selected month
        filtered_cost_data = cost_data[cost_data['Month-Year'] == selected_month_year].copy() # Use .copy() to avoid SettingWithCopyWarning

        if filtered_cost_data.empty:
            st.warning(f"No cost data available for {selected_month_year}.")
            return

        col1, col2 = st.columns([2,1])
        with col1:
            st.subheader(f"Cost per Data Model ({selected_month_year})")
            cost_chart = alt.Chart(filtered_cost_data).mark_bar().encode(
                x=alt.X('Data Model:N', sort='-y'),
                y=alt.Y('Materialization Cost (Credits):Q', title='Cost (Credits)'),
                tooltip=['Data Model', 'Materialization Cost (Credits)', 'Last Run', 'Model Type:N']
            ).properties(
                title=f"Materialization Costs for {selected_schema} ({selected_month_year})"
            )
            st.altair_chart(cost_chart, use_container_width=True)
        
        with col2:
            total_cost = filtered_cost_data['Materialization Cost (Credits)'].sum()
            st.metric(f"Total Estimated Cost ({selected_month_year})", f"{total_cost:.2f} Credits")
            
            if not filtered_cost_data.empty:
                # Ensure the DataFrame is not empty before trying to find idxmax
                most_expensive = filtered_cost_data.loc[filtered_cost_data['Materialization Cost (Credits)'].idxmax()]
                st.markdown(f"""
                **Most Expensive Model ({selected_month_year}):**
                - **Name:** {most_expensive['Data Model']}
                - **Cost:** {most_expensive['Materialization Cost (Credits)']} Credits 
                """ ) 
            
            st.markdown("---")
            st.subheader(f"Detailed Model Costs ({selected_month_year})")
            display_columns = ['Data Model', 'Last Run', 'Materialization Cost (Credits)']
            if 'Model Type' in filtered_cost_data.columns:
                display_columns.insert(1, 'Model Type')
            # 'Cost Period' might be redundant if we are filtering by 'Month-Year'
            # but can be kept if it provides additional granularity (e.g. daily within the month)
            if 'Cost Period' in filtered_cost_data.columns: 
                display_columns.insert(2, 'Cost Period')
                
            st.dataframe(filtered_cost_data[display_columns].sort_values(by="Last Run", ascending=False), height=200)

    elif cost_data.empty:
        st.warning("No cost data available.")
    else:
        st.warning("Cost data is missing 'Last Run' column, cannot filter by month.")
