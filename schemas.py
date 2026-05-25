# schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class DBSchema(BaseModel):
    tables: Dict[str, List[str]] = Field(description="Database structures mapping table names to column type definitions.")
    relations: List[str] = Field(description="Foreign key constraint arrays establishing inter-table integrity chains.")

class APISchema(BaseModel):
    endpoints: List[Dict[str, str]] = Field(description="Routing matrix parameters containing: path, method, and required_db_table keys.")

class UISchema(BaseModel):
    pages: List[str] = Field(description="Frontend client routing paths array.")
    components: Dict[str, List[str]] = Field(description="Dynamic rendering mapping from page targets to UI element arrays.")

class AuthRules(BaseModel):
    roles: List[str] = Field(description="System identity tokens like Admin, PremiumUser, or Guest.")
    permissions: Dict[str, List[str]] = Field(description="Identity token strings mapped to explicit path allowance strings.")

class FullAppConfig(BaseModel):
    app_name: str
    db_schema: DBSchema
    api_schema: APISchema
    ui_schema: UISchema
    auth_rules: AuthRules