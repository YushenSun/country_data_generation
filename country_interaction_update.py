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
    'A Cultural Influence', 'A Global Trade Index', 'A Innovation Index', 'A Social Welfare Spending', 'A Social Security Reform','A Social Welfare', 'A Tax Rate',
    'A National Security', 'A Financial Stability',

    # B state parameters
    'B GDP', 'B Unemployment Rate', 'B Inflation Rate', 'B Foreign Debt',
    'B Government Spending', 'B Military Spending', 'B Education Spending',
    'B Health Spending', 'B Environment Spending', 'B Technology Investment',
    'B Internet Penetration', 'B Energy Production', 'B Energy Consumption',
    'B Pollution Level', 'B Population', 'B Urbanization Rate', 'B Political Stability',
    'B Human Development Index', 'B Public Trust', 'B Freedom of Press', 'B Corruption Index',
    'B Military Power', 'B Alliances', 'B Environmental Quality', 'B Natural Resources Availability',
    'B Trade Balance', 'B Public Health', 'B Democracy Index', 'B Technology Adoption Rate',
    'B Cultural Influence', 'B Global Trade Index', 'B Innovation Index', 'B Social Welfare Spending', 'B Social Security Reform', 'B Social Welfare', 'B Tax Rate',
    'B National Security', 'B Financial Stability',

    # Relationship Parameters
    'A to B Imports', 'A to B Exports', 'B to A Imports', 'B to A Exports',
    'A Bond Status', 'B Bond Status', 'A Sovereignty Disputes', 'B Sovereignty Disputes',
    'Political Similarity', 'Ethnic Similarity', 'Cultural Compatibility'
]

# Define the action columns for the dataframe (only current actions for A and B)
action_columns = [
    'A Political T', 'A Economic T', 'A Military T', 'A Diplomatic T',
    'A Social T', 'A Environmental T', 'A Technology T', 'A Health T',
    'B Political T', 'B Economic T', 'B Military T', 'B Diplomatic T',
    'B Social T', 'B Environmental T', 'B Technology T', 'B Health T',
    'A Political I', 'A Economic I', 'A Military I', 'A Diplomatic I',
    'A Social I', 'A Environmental I', 'A Technology I', 'A Health I',
    'B Political I', 'B Economic I', 'B Military I', 'B Diplomatic I',
    'B Social I', 'B Environmental I', 'B Technology I', 'B Health I'
]

