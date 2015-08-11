import pandas as pd
from StringIO import StringIO

PLATFORM_START = '!platform_table_begin'
PLATFORM_END = '!platform_table_end'
SAMPLE_TITLE = '!Sample_title'
SAMPLE_BEGIN = '!sample_table_begin'
SAMPLE_END = '!sample_table_end'

def read_soft(filename):
    """Return a Pandas DataFrame of parsed SOFT data.
    
    TODO: make the code more paranoid about errors in order/casing. 
    
    Args:
        filename: the name of the SOFT file to read from.
    
    Returns:
        A DataFrame containing metadata and all conditions.
    """
    df = None
    sample_title = None
    with open(filename) as f:    
        try: 
            while True:
                line = f.next()
                stripped = line.strip()
                if stripped == PLATFORM_START:
                    metadata = []
                    while stripped != PLATFORM_END:
                        line = f.next() 
                        stripped = line.strip()
                        metadata.append(stripped)
                    sio = StringIO('\n'.join(metadata[:-1]))
                    df = pd.read_csv(sio, sep='\t', index_col=0)
            
                if stripped.startswith(SAMPLE_TITLE):
                    sample_title = stripped.split('=')[1].strip()
                    
                if stripped == SAMPLE_BEGIN:
                    sample_data = []
                    while stripped != SAMPLE_END:
                        line = f.next() 
                        stripped = line.strip()
                        sample_data.append(stripped)
                    sio = StringIO('\n'.join(sample_data[:-1]))
                    sample_df = pd.read_csv(sio, sep='\t', index_col=0)
                    sample_df.columns = [sample_title]
                    df = pd.merge(df, sample_df, how='left',
                                  left_index=True, right_index=True)
        except StopIteration:
            pass

    return df