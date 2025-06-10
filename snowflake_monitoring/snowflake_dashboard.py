import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta

# Import tab functions
from tabs.cost_tab import display_cost_tab
from tabs.usage_tab import display_usage_tab
from tabs.governance_tab import display_governance_tab
from tabs.performance_tab import display_performance_tab
from tabs.quality_tab import display_quality_tab
from tabs.summary_tab import display_summary_tab

# --- Mock Data Generation ---

def get_mock_cost_data():
    """Generates mock data for materialization costs."""
    data = {
        'Data Model': [f'model_{chr(65+i)}' for i in range(5)],
        'Materialization Cost (Credits)': np.random.uniform(5, 50, 5).round(2),
        'Last Run': [datetime.now() - timedelta(hours=i*2) for i in range(5)]
    }
    return pd.DataFrame(data)

def get_mock_usage_data():
    """Generates mock data for schema usage."""
    users = [f'user_{i}' for i in range(10)]
    data_models = [f'model_{chr(65+i)}' for i in range(5)]
    
    query_log = []
    for _ in range(100):
        query_log.append({
            'Timestamp': datetime.now() - timedelta(minutes=np.random.randint(1, 60*24*7)),
            'User': np.random.choice(users),
            'Data Model Queried': np.random.choice(data_models),
            'Query Type': np.random.choice(['SELECT', 'INSERT', 'UPDATE', 'DELETE'])
        })
    return pd.DataFrame(query_log)

def get_mock_governance_data():
    """Generates mock data for governance metrics."""
    data = {
        'Data Model': [f'model_{chr(65+i)}' for i in range(10)],
        'Has Documentation': np.random.choice([True, False], 10, p=[0.6, 0.4]),
        'Owner': [f'owner_{chr(97+i)}' for i in range(10)]
    }
    return pd.DataFrame(data)

def get_mock_performance_data():
    """Generates mock data for performance issues."""
    data = {
        'Data Model': [f'model_{chr(65+i)}' for i in range(7)],
        'Poor Partition Pruning': np.random.choice([True, False], 7, p=[0.3, 0.7]),
        'Disk Spilling Occurrences (Last 24h)': np.random.randint(0, 5, 7),
        'Avg Query Duration (s)': np.random.uniform(1, 60, 7).round(1)
    }
    df = pd.DataFrame(data)
    # Ensure at least one model has issues for demonstration
    if not df['Poor Partition Pruning'].any():
        df.loc[0, 'Poor Partition Pruning'] = True
    if df['Disk Spilling Occurrences (Last 24h)'].sum() == 0:
        df.loc[1, 'Disk Spilling Occurrences (Last 24h)'] = np.random.randint(1,5)
    return df

def get_mock_quality_data():
    """Generates mock data for data quality/freshness."""
    data = {
        'Data Model': [f'model_{chr(65+i)}' for i in range(8)],
        'Last Refreshed': [datetime.now() - timedelta(hours=np.random.randint(1, 48)) for i in range(8)],
        'Source System': [f'source_{chr(88+i)}' for i in range(8)]
    }
    return pd.DataFrame(data)

# --- Snowflake Connection (Placeholder) ---
# In a real app, you would use snowflake.connector
# st.secrets["snowflake"] would store your credentials
# def get_snowflake_connection():
# try:
# conn = snowflake.connector.connect(
# user=st.secrets["snowflake"]["user"],
# password=st.secrets["snowflake"]["password"],
# account=st.secrets["snowflake"]["account"],
# warehouse=st.secrets["snowflake"]["warehouse"],
# database=st.secrets["snowflake"]["database"],
# schema=st.secrets["snowflake"]["schema"] # This might be overridden by user selection
# )
# return conn
# except Exception as e:
#     st.error(f"Error connecting to Snowflake: {e}")
#     return None

# --- App Layout ---
st.set_page_config(layout="wide", page_title="Snowflake Schema Metrics")

st.title("❄️ Snowflake Schema Performance Dashboard")
st.markdown("Visualizing key metrics for your selected Snowflake schema.")

# --- Sidebar (Placeholder for Schema Selection) ---
st.sidebar.header("Schema Selector")
# In a real app, you'd query Snowflake for available schemas
available_schemas = ["SALES_RAW", "MARKETING_DM", "FINANCE_PROD", "HR_ANALYTICS"]
selected_schema = st.sidebar.selectbox("Select Schema", available_schemas, index=1)
st.sidebar.info(f"Displaying metrics for schema: **{selected_schema}**")
st.sidebar.markdown("---")
st.sidebar.markdown("This dashboard uses mock data. Replace data fetching functions with your Snowflake queries.")


# --- Main Content Tabs ---
tab_cost, tab_usage, tab_governance, tab_performance, tab_quality, tab_summary = st.tabs([
    "💰 Cost", "📊 Usage", "📜 Governance", "⚡ Performance", "✅ Quality", "📝 Summary & Recommendations"
])

# --- 1. Cost Tab ---
with tab_cost:
    cost_data = get_mock_cost_data() # Replace with actual Snowflake query
    display_cost_tab(cost_data, selected_schema)

# --- 2. Usage Tab ---
with tab_usage:
    usage_data = get_mock_usage_data() # Replace with actual Snowflake query
    top_models = display_usage_tab(usage_data, selected_schema) # Capture top_models

# --- 3. Governance Tab ---
with tab_governance:
    governance_data = get_mock_governance_data() # Replace with actual Snowflake query
    display_governance_tab(governance_data, selected_schema)

# --- 4. Performance Tab ---
with tab_performance:
    performance_data = get_mock_performance_data() # Replace with actual Snowflake query
    display_performance_tab(performance_data, selected_schema)

# --- 5. Quality Tab ---
with tab_quality:
    quality_data = get_mock_quality_data() # Replace with actual Snowflake query
    display_quality_tab(quality_data, selected_schema)

# --- 6. Summary & Recommendations Tab ---
with tab_summary:
    # Ensure all data is fetched before displaying summary
    cost_data_summary = get_mock_cost_data() 
    usage_data_summary = get_mock_usage_data()
    # top_models should be available from the usage_tab call if it ran
    # If usage_tab might not run or return top_models, fetch it again or handle None
    if 'top_models' not in locals() or top_models is None: 
        # Recalculate if not available, or pass placeholder
        temp_usage_data_for_summary = get_mock_usage_data()
        if not temp_usage_data_for_summary.empty:
            top_models_summary = temp_usage_data_for_summary['Data Model Queried'].value_counts().nlargest(5).reset_index()
            top_models_summary.columns = ['Data Model', 'Query Count']
        else:
            top_models_summary = pd.DataFrame() # Empty DataFrame
    else:
        top_models_summary = top_models

    governance_data_summary = get_mock_governance_data()
    performance_data_summary = get_mock_performance_data()
    quality_data_summary = get_mock_quality_data()
    
    display_summary_tab(
        cost_data_summary, 
        usage_data_summary, 
        governance_data_summary, 
        performance_data_summary, 
        quality_data_summary, 
        top_models_summary, # Pass the potentially recalculated top_models
        selected_schema
    )

# To run this app:
# 1. Save as snowflake_dashboard.py
# 2. Install dependencies: pip install streamlit pandas altair numpy
# 3. Run in terminal: streamlit run snowflake_dashboard.py