# Define a function to handle political actions
def political_T(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Political T'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator and target
    initiator_public_trust = f'{initiator} Public Trust'
    initiator_political_stability = f'{initiator} Political Stability'
    initiator_unemployment_rate = f'{initiator} Unemployment Rate'
    initiator_to_target_exports = f'{initiator} to {target} Exports'
    initiator_to_target_imports = f'{initiator} to {target} Imports'
    target_public_trust = f'{target} Public Trust'
    target_political_stability = f'{target} Political Stability'
    
    # Calculate support action (Public Declaration of Support)
    initiator_public_trust_value = current_values[initiator_public_trust]
    initiator_political_stability_value = current_values[initiator_political_stability]
    initiator_unemployment_rate_value = current_values[initiator_unemployment_rate]
    initiator_bilateral_diplomatic_relations_opposition = current_values[initiator_to_target_exports] - current_values[initiator_to_target_imports]
    initiator_bilateral_diplomatic_relations_support = current_values['Ethnic Similarity']
    
    support_probability = 0.3 + 0.05 * (initiator_public_trust_value - 60) + 0.1 * (initiator_political_stability_value - 6.5) + 0.2 * initiator_bilateral_diplomatic_relations_support
    random_value = np.random.random()

    if random_value < support_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 3  # Positive action for support
        # Accumulate the impact on the state parameters
        action_impacts[columns_X.index(initiator_public_trust)] += 0.1
        action_impacts[columns_X.index(initiator_political_stability)] += 0.05
        action_impacts[columns_X.index(f'{initiator} Trade Balance')] += 0.03

    # Calculate opposition action (A Opposes B)
    opposition_probability = 0.3 + 0.05 * (initiator_unemployment_rate_value - 8) - 0.1 * initiator_bilateral_diplomatic_relations_opposition
    random_value = np.random.random()

    if random_value < opposition_probability:
        # Negative action for opposition
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -4
        # Accumulate the impact on the state parameters
        action_impacts[columns_X.index(initiator_public_trust)] -= 0.05
        action_impacts[columns_X.index(initiator_political_stability)] -= 0.02

    return row_actions, action_impacts

def economic_T(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Economic T'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator and target
    initiator_trade_balance = f'{initiator} Trade Balance'
    initiator_unemployment_rate = f'{initiator} Unemployment Rate'
    initiator_to_target_exports = f'{initiator} to {target} Exports'
    initiator_to_target_imports = f'{initiator} to {target} Imports'
    initiator_gdp = f'{initiator} GDP'
    target_unemployment_rate = f'{target} Unemployment Rate'
    political_similarity = 'Political Similarity'

    # Extract relevant state values for economic sanctions and aid
    initiator_trade_balance_value = current_values[initiator_trade_balance]
    initiator_unemployment_rate_value = current_values[initiator_unemployment_rate]
    initiator_bilateral_diplomatic_relations = current_values[initiator_to_target_exports] - current_values[initiator_to_target_imports]
    initiator_gdp_value = current_values[initiator_gdp]
    target_unemployment_rate_value = current_values[target_unemployment_rate]
    initiator_political_similarity = current_values[political_similarity]

    # Trade sanctions condition
    if initiator_trade_balance_value < -0.05 * initiator_gdp_value and initiator_unemployment_rate_value > 8 and initiator_political_similarity < 0.5:
        sanction_probability = 0.3 + 0.05 * (initiator_unemployment_rate_value - 8) - 0.02 * initiator_bilateral_diplomatic_relations
        random_value = np.random.random()

        if random_value < sanction_probability:
            # Find the correct index of the action column dynamically
            action_index = action_columns.index(action_column)
            row_actions[action_index] = -4  # Negative action for trade sanctions
            # Apply the impact on states (e.g., a decrease in public trust, economic stability, etc.)
            action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.1
            action_impacts[columns_X.index(f'{initiator} Political Stability')] -= 0.05
            action_impacts[columns_X.index(initiator_trade_balance)] -= 0.05
            # Apply the impact on states for B
            action_impacts[columns_X.index(f'{target} Public Trust')] -= 0.05
            action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.02
            action_impacts[columns_X.index(f'{target} Trade Balance')] += 0.05

    # Economic aid condition
    aid_probability = 0.2 + 0.05 * (initiator_gdp_value - 10000) - 0.05 * (target_unemployment_rate_value - 5) + 0.1 * initiator_political_similarity
    random_value = np.random.random()

    if random_value < aid_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 5  # Positive action for economic aid
        # Apply the impact on states for initiator (A)
        action_impacts[columns_X.index(f'{initiator} Public Trust')] += 0.05
        action_impacts[columns_X.index(f'{initiator} Political Stability')] += 0.02
        action_impacts[columns_X.index(initiator_trade_balance)] -= 0.05  # Could worsen initiator's trade balance if aid is cash flow out

        # Apply the impact on states for target (B)
        action_impacts[columns_X.index(f'{target} Public Trust')] += 0.1
        action_impacts[columns_X.index(f'{target} Political Stability')] += 0.03
        action_impacts[columns_X.index(f'{target} Trade Balance')] += 0.05

    return row_actions, action_impacts

def military_T(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Military T'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator and target
    initiator_military_power = f'{initiator} Military Power'
    target_political_stability = f'{target} Political Stability'
    political_similarity = 'Political Similarity'
    target_military_power = f'{target} Military Power'
    initiator_military_spending = f'{initiator} Military Spending'
    initiator_political_stability = f'{initiator} Political Stability'

    # Extract relevant state values for military actions
    initiator_military_power_value = current_values[initiator_military_power]
    target_political_stability_value = current_values[target_political_stability]
    political_similarity_value = current_values[political_similarity]
    target_military_power_value = current_values[target_military_power]
    initiator_military_spending_value = current_values[initiator_military_spending]
    initiator_political_stability_value = current_values[initiator_political_stability]

    # Military display (probability of displaying military power)
    military_display_probability = 0.3 + 0.05 * (initiator_military_power_value - 700) - 0.1 * (target_political_stability_value - 7) + 0.2 * (1 - political_similarity_value)
    random_value = np.random.random()

    if random_value < military_display_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -5  # Action taken (negative value indicates displaying military power)
        
        # Apply the impact on states for A
        action_impacts[columns_X.index(initiator_military_power)] += 0.05  # Increase A's military power
        action_impacts[columns_X.index(f'{initiator} Government Spending')] += 0.05  # Increase A's government spending due to military display

        # Apply the impact on states for B
        action_impacts[columns_X.index(target_political_stability)] -= 0.05  # Decrease B's political stability due to military show of force

    # Military exercise (probability of conducting a military exercise near B)
    military_exercise_probability = 0.3 + 0.1 * (initiator_military_power_value - 800) - 0.2 * (target_military_power_value - 1000) + 0.3 * political_similarity_value
    random_value = np.random.random()

    if random_value < military_exercise_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -4  # Action taken for military exercise near B (negative value indicates exercise)

        # Apply the impact on states for A
        action_impacts[columns_X.index(initiator_military_power)] += 0.05  # Increase A's military trust
        action_impacts[columns_X.index(target_political_stability)] -= 0.1  # Decrease B's political stability
        action_impacts[columns_X.index(target_military_power)] -= 0.1  # Decrease B's military power due to military exercise

    # Military conflict (probability of engaging in a military conflict with B)
    military_conflict_probability = 0.2 + 0.1 * (initiator_military_power_value - 1000) - 0.2 * (political_similarity_value) + 0.1 * (initiator_military_spending_value - 200)
    random_value = np.random.random()

    if random_value < military_conflict_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -6  # Action taken for military conflict (negative value indicates conflict)

        # Apply the impact on states for A
        action_impacts[columns_X.index(initiator_military_power)] += 0.1  # Increase A's military power due to conflict preparation
        action_impacts[columns_X.index(initiator_political_stability)] -= 0.1  # Decrease A's political stability due to the conflict

        # Apply the impact on states for B
        action_impacts[columns_X.index(target_political_stability)] -= 0.2  # Decrease B's political stability as a result of conflict
        action_impacts[columns_X.index(target_military_power)] -= 0.15  # Decrease B's military power due to conflict engagement

    return row_actions, action_impacts

def diplomatic_T(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Diplomatic T'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_political_stability = f'{initiator} Political Stability'
    target_political_stability = f'{target} Political Stability'
    initiator_military_power = f'{initiator} Military Power'
    target_military_power = f'{target} Military Power'
    political_similarity = 'Political Similarity'

    # Extract relevant state values
    initiator_political_stability_value = current_values[initiator_political_stability]
    target_political_stability_value = current_values[target_political_stability]
    initiator_military_power_value = current_values[initiator_military_power]
    target_military_power_value = current_values[target_military_power]
    political_similarity_value = current_values[political_similarity]

    # Calculate the probability of signing a peace agreement
    peace_probability = 0.4 + 0.1 * (initiator_political_stability_value - 6) - 0.05 * (initiator_military_power_value - target_military_power_value) + 0.2 * political_similarity_value
    random_value = np.random.random()

    if random_value < peace_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 6  # Positive action for peace agreement
        
        # Apply the impact on states for A (Positive impact due to peace agreement)
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1  # Increased political stability
        action_impacts[columns_X.index(f'{initiator} Trade Balance')] += 0.05  # Trade balance might improve
        action_impacts[columns_X.index(f'{initiator} Military Spending')] -= 0.05  # Military spending might decrease as a result of peace

        # Apply the impact on states for B (Positive impact due to peace agreement)
        action_impacts[columns_X.index(target_political_stability)] += 0.1  # Increased political stability for B
        action_impacts[columns_X.index(f'{target} Trade Balance')] += 0.05  # Trade balance might improve for B
        action_impacts[columns_X.index(f'{target} Military Spending')] -= 0.05  # B's military spending might decrease as a result of peace

    # Calculate the probability of participating in international sanctions
    a_unemployment_rate = current_values[f'{initiator} Unemployment Rate']
    a_bilateral_diplomatic_relations = current_values[political_similarity]  # This represents the diplomatic relation between A and B
    a_trade_balance = current_values[f'{initiator} to {target} Exports'] - current_values[f'{initiator} to {target} Imports']  # Economic cooperation index

    sanction_probability = 0.3 + 0.05 * (a_unemployment_rate - 8) - 0.1 * a_trade_balance - 0.2 * (1 - a_bilateral_diplomatic_relations)
    random_value = np.random.random()

    if random_value < sanction_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -6  # Negative action indicating participation in sanctions

        # Apply the impact on states for A (International sanctions)
        action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.1  # Public trust in A could decrease due to sanctions
        action_impacts[columns_X.index(f'{initiator} Political Stability')] -= 0.05  # Political stability in A might decrease due to sanctions
        action_impacts[columns_X.index(f'{initiator} Trade Balance')] -= 0.05  # Trade balance could worsen as a result of sanctions

        # Apply the impact on states for B (Sanctions impact)
        action_impacts[columns_X.index(f'{target} Public Trust')] -= 0.15  # Public trust in B might decrease due to sanctions
        action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.1  # B's political stability could decrease
        action_impacts[columns_X.index(f'{target} Military Power')] -= 0.1  # B's military power could decrease as a result of sanctions

    return row_actions, action_impacts

def social_T(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Social T'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_social_welfare_spending = f'{initiator} Social Welfare Spending'
    initiator_social_security_reform = f'{initiator} Social Security Reform'
    target_social_welfare = f'{target} Social Welfare'
    political_similarity = 'Political Similarity'

    # Extract relevant state values
    initiator_social_welfare_spending_value = current_values[initiator_social_welfare_spending]
    initiator_social_security_reform_value = current_values[initiator_social_security_reform]
    target_social_welfare_value = current_values[target_social_welfare]
    political_similarity_value = current_values[political_similarity]

    # Calculate the probability of implementing social welfare reform
    social_policy_probability = 0.3 + 0.05 * (initiator_social_welfare_spending_value - 100) + 0.1 * (initiator_social_security_reform_value - 50) + 0.2 * political_similarity_value - 0.1 * target_social_welfare_value
    random_value = np.random.random()

    if random_value < social_policy_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 3  # Positive action for Social T
        
        # Apply the impact on states for A (Social policy)
        action_impacts[columns_X.index(initiator_social_welfare_spending)] += 0.1  # A's social welfare spending increases
        action_impacts[columns_X.index(initiator_social_security_reform)] += 0.05  # A's social security reform improves
        action_impacts[columns_X.index(f'{initiator} Public Trust')] += 0.05  # A's public trust might increase due to the welfare reform

        # Apply the impact on states for B (Benefiting from A's social reform)
        action_impacts[columns_X.index(target_social_welfare)] += 0.1  # B's social welfare improves from cooperation
        action_impacts[columns_X.index(f'{target} Political Stability')] += 0.03  # B's political stability improves as a result of the welfare cooperation

    # Calculate the probability of not implementing the welfare reform (negation)
    social_reform_negation_probability = 0.2 + 0.05 * (initiator_social_welfare_spending_value - 100) - 0.1 * target_social_welfare_value
    random_value = np.random.random()

    if random_value < social_reform_negation_probability:
        # Negative action for failing to reform or withdrawing support
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -3  # Negative action for withdrawing support
        
        # Apply the impact on states for A (Negative impact)
        action_impacts[columns_X.index(initiator_social_welfare_spending)] -= 0.1  # A's social welfare spending decreases
        action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.05  # A's public trust might decrease due to the failure

        # Apply the impact on states for B (Negative impact)
        action_impacts[columns_X.index(target_social_welfare)] -= 0.1  # B's social welfare decreases due to the lack of cooperation
        action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.05  # B's political stability decreases due to the broken cooperation

    # Calculate the probability of reducing social welfare support (if unemployment rate is high)
    a_unemployment_rate = current_values[f'{initiator} Unemployment Rate']

    if a_unemployment_rate > 8 and political_similarity_value < 0.5:
        # Calculate the probability of reducing social welfare support
        welfare_reduction_probability = 0.4 + 0.05 * (a_unemployment_rate - 8) - 0.2 * political_similarity_value
        random_value = np.random.random()

        if random_value < welfare_reduction_probability:
            action_index = action_columns.index(action_column)
            row_actions[action_index] = -3  # Negative action for reducing social welfare (e.g., -3 indicates reduction)
            
            # Apply the impact on states for A (Social Welfare Reduction)
            action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.1  # A's public trust could decrease due to social welfare cuts
            action_impacts[columns_X.index(f'{initiator} Political Stability')] -= 0.05  # A's political stability might decrease due to dissatisfaction
            action_impacts[columns_X.index(f'{initiator} Trade Balance')] -= 0.03  # A's trade balance might worsen due to reduced cooperation with B
            
            # Apply the impact on states for B (Reduction in cooperation)
            action_impacts[columns_X.index(f'{target} Public Trust')] -= 0.1  # B's public trust decreases due to the reduction in social welfare
            action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.05  # B's political stability might decrease due to reduced cooperation
            action_impacts[columns_X.index(f'{target} Trade Balance')] -= 0.05  # B's trade balance might worsen due to A's reduced support

    return row_actions, action_impacts

def environmental_T(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Environmental T'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_environment_spending = f'{initiator} Environment Spending'
    target_environment_spending = f'{target} Environment Spending'
    political_similarity = 'Political Similarity'

    # Extract relevant state values
    initiator_environment_spending_value = current_values[initiator_environment_spending]
    target_environment_spending_value = current_values[target_environment_spending]
    political_similarity_value = current_values[political_similarity]

    # Calculate the probability of A taking environmental policy action with B
    policy_probability = 0.3 + 0.05 * (initiator_environment_spending_value - 30) + 0.1 * (target_environment_spending_value - 40) + 0.15 * (political_similarity_value - 0.5)
    random_value = np.random.random()

    if random_value < policy_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 4  # Positive action for environmental policy cooperation

        # Apply the impact on states for A (Environmental policy)
        action_impacts[columns_X.index(f'{initiator} Environment Spending')] += 0.05  # Increase A's environmental spending
        action_impacts[columns_X.index(f'{initiator} Environmental Quality')] += 0.1  # Improve A's environmental quality

        # Apply the impact on states for B (Environmental cooperation)
        action_impacts[columns_X.index(f'{target} Environment Spending')] += 0.05  # Increase B's environmental spending
        action_impacts[columns_X.index(f'{target} Environmental Quality')] += 0.1  # Improve B's environmental quality

    # Extract parameters for energy consumption and collaboration action calculation
    initiator_energy_consumption = f'{initiator} Energy Consumption'
    target_energy_production = f'{target} Energy Production'

    # Calculate the probability of A increasing energy consumption and collaborating with B
    energy_cooperation_probability = 0.3 + 0.05 * (current_values[initiator_energy_consumption] - 850) + 0.1 * (current_values[target_energy_production] - 1000) + 0.2 * (political_similarity_value - 0.5)
    random_value = np.random.random()

    if random_value < energy_cooperation_probability:
        # Positive action for increasing energy consumption and collaborating with B
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2

        # Apply the impact on states for A (Energy consumption)
        action_impacts[columns_X.index(f'{initiator} Energy Consumption')] += 0.05  # Increase A's energy consumption
        action_impacts[columns_X.index(f'{initiator} Energy Production')] += 0.02  # A might increase its energy production to support the consumption increase

        # Apply the impact on states for B (Energy cooperation)
        action_impacts[columns_X.index(f'{target} Energy Consumption')] += 0.03  # B's energy consumption might rise due to cooperation
        action_impacts[columns_X.index(f'{target} Energy Production')] += 0.05  # B may increase energy production as part of cooperation

    # Extract parameters for the environmental restriction action calculation
    initiator_to_target_exports = f'{initiator} to {target} Exports'

    # Calculate the probability of A implementing environmental measures and restricting energy exports to B
    environmental_restriction_probability = 0.3 + 0.05 * (current_values[initiator_energy_consumption] - 850) - 0.1 * (current_values[initiator_to_target_exports] - 150) + 0.2 * (current_values[initiator_environment_spending] - 30)
    random_value = np.random.random()

    if random_value < environmental_restriction_probability:
        # Negative action for restricting energy exports to B
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -4  # Indicating restriction

        # Apply the impact on states for A (Energy policy)
        action_impacts[columns_X.index(f'{initiator} Energy Consumption')] -= 0.05  # A may reduce energy consumption as part of the restriction
        action_impacts[columns_X.index(f'{initiator} Environmental Quality')] += 0.1  # A's environmental quality could improve with the policy

        # Apply the impact on states for B (Energy exports restriction)
        action_impacts[columns_X.index(f'{target} Energy Consumption')] -= 0.05  # B's energy consumption might decrease due to the restriction
        action_impacts[columns_X.index(f'{target} Trade Balance')] -= 0.03  # B's trade balance could worsen due to restricted energy imports

    return row_actions, action_impacts

def technology_T(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Technology T'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_technology_investment = f'{initiator} Technology Investment'
    initiator_innovation_index = f'{initiator} Innovation Index'
    target_technology_investment = f'{target} Technology Investment'

    # Extract relevant state values
    initiator_technology_investment_value = current_values[initiator_technology_investment]
    initiator_innovation_index_value = current_values[initiator_innovation_index]
    political_similarity_value = current_values['Political Similarity']
    target_technology_investment_value = current_values[target_technology_investment]

    # Calculate the probability of sharing technology with B
    tech_sharing_probability = 0.3 + 0.05 * (initiator_technology_investment_value - 250) + 0.1 * (initiator_innovation_index_value - 50) + 0.2 * political_similarity_value
    random_value = np.random.random()

    if random_value < tech_sharing_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 4  # Positive action for technology sharing
        # Apply the impact on states for A (Technology Sharing)
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.05  # Technology investment might increase due to shared knowledge
        action_impacts[columns_X.index(initiator_innovation_index)] += 0.05  # Innovation index might rise as a result of sharing

        # Apply the impact on states for B (Technology Sharing)
        action_impacts[columns_X.index(f'{target} Technology Adoption Rate')] += 0.05  # B's technology adoption might increase
        action_impacts[columns_X.index(f'{target} Technology Investment')] += 0.03  # B's technology investment might rise due to shared knowledge

    # Calculate the probability of A competing with B in the technology field
    tech_competition_probability = 0.4 + 0.05 * (initiator_technology_investment_value - 250) + 0.1 * (initiator_innovation_index_value - 50) - 0.15 * (target_technology_investment_value - 280)
    random_value = np.random.random()

    if random_value < tech_competition_probability:
        # Negative action indicating competition (e.g., -4 represents A's active competition with B in technology)
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -4
        # Apply the impact on states for A (Competition)
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.05  # A's technology investment might increase as a result of competition
        action_impacts[columns_X.index(initiator_innovation_index)] += 0.05  # Innovation index might rise as a result of competition
        action_impacts[columns_X.index(f'{initiator} Military Spending')] += 0.03  # Competition may drive more military spending as a countermeasure

        # Apply the impact on states for B (Competition)
        action_impacts[columns_X.index(f'{target} Technology Investment')] -= 0.05  # B's technology investment might decline due to increased competition
        action_impacts[columns_X.index(f'{target} Innovation Index')] -= 0.05  # B's innovation index might be impacted

    # Calculate the probability of A restricting technology exports to B
    tech_export_restriction_probability = 0.3 + 0.1 * (initiator_technology_investment_value - 300) - 0.1 * (target_technology_investment_value - 280) - 0.2 * (current_values[f'{initiator} Political Stability'] - 6.5)
    random_value = np.random.random()

    if random_value < tech_export_restriction_probability:
        # Negative action for restricting exports
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -5
        # Apply the impact on states for A (Restricting exports)
        action_impacts[columns_X.index(initiator_technology_investment)] -= 0.1  # A's technology investment might be impacted by restrictions
        action_impacts[columns_X.index(f'{initiator} Government Spending')] += 0.05  # Possible increase in government spending to maintain control

        # Apply the impact on states for B (Restrictions)
        action_impacts[columns_X.index(f'{target} Technology Investment')] -= 0.1  # B's technology investment might decrease due to lack of access to A's technology
        action_impacts[columns_X.index(f'{target} Innovation Index')] -= 0.05  # B's innovation index could be impacted by technology restrictions

    return row_actions, action_impacts

def health_T(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Health T'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_public_health = f'{initiator} Public Health'
    target_public_health = f'{target} Public Health'
    political_similarity = 'Political Similarity'

    # Extract relevant state values
    initiator_public_health_value = current_values[initiator_public_health]
    target_public_health_value = current_values[target_public_health]
    political_similarity_value = current_values[political_similarity]

    # Calculate the probability of providing public health support to B
    health_support_probability = 0.3 + 0.1 * (initiator_public_health_value - 70) - 0.1 * (target_public_health_value - 60) + 0.2 * political_similarity_value
    random_value = np.random.random()

    if random_value < health_support_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 3  # Positive action for support
        
        # Accumulate the impact on the state parameters
        action_impacts[columns_X.index(f'{initiator} Public Trust')] += 0.05
        action_impacts[columns_X.index(f'{initiator} Political Stability')] += 0.03
        action_impacts[columns_X.index(f'{target} Public Health')] += 0.1
        action_impacts[columns_X.index(f'{target} Political Stability')] += 0.02

    # Calculate the probability of restricting medical supplies to B
    supply_restriction_probability = 0.3 + 0.05 * (initiator_public_health_value - 70) - 0.1 * (target_public_health_value - 60) - 0.2 * political_similarity_value
    random_value = np.random.random()

    if random_value < supply_restriction_probability:
        # Negative action for restricting medical supplies
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -3
        
        # Accumulate the impact on the state parameters
        action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.05
        action_impacts[columns_X.index(f'{initiator} Political Stability')] -= 0.02
        action_impacts[columns_X.index(f'{target} Public Health')] -= 0.1
        action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.03

    return row_actions, action_impacts

def political_I(initiator, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Political I'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator
    initiator_public_trust = f'{initiator} Public Trust'
    initiator_political_stability = f'{initiator} Political Stability'
    initiator_unemployment_rate = f'{initiator} Unemployment Rate'

    # Extract relevant state values for action calculation
    initiator_public_trust_value = current_values[initiator_public_trust]
    initiator_political_stability_value = current_values[initiator_political_stability]
    initiator_unemployment_rate_value = current_values[initiator_unemployment_rate]

    # Formula for the probability of the political action outcome
    # 1. 总统大选
    election_probability = 0.4 + 0.1 * (initiator_public_trust_value - 60) - 0.05 * (initiator_unemployment_rate_value - 8)
    
    # 2. 政治改革
    reform_probability = 0.3 + 0.1 * (initiator_political_stability_value - 6) - 0.1 * (initiator_unemployment_rate_value - 8)
    
    # 3. 宪法修改
    constitution_amendment_probability = 0.5 + 0.15 * (initiator_political_stability_value - 6) - 0.1 * (initiator_unemployment_rate_value - 8)

    # 4. 领导人变动
    leadership_change_probability = 0.3 + 0.05 * (initiator_public_trust_value - 60) - 0.1 * (initiator_unemployment_rate_value - 8)

    # Simulate random outcome for the actions
    random_value = np.random.random()
    if random_value < election_probability:
        row_actions[action_columns.index(action_column)] = 1  # Positive action for democracy (positive change)
        action_impacts[columns_X.index(initiator_public_trust)] += 0.1  # Increase public trust due to democratic action
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1  # Increase stability due to positive election outcome

    elif random_value < reform_probability:
        row_actions[action_columns.index(action_column)] = -1  # Negative action for authoritarianism (negative change)
        action_impacts[columns_X.index(initiator_public_trust)] -= 0.1  # Decrease public trust due to authoritarianism
        action_impacts[columns_X.index(initiator_political_stability)] -= 0.1  # Decrease stability due to negative reform

    elif random_value < constitution_amendment_probability:
        row_actions[action_columns.index(action_column)] = 2  # Positive action for constitutional amendment
        action_impacts[columns_X.index(initiator_public_trust)] += 0.15  # Increase public trust
        action_impacts[columns_X.index(initiator_political_stability)] += 0.2  # Increase stability due to law and human rights protection

    elif random_value < leadership_change_probability:
        row_actions[action_columns.index(action_column)] = 1  # Positive action for leadership change (stability improvement)
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1  # Increase stability due to leadership change

    return row_actions, action_impacts

def economic_I(initiator, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Economic I'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator
    initiator_gdp = f'{initiator} GDP'
    initiator_unemployment_rate = f'{initiator} Unemployment Rate'
    initiator_inflation_rate = f'{initiator} Inflation Rate'
    initiator_government_spending = f'{initiator} Government Spending'
    initiator_tax_rate = f'{initiator} Tax Rate'
    initiator_trade_balance = f'{initiator} Trade Balance'

    # Extract relevant state values for economic actions
    initiator_gdp_value = current_values[initiator_gdp]
    initiator_unemployment_rate_value = current_values[initiator_unemployment_rate]
    initiator_inflation_rate_value = current_values[initiator_inflation_rate]
    initiator_government_spending_value = current_values[initiator_government_spending]
    initiator_tax_rate_value = current_values[initiator_tax_rate]
    initiator_trade_balance_value = current_values[initiator_trade_balance]

    # Economic stimulus policy (probability of implementing stimulus policy)
    stimulus_probability = 0.3 + 0.05 * (initiator_gdp_value - 10000) - 0.1 * initiator_unemployment_rate_value + 0.2 * initiator_inflation_rate_value
    random_value = np.random.random()

    if random_value < stimulus_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for economic stimulus
        # Apply the impact on states for A (Stimulus impact)
        action_impacts[columns_X.index(initiator_government_spending)] += 0.1  # Increased government spending
        action_impacts[columns_X.index(initiator_gdp)] += 0.2  # Stimulate economic growth
        action_impacts[columns_X.index(initiator_trade_balance)] -= 0.05  # Potentially worsen trade balance due to increased imports

    # Tax reform (probability of implementing tax reform)
    tax_reform_probability = 0.4 + 0.1 * (initiator_tax_rate_value - 25) - 0.1 * initiator_inflation_rate_value
    random_value = np.random.random()

    if random_value < tax_reform_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 1  # Positive action for tax reform
        # Apply the impact on states for A (Tax reform impact)
        action_impacts[columns_X.index(initiator_tax_rate)] -= 0.05  # Reduced tax rate
        action_impacts[columns_X.index(initiator_gdp)] += 0.15  # Boost economic growth due to higher consumption
        action_impacts[columns_X.index(initiator_unemployment_rate)] -= 0.05  # Decrease in unemployment due to boosted consumption

    # Fiscal austerity policy (probability of implementing fiscal austerity)
    austerity_probability = 0.3 + 0.05 * (initiator_gdp_value - 10000) - 0.2 * (initiator_government_spending_value - 2000)
    random_value = np.random.random()

    if random_value < austerity_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for fiscal austerity
        # Apply the impact on states for A (Austerity impact)
        action_impacts[columns_X.index(initiator_government_spending)] -= 0.1  # Reduced government spending
        action_impacts[columns_X.index(initiator_gdp)] -= 0.1  # Economic slowdown due to cuts in government spending
        action_impacts[columns_X.index(initiator_inflation_rate)] -= 0.05  # Inflation might decrease as a result of austerity

    # Economic sanctions (probability of implementing economic sanctions)
    sanctions_probability = 0.4 + 0.1 * (initiator_trade_balance_value - 100) - 0.1 * initiator_unemployment_rate_value
    random_value = np.random.random()

    if random_value < sanctions_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 1  # Positive action for economic sanctions (improve negotiation position)
        # Apply the impact on states for A (Sanctions impact)
        action_impacts[columns_X.index(initiator_trade_balance)] += 0.1  # Improved trade balance due to sanctions
        action_impacts[columns_X.index(initiator_gdp)] += 0.05  # Economic boost due to improved negotiations
        action_impacts[columns_X.index(initiator_inflation_rate)] += 0.03  # Inflation might increase due to retaliatory actions

    return row_actions, action_impacts

def military_I(initiator, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Military I'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator
    initiator_military_power = f'{initiator} Military Power'
    initiator_military_spending = f'{initiator} Military Spending'
    initiator_gdp = f'{initiator} GDP'
    initiator_inflation_rate = f'{initiator} Inflation Rate'
    initiator_trade_balance = f'{initiator} Trade Balance'
    initiator_population = f'{initiator} Population'

    # Extract relevant state values for military actions
    initiator_military_power_value = current_values[initiator_military_power]
    initiator_military_spending_value = current_values[initiator_military_spending]
    initiator_gdp_value = current_values[initiator_gdp]
    initiator_inflation_rate_value = current_values[initiator_inflation_rate]
    initiator_trade_balance_value = current_values[initiator_trade_balance]
    initiator_population_value = current_values[initiator_population]

    # Military expansion (probability of expanding military forces)
    expansion_probability = 0.3 + 0.1 * (initiator_military_power_value - 1000) + 0.1 * (initiator_gdp_value - 15000) - 0.1 * initiator_inflation_rate_value
    random_value = np.random.random()

    if random_value < expansion_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for military expansion
        # Apply the impact on states for A (Military Expansion impact)
        action_impacts[columns_X.index(initiator_military_spending)] += 0.1  # Increased military spending
        action_impacts[columns_X.index(initiator_military_power)] += 0.2  # Increase military power
        action_impacts[columns_X.index(initiator_trade_balance)] -= 0.05  # Trade balance may worsen due to increased military imports

    # Military reduction (probability of reducing military forces)
    reduction_probability = 0.4 - 0.05 * (initiator_military_spending_value - 500) - 0.1 * (initiator_military_power_value - 1000)
    random_value = np.random.random()

    if random_value < reduction_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 1  # Positive action for military reduction
        # Apply the impact on states for A (Military Reduction impact)
        action_impacts[columns_X.index(initiator_military_spending)] -= 0.1  # Decrease military spending
        action_impacts[columns_X.index(initiator_military_power)] -= 0.2  # Reduce military power
        action_impacts[columns_X.index(initiator_trade_balance)] += 0.05  # Trade balance may improve due to reduced military imports

    # Military reform (probability of implementing military reform)
    reform_probability = 0.3 + 0.05 * (initiator_military_spending_value - 500) + 0.2 * (initiator_gdp_value - 15000) - 0.1 * initiator_population_value
    random_value = np.random.random()

    if random_value < reform_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 3  # Positive action for military reform
        # Apply the impact on states for A (Military Reform impact)
        action_impacts[columns_X.index(initiator_military_spending)] += 0.1  # Increased military spending for reform
        action_impacts[columns_X.index(initiator_military_power)] += 0.1  # Improvement in military power due to reform
        action_impacts[columns_X.index(initiator_gdp)] += 0.05  # Potential increase in GDP due to military industry reform

    # New weapons development (probability of developing new weapons)
    weapons_development_probability = 0.3 + 0.1 * (initiator_military_spending_value - 500) - 0.1 * (initiator_inflation_rate_value - 3) + 0.15 * (initiator_population_value - 1000000)
    random_value = np.random.random()

    if random_value < weapons_development_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 4  # Positive action for new weapons development
        # Apply the impact on states for A (Weapons Development impact)
        action_impacts[columns_X.index(initiator_military_spending)] += 0.2  # Increased spending on weapons development
        action_impacts[columns_X.index(initiator_military_power)] += 0.3  # Military power increases due to new weapons
        action_impacts[columns_X.index(initiator_trade_balance)] -= 0.05  # Possible trade balance deterioration due to import of raw materials

    # Third-party military interactions (probability of engaging with third parties)
    third_party_interaction_probability = 0.2 + 0.1 * (initiator_military_power_value - 1000) - 0.05 * (initiator_trade_balance_value - 50) + 0.1 * (initiator_inflation_rate_value - 3)
    random_value = np.random.random()

    if random_value < third_party_interaction_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 5  # Positive action for military interaction with third party
        # Apply the impact on states for A (Third-party interaction impact)
        action_impacts[columns_X.index(initiator_military_spending)] += 0.1  # Increased spending on foreign military cooperation
        action_impacts[columns_X.index(initiator_military_power)] += 0.2  # Military power increases due to collaboration
        action_impacts[columns_X.index(initiator_trade_balance)] -= 0.05  # Trade balance may be affected due to foreign trade links

    return row_actions, action_impacts

def diplomatic_I(initiator, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Diplomatic I'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for the initiator
    initiator_public_trust = f'{initiator} Public Trust'
    initiator_political_stability = f'{initiator} Political Stability'
    initiator_military_power = f'{initiator} Military Power'

    # 1. 外交政策调整 (Diplomatic Policy Adjustment)
    diplomatic_policy_adjustment_probability = 0.3 + 0.1 * (current_values[initiator_public_trust] - 60) + 0.1 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()
    
    if random_value < diplomatic_policy_adjustment_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for diplomatic policy adjustment
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_public_trust)] += 0.1
        action_impacts[columns_X.index(initiator_political_stability)] += 0.05

    # 2. 国际条约签署 (International Treaty Signing)
    international_treaty_signing_probability = 0.4 + 0.05 * (current_values[initiator_public_trust] - 60)
    random_value = np.random.random()
    
    if random_value < international_treaty_signing_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 3  # Positive action for signing international treaties
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1
        action_impacts[columns_X.index(initiator_military_power)] += 0.05

    # 3. 加入国际军事联盟 (Join International Military Alliance)
    international_military_alliance_probability = 0.3 + 0.1 * (current_values[initiator_public_trust] - 60) - 0.1 * (current_values[initiator_military_power] - 700)
    random_value = np.random.random()
    
    if random_value < international_military_alliance_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for joining military alliance
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_military_power)] += 0.1
        action_impacts[columns_X.index(initiator_political_stability)] += 0.05

    # 4. 维护国家主权 (Maintain National Sovereignty)
    national_sovereignty_probability = 0.4 + 0.05 * (current_values[initiator_public_trust] - 60) - 0.05 * (current_values[initiator_military_power] - 700)
    random_value = np.random.random()

    if random_value < national_sovereignty_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for maintaining national sovereignty
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_political_stability)] += 0.05
        action_impacts[columns_X.index(initiator_military_power)] += 0.1

    # 5. 结束外交关系 (End Diplomatic Relations)
    end_diplomatic_relations_probability = 0.3 - 0.05 * (current_values[initiator_public_trust] - 60) - 0.1 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()
    
    if random_value < end_diplomatic_relations_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -2  # Negative action for ending diplomatic relations
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_public_trust)] -= 0.1
        action_impacts[columns_X.index(initiator_political_stability)] -= 0.05

    return row_actions, action_impacts

def social_I(initiator, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Social I'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for the initiator
    initiator_public_trust = f'{initiator} Public Trust'
    initiator_political_stability = f'{initiator} Political Stability'
    initiator_unemployment_rate = f'{initiator} Unemployment Rate'

    # 1. 实施社会福利增加 (Increase Social Welfare)
    increase_social_welfare_probability = 0.4 + 0.1 * (current_values[initiator_public_trust] - 60) + 0.05 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()

    if random_value < increase_social_welfare_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for increasing social welfare
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_public_trust)] += 0.1
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1

    # 2. 社会福利改革 (Social Welfare Reform)
    social_welfare_reform_probability = 0.4 + 0.05 * (current_values[initiator_public_trust] - 60) - 0.05 * (current_values[initiator_unemployment_rate] - 5)
    random_value = np.random.random()

    if random_value < social_welfare_reform_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for social welfare reform
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_public_trust)] += 0.1
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1

    # 3. 养老保障/医疗改革 (Pension/Healthcare Reform)
    pension_healthcare_reform_probability = 0.5 + 0.1 * (current_values[initiator_public_trust] - 60) - 0.1 * (current_values[initiator_unemployment_rate] - 5)
    random_value = np.random.random()

    if random_value < pension_healthcare_reform_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for pension/healthcare reform
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_public_trust)] += 0.2
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1

    # 4. 教育水平改革 (Education Reform)
    education_reform_probability = 0.3 + 0.05 * (current_values[initiator_public_trust] - 60) - 0.05 * (current_values[initiator_unemployment_rate] - 5)
    random_value = np.random.random()

    if random_value < education_reform_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for education reform
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_public_trust)] += 0.1
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1

    # 5. 劳动市场改革 (Labor Market Reform)
    labor_market_reform_probability = 0.3 + 0.05 * (current_values[initiator_public_trust] - 60) - 0.05 * (current_values[initiator_unemployment_rate] - 5)
    random_value = np.random.random()

    if random_value < labor_market_reform_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for labor market reform
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_public_trust)] += 0.1
        action_impacts[columns_X.index(initiator_political_stability)] += 0.05

    return row_actions, action_impacts

