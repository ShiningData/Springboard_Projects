@callback(
    Output("download", "data"),
    Input("button_download_wire_report", "n_clicks"),
    Input("dropdown_report_timeframe", "value"),
    prevent_initial_call=True,
    background=True,
)
def create_report(
    n_clicks,
    value,
):
    if n_clicks is None:
        raise PreventUpdate
    
    logging.info(f"{_PAGE} {_NAME} update callback triggered")
    logging.debug(f"Callback context = {ctx.triggered_id}")
    
    value = int(value[:2])
    table = f"wire_final_report_{value}_months"
    
    # Get only necessary columns to reduce memory footprint
    # Specify only the columns you need instead of querying all columns
    df = _query_data_table(
        table,
        # Add column list here if applicable
    )
    
    # Optimize dataframe memory usage before conversion
    df = optimize_dataframe(df)
    
    # Process excel file directly to send_bytes without caching
    return stream_excel_file(df, f"wire_trx_{value}.xlsx")

def optimize_dataframe(df):
    """Optimize DataFrame memory usage before Excel conversion."""
    # Convert object columns to categories when appropriate
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')
    
    # Downcast numeric columns
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df

def stream_excel_file(df, filename):
    """Stream DataFrame to Excel without caching."""
    import tempfile
    import os
    
    logging.debug("Starting optimized conversion to xlsx file")
    
    # Use a temporary file to avoid memory issues
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        # Set up xlsxwriter with memory optimization options
        writer = pd.ExcelWriter(
            tmp.name,
            engine='xlsxwriter',
            engine_kwargs={'options': {'constant_memory': True}}
        )
        
        # For very large DataFrames, use chunking
        max_rows = 100000  # Adjust based on your typical data size
        if len(df) > max_rows:
            # Write the header first
            df.iloc[:0].to_excel(writer, index=False, sheet_name="sheet1")
            
            # Write data in chunks
            for start_row in range(0, len(df), max_rows):
                end_row = min(start_row + max_rows, len(df))
                logging.debug(f"Writing rows {start_row} to {end_row}")
                
                df.iloc[start_row:end_row].to_excel(
                    writer,
                    startrow=start_row + 1,  # +1 for header row
                    index=False,
                    header=False,
                    sheet_name="sheet1"
                )
        else:
            # For smaller DataFrames, write all at once
            df.to_excel(writer, index=False, sheet_name="sheet1")
        
        # Close the writer to ensure all data is written
        writer.close()
        
        # Read the file in binary mode
        with open(tmp.name, 'rb') as f:
            data = f.read()
        
        # Clean up the temporary file
        os.unlink(tmp.name)
    
    logging.debug("Finished optimized conversion to xlsx file")
    
    # Return directly without caching
    return dcc.send_bytes(data, filename)
