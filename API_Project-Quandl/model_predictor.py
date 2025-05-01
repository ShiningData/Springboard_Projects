import pandas as pd
import logging
import tempfile
import os
from dash import callback, Input, Output, dcc, ctx, no_update
from dash.exceptions import PreventUpdate

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Define the callback for the download button
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
    
    try:
        # Extract value from dropdown
        value = int(value[:2])
        table = f"wire_final_report_{value}_months"
        
        # Query data table
        logging.debug(f"Querying table: {table}")
        df = _query_data_table(
            table,
            # Specify only needed columns if applicable
        )
        
        # Verify data was retrieved successfully
        if df is None or df.empty:
            logging.error(f"No data retrieved from table {table}")
            raise PreventUpdate
            
        logging.debug(f"Retrieved dataframe with {len(df)} rows and {len(df.columns)} columns")
        
        # Optimize dataframe for memory efficiency
        df = optimize_dataframe(df)
        
        # Process to Excel and return download
        filename = f"wire_trx_{value}.xlsx"
        return export_dataframe_to_excel(df, filename)
        
    except Exception as e:
        logging.exception(f"Error in create_report: {str(e)}")
        return no_update

def _query_data_table(table, columns=None):
    """
    Query data from the specified table.
    Replace this function with your actual data query implementation.
    """
    # Your existing query implementation...
    # This is a placeholder - use your actual query function
    
    return df  # Return the queried dataframe

def optimize_dataframe(df):
    """Optimize DataFrame memory usage."""
    logging.debug("Optimizing DataFrame memory usage")
    
    # Make a copy to avoid modifying the original
    df = df.copy()
    
    # Convert object columns to categories when appropriate
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # If low cardinality
            df[col] = df[col].astype('category')
    
    # Downcast numeric columns
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df

def export_dataframe_to_excel(df, filename):
    """Export DataFrame to Excel with optimized memory usage."""
    logging.debug(f"Starting export to Excel: {filename}")
    
    try:
        # Debug - Check column information
        logging.debug(f"DataFrame columns before export: {list(df.columns)}")
        
        # Handle MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [' '.join(str(x) for x in col).strip() if isinstance(col, tuple) else col for col in df.columns]
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            temp_path = tmp.name
        
        logging.debug(f"Created temporary file: {temp_path}")
        
        # Write DataFrame to Excel in chunks if large
        chunk_size = 50000  # Adjust based on your data size
        if len(df) > chunk_size:
            logging.debug(f"Large DataFrame detected ({len(df)} rows). Using chunked writing.")
            
            # Initialize writer with openpyxl (tends to have fewer issues with columns)
            with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
                # Write header first
                df.iloc[:0].to_excel(writer, sheet_name='sheet1', index=False)
                
                # Write data in chunks
                for i in range(0, len(df), chunk_size):
                    chunk_end = min(i + chunk_size, len(df))
                    logging.debug(f"Writing chunk {i//chunk_size + 1}: rows {i} to {chunk_end}")
                    
                    chunk = df.iloc[i:chunk_end]
                    chunk.to_excel(
                        writer,
                        sheet_name='sheet1',
                        startrow=i + 1,  # +1 for header
                        index=False,
                        header=False
                    )
        else:
            # For smaller DataFrames, use direct export
            logging.debug("Using direct Excel export (smaller dataset)")
            with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
                df.to_excel(
                    writer,
                    sheet_name='sheet1',
                    index=False
                )
        
        logging.debug("Excel writing completed successfully")
        
        # Read the file into memory
        with open(temp_path, 'rb') as f:
            data = f.read()
            
        # Clean up temporary file
        os.unlink(temp_path)
        logging.debug(f"Temporary file removed. Excel file size: {len(data)/1024/1024:.2f} MB")
        
        # Return file for download
        logging.debug(f"Returning file for download: {filename}")
        return dcc.send_bytes(data, filename)
        
    except Exception as e:
        logging.exception(f"Error in export_dataframe_to_excel: {str(e)}")
        return no_update

# Make sure to include this in your app's layout
# html.Div([
#     dcc.Download(id="download"),  # This MUST be in your layout
#     html.Button("Download Report", id="button_download_wire_report"),
#     dcc.Dropdown(
#         id="dropdown_report_timeframe",
#         options=[
#             {"label": "6 Months", "value": "6_months"},
#             {"label": "12 Months", "value": "12_months"},
#             {"label": "24 Months", "value": "24_months"}
#         ],
#         value="12_months"
#     ),
# ])
