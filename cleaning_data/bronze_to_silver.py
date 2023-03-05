import pandas as pd

###################################################################
# ------------- BRONZE TO SILVER ----------------------------------
################################################################### 

# read CSV file with new activities exported from web
# BRONZE LAYER
df1 = pd.read_csv('Activities.csv')

# read CSV file that was concatenated last
df2 = pd.read_csv('Activities_silver.csv')

print(df1)

# concatenate the two dataframes vertically and drop duplicate rows
concatenated_df = pd.concat([df1, df2]).drop_duplicates()

# save the concatenated dataframe to a new CSV file
# SILVER LAYER
concatenated_df.to_csv('Activities_silver.csv', index=False)

print('Data concatenated')


