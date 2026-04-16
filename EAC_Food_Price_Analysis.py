import pandas as pd
import matplotlib.pyplot as plt

# Load the three files
# Replace 'filename.csv' with the actual names of the files you downloaded
df_kenya = pd.read_csv('KENYA_wfp_food_prices.csv')
df_uganda = pd.read_csv('UGANDA_wfp_food_prices.csv')
df_tanzania = pd.read_csv('TANZANIA_wfp_food_prices.csv')

# Check the first 5 rows of Kenya to see the column names
print("Kenya Data Preview:")
print(df_kenya.head())
# Show columns for all three to compare
print(f"Kenya Columns: {df_kenya.columns.tolist()}")
print(f"Uganda Columns: {df_uganda.columns.tolist()}")
print(f"Tanzania Columns: {df_tanzania.columns.tolist()}")
# 1. Add a country identifier so we can compare them later
df_kenya['country'] = 'Kenya'
df_uganda['country'] = 'Uganda'
df_tanzania['country'] = 'Tanzania'

# 2. Merge them into one master dataframe
df_master = pd.concat([df_kenya, df_uganda, df_tanzania], ignore_index=True)

# 3. Quick Audit: How many records do we have from each?
print("Project Dataset Overview:")
print(df_master['country'].value_counts())

# 4. Check for missing values (Essential for your 'Data Quality' LinkedIn post)
print("\nMissing Values Audit:")
print(df_master.isnull().sum())
# 1. Convert the 'date' column to actual datetime objects
df_master['date'] = pd.to_datetime(df_master['date'])

# 2. Filter for just White Maize (the most critical staple)
maize_df = df_master[df_master['commodity'] == 'Maize (white)']

# 3. Let's look at the average price per country for the year 2026
maize_2026 = maize_df[maize_df['date'].dt.year == 2026]
avg_prices = maize_2026.groupby('country')['usdprice'].mean().sort_values(ascending=False)

print("Average Maize Price (USD) in 2026:")
print(avg_prices)
# 1. Convert date to datetime objects (Crucial for the .dt accessor)
df_master['date'] = pd.to_datetime(df_master['date'])

# 2. THE FIX: Normalize Kenya's prices (Standardizing 90 KG bags to 1 KG)
# We do this BEFORE plotting so the 'usdprice' is already corrected
df_master.loc[(df_master['country'] == 'Kenya') & (df_master['unit'] == '90 KG'), 'usdprice'] = df_master['usdprice'] / 90

# 3. Create the Figure
plt.figure(figsize=(12, 6))

# 4. Plot each country
for country in ['Kenya', 'Tanzania', 'Uganda']:
    # Filter for White Maize
    country_data = df_master[(df_master['country'] == country) & (df_master['commodity'] == 'Maize (white)')]
    
    # Calculate yearly average using the now-corrected usdprice
    yearly = country_data.groupby(country_data['date'].dt.year)['usdprice'].mean()
    plt.plot(yearly.index, yearly.values, label=country, linewidth=2)

# 5. Branding, Labels, and Watermarks
plt.title('Normalized White Maize Prices: Kenya vs. Uganda vs. Tanzania (2006-2026)', fontsize=14)
plt.ylabel('Average Price per KG (USD)', fontsize=12)
plt.xlabel('Year', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Add your signature watermarks
plt.text(0.95, 0.05, 'Analyzed by Ann Nyakwea', fontsize=10, color='gray', ha='right', va='bottom', alpha=0.6, transform=plt.gca().transAxes)
plt.text(0.05, 0.95, 'github.com/ann-nyakwea', fontsize=9, color='blue', alpha=0.4, transform=plt.gca().transAxes)

plt.show()

# 6. Save the Cleaned Data for Power BI
df_master.to_csv('EAC_Food_Prices_Cleaned.csv', index=False)
