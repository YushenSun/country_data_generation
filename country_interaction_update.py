import numpy as np
import pandas as pd

number_rows = 522  # Number of rows you want

# Define the columns for the X data (country states for A and B and their relations)
columns_X = [
    # A state parameters
    'A GDP', 'A Unemployment Rate', 'A Inflation Rate', 'A Foreign Debt',
    'A Government Spending', 'A Military Spending', 'A Education Spending',
    'A Health Spending', 'A Environment Spending', 'A Technology Investment',
    'A Internet Penetration', 'A Energy Production', 'A Energy Consumption',
    'A Pollution Level', 'A Population', 'A Urbanization Rate', 'A Political Stability',
    'A Human Development Index', 'A Public Trust', 'A Freedom of Press', 'A Corruption Index',
    'A Military Power', 'A Alliances', 'A Environmental Quality', 'A Natural Resources Availability',
    'A Trade Balance', 'A Public Health', 'A Democracy Index', 'A Technology Adoption Rate',
    'A Cultural Influence', 'A Global Trade Index',

    # B state parameters
    'B GDP', 'B Unemployment Rate', 'B Inflation Rate', 'B Foreign Debt',
    'B Government Spending', 'B Military Spending', 'B Education Spending',
    'B Health Spending', 'B Environment Spending', 'B Technology Investment',
    'B Internet Penetration', 'B Energy Production', 'B Energy Consumption',
    'B Pollution Level', 'B Population', 'B Urbanization Rate', 'B Political Stability',
    'B Human Development Index', 'B Public Trust', 'B Freedom of Press', 'B Corruption Index',
    'B Military Power', 'B Alliances', 'B Environmental Quality', 'B Natural Resources Availability',
    'B Trade Balance', 'B Public Health', 'B Democracy Index', 'B Technology Adoption Rate',
    'B Cultural Influence', 'B Global Trade Index',

    # Relationship Parameters
    'A to B Imports', 'A to B Exports', 'B to A Imports', 'B to A Exports',
    'A Bond Status', 'B Bond Status', 'A Sovereignty Disputes', 'B Sovereignty Disputes',
    'Political Similarity', 'Ethnic Similarity', 'Cultural Compatibility'
]

# Define the action columns for the dataframe (only current actions for A and B)
action_columns = [
    'A Major Political Actions', 'A Economic Policy Adjustment', 'A Military Activity', 'A Diplomatic Policy Change',
    'A Social Policy and Welfare Reform', 'A Environmental and Energy Policy', 'A Technology and Innovation Strategy', 'A Public Health and Safety Policy',
    'B Major Political Actions', 'B Economic Policy Adjustment', 'B Military Activity', 'B Diplomatic Policy Change',
    'B Social Policy and Welfare Reform', 'B Environmental and Energy Policy', 'B Technology and Innovation Strategy', 'B Public Health and Safety Policy'
]

# Initialize an empty DataFrame for actions with columns and the appropriate number of rows
data_actions = pd.DataFrame(columns=action_columns, index=range(number_rows))
data_X_optimized = []  # Initialize an empty list for X data (states)

# First row initialization (start with 0 actions for all)
first_row_actions = [0] * len(action_columns)
data_actions.loc[0] = first_row_actions  # Add first row of actions

