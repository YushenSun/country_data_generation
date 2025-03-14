import numpy as np
import pandas as pd

number_rows = 100 # Number of rows you want

# Define the columns for the X data (country states)
columns_X = [
    'GDP', 'Unemployment Rate', 'Inflation Rate', 'Foreign Debt',
    'Government Spending', 'Military Spending', 'Education Spending',
    'Health Spending', 'Environment Spending', 'Technology Investment',
    'Internet Penetration', 'Energy Production', 'Energy Consumption',
    'Pollution Level', 'Population', 'Urbanization Rate', 'Political Stability',
    'Human Development Index', 'Public Trust', 'Freedom of Press', 'Corruption Index',
    'Military Power', 'Alliances', 'Environmental Quality', 'Natural Resources Availability',
    'Trade Balance', 'Public Health', 'Democracy Index', 'Technology Adoption Rate',
    'Cultural Influence', 'Global Trade Index'
]

# Define the columns for the Y data (future actions)
future_action_columns = [
    'Major Political Actions - Future', 'Economic Policy Adjustment - Future', 'Military Activity - Future', 'Diplomatic Policy Change - Future',
    'Social Policy and Welfare Reform - Future', 'Environmental and Energy Policy - Future', 'Technology and Innovation Strategy - Future', 'Public Health and Safety Policy - Future'
]

# Define the action impact rules (positive and negative direction with weights)
action_impacts = {
    'Major Political Actions': {'Positive Direction': 1, 'Negative Direction': -1},
    'Economic Policy Adjustment': {'Positive Direction': 1, 'Negative Direction': -1},
    'Military Activity': {'Positive Direction': 1, 'Negative Direction': -1},
    'Diplomatic Policy Change': {'Positive Direction': 1, 'Negative Direction': -1},
    'Social Policy and Welfare Reform': {'Positive Direction': 1, 'Negative Direction': -1},
    'Environmental and Energy Policy': {'Positive Direction': 1, 'Negative Direction': -1},
    'Technology and Innovation Strategy': {'Positive Direction': 1, 'Negative Direction': -1},
    'Public Health and Safety Policy': {'Positive Direction': 1, 'Negative Direction': -1}
}

# Define the action columns for the dataframe
action_columns = [
    'Major Political Actions', 'Economic Policy Adjustment', 'Military Activity', 'Diplomatic Policy Change',
    'Social Policy and Welfare Reform', 'Environmental and Energy Policy', 'Technology and Innovation Strategy', 'Public Health and Safety Policy'
]

# Initialize the starting values for each parameter based on realistic data (for example, as of 2025)
initial_values = {
    'GDP': 15000,  # Initial GDP in billion USD
    'Unemployment Rate': 5.0,  # Initial Unemployment Rate %
    'Inflation Rate': 2.5,  # Initial Inflation Rate %
    'Foreign Debt': 500,  # Foreign Debt in billion USD
    'Government Spending': 1200,  # Government Spending in billion USD
    'Military Spending': 200,  # Military Spending in billion USD
    'Education Spending': 100,  # Education Spending in billion USD
    'Health Spending': 150,  # Health Spending in billion USD
    'Environment Spending': 50,  # Environment Spending in billion USD
    'Technology Investment': 300,  # Technology Investment in billion USD
    'Internet Penetration': 75.0,  # Initial Internet Penetration %
    'Energy Production': 1200,  # Energy Production in TWh
    'Energy Consumption': 1150,  # Energy Consumption in TWh
    'Pollution Level': 15,  # Pollution Level
    'Population': 1000000000,  # Population
    'Urbanization Rate': 70.0,  # Urbanization Rate %
    'Political Stability': 7.5,  # Political Stability (scale 0-10)
    'Human Development Index': 0.8,  # HDI (scale 0-1)
    'Public Trust': 65.0,  # Public Trust %
    'Freedom of Press': 70.0,  # Freedom of Press %
    'Corruption Index': 40.0,  # Corruption Index
    'Military Power': 1000,  # Military Power (index)
    'Alliances': 3,  # Number of alliances
    'Environmental Quality': 75.0,  # Environmental Quality %
    'Natural Resources Availability': 120,  # Natural Resources Availability
    'Trade Balance': 10,  # Trade Balance
    'Public Health': 85.0,  # Public Health %
    'Democracy Index': 7.0,  # Democracy Index
    'Technology Adoption Rate': 0.6,  # Technology Adoption Rate
    'Cultural Influence': 50.0,  # Cultural Influence (index)
    'Global Trade Index': 0.7  # Global Trade Index
}

# Generate  number_rows rows of data for actions (X) and apply the rules based on the above factors
data_actions = []
for i in range(number_rows):
    row = []
    for action in action_impacts:
        # Define logic for actions based on realistic tendencies
        if action == 'Economic Policy Adjustment':
            if initial_values['Inflation Rate'] > 3.0:  # High inflation triggers contractionary policies
                action_type = 'Negative Direction'
            else:  # Economic slowdown triggers stimulative policies
                action_type = 'Positive Direction'
        elif action == 'Military Activity':
            if initial_values['Military Spending'] > 250:  # High spending indicates military expansion
                action_type = 'Positive Direction'
            else:  # Low military spending indicates likely contraction
                action_type = 'Negative Direction'
        elif action == 'Major Political Actions':
            if initial_values['Public Trust'] < 60:  # Low public trust favors political reforms
                action_type = 'Positive Direction'
            else:  # High trust limits political upheaval
                action_type = 'Negative Direction'
        else:
            action_type = np.random.choice(['Positive Direction', 'Negative Direction'])

        impact = action_impacts[action]
        
        # Randomize the actions with small float values rather than just 1 or -1
        if np.random.rand() < 0.3:  # 30% chance of no action (value = 0)
            action_value = 0
        else:
            action_value = impact[action_type] * np.random.uniform(0.5, 1.5)  # Randomize with magnitude 0.5 to 1.5 times

        row.append(round(action_value, 2))
    data_actions.append(row)

# Future actions based on previous period (Y)
data_future_actions = []
for i in range(number_rows):
    row = []
    for action in future_action_columns:
        action_type = np.random.choice(['Positive Direction', 'Negative Direction'])
        impact = action_impacts[action.split(' - ')[0]]
        
        # Randomize the future action with small float values
        future_value = impact[action_type] * np.random.uniform(0.5, 1.5)  # Randomize with magnitude 0.5 to 1.5 times
        row.append(round(future_value, 2))
    data_future_actions.append(row)

# Combine X (current data) and Y (future predictions)
df_actions = pd.DataFrame(data_actions, columns=action_columns)
df_future_actions = pd.DataFrame(data_future_actions, columns=future_action_columns)

# Generate X data with realistic fluctuations
data_X_optimized = []
current_values = initial_values.copy()

for i in range(number_rows):
    # Create a new row based on the current values, applying small fluctuations
    row = []
    for col in columns_X:
        change = np.random.uniform(-2, 2)  # Apply small fluctuations
        new_value = current_values[col] * (1 + change / 100) if 'Rate' in col or 'Index' in col else current_values[col] + change
        current_values[col] = new_value
        row.append(round(new_value, 2))
    data_X_optimized.append(row)

# Combine all the data
df_X_optimized = pd.DataFrame(data_X_optimized, columns=columns_X)
df_optimized = pd.concat([df_X_optimized, df_actions, df_future_actions], axis=1)

# Save the data to a CSV file for further analysis
df_optimized.to_csv('country_data_optimized.csv', index=False)

# Display the first few rows of the dataframe for verification
print("Displaying Optimized Country Actions and Predictions:")
print(df_optimized.head())
