from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from schemas.routing import KeySelectionResponse
from datetime import datetime, timedelta, timezone # Import timezone

# from sqlalchemy.orm import Session # Placeholder for DB session
# from models.api_key import APIKey # Placeholder for DB model

router = APIRouter()

# Placeholder for database dependency
def get_db():
    print("DB session requested for Routing operations")
    try:
        # In a real app, this would be a SQLAlchemy Session or similar DB connection
        db = {} # Dummy DB session
        yield db
    finally:
        print("DB session closed for Routing operations")

# Placeholder for SDK authentication/authorization
def verify_sdk_request():
    print("SDK request verification placeholder: Access granted.")
    return True

# Mock database - In a real app, this data would come from a database.
# Add new fields: last_reset_time, last_selected_at, current_usage_requests, current_usage_tokens, rate_limit_requests_per_minute
MOCK_API_KEYS_DB = [
    {"id": 101, "api_key_value": "decrypted_mock_key_bu1_plat1_keyA", "platform_id": "1", "business_unit_id": "1", "is_active": True, "last_reset_time": datetime.now(timezone.utc) - timedelta(seconds=70), "last_selected_at": None, "last_used_at": None, "current_usage_requests": 5, "current_usage_tokens": 500, "rate_limit_requests_per_minute": 10},
    {"id": 102, "api_key_value": "decrypted_mock_key_bu1_plat1_keyB", "platform_id": "1", "business_unit_id": "1", "is_active": True, "last_reset_time": datetime.now(timezone.utc), "last_selected_at": None, "last_used_at": None, "current_usage_requests": 1, "current_usage_tokens": 100, "rate_limit_requests_per_minute": 5},
    {"id": 103, "api_key_value": "unlimited_key_bu1_plat1", "platform_id": "1", "business_unit_id": "1", "is_active": True, "last_reset_time": datetime.now(timezone.utc), "last_selected_at": None, "last_used_at": None, "current_usage_requests": 100, "current_usage_tokens": 10000, "rate_limit_requests_per_minute": None}, # No rate limit
    {"id": 201, "api_key_value": "decrypted_mock_key_bu2_plat2", "platform_id": "2", "business_unit_id": "2", "is_active": True, "last_reset_time": datetime.now(timezone.utc), "last_selected_at": None, "last_used_at": None, "current_usage_requests": 0, "current_usage_tokens": 0, "rate_limit_requests_per_minute": 20},
    {"id": 301, "api_key_value": "inactive_key_bu1_plat1", "platform_id": "1", "business_unit_id": "1", "is_active": False, "last_reset_time": datetime.now(timezone.utc), "last_selected_at": None, "last_used_at": None, "current_usage_requests": 0, "current_usage_tokens": 0, "rate_limit_requests_per_minute": 10}, # Inactive
    {"id": 104, "api_key_value": "rate_limited_key_bu1_plat1", "platform_id": "1", "business_unit_id": "1", "is_active": True, "last_reset_time": datetime.now(timezone.utc), "last_selected_at": None, "last_used_at": None, "current_usage_requests": 10, "current_usage_tokens": 1000, "rate_limit_requests_per_minute": 10}, # Already at limit
]

