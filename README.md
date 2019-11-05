# ECE720Assignment1

Step 1: I used the query below to look for what tags combination has 500 - 1000 questions and answers:
------------------------------------------------------------
select Tags, n from
(select count(*) as n, Tags from Posts group by Tags) m
where n >= 500 and n <= 1000
------------------------------------------------------------
Then I got the results, some of the results showed in table below, and I chose <javascript><jquery><html><css><animation> as my tags to do this assignment and there are 522 posts.

Step 2: I wrote a python script "get_data.py" below to use the API to get the questions and the answers of these questions using the question_id. Then I used the question_id and answer_id to get all the posts. After that, I removed the tab syntax and save the data in "allPost.tsv" and save the ids and type as  "allPosts-metaData.tsv".
------------------------------------------------------------
from stackapi import StackAPI
import math
import pandas as pd

SITE = StackAPI('stackoverflow')
SITE.page_size = 100
SITE.max_pages= 500

questions = SITE.fetch('questions', tagged='javascript;jquery;html;css;animation')

questions = str(questions)
with open('data/questions.json', 'w') as f:
    f.write(questions)

with open('data/questions.json', 'r') as f:
	questions = eval(f.read())['items']
qid = [q['question_id'] for q in questions]

times = math.ceil(len(qid) / 100.0)
ans = []
for i in range(times - 1):
	ans += SITE.fetch('/questions/{ids}/answers', ids=qid[i * 100: (i+1) * 100])['items']
ans += SITE.fetch('/questions/{ids}/answers', ids=qid[(i+1) * 100:])['items']
with open('data/answers.json', 'w') as f:
	f.write(str(ans))

with open('data/answers.json', 'r') as f:
	ans = eval(f.read())
aid = [a['answer_id'] for a in ans]
ids = qid + aid


times = math.ceil(len(ids) / 100.0)
posts = []
for i in range(times - 1):
	posts += SITE.fetch('/posts/{ids}', ids=ids[i * 100: (i+1) * 100])['items']
posts += SITE.fetch('/posts/{ids}', ids=ids[(i+1) * 100:])['items']
with open('data/posts.json', 'w') as f:
	f.write(str(posts))

with open('data/posts.json', 'r') as f:
	posts = eval(f.read())
df = pd.DataFrame(posts)
df[['owner']] = df[['owner']].astype(str)
df['owner'] = df['owner'].map(lambda x: x.replace('\t', ''))
df.to_csv("allPosts.tsv", index=False, sep = '\t')

df = pd.DataFrame(posts)
df = df[['owner', 'post_type', 'post_id']]
df = df.dropna()
df['user_id'] = df['owner'].map(lambda x: x['user_id'])
df = df[['user_id', 'post_type', 'post_id']]
df.to_csv("data/allPosts-metaData.tsv", index = False, sep = '\t')
------------------------------------------------------------
Step 3: Then I wrote a python script “process.py” using the questions and the answers to generate the edges file " ask2answers.tsv" between answers and askers:
------------------------------------------------------------
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

------------------------------------------------------------
Step 4: When I got the edges file, I used R to transfer the edges to adjacency matrix and plotted the graph. Then I found the giant component using component.largest() and plot the component. Then I saved the two graphs to files "askerAnswerer.tsv" and " asker-answer-giant.tsv". R codes and graphs are shown below:
------------------------------------------------------------
ask2answers = read.csv("../data/ask2answers.tsv", sep = '\t')
net <- graph_from_data_frame(d=ask2answers, directed=T) 
mat = as.matrix(as_adjacency_matrix(net))
write.table(mat, file ="../data/askerAnswerer.tsv")
gplot(mat)
giant_com = component.largest(mat, connected = "weak", result="graph")
write.table(giant_com, file ="../data/asker-answer-giant.tsv")
gplot(giant_com)

------------------------------------------------------------



