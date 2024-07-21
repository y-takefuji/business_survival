import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('jpkorea.csv')

# Filter the data
variables = ["Death rate of employer enterprises", "Birth rate of employer enterprises", 
             "Number of births (employer enterprises)", "Number of deaths (employer enterprises)"]
df = df[df['Variable'].isin(variables)]
df = df[df['Size Class'] == 'Total']
df = df[df['OBS_STATUS'] == 'A']

# Sort the data
df = df.sort_values('TIME_PERIOD')

# Ask the user to select countries
print("Select up to 2 countries by number (separated by space):")
for i, country in enumerate(df['Country'].unique(), start=1):
    print(f"{i}. {country}")
selected_countries = input().split()
selected_countries = [df['Country'].unique()[int(i)-1] for i in selected_countries]

# Filter the selected countries and apply the filter for Korea only to the subset of the data for Korea
dfs = []
for country in selected_countries:
    country_df = df[df['Country'] == country]
    if country == "Korea":
        country_df = country_df[country_df['ISIC4'].isin(["Total industry, construction and market services except holding companies", "Business economy"])]
    dfs.append(country_df)
df = pd.concat(dfs)

# Plot the graph
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
styles = ['-', '--', '-.', ':']
widths = [1, 2]
lines = []
labels = []
for i, (country, country_df) in enumerate(df.groupby('Country')):
    for j, (variable, variable_df) in enumerate(country_df.groupby('Variable')):
        if 'rate' in variable.lower():
            ax = ax1
            ax.set_ylabel('Rate', color='black')
        else:
            ax = ax2
            ax.set_ylabel('Number of Cases', color='black')
        line, = ax.plot(variable_df['TIME_PERIOD'], variable_df['OBS_VALUE'], 
                color='black', linestyle=styles[(i*len(variables)+j)%len(styles)], linewidth=widths[i%len(widths)])
        lines.append(line)
        labels.append(f"{country} - {variable}")

# Set labels and legend
ax1.set_xlabel('TIME_PERIOD')

# Shrink current axis's height by 10% on the bottom to make room for the legend
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width, box.height * 0.9])
ax2.set_position([box.x0, box.y0, box.width, box.height * 0.9])

# Add a legend below the plot with one column per legend item
plt.legend(lines, labels, bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=1)

plt.tight_layout()
filename = '_'.join(selected_countries) + '.csv'
df.to_csv(filename, index=False)
plt.savefig(filename+'.png',dpi=300)
plt.show()

