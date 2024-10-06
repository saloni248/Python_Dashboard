import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
# Custom CSS for background color
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;  /* Set your desired background color here */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Load dataset
df = pd.read_csv(r'Imports_Exports_Dataset.csv')

# Sample the dataset
df_sample = df.sample(n=3001, random_state=55011)

# Sidebar filters
st.sidebar.title("Filters")
categories = df_sample['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

import_export_options = df_sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect("Select Import/Export", options=import_export_options, default=import_export_options)

payment_terms = df_sample['Payment_Terms'].unique()
selected_payment_terms = st.sidebar.multiselect("Select Payment Terms", options=payment_terms, default=payment_terms)

ship_modes = df_sample['Shipping_Method'].unique()
selected_ship_modes = st.sidebar.multiselect("Select Shipping Method", options=ship_modes, default=ship_modes)

# Filter the dataframe based on the selected filters
filtered_df = df_sample[
    (df_sample['Category'].isin(selected_categories)) &
    (df_sample['Import_Export'].isin(selected_import_export)) &
    (df_sample['Payment_Terms'].isin(selected_payment_terms)) &
    (df_sample['Shipping_Method'].isin(selected_ship_modes))
]

# Title of the app
st.title("Imports and Exports Dashboard")

# Proceed with filtered data
if not filtered_df.empty:
    # First row of charts
    col1, col2 = st.columns(2)

    with col1:
        # Create pie chart for Import and Export distribution
        st.markdown('### Percentage of Import and Export Transactions')
        transaction_counts = filtered_df['Import_Export'].value_counts()
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        ax2.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%', startangle=90, 
                colors=['#ff9999', '#66b3ff'])  # New colors for the pie chart
        ax2.axis('equal')
        st.pyplot(fig2)

    with col2:
        st.markdown('### Transactions by Category')
        category_transaction_counts = filtered_df.groupby(['Category', 'Import_Export']).size().unstack()
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        category_transaction_counts.plot(kind='bar', stacked=True, ax=ax3, 
                                         color=['#fdae61', '#4575b4'])  # New color scheme for the bar chart
        ax3.set_title('Transactions by Category', fontsize=10)
        ax3.set_xlabel('Category', fontsize=10)
        ax3.set_ylabel('Number of Transactions', fontsize=10)
        ax3.legend(title='Transaction Type')
        st.pyplot(fig3)

    # Second row: Bar Chart for Customers
    st.markdown("### Customer-wise Highest Import/Export Transactions")
    customer_values = filtered_df.groupby(['Customer', 'Import_Export'])['Value'].sum().unstack().fillna(0)
    top_customers = customer_values.sum(axis=1).sort_values(ascending=False).head(10)  # Select top 10 customers
    top_customer_values = customer_values.loc[top_customers.index]

    fig4, ax4 = plt.subplots(figsize=(10, 6))
    top_customer_values.plot(kind='bar', stacked=True, color=['#ff6666', '#87CEFA'], edgecolor='black', ax=ax4)

    ax4.set_title('Customer-wise Highest Import/Export Transactions')
    ax4.set_xlabel('Customer')
    ax4.set_ylabel('Transaction Value (in USD)')
    ax4.legend(title='Transaction Type', loc='upper right')
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better readability
    plt.tight_layout()  # Adjust layout for better spacing
    st.pyplot(fig4)

    # Third row: Treemap Chart (smaller, simpler column for better visualization)
    st.markdown("### Treemap: Transaction Value by Payment Terms and Category")
    treemap_fig = px.treemap(filtered_df, 
                             path=['Payment_Terms', 'Category'], 
                             values='Value', 
                             color='Value', 
                             hover_data=['Payment_Terms'], 
                             color_continuous_scale='RdBu', 
                             title="Treemap of Transaction Value by Payment Terms and Category",
                             height=600,  # Increased height for better clarity
                             width=900)
    st.plotly_chart(treemap_fig)

    # Fourth row: Bubble Chart (smaller columns for simpler visualization)
    st.markdown("### Bubble Chart: Transaction Value by Category and Shipping Method")
    bubble_fig = px.scatter(filtered_df, 
                            x='Shipping_Method', 
                            y='Value', 
                            size='Value', 
                            color='Category', 
                            hover_name='Shipping_Method', 
                            title="Bubble Chart of Transaction Value by Shipping Method and Category", 
                            size_max=60,  # Controlled bubble size
                            height=600,  # Increased height for better clarity
                            width=900)
    st.plotly_chart(bubble_fig)

  # Fifth row: Sunburst Chart (smaller version)
    st.markdown("### Sunburst Chart: Hierarchical View of Transactions")
    sunburst_fig = px.sunburst(filtered_df, 
                               path=['Category', 'Country', 'Import_Export'], 
                               values='Value', 
                               color='Value', 
                               hover_data=['Country'], 
                               color_continuous_scale='Blues', 
                               title="Sunburst Chart of Transactions by Category, Country, and Import/Export",
                               height=500,  # Reduced size for a smaller visualization
                               width=700)
    st.plotly_chart(sunburst_fig)

    # Sixth row: Line Chart for Average Value of Transactions
    st.markdown("### Line Chart: Average Value of Transactions by Category")
    avg_transaction_values = filtered_df.groupby('Category')['Value'].mean().sort_values(ascending=False)

    fig6, ax6 = plt.subplots(figsize=(8, 5))
    avg_transaction_values.plot(kind='line', marker='o', color='blue', ax=ax6)

    ax6.set_title('Average Transaction Value by Category')
    ax6.set_xlabel('Category')
    ax6.set_ylabel('Average Transaction Value (in USD)')
    st.pyplot(fig6)

else:
    st.warning("No data available for the selected filters. Please select at least 1 item from each filter.")