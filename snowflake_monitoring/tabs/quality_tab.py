import streamlit as st
import pandas as pd
from datetime import datetime

def display_quality_tab(quality_data, selected_schema):
    st.header("Data Freshness & Quality")
    st.markdown("Timeliness of data model refreshes.")

    if not quality_data.empty:
        quality_data['Last Refreshed'] = pd.to_datetime(quality_data['Last Refreshed'])
        quality_data['Hours Since Last Refresh'] = ((datetime.now() - quality_data['Last Refreshed']).dt.total_seconds() / 3600).round(1)
        
        st.subheader("Data Model Freshness")
        
        def highlight_stale(row):
            hours = row['Hours Since Last Refresh']
            if hours > 24:
                return ['background-color: #FFCCCB'] * len(row)
            elif hours > 12:
                return ['background-color: #FFFFE0'] * len(row)
            return [''] * len(row)

        st.dataframe(
            quality_data[['Data Model', 'Last Refreshed', 'Hours Since Last Refresh', 'Source System']]
            .sort_values(by='Hours Since Last Refresh', ascending=False)
            .style.apply(highlight_stale, axis=1),
            height=350
        )

        avg_freshness = quality_data['Hours Since Last Refresh'].mean()
        stale_models_count = len(quality_data[quality_data['Hours Since Last Refresh'] > 24])
        
        col1, col2 = st.columns(2)
        col1.metric("Average Data Age (Hours)", f"{avg_freshness:.1f}h")
        col2.metric("Models Stale (>24h)", stale_models_count)

    else:
        st.warning("No data quality/freshness information available.")
