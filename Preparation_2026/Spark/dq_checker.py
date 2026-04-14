import pandas as pd 

valid_gender=['male','female','other']

def validate_row(row):
    if pd.isnull(row["id"]) or not str(row["id"]).isdigit():
        print ("id is not valid",row["id"])
    if pd.isnull(row["name"]) or not str(row["name"]).isalpha():
        print ("name is not valid",row["name"])
    if not str(row["age"]).isdigit():
        print("age is not valid",row["age"])
    if str(row["gender"]).lower() not in valid_gender :
        print ("gender is not valid",row["gender"])
    print ("Columns satisfies the check conditions")

df=pd.read_csv("Data.csv")


for index,row in df.iterrows():
    validate_row(row)