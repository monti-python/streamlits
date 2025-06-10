import streamlit as st
import altair as alt
import pandas as pd

def display_usage_tab(usage_data, selected_schema):
    st.header("Schema Usage Insights")
    st.markdown("How data models within this schema are being consumed.")

    if not usage_data.empty:
        num_queries = len(usage_data)
        num_users = usage_data['User'].nunique()
        
        col1, col2 = st.columns(2)
        col1.metric("Total Queries (Last 7 Days)", num_queries)
        col2.metric("Unique Users (Last 7 Days)", num_users)
        
        st.subheader("Queries Over Time (Last 7 Days)")
        usage_data['Timestamp'] = pd.to_datetime(usage_data['Timestamp'])
        queries_by_day = usage_data.set_index('Timestamp').resample('D')['Data Model Queried'].count().reset_index()
        queries_by_day.columns = ['Date', 'Number of Queries']

        time_chart = alt.Chart(queries_by_day).mark_line(point=True).encode(
            x=alt.X('Date:T', title='Date'),
            y=alt.Y('Number of Queries:Q', title='Number of Queries'),
            tooltip=['Date', 'Number of Queries']
        ).properties(
            title="Daily Query Volume"
        )
        st.altair_chart(time_chart, use_container_width=True)

        st.subheader("Top Queried Data Models")
        top_models = usage_data['Data Model Queried'].value_counts().nlargest(5).reset_index()
        top_models.columns = ['Data Model', 'Query Count']
        model_chart = alt.Chart(top_models).mark_bar().encode(
            x=alt.X('Data Model:N', sort='-y'),
            y=alt.Y('Query Count:Q'),
            tooltip=['Data Model', 'Query Count']
        ).properties(
            title="Most Frequently Queried Models"
        )
        st.altair_chart(model_chart, use_container_width=True)

        st.subheader("Recent Query Log (Sample)")
        st.dataframe(usage_data.head(10), height=300)
        return top_models # Return top_models for summary tab
    else:
        st.warning("No usage data available.")
        return pd.DataFrame() # Return empty DataFrame if no data