@router.get("/routing/select-key", response_model=KeySelectionResponse)
async def select_api_key(
    business_unit_id: str = Query(..., description="Business Unit ID to select a key for."),
    platform_id: str = Query(..., description="AI Platform ID to select a key for."),
    model_name: Optional[str] = Query(None, description="Optional model name for more specific key selection."),
    db = Depends(get_db), # db placeholder
    is_sdk_authenticated: bool = Depends(verify_sdk_request)
):
    if not is_sdk_authenticated:
        raise HTTPException(status_code=401, detail="Not authorized for SDK access")

    print(f"SDK attempting to select key for BU ID: {business_unit_id}, Platform ID: {platform_id}, Model: {model_name}")

    # --- Simulate Database Query and Operations ---
    # 1. Fetch active keys for the given business_unit_id and platform_id
    print("Simulating database query for active keys...")
    candidate_keys = [
        key for key in MOCK_API_KEYS_DB
        if key["business_unit_id"] == business_unit_id and \
           key["platform_id"] == platform_id and \
           key["is_active"]
    ]

    if not candidate_keys:
        print("No active keys found for the given criteria before rate limit checks.")
        raise HTTPException(status_code=404, detail="No active API key found for the given criteria.")

    usable_keys: List[dict] = []
    current_time = datetime.now(timezone.utc)

    print("Processing candidate keys for rate limits and usage reset...")
    for key_data in candidate_keys:
        key_copy = key_data.copy() # Work with a copy to simulate DB changes

        # 2. Check and reset usage window if necessary
        if key_copy["last_reset_time"]:
            # Assuming a 60-second usage window for rate limits
            if current_time - key_copy["last_reset_time"] > timedelta(seconds=60):
                print(f"Key ID {key_copy['id']}: Usage window expired. Resetting usage and last_reset_time.")
                # Simulate DB update:
                key_copy["current_usage_requests"] = 0
                key_copy["current_usage_tokens"] = 0
                key_copy["last_reset_time"] = current_time
                # In a real DB, you'd save this change.
                # For MOCK_API_KEYS_DB, find and update the original dict if you want persistence across calls in this mock.
                original_key_in_mock_db = next((k for k in MOCK_API_KEYS_DB if k["id"] == key_copy["id"]), None)
                if original_key_in_mock_db:
                    original_key_in_mock_db.update(key_copy)


        # 3. Filter out keys that are over their rate limit
        if key_copy.get("rate_limit_requests_per_minute") is not None:
            if key_copy["current_usage_requests"] >= key_copy["rate_limit_requests_per_minute"]:
                print(f"Key ID {key_copy['id']}: Over rate limit ({key_copy['current_usage_requests']}/{key_copy['rate_limit_requests_per_minute']}). Skipping.")
                continue # Skip this key

        # If model_name is provided, you might add logic here to prefer keys
        # specifically designated for that model (not implemented in this mock)

        usable_keys.append(key_copy)

    if not usable_keys:
        print("No keys available after rate limit filtering.")
        raise HTTPException(status_code=429, detail="All suitable API keys are currently rate-limited.")

    # 4. Sort keys:
    #    - Prioritize keys with more available capacity.
    #    - Keys without a rate limit can be considered as having "infinite" capacity or handled separately.
    #    - Secondary sort by least recently selected (`last_selected_at` ascending, None first).
    def sort_key_logic(key):
        available_capacity = float('inf')
        if key.get("rate_limit_requests_per_minute") is not None:
            available_capacity = key["rate_limit_requests_per_minute"] - key["current_usage_requests"]
        
        last_selected = key.get("last_selected_at")
        # Sort by:
        # 1. Descending available capacity (more is better)
        # 2. Ascending last_selected_at (None or older is better)
        return (-available_capacity, last_selected or datetime.min.replace(tzinfo=timezone.utc))

    usable_keys.sort(key=sort_key_logic)
    
    print(f"Sorted usable keys (best first): {[k['id'] for k in usable_keys]}")

    selected_key_data = usable_keys[0] # Select the best key

    # 5. Simulate updating the selected key's `last_selected_at`
    print(f"Simulating update of 'last_selected_at' for key ID {selected_key_data['id']} to {current_time}.")
    # In a real DB: APIKey.update(last_selected_at=current_time).where(APIKey.id == selected_key_data['id'])
    selected_key_data["last_selected_at"] = current_time # Simulate update
    original_key_in_mock_db = next((k for k in MOCK_API_KEYS_DB if k["id"] == selected_key_data["id"]), None)
    if original_key_in_mock_db:
        original_key_in_mock_db["last_selected_at"] = current_time


    # --- End Placeholder: Simulate Database Query and Operations ---

    print(f"Selected key ID: {selected_key_data['id']} for BU ID: {business_unit_id}, Platform ID: {platform_id}")

    return KeySelectionResponse(
        api_key_id=selected_key_data["id"],
        api_key_value=selected_key_data["api_key_value"], # Actual (decrypted) key value
        platform_id=int(selected_key_data["platform_id"]),
        business_unit_id=int(selected_key_data["business_unit_id"])
    )
