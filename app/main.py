"""import json

def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

members=load_data("data/members.json")

print("Care AI- Healthcare Insurance Agent")
print("____________________________________")

for member in members:
    print(
        f"Member_Id: {member['member_id']} |"
        f"Name: {member['name']} |"
        f"Plan: {member['plan_name']}"
    )
"""

"""
#Test Member tool
from insurance_tools import get_member


member = get_member("M1001")

if member:
    print("Member found!")
    print(f"Name: {member['name']}")
    print(f"Plan: {member['plan_name']}")
    print(f"Status: {member['status']}")
else:
    print("Member not found.")
"""

"""
#Test Provider Network
from insurance_tools import check_provider


provider = check_provider("Dr. John Smith")

if provider:
    print("Provider found!")
    print(f"Name: {provider['name']}")
    print(f"Specialty: {provider['specialty']}")
    print(f"Location: {provider['location']}")
    print(f"Network Status: {provider['network_status']}")
else:
    print("Provider not found.")
"""
"""
#Test Claim Status
from insurance_tools import get_claim_status


claim = get_claim_status("CLM10001")

if claim:
    print("Claim found!")
    print(f"Claim ID: {claim['claim_id']}")
    print(f"Service: {claim['service']}")
    print(f"Amount: ${claim['amount']}")
    print(f"Status: {claim['status']}")
else:
    print("Claim not found.")
"""

"""
#Test Authorization
from insurance_tools import get_authorization_status


authorization = get_authorization_status("AUTH1001")

if authorization:
    print("Authorization found!")
    print(f"Authorization ID: {authorization['authorization_id']}")
    print(f"Service: {authorization['service']}")
    print(f"Provider: {authorization['provider']}")
    print(f"Status: {authorization['status']}")
else:
    print("Authorization not found.")
"""
from insurance_tools import(
    get_member,
    get_authorization_details,
    get_provider_network_status,
    get_authorization_status,
    get_claim_details
)

print("\n--- MEMBER ---")
print(get_member("M1001"))

print("\n--- PROVIDER ---")
print(get_provider_network_status("Dr. John Smith"))

print("\n--- CLAIM ---")
print(get_claim_details("CLM10001"))

print("\n--- AUTHORIZATION ---")
print(get_authorization_details("AUTH1001"))