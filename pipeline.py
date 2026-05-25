# pipeline.py
import os
import json
from groq import Groq
from schemas import FullAppConfig

client = Groq(api_key=("GROQ_API_KEY"))

def run_llm_stage(system_prompt: str, user_content: str, response_format=None):
    """Executes deterministic structured transformations using active Llama models."""
    kwargs = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.0  # Zero variance keeps it highly predictable
    }
    
    if response_format:
        kwargs["response_format"] = {"type": "json_object"}
        # CRITICAL FIX: Explicitly forcing the model to wrap components correctly under keys
        user_content += f"""
        \nIMPORTANT: You must output a complete single JSON object containing ALL requested root keys.
        Do NOT wrap configurations inside each other. Follow this exact JSON schema structure:
        {json.dumps(response_format.model_json_schema())}
        """
        kwargs["messages"][1]["content"] = user_content

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content

def compile_app(user_instruction: str) -> FullAppConfig:
    # Phase 1: Intent Extraction Engine
    stage1_prompt = """You are a software architecture parser. Extract the core functional app features from the user prompt. 
    Ignore meta-text, task descriptions, or rules listed in the prompt. Focus only on what the app should do."""
    intent_graph = run_llm_stage(stage1_prompt, user_instruction)
    
    # Phase 2: System Topology Design Layer
    stage2_prompt = "Convert the extracted features into a clear micro-systems blueprint mapping tables, endpoints, and roles."
    system_blueprint = run_llm_stage(stage2_prompt, intent_graph)
    
    # Phase 3: Structured Config Compiling
    stage3_prompt = """Convert this system architecture blueprint into the strict target FullAppConfig configuration layout.
    Make sure to populate every single field: app_name, db_schema, api_schema, ui_schema, and auth_rules. Do not skip any key."""
    raw_json = run_llm_stage(stage3_prompt, system_blueprint, response_format=FullAppConfig)
    
    return FullAppConfig.model_validate_json(raw_json)