# Agents

## DataGuide UI Agent

### Purpose
- Manage navigation and theme behavior across the Data Guide static site.
- Keep topbar interaction consistent across pages and screen sizes.

### Capabilities
- responsive hamburger menu control
- desktop and mobile layout adaptation
- theme toggle state persistence (dark/light)

### Files
- `assets/js/app.js`: core behavior and DOM interaction logic
- `source/styles.css`: topbar, menu and mobile style rules

### Usage
- This is a static site that runs in browser; no server-side agent runtime required.
- For local development, simply open `index.html` or run with any static web server (e.g., VS Code Live Server).

## AzqrCostOptimizeAgent

### Description
You are an Azure Cost Optimization Agent. Your mission is to identify, quantify, and recommend cost savings across an Azure subscription.

## MCP AppService Builder

### Description
Plan, scaffold, extend, and deploy .NET 10 MCP App Service MCP servers with azd/Bicep and RBAC

### Argument Hint
Describe the MCP server, tools to add, and your Azure subscription/resource group/location

## Azure IaC Exporter

### Description
Export existing Azure resources to Infrastructure as Code templates via Azure Resource Graph analysis, Azure Resource Manager API calls, and azure-iac-generator integration. Use this skill when the user asks to export, convert, migrate, or extract existing Azure resources to IaC templates (Bicep, ARM Templates, Terraform, Pulumi).

### Argument Hint
Specify which IaC format you want (Bicep, ARM, Terraform, Pulumi) and provide Azure resource details

## Azure IaC Generator

### Description
Central hub for generating Infrastructure as Code (Bicep, ARM, Terraform, Pulumi) with format-specific validation and best practices. Use this skill when the user asks to generate, create, write, or build infrastructure code, deployment code, or IaC templates in any format (Bicep, ARM Templates, Terraform, Pulumi).

### Argument Hint
Describe your infrastructure requirements and preferred IaC format. Can receive handoffs from export/migration agents.

## AIAgentExpert

### Description
Expert in streamlining and enhancing the development of AI Agent Applications / Workflows, including code generation, AI model comparison and recommendation, tracing setup, evaluation, deployment. Using Microsoft Agent Framework and can be fully integrated with Microsoft Foundry.

### Argument Hint
Create, debug, evaluate, deploy your AI agent/workflow using Microsoft Agent Framework.

## DataAnalysisExpert

### Description
Expert in analyzing data files using Data Viewer. Can explore data structure, read specific rows and cells, and provide insights.

### Argument Hint
Explore and compare your data.

## Explore

### Description
Fast read-only codebase exploration and Q&A subagent. Prefer over manually chaining multiple search and file-reading operations to avoid cluttering the main conversation. Safe to call in parallel. Specify thoroughness: quick, medium, or thorough.

### Argument Hint
Describe WHAT you're looking for and desired thoroughness (quick/medium/thorough)