def environmental_I(initiator, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Environmental I'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for the initiator
    initiator_environment_spending = f'{initiator} Environment Spending'
    initiator_political_stability = f'{initiator} Political Stability'

    # 1. 环境保护政策 (Environmental Protection Policy)
    environmental_protection_policy_probability = 0.5 + 0.1 * (current_values[initiator_environment_spending] - 30) + 0.2 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()

    if random_value < environmental_protection_policy_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for environmental protection
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_environment_spending)] += 0.2
        action_impacts[columns_X.index(f'{initiator} Environmental Quality')] += 0.2

    # 2. 实施能源独立政策 (Energy Independence Policy)
    energy_independence_policy_probability = 0.4 + 0.1 * (current_values[initiator_environment_spending] - 30) + 0.05 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()

    if random_value < energy_independence_policy_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for energy independence
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_environment_spending)] += 0.1
        action_impacts[columns_X.index(f'{initiator} Energy Production')] += 0.1

    # 3. 推行可再生能源计划 (Renewable Energy Plan)
    renewable_energy_plan_probability = 0.5 + 0.2 * (current_values[initiator_environment_spending] - 30) + 0.1 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()

    if random_value < renewable_energy_plan_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for renewable energy
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_environment_spending)] += 0.2
        action_impacts[columns_X.index(f'{initiator} Energy Production')] += 0.15

    # 4. 实施碳税政策 (Carbon Tax Policy)
    carbon_tax_policy_probability = 0.5 + 0.15 * (current_values[initiator_environment_spending] - 30) - 0.1 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()

    if random_value < carbon_tax_policy_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for carbon tax
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_environment_spending)] += 0.2
        action_impacts[columns_X.index(f'{initiator} Energy Consumption')] -= 0.1

    # 5. 启动生态修复项目 (Ecological Restoration Project)
    ecological_restoration_probability = 0.5 + 0.1 * (current_values[initiator_environment_spending] - 30) + 0.1 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()

    if random_value < ecological_restoration_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for ecological restoration
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_environment_spending)] += 0.2
        action_impacts[columns_X.index(f'{initiator} Environmental Quality')] += 0.3

    return row_actions, action_impacts

