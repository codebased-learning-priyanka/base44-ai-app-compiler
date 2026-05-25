# engine.py
import json
from schemas import FullAppConfig
from pipeline import run_llm_stage

def verify_cross_layer_alignment(config: FullAppConfig) -> list:
    """Performs isolated dependency graph parsing to verify internal structural balance."""
    anomalies = []
    
    # Rule 1: Validation of API data pipeline targeting existing database entities
    defined_tables = set(config.db_schema.tables.keys())
    for route in config.api_schema.endpoints:
        bound_table = route.get("required_db_table")
        if bound_table and bound_table not in defined_tables:
            anomalies.append(f"Broken Link: API endpoint '{route.get('path')}' handles query targeting non-existent database table structure '{bound_table}'.")
            
    # Rule 2: Gated Auth resource targets checking inside active UI matrix definitions
    active_views = set(config.ui_schema.pages)
    for credential_token, access_paths in config.auth_rules.permissions.items():
        for track in access_paths:
            if "/" in track: 
                continue  # Bypassing raw API paths targeting service endpoints
            if track not in active_views:
                anomalies.append(f"Security Alert: Role definition constraint '{credential_token}' grants authorization route access to uninstantiated UI path allocation point '{track}'.")
                
    return anomalies

def validate_and_repair(config: FullAppConfig, context_prompt: str, operational_depth=0, ceiling_limit=2) -> FullAppConfig:
    anomalies = verify_cross_layer_alignment(config)
    
    if not anomalies:
        return config  # State convergence reached safely
        
    if operational_depth >= ceiling_limit:
        raise RuntimeError(f"Compiler Core Failure: Self-healing loop depth exceeded baseline ceiling limits. Current discrepancies trace: {anomalies}")
        
    patch_payload_context = f"""
    Context: Automated compiler validation diagnostics tracked layer alignment discrepancies.
    Structural Inconsistencies Detected: {json.dumps(anomalies, indent=2)}
    
    Task: Apply atomic schema configuration corrections. Maintain the exact user intent defined in: '{context_prompt}'
    """
    
    healed_raw_output = run_llm_stage(
        system_prompt="Correct structural configuration properties. Return an integrated, fully updated app state profile configuration blueprint.",
        user_content=patch_payload_context,
        response_format=FullAppConfig
    )
    
    healed_instance = FullAppConfig.model_validate_json(healed_raw_output)
    return validate_and_repair(healed_instance, context_prompt, operational_depth + 1, ceiling_limit)