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