def technology_I(initiator, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Technology I'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for the initiator
    initiator_technology_investment = f'{initiator} Technology Investment'
    initiator_innovation_index = f'{initiator} Innovation Index'
    initiator_political_stability = f'{initiator} Political Stability'
    initiator_financial_stability = f'{initiator} Financial Stability'
    initiator_industrial_competitiveness = f'{initiator} Industrial Competitiveness'
    initiator_national_security = f'{initiator} National Security'

    # 1. 科技政策改革 (Technology Policy Reform)
    technology_policy_reform_probability = 0.5 + 0.1 * (current_values[initiator_technology_investment] - 250) + 0.1 * (current_values[initiator_innovation_index] - 50)
    random_value = np.random.random()

    if random_value < technology_policy_reform_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for technology policy reform
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.2
        action_impacts[columns_X.index(initiator_innovation_index)] += 0.2

    # 2. 推动数字货币政策 (Digital Currency Policy)
    digital_currency_policy_probability = 0.4 + 0.1 * (current_values[initiator_technology_investment] - 250) + 0.1 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()

    if random_value < digital_currency_policy_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 1  # Positive action for digital currency policy
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.1
        action_impacts[columns_X.index(initiator_financial_stability)] += 0.1

    # 3. 推动人工智能发展计划 (Artificial Intelligence Development Plan)
    ai_development_plan_probability = 0.5 + 0.1 * (current_values[initiator_innovation_index] - 50) + 0.1 * (current_values[initiator_technology_investment] - 250)
    random_value = np.random.random()

    if random_value < ai_development_plan_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for AI development
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.2
        action_impacts[columns_X.index(initiator_innovation_index)] += 0.2

    # 4. 网络安全政策加强 (Cybersecurity Policy Enhancement)
    cybersecurity_policy_enhancement_probability = 0.4 + 0.1 * (current_values[initiator_technology_investment] - 250) + 0.05 * (current_values[initiator_political_stability] - 6)
    random_value = np.random.random()

    if random_value < cybersecurity_policy_enhancement_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 1  # Positive action for cybersecurity policy
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.1
        action_impacts[columns_X.index(initiator_national_security)] += 0.1

    # 5. 创新型技术研发投资 (Innovative Technology R&D Investment)
    technology_rnd_investment_probability = 0.5 + 0.15 * (current_values[initiator_technology_investment] - 250) + 0.1 * (current_values[initiator_innovation_index] - 50)
    random_value = np.random.random()

    if random_value < technology_rnd_investment_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for R&D investment
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.2
        #action_impacts[columns_X.index(initiator_industrial_competitiveness)] += 0.15

    return row_actions, action_impacts

def health_I(initiator, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Health I'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for the initiator
    initiator_public_health = f'{initiator} Public Health'
    initiator_health_spending = f'{initiator} Health Spending'
    initiator_public_trust = f'{initiator} Public Trust'

    # 1. 公共卫生改革 (Public Health Reform)
    public_health_reform_probability = 0.5 + 0.1 * (current_values[initiator_health_spending] - 100) + 0.1 * (current_values[initiator_public_trust] - 60)
    random_value = np.random.random()

    if random_value < public_health_reform_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for public health reform
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_health_spending)] += 0.2
        action_impacts[columns_X.index(initiator_public_health)] += 0.2

    # 2. 疫苗研发与推广 (Vaccine Development and Promotion)
    vaccine_development_probability = 0.5 + 0.15 * (current_values[initiator_health_spending] - 100) + 0.2 * (current_values[initiator_public_trust] - 60)
    random_value = np.random.random()

    if random_value < vaccine_development_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for vaccine development
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_health_spending)] += 0.2
        action_impacts[columns_X.index(initiator_public_health)] += 0.25

    # 3. 防疫措施 (Epidemic Prevention Measures)
    epidemic_prevention_probability = 0.5 + 0.1 * (current_values[initiator_health_spending] - 100) + 0.15 * (current_values[initiator_public_trust] - 60)
    random_value = np.random.random()

    if random_value < epidemic_prevention_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2  # Positive action for epidemic prevention
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_health_spending)] += 0.2
        action_impacts[columns_X.index(initiator_public_health)] += 0.2

    # 4. 国家应急响应 (National Emergency Response)
    emergency_response_probability = 0.5 + 0.1 * (current_values[initiator_health_spending] - 100) + 0.1 * (current_values[initiator_public_trust] - 60)
    random_value = np.random.random()

    if random_value < emergency_response_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 1  # Positive action for national emergency response
        # Apply the impact on states
        action_impacts[columns_X.index(initiator_health_spending)] += 0.1
        action_impacts[columns_X.index(initiator_public_health)] += 0.15

    return row_actions, action_impacts