# Initialize the starting values for each parameter based on realistic data (for example, as of 2025)
initial_values = {
    'A Public Trust': 60.0,  # Initial Public Trust value for A
    'A Political Stability': 6.5,  # Initial Political Stability for A
    'Political Similarity': 0.6,  # Bilateral Political Similarity
    'A Trade Balance': 15,  # Trade balance (example value)
    # Add other state parameters here...
    'A GDP': 10000, 'A Unemployment Rate': 6.0, 'A Inflation Rate': 3.0, 'A Foreign Debt': 300, 'A Government Spending': 800,
    'A Military Spending': 150, 'A Education Spending': 70, 'A Health Spending': 120, 'A Environment Spending': 30, 'A Technology Investment': 250,
    'A Internet Penetration': 70.0, 'A Energy Production': 900, 'A Energy Consumption': 850, 'A Pollution Level': 20, 'A Population': 500000000,
    'A Urbanization Rate': 60.0, 'A Human Development Index': 0.75, 'A Freedom of Press': 60.0, 'A Corruption Index': 50.0,
    'A Military Power': 800, 'A Alliances': 2, 'A Environmental Quality': 70.0, 'A Natural Resources Availability': 100,
    'A Public Health': 80.0, 'A Democracy Index': 6.0, 'A Technology Adoption Rate': 0.5, 'A Cultural Influence': 40.0, 'A Global Trade Index': 0.6,
    'B GDP': 12000, 'B Unemployment Rate': 5.5, 'B Inflation Rate': 2.0, 'B Foreign Debt': 400, 'B Government Spending': 1000,
    'B Military Spending': 180, 'B Education Spending': 90, 'B Health Spending': 140, 'B Environment Spending': 40, 'B Technology Investment': 280,
    'B Internet Penetration': 80.0, 'B Energy Production': 1100, 'B Energy Consumption': 1000, 'B Pollution Level': 18, 'B Population': 750000000,
    'B Urbanization Rate': 75.0, 'B Political Stability': 8.0, 'B Human Development Index': 0.85, 'B Public Trust': 70.0, 'B Freedom of Press': 80.0,
    'B Corruption Index': 35.0, 'B Military Power': 1200, 'B Alliances': 4, 'B Environmental Quality': 80.0, 'B Natural Resources Availability': 110,
    'B Trade Balance': 20, 'B Public Health': 90.0, 'B Democracy Index': 8.0, 'B Technology Adoption Rate': 0.7, 'B Cultural Influence': 60.0, 'B Global Trade Index': 0.8,
    'A to B Imports': 200, 'A to B Exports': 150, 'B to A Imports': 180, 'B to A Exports': 130,
    'A Bond Status': 1, 'B Bond Status': 1, 'A Sovereignty Disputes': 0, 'B Sovereignty Disputes': 0,
    'Ethnic Similarity': 0.5, 'Cultural Compatibility': 0.7
}

# Generate state data and actions row by row
current_values = initial_values.copy()

# Initialize the action impact matrix M (the coefficients that define the action effects on the states)
M = np.zeros((len(action_columns), len(columns_X)))  # Number of actions x Number of states

# Example: Set the matrix M for A Major Political Actions
M[action_columns.index('A Major Political Actions')][columns_X.index('A Public Trust')] = 0.1  # A Major Political Actions increases A Public Trust
M[action_columns.index('A Major Political Actions')][columns_X.index('A Political Stability')] = 0.05  # A Major Political Actions increases A Political Stability
M[action_columns.index('A Major Political Actions')][columns_X.index('A Trade Balance')] = 0.03  # A Major Political Actions increases A Trade Balance

# Generate the first row of actions and states
for i in range(1, number_rows):
    row_actions = [0] * len(action_columns)  # Initialize the row actions to zero for each action
    row_state = []  # Initialize a list for the state values

    # For each action, calculate its value based on the current state values (from the previous row)
    for j, action in enumerate(action_columns):
        if action == 'A Major Political Actions':  # For the first action: A Major Political Action (e.g., public declaration of support)
            # Extract parameters from the previous row's state data
            a_public_trust = current_values['A Public Trust']
            a_political_stability = current_values['A Political Stability']
            a_bilateral_diplomatic_relations = current_values['Ethnic Similarity']

            # Define the public declaration of support formula
            support_probability = 0.3 + 0.05 * (a_public_trust - 50) + 0.1 * (a_political_stability - 5.5) + 0.2 * a_bilateral_diplomatic_relations

            # Generate a random number between 0 and 1
            random_value = np.random.random()

            # Trigger the action if the random value is less than the support probability
            if random_value < support_probability:
                row_actions[j] = 3  # Action taken (3 indicates action)
            else:
                row_actions[j] = 0  # No action taken

        else:
            row_actions[j] = 0  # Default to 0 if the action isn't defined yet

    # Assign the row actions directly to the DataFrame
    data_actions.loc[i] = row_actions

    # Apply action effects on states using matrix multiplication
    for col in columns_X:
        # Linear growth or change
        change = np.random.uniform(-2, 2)  # Random fluctuation
        new_value = current_values[col] * (1 + change / 100)  # Apply random fluctuation

        # Apply the effects of actions on the states by matrix multiplication
        action_effect = np.dot(row_actions, M[:, columns_X.index(col)])  # Action impact on state
        print(f"Action effect for {col}: {action_effect}")  # Debug statement to check action effects

        # Update the state value considering the action effect
        new_value += action_effect

        current_values[col] = new_value  # Update the current value
        row_state.append(round(new_value, 2))  # Append the updated state value to the row state

    data_X_optimized.append(row_state)  # Append the row state data

# Convert the list of rows into a DataFrame
df_X_optimized = pd.DataFrame(data_X_optimized, columns=columns_X)

# Combine all the data
df_optimized = pd.concat([df_X_optimized, data_actions], axis=1)

# Save the data to a CSV file for further analysis
df_optimized.to_csv('country_inter_gen.csv', index=False)

# Display the first few rows of the dataframe for verification
print("Displaying Optimized Country Actions and Predictions:")
print(df_optimized.head())
