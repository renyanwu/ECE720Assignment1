import pandas as pd

df = pd.read_csv("data/allPosts.tsv")
df['Body'] = df['Body'].map(lambda x: x.replace('\t', ''))
df.to_csv("data/allPosts.tsv", sep = '\t', index = False)

df_meta = df[['Id', 'PostTypeId', 'OwnerUserId']]
df_meta = df_meta.dropna()
df_meta[['OwnerUserId']] = df_meta[['OwnerUserId']].astype(int)
df_meta.to_csv("data/allPosts-metaData.tsv", sep = '\t', index = False)


df_ans = df[df['PostTypeId'] == 2][['ParentId', 'OwnerUserId']]
df_ans = df_ans.dropna()
df_ans[['ParentId', 'OwnerUserId']] = df_ans[['ParentId', 'OwnerUserId']].astype(int)
answers_map = {}
for i, row in df_ans.iterrows():
    answers_map[row['ParentId']] = row['OwnerUserId']

ask_ans = {}
for index, row in df_meta.iterrows():
    if row['PostTypeId'] == 1 and row['Id'] in answers_map:
        ask_ans[int(row['OwnerUserId'])] = answers_map[row['Id']]

df_aa = {'answer':list(ask_ans.values()), 'asker':list(ask_ans.keys())}
df_aa = pd.DataFrame(df_aa, columns=['answer', 'asker'])
df_aa.to_csv('data/ask2answers.tsv', index=False, sep = '\t')
