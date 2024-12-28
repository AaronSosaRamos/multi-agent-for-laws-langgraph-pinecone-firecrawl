from pydantic import BaseModel, Field

# Subschemas

class PartySchema(BaseModel):
    name: str = Field(..., description="Name of the party involved.")
    role: str = Field(..., description="Role of the party in the legal context (e.g., plaintiff, defendant).")
    contact_info: str = Field(..., description="Contact information of the party.")
    legal_representative: str = Field(..., description="Name of the legal representative, if any.")
    stake: str = Field(..., description="Stake or interest of the party in the case.")

class DateSchema(BaseModel):
    event: str = Field(..., description="Description of the event related to the date.")
    date: str = Field(..., description="The specific date in YYYY-MM-DD format.")

class SectionSchema(BaseModel):
    title: str = Field(..., description="Title of the section or clause.")
    content: str = Field(..., description="Content of the section or clause.")
    reference: str = Field(..., description="Reference identifier for the section, if applicable.")

class RiskSchema(BaseModel):
    type: str = Field(..., description="Type of risk (e.g., financial, reputational, legal).")
    severity: str = Field(..., description="Severity of the risk (e.g., high, medium, low).")
    mitigation_suggestions: list[str] = Field(..., description="Suggestions to mitigate the identified risk.")

class OutcomeSchema(BaseModel):
    description: str = Field(..., description="Description of the expected outcome.")
    likelihood: str = Field(..., description="Likelihood of achieving the outcome (e.g., high, medium, low).")
    benefits: list[str] = Field(..., description="List of benefits associated with the outcome.")
    dependencies: list[str] = Field(..., description="Dependencies required to achieve the outcome.")

# Primary Schemas

class LegalSummarySchema(BaseModel):
    context: str = Field(..., description="The context or scenario requiring legal summary.")
    parties: list[PartySchema] = Field(..., description="Details of the parties involved.")
    relevant_dates: list[DateSchema] = Field(..., description="Key dates relevant to the case or legal scenario.")
    summary_length: int = Field(..., description="Desired length of the summary in words.")
    jurisdiction: str = Field(..., description="Jurisdiction or legal area applicable.")
    keywords: list[str] = Field(..., description="Keywords to focus on in the summary.")

class LawContentAnalysisSchema(BaseModel):
    document_id: str = Field(..., description="Unique identifier for the document under analysis.")
    content: str = Field(..., description="The full content of the legal document.")
    document_type: str = Field(..., description="Type of legal document (e.g., contract, statute, case law).")
    sections_to_analyze: list[SectionSchema] = Field(..., description="Specific sections or clauses for detailed analysis.")
    legal_issues: list[str] = Field(..., description="List of legal issues identified or to focus on.")
    applicable_laws: list[str] = Field(..., description="List of laws or precedents relevant to the document.")
    analysis_depth: str = Field(..., description="Depth of analysis required (e.g., summary, detailed, critical).")

class LegalActionsSuggestionsSchema(BaseModel):
    scenario: str = Field(..., description="Description of the legal scenario requiring action suggestions.")
    goals: list[str] = Field(..., description="List of desired outcomes or goals for the legal actions.")
    risks: list[RiskSchema] = Field(..., description="Identified risks associated with the scenario.")
    resources: list[str] = Field(..., description="Resources available to implement the legal actions.")
    previous_attempts: list[str] = Field(..., description="Summary of any prior actions taken in this scenario.")
    timeline: str = Field(..., description="Expected or desired timeline for the legal actions.")
    constraints: list[str] = Field(..., description="Constraints or limitations to consider when suggesting actions.")

class LegalActionsEvaluationSchema(BaseModel):
    actions: list[str] = Field(..., description="List of proposed legal actions for evaluation.")
    evaluation_criteria: list[str] = Field(..., description="Criteria for evaluating the proposed actions.")
    risks: list[RiskSchema] = Field(..., description="Potential risks associated with each action.")
    outcomes: list[OutcomeSchema] = Field(..., description="Expected outcomes or benefits of the actions.")
    legal_compliance: list[str] = Field(..., description="Legal requirements or compliance issues for each action.")
    stakeholder_impact: list[str] = Field(..., description="Impact of actions on stakeholders involved.")
    prioritization: list[str] = Field(..., description="Suggested prioritization of actions based on evaluation.")
