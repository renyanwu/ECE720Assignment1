import pandas as pd

with open('data/questions.json', 'r') as f:
	questions = eval(f.read())['items']
questions = pd.DataFrame(questions)[['owner', 'question_id']].dropna()


with open('data/answers.json', 'r') as f:
	ans = eval(f.read())
ans = pd.DataFrame(ans)[['owner', 'question_id']].dropna()

print(questions.head())
print(ans.head())

answers_map = {}
for i, row in ans.iterrows():
    if 'user_id' in row['owner']:
        answers_map[row['question_id']] = row['owner']['user_id']

q_a = {}
for i, row in questions.iterrows():
    if 'user_id' in row['owner'] and row['question_id'] in answers_map:
        q_a[row['owner']['user_id']] = answers_map[row['question_id']]

df_aa = {'asker':list(q_a.keys()), 'answer':list(q_a.values())}
df_aa = pd.DataFrame(df_aa, columns=['asker', 'answer'])
df_aa.to_csv('data/ask2answers.tsv', index=False, sep = '\t')




'''
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

df_aa = {'asker':list(ask_ans.keys()), 'answer':list(ask_ans.values())}
df_aa = pd.DataFrame(df_aa, columns=['asker', 'answer'])
df_aa.to_csv('data/ask2answers.tsv', index=False, sep = '\t')
'''