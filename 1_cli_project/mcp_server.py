from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field
mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document given its name.",
)
def read_documents(
    doc_id: str = Field(description="The name of the document to read."),
):
    if doc_id not in docs:
        raise ValueError(f"Document '{doc_id}' not found.")
    else:
        return docs[doc_id]
    

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_doc_contents",
    description="Edits the contents of a document given its name and new content.",
)
def edit_documents(
    doc_id:str = Field(description="The name of the document to edit."),
    old_str:str = Field(description="The string to be replaced in the document."),
    new_str:str = Field(description="The string to replace the old string with in the document."),
):
    if doc_id in docs:
        raise ValueError(f"Document '{doc_id}' not found.")
    else:
        docs[doc_id] = docs[doc_id].replace(old_str, new_str)
        return f"Document '{doc_id}' has been updated."
    
# TODO: Write a resource to return all doc id's
@mcp.resource("docs://documents", mime_type="application/json")
def list_docs()-> list[str]:
    return list(docs.keys())
# TODO: Write a resource to return the contents of a particular doc
@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id:str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document '{doc_id}' not found.")
    return docs[doc_id]
# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(name="format",description="Rewrites the contents of the document in Markdown Format")
def format_document(doc_id:str = Field(description="The name of the document to format."))-> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:

<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary.
Feel free to add in structure.
Use the 'edit_document' tool to edit the document.
After the document has been reformatted...
"""
    return base.UserMessage(prompt)

# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
