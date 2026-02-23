import pandas as pd
import random
import time

def generate_large_dataset(num_rows=100, filename="data/large_sample.csv"):
    """
    Generates a CSV with a mix of valid and invalid data for stress testing.
    """
    print(f"Generating {num_rows} rows...")
    
    first_names = ["John", "Jane", "Bob", "Alice", "Charlie", "David", "Eva", "Frank"]
    last_names = ["Doe", "Smith", "Brown", "Johnson", "Williams", "Jones", "Miller"]
    domains = ["example.com", "test.org", "company.net", "email.io"]
    
    data = []
    
    for i in range(num_rows):
        # 80% chance of generally good data, 20% chaotic
        is_messy = random.random() < 0.2
        
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        full_name = f"{fname} {lname}"
        
        email = f"{fname.lower()}.{lname.lower()}@{random.choice(domains)}"
        
        age = random.randint(18, 80)
        account = random.choice(["free", "pro", "enterprise"])
        date = f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        active = random.choice(["true", "false", "yes", "no", "1", "0"])
        
        if is_messy:
            error_type = random.choice(["missing_email", "bad_age", "bad_date", "typo_account"])
            
            if error_type == "missing_email":
                email = ""
            elif error_type == "bad_age":
                age = random.choice([-5, 10, 150, "twenty"])
            elif error_type == "bad_date":
                date = "Jan 1st 2023" # deviations
            elif error_type == "typo_account":
                account = "freemium" # Not in enum
            
            # Occasionally mangle the name structure
            if random.random() < 0.3:
                full_name = f"{lname}, {fname}" # Comma format
                
        data.append([full_name, email, age, account, date, active])
    
    df = pd.DataFrame(data, columns=["Raw_Name", "Contact_Email", "User_Age", "Subscription", "Join_Date", "Is_Active_Flag"])
    
    # Save
    df.to_csv(filename, index=False)
    print(f"✅ Saved to {filename}")

if __name__ == "__main__":
    # Generate 50 rows by default for a quick test
    generate_large_dataset(50)
