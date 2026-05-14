from fastapi import FastAPI
from pydantic import BaseModel

from agent.agent import generate_drive_query
from tools.drive_search import search_drive

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


# ---------------------------------------------------------
# SEARCH KEYWORDS
# ---------------------------------------------------------

search_keywords = [
    "find",
    "search",
    "show",
    "get",
    "locate",
    "pdf",
    "image",
    "report",
    "invoice",
    "document",
    "file",
    "files",
    "photo",
    "photos"
]


# ---------------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message.strip()

    # ---------------------------------------------------------
    # CHECK IF USER WANTS SEARCH
    # ---------------------------------------------------------

    user_message_lower = user_message.lower()

    is_search_request = any(
        keyword in user_message_lower
        for keyword in search_keywords
    )

    # ---------------------------------------------------------
    # NORMAL CHAT
    # ---------------------------------------------------------

    if not is_search_request:

        return {
            "reply": (
                "Hey! I can help you search PDFs, images, "
                "reports, invoices, and other files from "
                "your Google Drive."
            ),
            "query": "",
            "results": [],
            "is_search": False
        }

    # ---------------------------------------------------------
    # GENERATE DRIVE QUERY
    # ---------------------------------------------------------

    drive_query = generate_drive_query(user_message)

    # ---------------------------------------------------------
    # SEARCH GOOGLE DRIVE
    # ---------------------------------------------------------

    results = search_drive(drive_query)

    # ---------------------------------------------------------
    # HANDLE ERRORS
    # ---------------------------------------------------------

    if isinstance(results, dict) and "error" in results:

        return {
            "reply": (
                "Something went wrong while searching "
                "Google Drive."
            ),
            "query": drive_query,
            "results": [],
            "is_search": True
        }

    # ---------------------------------------------------------
    # AI REPLY
    # ---------------------------------------------------------

    total = len(results)

    if total == 0:

        reply = (
            "I couldn't find any matching files "
            "in your Google Drive."
        )

    elif total == 1:

        reply = (
            "I found 1 matching file in your Google Drive."
        )

    else:

        reply = (
            f"I found {total} matching files "
            f"in your Google Drive."
        )

    # ---------------------------------------------------------
    # RETURN RESPONSE
    # ---------------------------------------------------------

    return {
        "reply": reply,
        "query": drive_query,
        "results": results,
        "is_search": True
    }