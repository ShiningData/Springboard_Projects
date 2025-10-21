Here’s the updated script with styled pandas table:

```python
# Grouping for Distribution Plot
freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}

# Create a copy and ensure createTime is datetime
current_df_copy = current_df.copy()
current_df_copy["createTime"] = pd.to_datetime(current_df_copy["createTime"])

grouped = (
    current_df_copy.groupby([
        pd.Grouper(key="createTime", freq=freq_map[interval]),
        "rule_status"
    ]).size().reset_index(name="count")
)

# Format x-axis labels based on interval
if interval == "Daily":
    grouped["x_label"] = grouped["createTime"].dt.strftime("%Y-%m-%d")
elif interval == "Weekly":
    # For weekly, show start (Monday) to end (Sunday) of the week
    grouped["x_label"] = (
        grouped["createTime"].dt.strftime("%b %d") + " - " +
        (grouped["createTime"] + pd.Timedelta(days=6)).dt.strftime("%b %d")
    )
elif interval == "Monthly":
    grouped["x_label"] = grouped["createTime"].dt.strftime("%B %Y")

grouped["total"] = grouped.groupby("createTime")["count"].transform("sum")
grouped["percentage"] = (grouped["count"] / grouped["total"]*100).round(1)
grouped["hover"] = grouped["rule_status"] + ": " + grouped["count"].astype(str) + " (" + grouped["percentage"].astype(str) + "%)"

# Bar Chart
st.subheader(f"Request Distribution by {interval}")

fig = px.bar(
    grouped,
    x="x_label",
    y="count",
    color="rule_status",
    text="hover",
    color_discrete_map={"Success": "#4CAF50", "Failed": "#f44336"},
    labels={"x_label": "Date", "count": "Request Count", "rule_status": "Request Status"}
)

fig.update_traces(textposition='auto', hovertemplate='%{text}')
fig.update_layout(
    showlegend=True,
    xaxis_title="Date",
    yaxis_title="Request Count",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

# Table below the chart
st.subheader(f"{interval} Distribution Table")

# Create pivot table
table_data = (
    current_df_copy.groupby([
        pd.Grouper(key="createTime", freq=freq_map[interval]),
        "rule_status"
    ])
    .size()
    .reset_index(name='count')
    .pivot(index='createTime', columns='rule_status', values='count')
    .fillna(0)
    .astype(int)
)

# Add Total column
table_data['Total'] = table_data.sum(axis=1)

# Format index based on interval
if interval == "Daily":
    table_data.index = pd.to_datetime(table_data.index).strftime('%Y-%m-%d')
    table_data.index.name = 'Date'
elif interval == "Weekly":
    table_data.index = [
        f"{pd.to_datetime(dt).strftime('%b %d')} - {(pd.to_datetime(dt) + pd.Timedelta(days=6)).strftime('%b %d')}"
        for dt in table_data.index
    ]
    table_data.index.name = 'Week'
elif interval == "Monthly":
    table_data.index = pd.to_datetime(table_data.index).strftime('%B %Y')
    table_data.index.name = 'Month'

# Style the table
styled_table = table_data.style.set_properties(**{
    'background-color': '#FFE5CC',  # Light orange background
    'color': 'black',
    'font-weight': 'bold',
    'font-size': '16px',
    'text-align': 'center',
    'border': '1px solid #FF8C00'
}).set_table_styles([
    {'selector': 'thead th', 'props': [
        ('background-color', '#FF8C00'),  # Dark orange for column headers
        ('color', 'white'),
        ('font-weight', 'bold'),
        ('font-size', '18px'),
        ('text-align', 'center'),
        ('border', '1px solid #FF8C00')
    ]},
    {'selector': 'th', 'props': [
        ('background-color', '#FF8C00'),  # Dark orange for index
        ('color', 'white'),
        ('font-weight', 'bold'),
        ('font-size', '16px'),
        ('text-align', 'center'),
        ('border', '1px solid #FF8C00')
    ]},
    {'selector': '', 'props': [
        ('border-collapse', 'collapse'),
        ('width', '100%')
    ]}
])

st.dataframe(styled_table, use_container_width=True, height=600)
```

This styled table features:

- **Light orange background** (#FFE5CC) for all table cells
- **Dark orange background** (#FF8C00) for column headers and index
- **Bold text** throughout the table
- **Larger font sizes** (16px for cells, 18px for headers)
- **White text** on dark orange headers for better contrast
- **Increased height** (600px) to make the table bigger
- **Centered text alignment** for better readability
- **Borders** for clear cell separation​​​​​​​​​​​​​​​​
