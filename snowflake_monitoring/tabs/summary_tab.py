import streamlit as st

def display_summary_tab(cost_data, usage_data, governance_data, performance_data, quality_data, top_models, selected_schema):
    st.header("Summary & Recommendations")
    st.markdown(f"Key observations and actionable insights for the **{selected_schema}** schema based on the (mock) data.")

    # Cost Summary
    st.subheader("💰 Cost Insights")
    if not cost_data.empty:
        total_cost = cost_data['Materialization Cost (Credits)'].sum()
        most_expensive_model = cost_data.loc[cost_data['Materialization Cost (Credits)'].idxmax()]
        st.write(f"- The total estimated materialization cost for the last cycle was **{total_cost:.2f} credits**.")
        st.write(f"- **{most_expensive_model['Data Model']}** is the most expensive model to materialize ({most_expensive_model['Materialization Cost (Credits)']} credits). Consider optimizing its definition or refresh frequency if possible.")
    else:
        st.write("- No cost data to summarize.")

    # Usage Summary
    st.subheader("📊 Usage Insights")
    if not usage_data.empty:
        num_queries = len(usage_data)
        num_users = usage_data['User'].nunique()
        st.write(f"- There were **{num_queries} queries** by **{num_users} unique users** in the last 7 days.")
        if not top_models.empty: # Check if top_models is not None and not empty
             st.write(f"- The most queried model is **{top_models.iloc[0]['Data Model']}** with {top_models.iloc[0]['Query Count']} queries. Ensure this model is performant and up-to-date.")
    else:
        st.write("- No usage data to summarize.")

    # Governance Summary
    st.subheader("📜 Governance Insights")
    if not governance_data.empty:
        documentation_percentage = (governance_data['Has Documentation'].sum() / len(governance_data)) * 100 if len(governance_data) > 0 else 0
        st.write(f"- **{documentation_percentage:.1f}%** of models have documentation.")
        if documentation_percentage < 80:
            st.warning("- Recommendation: Prioritize adding documentation (Snowflake comments) to undocumented models to improve data discoverability and understanding.")
        else:
            st.success("- Good job on model documentation!")
    else:
        st.write("- No governance data to summarize.")

    # Performance Summary
    st.subheader("⚡ Performance Insights")
    if not performance_data.empty:
        pruning_issues_count = len(performance_data[performance_data['Poor Partition Pruning']])
        spilling_issues_count = len(performance_data[performance_data['Disk Spilling Occurrences (Last 24h)'] > 0])
        if pruning_issues_count > 0:
            st.write(f"- **{pruning_issues_count} model(s)** show signs of poor partition pruning. Investigate query patterns and table clustering for these models.")
        if spilling_issues_count > 0:
            st.write(f"- **{spilling_issues_count} model(s)** experienced disk spilling. This can indicate queries processing large volumes of data inefficiently. Review query logic and consider warehouse scaling if appropriate.")
        if pruning_issues_count == 0 and spilling_issues_count == 0:
            st.success("- No major performance red flags (partition pruning, disk spilling) detected.")
    else:
        st.write("- No performance data to summarize.")

    # Quality Summary
    st.subheader("✅ Quality Insights")
    if not quality_data.empty:
        avg_freshness = quality_data['Hours Since Last Refresh'].mean() if 'Hours Since Last Refresh' in quality_data else 0
        stale_models_count = len(quality_data[quality_data['Hours Since Last Refresh'] > 24]) if 'Hours Since Last Refresh' in quality_data and not quality_data[quality_data['Hours Since Last Refresh'] > 24].empty else 0
        st.write(f"- The average data age across models is **{avg_freshness:.1f} hours**.")
        if stale_models_count > 0:
            st.warning(f"- **{stale_models_count} model(s)** are potentially stale (refreshed more than 24 hours ago). Verify their refresh schedules and investigate any failures.")
        else:
            st.success("- Data freshness appears to be good across models.")
    else:
        st.write("- No quality data to summarize.")

    st.markdown("---")
    st.info("Remember: These are automated observations on mock data. Always combine with domain knowledge and specific investigations.")

