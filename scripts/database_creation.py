from sqlalchemy 
import create_engine

# Create a SQLite engine
engine = create_engine('sqlite:///yelp.db')

# Define function to load DataFrame into a SQL table with chunksize
def load_dataframe(df, table_name, engine, chunksize=5000):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=chunksize)


# Load each DataFrame into a separate table using chunking for large DataFrames
load_dataframe(business_df, 'business', engine , chunksize=5000)
load_dataframe(review_df, 'review', engine, chunksize=5000)  # Large file uses chunksize
load_dataframe(user_df, 'user', engine , chunksize=5000)
load_dataframe(tip_df, 'tip', engine , chunksize=5000)
load_dataframe(checkin_df, 'checkin', engine , chunksize=5000)

file_path = r"C:\Users\HP\Documents\Restaurent_database\yelp_academic_dataset_business.json"
chunk_size = 5000
chunks=[] 

with open(file_path, 'r', encoding='utf-8') as f:
    batch = []
    for i, line in enumerate(f):
        batch.append(json.loads(line))
        if (i+1) % chunk_size == 0:
            chunk_df = pd.DataFrame(batch)
            chunks.append(chunk_df)
            batch = []
    # last batch
    if batch:
        chunk_df = pd.DataFrame(batch)
        chunks.append(chunk_df)

business_df = pd.concat(chunks, ignore_index=True) 
# print(business_df.shape)

file_path = r"C:\Users\HP\Documents\Restaurent_database\yelp_academic_dataset_checkin.json"
chunk_size = 5000
chunks=[] 

with open(file_path, 'r', encoding='utf-8') as f:
    batch = []
    for i, line in enumerate(f):
        batch.append(json.loads(line))
        if (i+1) % chunk_size == 0:
            chunk_df = pd.DataFrame(batch)
            chunks.append(chunk_df)
            batch = []
    # last batch
    if batch:
        chunk_df = pd.DataFrame(batch)
        chunks.append(chunk_df)

checkin_df = pd.concat(chunks, ignore_index=True) 
# print(checkin_df.shape)

file_path = r"C:\Users\HP\Documents\Restaurent_database\yelp_academic_dataset_review.json"
chunk_size = 20000
chunks = []

with open(file_path, 'r', encoding='utf-8') as f:
    batch = []
    for i, line in enumerate(f):
        batch.append(json.loads(line))
        if (i+1) % chunk_size == 0:
            chunk_df = pd.DataFrame(batch)
            chunks.append(chunk_df)
            batch = []
    # last batch
    if batch:
        chunk_df = pd.DataFrame(batch)
        chunks.append(chunk_df)

review_df = pd.concat(chunks, ignore_index=True)
# print(review_df.shape)

file_path = r"C:\Users\HP\Documents\Restaurent_database\yelp_academic_dataset_tip.json"
chunk_size = 20000
chunks = []

with open(file_path, 'r', encoding='utf-8') as f:
    batch = []
    for i, line in enumerate(f):
        batch.append(json.loads(line))
        if (i+1) % chunk_size == 0:
            chunk_df = pd.DataFrame(batch)
            chunks.append(chunk_df)
            batch = []
    # last batch
    if batch:
        chunk_df = pd.DataFrame(batch)
        chunks.append(chunk_df)

tip_df = pd.concat(chunks, ignore_index=True)
# print(tip_df.shape)

file_path = r"C:\Users\HP\Documents\Restaurent_database\yelp_academic_dataset_user.json"
chunk_size = 20000
chunks = []

with open(file_path, 'r', encoding='utf-8') as f:
    batch = []
    for i, line in enumerate(f):
        batch.append(json.loads(line))
        if (i+1) % chunk_size == 0:
            chunk_df = pd.DataFrame(batch)
            chunks.append(chunk_df)
            batch = []
    # last batch
    if batch:
        chunk_df = pd.DataFrame(batch)
        chunks.append(chunk_df)

user_df = pd.concat(chunks, ignore_index=True)
# print(user_df.shape)
# Print shapes for verification
print(business_df.shape)
print(checkin_df.shape)
print(review_df.shape)
print(tip_df.shape)
print(user_df.shape)


# Drop specified columns from business_df
business_df.drop(['attributes', 'hours'], axis=1, inplace=True)

from sqlalchemy import create_engine

# Create a SQLite engine
engine = create_engine('sqlite:///yelp.db')

# Define function to load DataFrame into a SQL table with chunksize
def load_dataframe(df, table_name, engine, chunksize=5000):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=chunksize)


# Load each DataFrame into a separate table using chunking for large DataFrames
load_dataframe(business_df, 'business', engine , chunksize=5000)
load_dataframe(review_df, 'review', engine, chunksize=5000)  # Large file uses chunksize
load_dataframe(user_df, 'user', engine , chunksize=5000)
load_dataframe(tip_df, 'tip', engine , chunksize=5000)
load_dataframe(checkin_df, 'checkin', engine , chunksize=5000)

