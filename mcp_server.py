"""The agent's four lookups, served over the Model Context Protocol (MCP).

MCP is a standard way for a program that runs a language model (the client) to
find and call tools that live in another program (the server). The two talk in
JSON-RPC 2.0 messages. Here the server is started by the client as a child
process and the messages travel over its standard input and output ("stdio").

What changes with this file: where the lookups run. What does not change: the
lookups themselves. Each tool below calls the same code in agent/tools.py that
the agent calls directly in steps 5 to 9, so the text the model reads is the
same either way. Step 10 proves that, lookup by lookup.

    python mcp_server.py                    started by the client; not meant to be run by hand
    python mcp_server.py --registry-down    stress test: the registry does not answer

A tool result carries two things, as in the direct path: the text the model
reads (the result's content) and the facts in it as data (its structured
content), which the checks use to verify what the model says it saw.
None of the tools can read the answer key.
"""
import sys

from mcp.server import MCPServer
from mcp.types import CallToolResult, TextContent

from agent.tools import Lookups
from common import LEDGER_CSV, read_csv
from registry import Registry

server = MCPServer(
    "exception-agent-lookups",
    instructions="Four read-only lookups over a payments ledger and a snapshot of the NPI registry. "
                 "Nothing here changes the ledger or the filing.",
)
lookups = Lookups(read_csv(LEDGER_CSV), Registry(), registry_down="--registry-down" in sys.argv)


def reply(name, text, case=None):
    """Run one lookup and wrap its two outputs as an MCP tool result."""
    said, facts = lookups.run(name, text, case or {})
    return CallToolResult(content=[TextContent(type="text", text=said)], structured_content={"facts": facts})


@server.tool(structured_output=False)
def registry_lookup(npi: str) -> CallToolResult:
    """Look up one ten-digit NPI in the registry snapshot. Returns the registered person, or says there is no record."""
    return reply("registry_lookup", npi)


@server.tool(structured_output=False)
def registry_search(name: str, line_npi: str) -> CallToolResult:
    """Search the registry snapshot by first and last name. line_npi is the NPI on the ledger line, so each
    match can say in how many digits it differs from it."""
    return reply("registry_search", name, {"npi": line_npi})


@server.tool(structured_output=False)
def ledger_history(name: str) -> CallToolResult:
    """Count the ledger lines under a person's name, by the NPI each line carries."""
    return reply("ledger_history", name)


@server.tool(structured_output=False)
def source_documents(line_ids: str) -> CallToolResult:
    """Give the source document number, feed and load date of ledger lines. Input: line IDs such as L00012, separated by commas."""
    return reply("source_documents", line_ids)


if __name__ == "__main__":
    server.run("stdio")
