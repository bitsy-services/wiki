---
title: "MCP"
weight: 70
---

The **Model Context Protocol** is the open specification for how a language model's harness talks to an external tool server — connecting an [agentic workflow](/wiki/ai/agentic-workflows) to filesystems, APIs, databases, and other tools without bespoke per-integration code. MCP standardizes the wire format (JSON-RPC over stdio or HTTP), the tool-discovery handshake, and the shape of tool calls and results, so the same server works across any compliant harness.

This page is a stub. The protocol shows up in this section as the substrate beneath [AI plugins](/wiki/ai/plugins) — a Claude Code plugin frequently bundles one or more MCP servers, and the [context-cost characteristics of MCP tools](/wiki/ai/plugins/claude-code#context-cost-in-practice) are what make plugin selection consequential.

## Further reading

- [Model Context Protocol specification](https://modelcontextprotocol.io/)
- Anthropic, [MCP in Claude Code](https://code.claude.com/docs/en/mcp)
- [MCP servers reference implementations](https://github.com/modelcontextprotocol/servers)
