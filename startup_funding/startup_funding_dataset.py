import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Reads your CSV file
df = pd.read_csv('startup_funding_dataset.csv')
print(df.head())
print(df.columns)

# Info and basic summary
print(df.info())
print(df.describe(include='all'))

# Rename columns if they have leading/trailing spaces
df.columns = [col.strip() for col in df.columns]

# Convert date
df['Date_dd/mm/yyyy'] = pd.to_datetime(df['Date_dd/mm/yyyy'], dayfirst=True, errors='coerce')

# Handle missing values
df = df.dropna(subset=['Startup_Name', 'Industry_Vertical', 'City_Location', 'Investors_Name',
                       'Investment_Type', 'Amount_in_USD'])
df['Amount_in_USD'] = pd.to_numeric(df['Amount_in_USD'], errors='coerce').fillna(0)

# Show number of startups per city
city_counts = df['City_Location'].value_counts().head(10)
print(city_counts)

# Top-funded startups
top_funded = df[['Startup_Name', 'Amount_in_USD']].groupby('Startup_Name').sum().sort_values('Amount_in_USD', ascending=False).head(10)
print(top_funded)

# Funding trend over years
df['Year'] = df['Date_dd/mm/yyyy'].dt.year
yearly_funding = df.groupby('Year')['Amount_in_USD'].sum()
yearly_funding.plot(kind='line')
plt.title('Total Funding by Year')
plt.xlabel('Year')
plt.ylabel('Funding (USD)')
plt.savefig("funding trend over years.png", bbox_inches='tight', dpi=300)

plt.show()

# Top industries by total funding
industry_funding = df.groupby('Industry_Vertical')['Amount_in_USD'].sum().sort_values(ascending=False).head(10)
industry_funding.plot(kind='bar')
plt.title('Top Funded Industries')
plt.ylabel('Funding Amount (USD)')
plt.xlabel('Industry')
plt.savefig("funded industries.png", bbox_inches='tight', dpi=300)
plt.show()

# Top investors by number of investments
investor_counts = df['Investors_Name'].value_counts().head(10)
investor_counts.plot(kind='barh')
plt.title('Most Active Investors')
plt.xlabel('Number of Investments')
plt.ylabel('Investor')
plt.savefig("investor.png", bbox_inches='tight', dpi=300)
plt.show()

# Basic statistics
print("Mean funding:", np.mean(df['Amount_in_USD']))
print("Median funding:", np.median(df['Amount_in_USD']))
print("Max funding:", np.max(df['Amount_in_USD']))

# Export summaries
industry_funding.to_excel('industry_funding_summary.xlsx')
top_funded.to_excel('top_funded_startups.xlsx')
