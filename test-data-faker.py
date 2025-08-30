import pandas as pd
from faker import Faker
import random
from datetime import date, timedelta

# --- Parameters ---
COUNTRIES = {
    'India': {'cities': ['Delhi', 'Bangalore', 'Pune', 'Mumbai'], 'locale': 'en_IN', 'start_count': 2500},
    'USA': {'cities': ['New York', 'San Francisco', 'Austin', 'Seattle'], 'locale': 'en_US', 'start_count': 1200},
    'Australia': {'cities': ['Sydney', 'Perth', 'Adelaide'], 'locale': 'en_AU', 'start_count': 800}
}
YEARS = range(2018, 2026)
ATTRITION_RATE_RANGE = (0.12, 0.18)
GROWTH_RATE_RANGE = (0.02, 0.05)
GENDER_RATIO_RANGE = (0.35, 0.50)
RETIREMENT_AGE = 60
AGE_AT_HIRE_RANGE = (22, 55)
TENURE_ATTRITION_DAYS = (15, 365 * 25)
DEPARTMENTS = {
    'Finance': 0.15, 'IT': 0.20, 'Retail': 0.30, 'Research': 0.05,
    'Marketing': 0.15, 'HR': 0.10, 'Risk Management': 0.05
}

# --- Department and Salary-based Roles ---
DEPARTMENT_ROLES = {
    'Finance': {
        'Junior': ['Financial Analyst', 'Accountant'],
        'Mid': ['Senior Financial Analyst', 'Finance Manager'],
        'Senior': ['Controller', 'Director of Finance']
    },
    'IT': {
        'Junior': ['Software Engineer', 'IT Support Specialist'],
        'Mid': ['Data Scientist', 'Solutions Architect'],
        'Senior': ['IT Manager', 'Principal Engineer']
    },
    'Retail': {
        'Junior': ['Sales Associate', 'Store Clerk'],
        'Mid': ['Store Manager', 'Retail Supervisor'],
        'Senior': ['Regional Director', 'Head of Retail Operations']
    },
    'Research': {
        'Junior': ['Research Assistant', 'Junior Scientist'],
        'Mid': ['Senior Researcher', 'Research Scientist'],
        'Senior': ['Lead Scientist', 'Director of Research']
    },
    'Marketing': {
        'Junior': ['Marketing Assistant', 'Digital Marketing Specialist'],
        'Mid': ['Marketing Manager', 'Brand Strategist'],
        'Senior': ['Head of Marketing', 'Chief Marketing Officer']
    },
    'HR': {
        'Junior': ['HR Assistant', 'Recruiter'],
        'Mid': ['HR Manager', 'Talent Acquisition Manager'],
        'Senior': ['HR Director', 'Chief Human Resources Officer']
    },
    'Risk Management': {
        'Junior': ['Risk Analyst', 'Compliance Officer'],
        'Mid': ['Senior Risk Analyst', 'Risk Manager'],
        'Senior': ['Chief Risk Officer', 'Director of Risk']
    }
}

# Define salary tiers for job roles.
SALARY_TIERS = {
    'Junior': (50000, 75000),
    'Mid': (75001, 120000),
    'Senior': (120001, 200000)
}

# --- Exit reasons with weights ---
EXIT_REASONS = {
    'Better Opportunity': 0.5,
    'Family Circumstances': 0.2,
    'Relocation/Migration': 0.15,
    'Health Issue': 0.1,
    'Termination': 0.05
}

# --- Additional Employee Attributes ---
MARITAL_STATUS = ['Single', 'Married', 'Divorced', 'Widowed']
RECRUITMENT_SOURCES = {
    'LinkedIn': 0.3,
    'Company Website': 0.25,
    'Referral': 0.2,
    'Job Fair': 0.1,
    'University Partner': 0.1,
    'Online Job Board': 0.05
}
ENGAGEMENT_RATING = [1, 2, 3, 4, 5]
SATISFACTION_RATING = [1, 2, 3, 4, 5]
ABSENCE_COUNT_RANGE = (0, 20)

# --- Bonus Multipliers based on Performance Rating ---
BONUS_MULTIPLIERS = {
    2: 0,
    3: 0,
    4: 1,
    5: 2,
    6: 3,
    7: 4
}

# --- Initialization ---
fake = Faker()
all_employees_history = []
employee_id_counter = 1

# --- Helper Functions ---
def get_locale_faker(country):
    """Returns a Faker instance for the country's locale."""
    return Faker(COUNTRIES[country]['locale'])

