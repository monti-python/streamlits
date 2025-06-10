import streamlit as st

def display_performance_tab(performance_data, selected_schema):
    st.header("Performance Monitoring")
    st.markdown("Identifying potential bottlenecks like poor partition pruning or disk spilling.")

    if not performance_data.empty:
        models_with_pruning_issues = performance_data[performance_data['Poor Partition Pruning']]
        models_with_spilling = performance_data[performance_data['Disk Spilling Occurrences (Last 24h)'] > 0]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Partition Pruning Issues")
            if not models_with_pruning_issues.empty:
                st.warning(f"{len(models_with_pruning_issues)} model(s) flagged for potential partition pruning issues.")
                st.dataframe(models_with_pruning_issues[['Data Model', 'Avg Query Duration (s)']], height=200)
            else:
                st.success("No models flagged for partition pruning issues.")
        
        with col2:
            st.subheader("Disk Spilling Occurrences (Last 24h)")
            if not models_with_spilling.empty:
                st.error(f"{len(models_with_spilling)} model(s) experienced disk spilling.")
                st.dataframe(models_with_spilling[['Data Model', 'Disk Spilling Occurrences (Last 24h)']], height=200)
            else:
                st.success("No disk spilling occurrences reported in the last 24 hours.")
        
        st.markdown("---")
        st.subheader("Overall Model Performance Metrics")
        st.dataframe(performance_data, height=300)
    else:
        st.warning("No performance data available.")
