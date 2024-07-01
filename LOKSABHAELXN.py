import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'class': 'table'})

party_data = []
for row in table.find_all('tr'):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    party_data.append([ele for ele in cols if ele])

party_data = [row for row in party_data if len(row) > 0 and row[0] != 'Party']

df = pd.DataFrame(party_data, columns=['Party', 'Won', 'Leading', 'Total'])

df['Won'] = df['Won'].astype(int)
df['Leading'] = df['Leading'].astype(int)
df['Total'] = df['Total'].astype(int)

total_seats = df['Won'].sum()

insights = []
insights.append(f"Total number of parties participated: {df.shape[0]}")
insights.append(f"Total seats won by all parties: {total_seats}")
top_party = df.loc[df['Won'].idxmax()]['Party']
top_party_seats = df['Won'].max()
insights.append(f"Party with the most seats won: {top_party} ({top_party_seats} seats)")
bottom_party = df.loc[df['Won'].idxmin()]['Party']
bottom_party_seats = df['Won'].min()
insights.append(f"Party with the least seats won: {bottom_party} ({bottom_party_seats} seats)")
average_seats_won = df['Won'].mean()
insights.append(f"Average number of seats won by parties: {average_seats_won:.2f}")
parties_more_than_20 = df[df['Won'] > 20].shape[0]
insights.append(f"Number of parties that won more than 20 seats: {parties_more_than_20}")
parties_no_seats = df[df['Won'] == 0].shape[0]
insights.append(f"Number of parties that won no seats: {parties_no_seats}")
top_3_parties_seats = df.nlargest(3, 'Won')['Won'].sum()
insights.append(f"Total number of seats won by the top 3 parties: {top_3_parties_seats}")
top_party_proportion = (top_party_seats / total_seats) * 100
insights.append(f"Proportion of total seats won by the top party: {top_party_proportion:.2f}%")
df['Total_Seats'] = df['Won'] + df['Leading']
highest_total_seats_party = df.loc[df['Total_Seats'].idxmax()]['Party']
highest_total_seats = df['Total_Seats'].max()
insights.append(f"Party with the highest number of total seats (won + leading): {highest_total_seats_party} ({highest_total_seats} seats)")

for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")

plt.figure(figsize=(10, 6))
plt.bar(df['Party'], df['Won'], color='skyblue')
plt.xlabel('Party')
plt.ylabel('Seats Won')
plt.title('Total Seats Won by Parties')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 8))
plt.pie([top_party_seats, total_seats - top_party_seats], labels=[f'{top_party} ({top_party_seats})', 'Other Parties'], autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue'])
plt.title('Proportion of Seats Won by Top Party')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(df['Won'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Seats Won')
plt.ylabel('Frequency')
plt.title('Distribution of Seats Won by Parties')
plt.tight_layout()
plt.show()



import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup

url = "https://results.eci.gov.in/AcResultByeJune2024/index.htm"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
constituency_boxes = soup.find_all('div', class_='col-md-3 col-12')

constituency_data = []
for box in constituency_boxes:
    h3 = box.find('h3').text.strip()  # Constituency name and number
    h4 = box.find('h4').text.strip()  # State name
    h5 = box.find('h5').text.strip()  # Winner's name
    h6 = box.find('h6').text.strip()  # Winning party
    
    constituency_data.append({
        'Constituency': h3,
        'State': h4,
        'Winner': h5,
        'Party': h6
    })

df = pd.DataFrame(constituency_data)

print(df.head())

df.to_csv('constituency_results.csv', index=False)
print(f"Scraped {len(df)} constituencies.")

plt.figure(figsize=(10, 6))
sns.countplot(y='Party', data=df, palette='viridis')
plt.xlabel('Number of Constituencies')
plt.ylabel('Party')
plt.title('Number of Constituencies Won by Parties')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
df.groupby(['State', 'Party']).size().unstack().plot(kind='bar', stacked=True, colormap='Set3')
plt.xlabel('State')
plt.ylabel('Number of Winners')
plt.title('Winners by State and Party')
plt.legend(title='Party', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()