def get_performance_rating():
    """Generates a performance rating based on a weighted distribution."""
    return random.choices(range(2, 8), weights=[0.05, 0.1, 0.2, 0.3, 0.2, 0.1], k=1)[0]

def get_salary_growth(rating):
    """Calculates salary growth percentage based on performance rating."""
    return 0.05 + (rating - 2) * (0.10 / 5)

def assign_job_title(department, salary):
    """Assigns a job title based on department and salary."""
    tier = None
    for job_tier, salary_range in SALARY_TIERS.items():
        if salary_range[0] <= salary <= salary_range[1]:
            tier = job_tier
            break
    
    if tier and department in DEPARTMENT_ROLES and tier in DEPARTMENT_ROLES[department]:
        return random.choice(DEPARTMENT_ROLES[department][tier])
    
    return 'General Employee'

def generate_employee(employee_id, country, hire_date, city, department, gender, age_at_hire):
    """Generates a single employee's record for their hire year."""
    locale_fake = get_locale_faker(country)
    first_name = locale_fake.first_name_male() if gender == 'M' else locale_fake.first_name_female()
    last_name = locale_fake.last_name()
    
    try:
        birth_date = hire_date.replace(year=hire_date.year - age_at_hire)
    except ValueError:
        birth_date = hire_date.replace(year=hire_date.year - age_at_hire, day=28)

    job_tier = random.choices(list(SALARY_TIERS.keys()), weights=[0.5, 0.4, 0.1], k=1)[0]
    start_salary = random.randint(*SALARY_TIERS[job_tier])

    marital_status = random.choice(MARITAL_STATUS)
    citizenship_country = country if random.random() < 0.9 else random.choice(list(COUNTRIES.keys()))
    recruitment_source = random.choices(list(RECRUITMENT_SOURCES.keys()), weights=list(RECRUITMENT_SOURCES.values()), k=1)[0]
    
    return {
        'employee_id': employee_id,
        'country': country,
        'city': city,
        'department': department,
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender,
        'hire_date': hire_date,
        'birth_date': birth_date,
        'age': hire_date.year - birth_date.year,
        'status': 'Active',
        'salary': start_salary,
        'tenure_days': (date(hire_date.year, 12, 31) - hire_date).days,
        'job_title': assign_job_title(department, start_salary),
        'marital_status': marital_status,
        'citizenship_country': citizenship_country,
        'recruitment_source': recruitment_source,
        'employee_engagement': random.choice(ENGAGEMENT_RATING),
        'employee_satisfaction': random.choice(SATISFACTION_RATING),
        'absence_count': random.randint(*ABSENCE_COUNT_RANGE)
    }

