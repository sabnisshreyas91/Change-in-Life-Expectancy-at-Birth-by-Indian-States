
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
print('imported necessary libraries')
print('')

response=requests.get('https://en.wikipedia.org/wiki/List_of_Indian_states_by_life_expectancy_at_birth')
content=response.content
parser=BeautifulSoup(content,'html.parser')
table_html=parser.find_all('table')[1]
#the second table is the one with the data we are interested in, hence parser.find_all('table')[1]

df=pd.DataFrame(columns=('rank','state','life expectancy at birth 2010-14','life expectancy at birth 2002-06'))
print('scraped the necessary data from https://en.wikipedia.org/wiki/List_of_Indian_states_by_life_expectancy_at_birth and loaded it into data frame df')
print('')
for row in table_html.find_all('tr'):
    row_values=row.find_all('td')
    if ((len(row_values)==4)): #and (row_values[2].find(text=True)!='-' and row_values[3].find(text=True)!='-')): #we're interested in tracking how the life expectancy has changed over the 2 readings, so we can discard any rows where the reading for 2002-06 is not available
        df.loc[row_values[0].find(text=True)]=(row_values[0].find(text=True),row_values[1].find(text=True),float(row_values[2].find(text=True).replace('-','0')),float(row_values[3].find(text=True).replace('-','0')))
#Removing the row for 'India' which has rank '*'
df.drop('*',inplace=True)
print('deleted data for all India, as we are only interested in individual states for now.')
print('deleted data for states that have no data available for the first period(2002-2006) as we need to calculate change in l.e.b')
print('')
df['change in life expectancy at birth']=0
df.loc[df['life expectancy at birth 2002-06']!=0,['change in life expectancy at birth']]=df['life expectancy at birth 2010-14']-df['life expectancy at birth 2002-06']
df['% change in life expectancy at birth']=0
df.loc[df['life expectancy at birth 2002-06']!=0,['% change in life expectancy at birth']]=round(((df['life expectancy at birth 2010-14']-df['life expectancy at birth 2002-06'])/df['life expectancy at birth 2002-06'])*100,2)
print('calculated change in l.e.b and percent change in l.e.b for each state')
print('')

#Rename states thta fall out of figure boundary
df.loc[df['state']=='Jammu and Kashmir',['state']]='J&K'
df.loc[df['state']=='Andhra Pradesh',['state']]='A.P'
df.loc[df['state']=='Madhya Pradesh',['state']]='M.P'
df.loc[df['state']=='Uttar Pradesh',['state']]='U.P'

df=df.loc[df['change in life expectancy at birth']>0,:]
df.sort_values('life expectancy at birth 2002-06',ascending=False,inplace=True)
print('sorted data by l.e.b in 2002-2006')
print('')
fig,ax=plt.subplots(figsize=(15,6))

n=df.shape[0]

ind=np.arange(n)
width=0.4
change_in_le=list(df['change in life expectancy at birth'])
per_change_in_le=list(df['% change in life expectancy at birth'])

rects1=ax.bar(ind,change_in_le,width,color='b')
rects2=ax.bar(ind+width,per_change_in_le,width,color='g')

ax.set_ylabel('Life expectancy at birth (percentage)')
ax.set_title('Change in life expectancy at birth by State')
ax.set_xticks(ind+width)
ax.set_xticklabels(list(df['state']),rotation='vertical')

ax.legend((rects1,rects2),('change in %L.E','% change in %L.E'))

def autolabel(rects):

    for rect in rects:
        height=rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2,1.01*height
                , '%.1f' %                float(height)
                ,ha='center'
                ,va='bottom'
                )
autolabel(rects1)
autolabel(rects2)
plt.tight_layout()
plt.show()
