# Create download button and table side by side
col1, col2 = st.columns([4, 1])

with col1:
    st.subheader(f"{interval} Distribution Table")

with col2:
    # Create Excel file in memory
    output = io.BytesIO()
    
    # Reset index to include Month column in the data
    table_download = table_data.reset_index()
    
    # Write to Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        table_download.to_excel(writer, index=False, sheet_name='Distribution')
        
        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Distribution']
        
        # Style the header row
        header_fill = PatternFill(start_color='FF9800', end_color='FF9800', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF', size=14)
        
        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Style data cells
        data_fill = PatternFill(start_color='FFE5CC', end_color='FFE5CC', fill_type='solid')
        data_font = Font(bold=True, size=12)
        
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
            for cell in row:
                cell.fill = data_fill
                cell.font = data_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    st.download_button(
        label="📥 Download",
        data=output,
        file_name=f"{interval}_distribution_table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Apply styles using Pandas Styler
styled_df = (
    table_data.style
    .set_table_styles([
        {'selector': 'th.col_heading', 'props': [('background-color', '#FF9800'), ('color', 'white'), ('font-size', '22px'), ('font-weight', 'bold'), ('text-align', 'center')]},
        {'selector': 'th.row_heading', 'props': [('background-color', '#FF9800'), ('color', 'white'), ('font-size', '22px'), ('font-weight', 'bold'), ('text-align', 'center')]},
        {'selector': 'td', 'props': [('background-color', '#FFE5CC'), ('color', '#000'), ('font-size', '20px'), ('font-weight', 'bold'), ('text-align', 'center')]}
    ])
    .set_table_attributes('style="width:100%; font-size:20px;"')
)

# Render styled table
st.markdown(styled_df.to_html(), unsafe_allow_html=True)
