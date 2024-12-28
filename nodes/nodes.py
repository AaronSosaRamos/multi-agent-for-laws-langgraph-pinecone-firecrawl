from pinecone import Pinecone
from document_loaders.firecrawl_handler import firecrawl_handler_scrape
from schemas.schemas import (
    LegalSummarySchemaOutput,
    LawContentAnalysisSchemaOutput,
    LegalActionsSuggestionsSchemaOutput,
    LegalActionsEvaluationSchemaOutput
)
from utils.logger import setup_logger
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv, find_dotenv
from langchain.schema import (
       HumanMessage,
       SystemMessage
)
from model.model import llm
from vector_store_db.vector_store_db import compile_pinecone_docs, return_pinecone_retriever
import os

load_dotenv(find_dotenv())

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index_name = "multi-agent-for-laws" 
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]


logger = setup_logger(__name__)

def generate_context(state):
    if index_name not in existing_indexes:
        docs = firecrawl_handler_scrape(state['url'])
        compile_pinecone_docs(docs)

    retriever = return_pinecone_retriever()
    context = retriever.invoke(state['legal_question'])

    logger.info(f"FIRST NODE - GENERATE CONTEXT: {context}")

    return {
        "context": context
    }

def generate_summary(state):
    json_parser = JsonOutputParser(pydantic_object=LegalSummarySchemaOutput)

    messages = [
        SystemMessage(content=f"""
        You are an expert in legal summarization. Your role is to analyze the provided legal context and generate a comprehensive summary that addresses the legal question posed. 
        Your summary must comply with the structure defined by the `LegalSummarySchema` and provide precise, legally sound insights.
        """),
        HumanMessage(content=f"""
        Please generate a detailed legal summary based on the following information:

        **Context**:
        {state['context']}

        **Legal Question**:
        {state['legal_question']}

        Your summary must include the following components:
        1. **Summary**: Provide a clear, concise version of the legal context, ensuring alignment with the posed legal question.
        2. **Key Points**: Identify and highlight the most relevant legal points from the context that address the legal question.
        3. **Parties Involved**: Specify the parties relevant to the legal case or context, using the `PartySchema`.
        4. **Relevant Dates**: List any critical dates in the legal context, formatted according to the `DateSchema`.
        5. **Jurisdiction**: Clearly state the jurisdiction or applicable legal area.
        6. **Keywords**: Extract key legal terms or phrases that are central to the context.

        Ensure your response is structured to comply with the format defined in the `LegalSummarySchema`:
        {json_parser.get_format_instructions()}

        You must provide your response in the specified language: {state['lang']}
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"SECOND NODE - GENERATE SUMMARY: {parsed_result}")

    return {
        "legal_summary_output": parsed_result
    }

def analyse_law_content(state):
    json_parser = JsonOutputParser(pydantic_object=LawContentAnalysisSchemaOutput)

    messages = [
        SystemMessage(content=f"""
        You are an expert in legal content analysis. Your role is to evaluate the provided legal document or content, focusing on its structure, clauses, and relevance to specific legal issues.
        Your analysis must comply with the structure defined by the `LawContentAnalysisSchema` and provide precise, detailed insights into the legal content.
        """),
        HumanMessage(content=f"""
        Please conduct a detailed legal content analysis based on the following information:

        **Legal Content**:
        {state['legal_summary_output']}

        **Legal Question**:
        {state['legal_question']}

        Your analysis must address the following components:
        1. **Document ID**: Assign or confirm a unique identifier for the legal document being analyzed.
        2. **Content**: Provide a detailed evaluation of the provided legal content, focusing on its relevance to the legal question.
        3. **Document Type**: Specify the type of the legal document (e.g., contract, statute, case law).
        4. **Sections to Analyze**: Identify specific sections or clauses that require detailed attention and use the `SectionSchema` to structure this analysis.
        5. **Legal Issues**: Highlight the key legal issues identified within the content that are pertinent to the legal question.
        6. **Applicable Laws**: Provide a list of relevant laws, precedents, or statutes that apply to the content.
        7. **Analysis Depth**: Indicate the required depth of the analysis (e.g., summary, detailed, critical).

        Ensure your response is structured to comply with the format defined in the `LawContentAnalysisSchema`:
        {json_parser.get_format_instructions()}

        You must provide your response in the specified language: {state['lang']}
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"THIRD NODE - ANALYSE LAW CONTENT: {parsed_result}")

    return {
        "law_content_analysis_output": parsed_result
    }

def suggest_legal_actions(state):
    json_parser = JsonOutputParser(pydantic_object=LegalActionsSuggestionsSchemaOutput)

    messages = [
        SystemMessage(content=f"""
        You are an expert in suggesting legal actions. Your role is to analyze the provided legal context and scenario, and propose practical and actionable legal strategies tailored to the situation.
        Your suggestions must comply with the structure defined by the `LegalActionsSuggestionsSchema` and provide precise, actionable recommendations.
        """),
        HumanMessage(content=f"""
        Please suggest detailed legal actions based on the following information:

        **Legal Context**:
        {state['law_content_analysis_output']}

        **Legal Question**:
        {state['legal_question']}

        Your suggestions must address the following components:
        1. **Scenario**: Provide a clear description of the scenario or situation requiring legal actions.
        2. **Goals**: List the desired outcomes or objectives for the suggested legal actions.
        3. **Risks**: Identify and describe the risks associated with the scenario and proposed actions, using the `RiskSchema`.
        4. **Resources**: Specify the resources available to implement the legal actions.
        5. **Previous Attempts**: Summarize any prior legal actions or strategies taken in this scenario and their results.
        6. **Timeline**: Provide a timeline for implementing the proposed legal actions.
        7. **Constraints**: Outline any constraints or limitations that should be considered when suggesting legal actions.

        Ensure your response is structured to comply with the format defined in the `LegalActionsSuggestionsSchema`:
        {json_parser.get_format_instructions()}

        You must provide your response in the specified language: {state['lang']}
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"FOURTH NODE - SUGGEST LEGAL ACTIONS: {parsed_result}")

    return {
        "legal_actions_suggestions_output": parsed_result
    }

def evaluate_legal_actions(state):
    json_parser = JsonOutputParser(pydantic_object=LegalActionsEvaluationSchemaOutput)

    messages = [
        SystemMessage(content=f"""
        You are an expert in evaluating legal actions. Your role is to assess proposed legal strategies based on their feasibility, potential risks, compliance, and expected outcomes.
        Your evaluation must comply with the structure defined by the `LegalActionsEvaluationSchema` and provide a clear, comprehensive assessment.
        """),
        HumanMessage(content=f"""
        Please evaluate the proposed legal actions based on the following information:

        **Proposed Legal Actions**:
        {state['legal_actions_suggestions_output']}

        **Legal Question**:
        {state['legal_question']}

        Your evaluation must address the following components:
        1. **Actions**: List and describe the proposed legal actions under evaluation.
        2. **Evaluation Criteria**: Specify the criteria used to evaluate the proposed actions (e.g., feasibility, cost, time, impact).
        3. **Risks**: Identify and describe potential risks associated with each action, using the `RiskSchema`.
        4. **Outcomes**: Provide an analysis of the expected outcomes for each action, using the `OutcomeSchema`.
        5. **Legal Compliance**: Assess the compliance of each proposed action with relevant legal requirements and standards.
        6. **Stakeholder Impact**: Evaluate the potential impact of each action on key stakeholders involved.
        7. **Prioritization**: Provide a prioritization of the proposed actions based on their evaluation and suitability.

        Ensure your response is structured to comply with the format defined in the `LegalActionsEvaluationSchema`:
        {json_parser.get_format_instructions()}

        You must provide your response in the specified language: {state['lang']}
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"FIFTH NODE - EVALUATE LEGAL ACTIONS: {parsed_result}")

    return {
        "legal_actions_evaluation_output": parsed_result
    }

def decide_legal_action(state):
    messages = [
        SystemMessage(content=f"""
        You are an expert in assessing the validity of legal actions. Your role is to analyze the provided evaluation of legal actions and determine if they are correct in addressing the specified legal question. 
        Your response must be either "yes" or "no," without any additional explanation or context.
        """),
        HumanMessage(content=f"""
        Based on the following information:

        **Evaluation of Legal Actions**:
        {state['legal_actions_evaluation_output']}

        **Legal Question**:
        {state['legal_question']}

        Are the evaluated legal actions correct in addressing the legal question?

        Respond with only "yes" or "no."
        """)
    ]

    result = llm.invoke(messages)

    logger.info(f"SIXTH NODE - DECIDE LEGAL ACTIONS: {result.content.strip()}")

    return {
        "are_legal_actions_correct": result.content.strip()
    }

def route_legal_action(state):
    if state["are_legal_actions_correct"] == "yes":
        return "re_implement_law_actions"
    else:
        return "take_decision"
    
def re_implement_law_actions(state):
    json_parser = JsonOutputParser(pydantic_object=LegalActionsEvaluationSchemaOutput)

    messages = [
        SystemMessage(content=f"""
        You are an expert in re-implementing legal actions. Your role is to analyze the provided evaluation of legal actions and refine or adjust them based on their feasibility, compliance, and potential for achieving the desired outcomes.
        Your response must comply with the structure defined by the `LegalActionsEvaluationSchema` and provide precise recommendations for re-implementation.
        """),
        HumanMessage(content=f"""
        Please re-implement the legal actions based on the following information:

        **Evaluation of Legal Actions**:
        {state['legal_actions_evaluation_output']}

        **Legal Question**:
        {state['legal_question']}

        Your re-implementation must address the following components:
        1. **Actions**: Refine or adjust the proposed legal actions based on the evaluation.
        2. **Evaluation Criteria**: Specify any updates to the criteria used to refine the actions (e.g., feasibility, cost, time, impact).
        3. **Risks**: Identify any new or remaining risks and describe how they are mitigated, using the `RiskSchema`.
        4. **Outcomes**: Refine the analysis of the expected outcomes for each action, using the `OutcomeSchema`.
        5. **Legal Compliance**: Ensure all actions comply with relevant legal requirements and standards, and note any updates.
        6. **Stakeholder Impact**: Reassess the potential impact of the refined actions on key stakeholders.
        7. **Prioritization**: Update the prioritization of the re-implemented actions based on their evaluation and suitability.

        Ensure your response is structured to comply with the format defined in the `LegalActionsEvaluationSchema`:
        {json_parser.get_format_instructions()}

        Provide your response in the specified language: {state['lang']}
        """)
    ]

    result = llm.invoke(messages)

    parsed_result = json_parser.parse(result.content)

    logger.info(f"CONDITIONAL NODE - RE-IMPLEMENT LAW ACTIONS: {parsed_result}")

    return {
        "legal_actions_evaluation_output": parsed_result
    }

def take_decision(state):
    messages = [
        SystemMessage(content=f"""
        You are an expert legal advisor. Your role is to analyze the provided evaluation of legal actions and deliver a clear, human-like decision on whether the legal actions align with the legal question.
        Your response must be professional, articulate, and provide a final recommendation in {state['lang']}, ensuring clarity for the intended audience.
        """),
        HumanMessage(content=f"""
        Based on the following:

        **Evaluation of Legal Actions**:
        {state['legal_actions_evaluation_output']}

        **Legal Question**:
        {state['legal_question']}

        Please provide a final decision in a human-like tone. The response must clearly explain whether the evaluated legal actions align with the legal question, and it must be written in {state['lang']}.
        """)
    ]

    result = llm.invoke(messages)

    logger.info(f"FINAL NODE - TAKE DECISIONS: {result.content}")

    return {
        "final_decision": result.content
    }