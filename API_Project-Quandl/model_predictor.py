def create_report(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate
    
    logging.info(f"{_PAGE} {_NAME} update callback triggered")
    logging.debug(f"Callback context = {ctx.triggered_id}")
    
    value = int(value[:2])
    table = f"wire_final_report_{value}_months"
    
    # Get only necessary columns to reduce memory footprint
    required_columns = ['col1', 'col2', 'col3']  # Replace with your actual needed columns
    df = query_data_table(
        table,
        columns=required_columns
    )
    
    # Convert to appropriate data types to reduce memory usage
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # If cardinality is low, convert to category
            df[col] = df[col].astype('category')
    
    # Use chunked processing for large dataframes
    return stream_excel_report(df, f"wire_trx_{value}")

def stream_excel_report(df, filename_prefix):
    from io import BytesIO
    import tempfile
    import os
    
    # Create a temporary file instead of keeping everything in memory
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        # Use the optimized xlsx writer with reduced memory options
        writer = pd.ExcelWriter(
            tmp.name,
            engine='xlsxwriter',
            engine_kwargs={'options': {'constant_memory': True, 'in_memory': False}}
        )
        
        # Write in chunks if dataframe is large
        chunk_size = 10000
        if len(df) > chunk_size:
            # Write the header
            df.iloc[0:0].to_excel(writer, index=False, sheet_name="sheet1")
            
            # Write the data in chunks
            for i in range(0, len(df), chunk_size):
                logging.debug(f"Writing chunk {i//chunk_size + 1}")
                chunk = df.iloc[i:i+chunk_size]
                chunk.to_excel(
                    writer, 
                    index=False, 
                    sheet_name="sheet1",
                    startrow=i+1,  # +1 for header
                    header=False
                )
        else:
            df.to_excel(writer, index=False, sheet_name="sheet1")
            
        writer.close()
        
        # Read the file in chunks directly to the response
        with open(tmp.name, 'rb') as f:
            excel_data = f.read()
        
        # Clean up the temp file
        os.unlink(tmp.name)
    
    # Send the file directly without caching
    return dcc.send_bytes(excel_data, f"{filename_prefix}.xlsx")
