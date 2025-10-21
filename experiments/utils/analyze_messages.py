import pandas as pd

# Load the previously generated data from the initial analysis
df_interactions = pd.read_csv('filtered_interactions.csv')

# Group by task category and calculate the necessary statistics
category_summary = df_interactions.groupby('task_category').agg(
    # Sums to be used for averages
    tester_message_sum=('tester_message_count', 'sum'),
    npc_message_sum=('NPC_message_count', 'sum'),
    total_messages_sum=('total_messages', 'sum'),
    # Other required stats
    task_count=('task', 'count'),
    min_messages=('total_messages', 'min'),
    max_messages=('total_messages', 'max'),
    median_messages=('total_messages', 'median')
)

# Calculate the per-task averages as requested
category_summary['Agent Messages (Avg)'] = category_summary['tester_message_sum'] / category_summary['task_count']
category_summary['Colleague Messages (Avg)'] = category_summary['npc_message_sum'] / category_summary['task_count']
category_summary['Total Messages (Avg)'] = category_summary['total_messages_sum'] / category_summary['task_count']

# Rename columns for the final table
category_summary.rename(columns={
    'task_count': 'Task Count',
    'min_messages': 'Min',
    'max_messages': 'Max',
    'median_messages': 'Median'
}, inplace=True)

# Select and reorder columns for the final output, excluding 'Std Deviation'
final_columns = [
    'Task Count',
    'Agent Messages (Avg)',
    'Colleague Messages (Avg)',
    'Total Messages (Avg)',
    'Min',
    'Max',
    'Median'
]
final_table = category_summary[final_columns]

# Format the float columns to two decimal places for better readability
for col in final_table.columns:
    if final_table[col].dtype == 'float64':
        final_table[col] = final_table[col].round(2)

# Generate and print the final table in Markdown format
print(final_table.to_markdown(index=True))
