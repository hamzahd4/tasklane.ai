import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # This loads your .env file so os.getenv() works

 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
def generate_sop(transcript_json, visual_json):
    prompt = f"""
You are an expert technical writer.
Given the following video narration transcript and visual frame data, write a clear numbered step-by-step Standard Operating Procedure (SOP).
 
Transcript JSON:
{transcript_json}
 
Visual Data JSON:
{visual_json}
 
Format your SOP as numbered steps, e.g.:
 
1. Step one description.
2. Step two description.
"""
 
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
    )
    return response.choices[0].message.content