# Initialize an empty DataFrame for actions with columns and the appropriate number of rows
data_actions = pd.DataFrame(columns=action_columns, index=range(number_rows))
data_X_optimized = []  # Initialize an empty list for X data (states)

# First row initialization (start with 0 actions for all)
first_row_actions = [0] * len(action_columns)
data_actions.loc[0] = first_row_actions  # Add first row of actions

# Initialize the starting values for each parameter based on realistic data
initial_values = {
    'A Public Trust': 80.0,  # Increased Public Trust to increase the probability of actions like support
    'A Political Stability': 8.0,  # Increased Political Stability to increase the likelihood of political actions
    'A Trade Balance': -10*100,  # Decreased Trade Balance (increase trade deficit to increase probability of sanctions)
    'A GDP': 15000,  # Increased A's GDP to make economic aid more likely
    'A Unemployment Rate': 6.0,  # Slightly reduced Unemployment Rate to keep A's economy healthy
    'A Inflation Rate': 3.0, 
    'A Foreign Debt': 300, 
    'A Government Spending': 800,
    'A Military Spending': 150, 
    'A Education Spending': 70, 
    'A Health Spending': 120, 
    'A Environment Spending': 30, 
    'A Technology Investment': 250,
    'A Internet Penetration': 70.0, 
    'A Energy Production': 900, 
    'A Energy Consumption': 850, 
    'A Pollution Level': 20, 
    'A Population': 500000000,
    'A Urbanization Rate': 60.0, 
    'A Human Development Index': 0.75, 
    'A Freedom of Press': 60.0, 
    'A Corruption Index': 50.0,
    'A Military Power': 800*10, 
    'A Alliances': 2, 
    'A Environmental Quality': 70.0, 
    'A Natural Resources Availability': 100,
    'A Public Health': 80.0, 
    'A Democracy Index': 6.0, 
    'A Technology Adoption Rate': 0.5, 
    'A Cultural Influence': 40.0, 
    'A Global Trade Index': 0.6,
    'A Innovation Index': 0.5,  # New added parameter for A's innovation level
    'A Social Welfare Spending': 100,  # New added parameter for A's social welfare spending
    'A Social Security Reform':1,
    'A Social Welfare':100,
    'A Tax Rate': 25,  # New added parameter for A's tax rate
    'A National Security': 100,
    'A Financial Stability':100,

    'B GDP': 12000, 
    'B Unemployment Rate': 8.5,  # Increased B's Unemployment Rate to make aid more likely
    'B Inflation Rate': 2.0, 
    'B Foreign Debt': 400, 
    'B Government Spending': 1000,
    'B Military Spending': 180, 
    'B Education Spending': 90, 
    'B Health Spending': 140, 
    'B Environment Spending': 40, 
    'B Technology Investment': 280,
    'B Internet Penetration': 80.0, 
    'B Energy Production': 1100, 
    'B Energy Consumption': 1000, 
    'B Pollution Level': 18, 
    'B Population': 750000000,
    'B Urbanization Rate': 75.0, 
    'B Political Stability': 8.0, 
    'B Human Development Index': 0.85, 
    'B Public Trust': 70.0, 
    'B Freedom of Press': 80.0,
    'B Corruption Index': 35.0, 
    'B Military Power': 1200, 
    'B Alliances': 4, 
    'B Environmental Quality': 80.0, 
    'B Natural Resources Availability': 110,
    'B Trade Balance': 20, 
    'B Public Health': 90.0, 
    'B Democracy Index': 8.0, 
    'B Technology Adoption Rate': 0.7, 
    'B Cultural Influence': 60.0, 
    'B Global Trade Index': 0.8,
    'B Innovation Index': 0.5,  # New added parameter for A's innovation level
    'B Social Welfare Spending': 100,  # New added parameter for B's social welfare spending
    'B Social Security Reform':1,
    'B Social Welfare':100,
    'B Tax Rate': 20,  # New added parameter for B's tax rate
    'B National Security': 100, 
    'B Financial Stability':100,
    
    'A to B Imports': 200, 
    'A to B Exports': 150, 
    'B to A Imports': 180, 
    'B to A Exports': 130,
    'A Bond Status': 1, 
    'B Bond Status': 1, 
    'A Sovereignty Disputes': 0, 
    'B Sovereignty Disputes': 0,
    'Ethnic Similarity': 0.5, 
    'Cultural Compatibility': 0.7,
    'Political Similarity': 0.8  # Increased political similarity to improve relations with B and make support more likely
}

