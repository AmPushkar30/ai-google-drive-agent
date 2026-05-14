import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from tools.drive_search import search_drive

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_drive_query(user_input):

    prompt = f"""
    You are a Google Drive query generator.

    Convert the user's request into a valid Google Drive API q query.

    Rules:
    - Return ONLY the query
    - No explanation
    - Use valid Google Drive syntax

    Use:
    - name contains ''
    - mimeType=''
    - fullText contains ''
    - modifiedTime >

    Guidelines:

    - For PDFs:
        mimeType='application/pdf'

    - For images:
        mimeType contains 'image/'

    - For documents:
        mimeType contains 'document'

    - Prefer:
        name contains ''

    - Use fullText contains only if:
        user explicitly asks for:
        - content
        - text inside file
        - mentioning
        - contains text

    Examples:

    User: Find invoice PDFs
    Query:
    mimeType='application/pdf' and name contains 'invoice'

    User: Find files mentioning revenue
    Query:
    fullText contains 'revenue'

    User Request:
    {user_input}
    """

    response = llm.invoke(prompt)

    return response.content.strip()


def ai_drive_agent(user_input):

    query = generate_drive_query(user_input)

    print("\nGenerated Query:")
    print(query)

    files = search_drive(query)

    return query, files



