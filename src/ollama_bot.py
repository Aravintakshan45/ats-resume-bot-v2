import streamlit as st
import groq

GROQ_MODEL = "llama-3.3-70b-versatile"

def get_ai_response(user_question, analysis_results):
    if not analysis_results:
        return "Please analyze your resume first."
    
    # Simple context
    context = f"""
Score: {analysis_results['final_score']:.1f}%
Missing Keywords: {', '.join(analysis_results.get('missing_keywords', [])[:5])}
Missing Sections: {', '.join(analysis_results.get('missing_sections', []))}
"""
    
    prompt = f"""
You are an ATS resume expert.
Analysis: {context}
Question: {user_question}
Give specific advice.
"""
    
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        client = groq.Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an ATS resume expert."},
                {"role": "user", "content": prompt}
            ],
            model=GROQ_MODEL,
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