# Generate state data and actions row by row
current_values = initial_values.copy()

# Generate the first row of actions and states
# For each action, calculate its value based on the current state values (from the previous row)
# Generate state data and actions row by row
for i in range(1, number_rows):
    row_actions = [0] * len(action_columns)  # Initialize the row actions to zero for each action
    row_state = []  # Initialize a list for the state values

    # Initialize the temporary impact values for this row (independent impacts for each action)
    action_impacts = np.zeros(len(columns_X))  # This will store the impact of actions on states for this row

    # For each action, calculate its value based on the current state values (from the previous row)
    for j, action in enumerate(action_columns):

        # List of initiators and targets        
        pairs = [('A', 'B'), ('B', 'A')]

        # Iterate over each pair and apply the corresponding action functions
        for initiator, target in pairs:
            row_actions, action_impacts = political_T(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = economic_T(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = military_T(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = diplomatic_T(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = social_T(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = environmental_T(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = technology_T(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = health_T(initiator, target, current_values, action_columns, row_actions, action_impacts)

        # List of initiators
        initiators = ['A', 'B']

        # Iterate over each initiator and apply the corresponding action functions
        for initiator in initiators:
            # Call political_I for the initiator, which does not need a target
            row_actions, action_impacts = political_I(initiator, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = economic_I(initiator, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = military_I(initiator, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = diplomatic_I(initiator, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = social_I(initiator, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = environmental_I(initiator, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = technology_I(initiator, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = health_I(initiator, current_values, action_columns, row_actions, action_impacts)

    # Apply the action impacts to the state values (i.e., update the state values with the impact of the actions)
    growth_trend = 0.0000  # Assumed average annual growth rate of 0.02% for most parameters

    # Periodic terms (sinusoidal variations)
    period_1 = 52.1775  # Annual cycle (weekly data, approximately 1 year per cycle)
    period_2 = 208.71  # Longer cycle (~4 years for example)

    # Random phase shifts for each periodic term
    phase_1 = np.random.uniform(0, 2 * np.pi)
    phase_2 = np.random.uniform(0, 2 * np.pi)

    for col in columns_X:
        # Base value with linear growth over time
        linear_growth = current_values[col] * (1 + growth_trend)  # Apply growth rate
        
        # Generate independent phase shifts and amplitudes for each parameter
        phase_1 = np.random.uniform(0, 2 * np.pi)  # Random phase shift for the first cycle
        phase_2 = np.random.uniform(0, 2 * np.pi)  # Random phase shift for the second cycle
        
        # Periodic sinusoidal fluctuations for the parameter
        periodic_1 = np.sin(2 * np.pi * (i / period_1) + phase_1) * (initial_values[col] * np.random.uniform(0.01, 0.03))
        periodic_2 = np.sin(2 * np.pi * (i / period_2) + phase_2) * (initial_values[col] * np.random.uniform(0.01, 0.03))

        # Add a small random fluctuation proportional to the initial value
        random_fluctuation = np.random.uniform(-0.01, 0.01) * initial_values[col]

        # Combine the trend, periodic fluctuations, and random fluctuation
        new_value = linear_growth + periodic_1 + periodic_2 + random_fluctuation
        current_values[col] = new_value  # Update the current value
        
        # Append the new value to the row
        row_state.append(round(new_value, 2))
    # Assign the row actions directly to the DataFrame
    data_actions.loc[i] = row_actions
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