# --- Generate Data Year by Year ---
for year in YEARS:
    print(f"Generating data for year {year}...")
    
    for country, params in COUNTRIES.items():
        if year == 2018:
            employee_count = params['start_count']
            
            for _ in range(employee_count):
                hire_year = random.randint(2007, 2017)
                hire_date = date(hire_year, 1, 1) + timedelta(days=random.randint(0, 364))
                gender_ratio = random.uniform(*GENDER_RATIO_RANGE)
                gender = 'F' if random.random() < gender_ratio else 'M'
                age_at_hire = random.randint(*AGE_AT_HIRE_RANGE)
                city = random.choice(params['cities'])
                department = random.choices(list(DEPARTMENTS.keys()), weights=list(DEPARTMENTS.values()), k=1)[0]
                
                employee = generate_employee(employee_id_counter, country, hire_date, city, department, gender, age_at_hire)
                employee['age'] = year - employee['birth_date'].year
                employee['job_title'] = assign_job_title(employee['department'], employee['salary'])
                
                all_employees_history.append((year, employee_id_counter, employee))
                employee_id_counter += 1
        
        else:
            current_employees = [
                emp for y, _, emp in all_employees_history 
                if y == year - 1 and emp['status'] == 'Active' and emp['country'] == country
            ]
            
            employees_to_update = []
            for emp in current_employees:
                if year - emp['birth_date'].year >= RETIREMENT_AGE:
                    employees_to_update.append({'id': emp['employee_id'], 'status': 'Retired', 'termination_date': date(year, 1, 1)})
                else:
                    attrition_rate = random.uniform(*ATTRITION_RATE_RANGE)
                    if random.random() < attrition_rate:
                        tenure_days = (date(year, 1, 1) - emp['hire_date']).days
                        if TENURE_ATTRITION_DAYS[0] <= tenure_days <= TENURE_ATTRITION_DAYS[1]:
                            termination_date = date(year, 1, 1) + timedelta(days=random.randint(0, 364))
                            exit_reason = random.choices(list(EXIT_REASONS.keys()), weights=list(EXIT_REASONS.values()), k=1)[0]
                            employees_to_update.append({'id': emp['employee_id'], 'status': 'Voluntary Attrition', 'termination_date': termination_date, 'exit_reason': exit_reason})

            for emp_update in employees_to_update:
                for emp_record in reversed(all_employees_history):
                    if emp_record[0] == year - 1 and emp_record[1] == emp_update['id']:
                        new_emp = emp_record[2].copy()
                        new_emp['status'] = emp_update['status']
                        new_emp['termination_date'] = emp_update.get('termination_date')
                        new_emp['exit_reason'] = emp_update.get('exit_reason', None)
                        new_emp['age'] = year - new_emp['birth_date'].year
                        all_employees_history.append((year, emp_update['id'], new_emp))
                        break
            
            ids_who_left = {update['id'] for update in employees_to_update}
            remaining_employees = [emp for emp in current_employees if emp['employee_id'] not in ids_who_left]
            
            # Simplified hiring logic for 2020
            if year == 2020:
                num_new_hires = int(len(remaining_employees) * 0.05) + len(ids_who_left)
            else:
                num_new_hires = int(len(remaining_employees) * random.uniform(*GROWTH_RATE_RANGE)) + len(ids_who_left)
            
            for _ in range(num_new_hires):
                hire_date = date(year, 1, 1) + timedelta(days=random.randint(0, 364))
                gender_ratio = random.uniform(*GENDER_RATIO_RANGE)
                gender = 'F' if random.random() < gender_ratio else 'M'
                age_at_hire = random.randint(*AGE_AT_HIRE_RANGE)
                city = random.choice(params['cities'])
                department = random.choices(list(DEPARTMENTS.keys()), weights=list(DEPARTMENTS.values()), k=1)[0]
                
                employee = generate_employee(employee_id_counter, country, hire_date, city, department, gender, age_at_hire)
                employee['job_title'] = assign_job_title(department, employee['salary'])
                all_employees_history.append((year, employee_id_counter, employee))
                employee_id_counter += 1

            for emp in remaining_employees:
                new_emp = emp.copy()
                rating = get_performance_rating()
                growth_percent = get_salary_growth(rating)
                
                new_emp['salary'] = round(new_emp['salary'] * (1 + growth_percent), 2)
                new_emp['tenure_days'] = (date(year, 12, 31) - new_emp['hire_date']).days
                new_emp['age'] = year - new_emp['birth_date'].year
                new_emp['status'] = 'Active'
                new_emp['performance_rating'] = rating
                new_emp['job_title'] = assign_job_title(new_emp['department'], new_emp['salary'])
                
                new_emp['employee_engagement'] = random.choice(ENGAGEMENT_RATING)
                new_emp['employee_satisfaction'] = random.choice(SATISFACTION_RATING)
                new_emp['absence_count'] = random.randint(*ABSENCE_COUNT_RANGE)
                
                bonus_months = BONUS_MULTIPLIERS.get(rating, 0)
                new_emp['bonus'] = round((new_emp['salary'] / 12) * bonus_months, 2)
                
                new_emp.pop('termination_date', None)
                new_emp.pop('exit_reason', None)
                all_employees_history.append((year, new_emp['employee_id'], new_emp))

# --- Convert to DataFrame and Export ---
final_data = [{'year': y, **emp} for y, _, emp in all_employees_history]
df = pd.DataFrame(final_data)

df = df[[
    'year', 'employee_id', 'first_name', 'last_name', 'gender', 'marital_status',
    'citizenship_country', 'recruitment_source', 'country', 'city', 'department',
    'job_title', 'hire_date', 'birth_date', 'age', 'status',
    'termination_date', 'exit_reason', 'tenure_days', 'salary', 'bonus',
    'performance_rating', 'employee_engagement', 'employee_satisfaction',
    'absence_count'
]]

df['hire_date'] = pd.to_datetime(df['hire_date'])
df['birth_date'] = pd.to_datetime(df['birth_date'])
df['termination_date'] = pd.to_datetime(df['termination_date'])
df = df.sort_values(by=['employee_id', 'year']).reset_index(drop=True)

print("Data generation complete. Here's a sample:")
print(df.head(20))
df.to_csv('fake_employee_data_2020_hiring_reduced.csv', index=False)
print("\nUpdated data saved to 'fake_employee_data_2020_hiring_reduced.csv'")
