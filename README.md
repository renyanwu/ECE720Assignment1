# ECE720Assignment1

Assignment#1
Yanwu Ren

Github link: https://github.com/renyanwu/ECE720Assignment1

Step 1: I used the query below to look for what tags combination has 500 - 1000 questions and answers:
------------------------------------------------------------
select num_que.tags, n_que + n_ans as n
from
(
select count(*) as n_que, Tags
from Posts
group by Tags
) as num_que
join
(
select Tags, sum(n) as n_ans from Posts
join
(
select ParentId as Id, count(*) as n from Posts
where PostTypeId = 2
group by ParentId
) as ans
on Posts.Id = ans.Id
group by Tags
) as num_ans
on num_que.tags = num_ans.tags
where n_que + n_ans >= 500 and n_que + n_ans <= 1000
------------------------------------------------------------
Then I got the results, some of the results showed in table below, and I chose <.net><linq> as my tags to do this assignment and there are 721 posts.

Step 2: I used the query below to get the raw data and downloaded the dataset and renamed it to allPosts.tsv
------------------------------------------------------------
select * from Posts
where id in (select id from Posts where Tags = '<.net><linq>')
or id in (
select id from Posts where ParentId in
(select id from Posts where Tags = '<.net><linq>')
)
------------------------------------------------------------

Step 3: Then I wrote a python script “reformat.py” shown below to remove the tab syntax, make it tab-separated, get the allPosts-metaData.tsv and generate the edges file between answers and askers:
------------------------------------------------------------
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

------------------------------------------------------------
Step 4: When I got the edges file, I used R to transfer the edges to adjacency matrix and plotted the graph. Then I found the giant component using component.largest() and plot the component. R codes are shown below:
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


