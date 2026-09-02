import json


def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


# Load mock data
members = load_data("data/members.json")
providers = load_data("data/providers.json")
claims = load_data("data/claims.json")
authorizations = load_data("data/authorizations.json")
policies = load_data("data/policies.json")


def get_member_plan(member_id):
    for member in members:
        if member["member_id"] == member_id:
            return member

    return None


def check_provider(provider_name):
    for provider in providers:
        if provider["name"].lower() == provider_name.lower():
            return provider

    return None


def get_claim_status(claim_id):
    for claim in claims:
        if claim["claim_id"] == claim_id:
            return claim

    return None


def get_authorization_status(authorization_id):
    for authorization in authorizations:
        if authorization["authorization_id"] == authorization_id:
            return authorization

    return None

def get_provider_network_status(provider_name):

    provider = check_provider(provider_name)

    if not provider:
        return {
            "success": False,
            "message": "Provider not found."
        }

    return {
        "success": True,
        "provider_name": provider["name"],
        "specialty": provider["specialty"],
        "location": provider["location"],
        "network_status": provider["network_status"]
    }

def get_claim_details(claim_id):

    claim = get_claim_status(claim_id)

    if not claim:
        return {
            "success": False,
            "message": "Claim not found."
        }

    return {
        "success": True,
        "claim_id": claim["claim_id"],
        "service": claim["service"],
        "amount": claim["amount"],
        "status": claim["status"],
        "member_responsibility": claim["member_responsibility"]
    }

def get_authorization_details(authorization_id):

    authorization = get_authorization_status(authorization_id)

    if not authorization:
        return {
            "success": False,
            "message": "Authorization not found."
        }

    return {
        "success": True,
        "authorization_id": authorization["authorization_id"],
        "service": authorization["service"],
        "provider": authorization["provider"],
        "status": authorization["status"]
    }

def get_policy_details(plan_id):

    for policy in policies:

        if policy["plan_id"] == plan_id:

            return {
                "success": True,
                "plan_id": policy["plan_id"],
                "plan_name": policy["plan_name"],
                "deductible": policy["deductible"],
                "out_of_pocket_max": policy["out_of_pocket_max"],
                "primary_care_copay": policy["primary_care_copay"],
                "specialist_copay": policy["specialist_copay"],
                "physical_therapy": policy["physical_therapy"],
                "referral_required": policy["referral_required"]
            }

    return {
        "success": False,
        "message": "Policy not found."
    }