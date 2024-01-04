import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming you have a CSV file with two columns - 'TagName' and 'CategoryName'
data = pd.read_csv('tagcats.csv')
# filtered_data = data[data['CategoryName'] == 'ENERGY']

# Create a count plot
# plt.figure(figsize=(10,6))
# sns.countplot(x='TagName', hue='CategoryName', data=filtered_data)
# plt.show()


# First, we need to compute the value for each combination of TagName and CategoryName.
# For simplicity let's assume we can simply count them.

heatmap_data = data.groupby(['TagName', 'CategoryName']).size().unstack().fillna(0)

plt.figure(figsize=(10,6))
sns.heatmap(heatmap_data)
plt.show()
