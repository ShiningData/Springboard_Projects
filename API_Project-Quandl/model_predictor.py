@cache.memoize(2.628e6)
def _query_data_table(
    table,
    cache_key=cache_key,
):
    # First get row count to determine pagination
    row_count_query = f"""SELECT 
                           count(*) FROM 
                           bdahg01p_dlcd11_cdi_tm.{table}"""
    
    row_count = dbi.db_get_query(
        row_count_query,
        dsn="DSN=bdpimp04-impala;",
        pool="root.cdi",
        conn_options={"SocketTimeout": 0},
    )
    
    table_length = row_count.values[0][0]
    chunk_size = 5000  # Smaller chunk size for better memory management
    
    # Use pandas read_sql with pagination instead of collecting dataframes
    result_df = None
    
    for i in range(0, int(table_length), chunk_size):
        # Use LIMIT and OFFSET for pagination instead of dense_rank
        query = f"""
            SELECT * FROM bdahg01p_dlcd11_cdi_tm.{table}
            ORDER BY cust_pwr_id
            LIMIT {chunk_size} OFFSET {i}
        """
        
        logging.debug(f"Queried rows between {i} and {i+chunk_size-1}")
        
        chunk_df = dbi.db_get_query(
            query,
            dsn="DSN=bdpimp04-impala;",
            pool="root.cdi",
            conn_options={"SocketTimeout": 0},
        )
        
        # Initialize result with first chunk or append to existing
        if result_df is None:
            result_df = chunk_df
        else:
            # Use more efficient concat approach
            result_df = pd.concat([result_df, chunk_df], ignore_index=True)
    
    # Return empty DataFrame if no results
    if result_df is None:
        return pd.DataFrame()
        
    return result_df
