import pandas as pd

""" ALREADY CLEANED DATA """
# import cleaned data
df = pd.read_csv("data/counts.csv", header=0, index_col="id")
# print(df.head())
""" END OF ALREADY CLEANED DATA """


# Raw cols and import of raw data
names = [
    "period",
    "code",
    "doc_id",
    "idk",
    "name",
    "uid",
    "party",
    "region",
    "vote",
    "type",
    "number2",
    "sex",
    "year_of_birth",
    "date",
]
raw_df = pd.read_csv("data/votering-201920.csv", names=names)

# grab subset and reset index
parties = raw_df[["name", "party"]].reset_index(drop=True)
parties.columns = ["id", "party"]

# lowercase
parties.id = parties.id.apply(lambda x: x.lower())

# drop duplicate ids and reindex with id (name)
parties = parties.drop_duplicates()
parties = parties.set_index("id")
# print(parties.head())

# Join raw party affiliations on cleaned df
main_df = pd.merge(df, parties, left_index=True, right_index=True)


print(main_df.head())

path = "data/countsparties.csv"
print(f"Exporting to: {path}")
main_df.to_csv(path)
