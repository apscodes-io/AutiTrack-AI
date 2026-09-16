import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Create a .env file with your API key."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

DOMAINS = [
    "Communication",
    "Social Interaction",
    "Sensory",
    "Routine",
    "Behavior",
    "Daily Activity",
]


def analyze_observation(
    observation_text,
    context=None,
    activity=None
):
    """
    Analyze one caregiver observation.

    This function organizes an observation into predefined domains.
    It does NOT diagnose autism or any medical condition.
    """

    if not observation_text or not observation_text.strip():
        return {
            "error": "Observation text cannot be empty."
        }

    context = context or "Not specified"
    activity = activity or "Not specified"

    prompt = f"""
You are an AI observation-analysis assistant for a developmental
observation tracking application called AutiTrack AI.

Your job is ONLY to organize the supplied observation.

Allowed domains:
{DOMAINS}

Observation:
{observation_text}

Context:
{context}

Activity:
{activity}

Return JSON with exactly these fields:

{{
    "domains": [],
    "observed_behavior": [],
    "trigger": null,
    "summary": ""
}}

Rules:

1. Select one or more relevant domains from the allowed domains.
2. Extract only behaviors explicitly described in the observation.
3. If a trigger/context is explicitly mentioned, summarize it.
4. If no trigger is mentioned, use null.
5. Keep the summary neutral and concise.
6. Do NOT diagnose autism.
7. Do NOT diagnose any medical or developmental condition.
8. Do NOT recommend treatment.
9. Do NOT invent information.
10. Do NOT compare this child with other children.
11. Do NOT infer causes that are not explicitly stated.
12. Return ONLY valid JSON.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

        result = json.loads(response.text)

        required_fields = [
            "domains",
            "observed_behavior",
            "trigger",
            "summary",
        ]

        for field in required_fields:
            if field not in result:
                result[field] = None

        return result

    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON.",
            "raw_response": response.text if response else ""
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def generate_trend_summary(analytics_data):
    """
    Generate a neutral summary from already-calculated
    longitudinal analytics.
    """

    prompt = f"""
You are an AI assistant for AutiTrack AI.

Summarize the following longitudinal observation analytics.

Analytics data:
{json.dumps(analytics_data, indent=2)}

Return JSON:

{{
    "summary": "",
    "notable_changes": [],
    "context_patterns": [],
    "discussion_topics": []
}}

Rules:

1. Describe recorded patterns neutrally.
2. Do not diagnose any condition.
3. Do not recommend treatment.
4. Do not infer unsupported causes.
5. Do not compare children.
6. Do not describe a change as inherently good or bad.
7. Use only information present in the supplied data.
8. Discussion topics should be suitable for discussion with a qualified professional.
9. Return ONLY valid JSON.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

        return json.loads(response.text)

    except Exception as e:
        return {
            "error": str(e)
        }


def generate_session_brief(session_data):
    """
    Generate a concise professional discussion brief.
    """

    prompt = f"""
You are an AI assistant for AutiTrack AI.

Create a concise session brief from the supplied observation data.

Session data:
{json.dumps(session_data, indent=2)}

Return JSON:

{{
    "observation_overview": "",
    "recent_changes": [],
    "contextual_patterns": [],
    "notable_observations": [],
    "discussion_points": []
}}

Rules:

1. Summarize recorded observations only.
2. Do not diagnose autism.
3. Do not diagnose any medical or developmental condition.
4. Do not provide treatment recommendations.
5. Do not make clinical conclusions.
6. Do not invent information.
7. Do not infer unsupported causal relationships.
8. Do not compare children.
9. Keep language neutral.
10. Discussion points should simply identify observations
   that may be discussed with a qualified professional.
11. Return ONLY valid JSON.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

        return json.loads(response.text)

    except Exception as e:
        return {
            "error": str(e)
        }


def test_ai():
    """Simple API connectivity test."""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Respond with exactly: AutiTrack AI is working."
    )

    return response.text
  
