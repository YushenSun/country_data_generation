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

# Initialize the state parameters
initial_values = {
    'A Public Trust': 60.0,  # Initial Public Trust value for A
    'A Political Stability': 6.5,  # Initial Political Stability for A
    'Political Similarity': 0.6,  # Bilateral Political Similarity
    'A Trade Balance': 15,  # Trade balance (example value)
    # Add other state parameters here...
}

# Initialize the action impact matrix M (the coefficients that define the action effects on the states)
M = np.zeros((len(action_columns), len(columns_X)))  # Number of actions x Number of states

# Example: Set the matrix M for A Major Political Actions
M[columns_X.index('A Major Political Actions')][columns_X.index('A Public Trust')] = 0.1  # A Major Political Actions increases A Public Trust
M[columns_X.index('A Major Political Actions')][columns_X.index('A Political Stability')] = 0.05  # A Major Political Actions increases A Political Stability
M[columns_X.index('A Major Political Actions')][columns_X.index('A Trade Balance')] = 0.03  # A Major Political Actions increases A Trade Balance

# Initialize data lists for actions and states
data_actions = []
data_states = []

# Generate the first row of actions and states
first_row_actions = [0] * len(action_columns)  # Start with all actions as zero
first_row_states = list(initial_values.values())  # First row is initialized based on initial values

data_actions.append(first_row_actions)
data_states.append(first_row_states)

# Iterate through rows, starting from the second row, to generate actions and states
for i in range(1, number_rows):
    row_actions = [0] * len(action_columns)  # Start with actions as zero for each row
    row_states = []  # Start with an empty list for the state values

    # Generate actions based on previous row state
    for j, action in enumerate(action_columns):
        if action == 'A Major Political Actions':  # For the first action: A Major Political Action (e.g., public declaration of support)
            # Extract parameters from the previous row's state data
            a_public_trust = data_states[i - 1][columns_X.index('A Public Trust')]
            a_political_stability = data_states[i - 1][columns_X.index('A Political Stability')]
            a_bilateral_diplomatic_relations = data_states[i - 1][columns_X.index('Political Similarity')]

            # Define the public declaration of support formula
            support_probability = 0.3 + 0.05 * (a_public_trust - 50) + 0.1 * (a_political_stability - 5.5) + 0.2 * a_bilateral_diplomatic_relations
            
            # Generate a random number between 0 and 1
            random_value = np.random.random()

            # Trigger the action if the random value is less than the support probability
            if random_value < support_probability:
                row_actions[columns_X.index('A Major Political Actions')] = 3  # Action taken, e.g., +3
            else:
                row_actions[columns_X.index('A Major Political Actions')] = 0  # No action taken

        else:
            row_actions[j] = 0  # Default to 0 if the action isn't defined yet

    # Add action values to the data list
    data_actions.append(row_actions)

    # Update state values based on previous row state and the actions taken
    for col in columns_X:
        # Linear growth or change
        change = np.random.uniform(-2, 2)  # Random fluctuation
        new_value = data_states[i - 1][columns_X.index(col)] * (1 + change / 100)  # Apply random fluctuation
        
        # Apply the effects of actions on the states by matrix multiplication
        action_effect = np.dot(row_actions, M[:, columns_X.index(col)])  # Action impact on state

        # Update the state value considering the action effect
        new_value += action_effect

        row_states.append(round(new_value, 2))

    # Add the updated state values to the state data list
    data_states.append(row_states)

# Create DataFrame for actions
df_actions = pd.DataFrame(data_actions, columns=action_columns)

# Create DataFrame for state data
df_states = pd.DataFrame(data_states, columns=columns_X)

# Save data to CSV
df_actions.to_csv('actions_data.csv', index=False)
df_states.to_csv('states_data.csv', index=False)

# Display the results for verification
print("Displaying actions and states data:")
print(df_actions.head())
print(df_states.head())
