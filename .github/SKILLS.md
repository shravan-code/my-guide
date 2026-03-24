# Skills

## Navigation and UI Enhancement Skill

### Description
Add and maintain consistent navigation experience:
- `Hamburger menu` at right side in mobile view
- `Data Guide` brand on left
- `theme toggle` in header-actions
- `menu` visibility toggle
- closing menu on outside click

### Implementation
- JavaScript: `assets/js/app.js`
- CSS: `assets/css/styles.css`

### Testing
- Confirm upon screen resize below 980px: hamburger appears, menu hidden, click opens/closes menu.
- Confirm above 980px: menu always shown and hamburger hidden.
- Confirm theme toggles and persists via localStorage.

## Troubleshooting
- If hamburger doesn’t appear: verify `initNavToggle` in `source/app.js` runs and attaches button.
- If menu does not close: verify `.mobile-open` class is toggled and click outside event is not blocked.

## appinsights-instrumentation

### Description
Guidance for instrumenting webapps with Azure Application Insights. Provides telemetry patterns, SDK setup, and configuration references.

### When to Use
- how to instrument app
- App Insights SDK
- telemetry patterns
- what is App Insights
- Application Insights guidance
- instrumentation examples
- APM best practices

## azure-ai

### Description
Use for Azure AI: Search, Speech, OpenAI, Document Intelligence. Helps with search, vector/hybrid search, speech-to-text, text-to-speech, transcription, OCR.

### When to Use
- AI Search
- query search
- vector search
- hybrid search
- semantic search
- speech-to-text
- text-to-speech
- transcribe
- OCR
- convert text to speech

## azure-aigateway

### Description
Configure Azure API Management as an AI Gateway for AI models, MCP tools, and agents.

### When to Use
- semantic caching
- token limit
- content safety
- load balancing
- AI model governance
- MCP rate limiting
- jailbreak detection
- add Azure OpenAI backend
- add AI Foundry model
- test AI gateway
- LLM policies
- configure AI backend
- token metrics
- AI cost control
- convert API to MCP
- import OpenAPI to gateway

## azure-cloud-migrate

### Description
Assess and migrate cross-cloud workloads to Azure. Generates assessment reports and converts code from AWS, GCP, or other providers to Azure services.

### When to Use
- migrate Lambda to Azure Functions
- migrate AWS to Azure
- Lambda migration assessment
- convert AWS serverless to Azure
- migration readiness report
- migrate from AWS
- migrate from GCP
- cross-cloud migration

## azure-compliance

### Description
Comprehensive Azure compliance and security auditing capabilities including best practices assessment, Key Vault expiration monitoring, and resource configuration validation.

### When to Use
- compliance scan
- security audit
- BEFORE running azqr (compliance cli tool)
- Azure best practices
- Key Vault expiration check
- compliance assessment
- resource review
- configuration validation
- expired certificates
- expiring secrets
- orphaned resources
- policy compliance
- security posture evaluation

## azure-compute

### Description
Recommend Azure VM sizes, VM Scale Sets (VMSS), and configurations based on workload requirements, performance needs, and budget constraints. No Azure account required — uses public documentation and the Azure Retail Prices API.

### When to Use
- recommend VM size
- which VM should I use
- choose Azure VM
- VM for web/database/ML/batch/HPC
- GPU VM
- compare VM sizes
- cheapest VM
- best VM for workload
- VM pricing
- cost estimate
- burstable/compute/memory/storage optimized VM
- confidential computing
- VM trade-offs
- VM families
- VMSS
- scale set recommendation
- autoscale VMs
- load balanced VMs
- VMSS vs VM
- scale out
- horizontal scaling
- flexible orchestration

## azure-cost-optimization

### Description
Identify and quantify cost savings across Azure subscriptions by analyzing actual costs, utilization metrics, and generating actionable optimization recommendations.

### When to Use
- optimize Azure costs
- reduce Azure spending
- reduce Azure expenses
- analyze Azure costs
- find cost savings
- generate cost optimization report
- find orphaned resources
- rightsize VMs
- cost analysis
- reduce waste
- Azure spending analysis
- find unused resources
- optimize Redis costs

### Do Not Use For
- deploying resources (use azure-deploy)
- general Azure diagnostics (use azure-diagnostics)
- security issues (use azure-security)

## azure-deploy

### Description
Execute Azure deployments for ALREADY-PREPARED applications that have existing .azure/plan.md and infrastructure files. DO NOT use this skill when the user asks to CREATE a new application — use azure-prepare instead. This skill runs azd up, azd deploy, terraform apply, and az deployment commands with built-in error recovery. Requires .azure/plan.md from azure-prepare and validated status from azure-validate.

### When to Use
- "run azd up"
- "run azd deploy"
- "execute deployment"
- "push to production"
- "push to cloud"
- "go live"
- "ship it"
- "bicep deploy"
- "terraform apply"
- "publish to Azure"
- "launch on Azure"

### Do Not Use When
- "create and deploy"
- "build and deploy"
- "create a new app"
- "set up infrastructure"
- "create and deploy to Azure using Terraform" — use azure-prepare for these.

## azure-diagnostics

### Description
Debug Azure production issues on Azure using AppLens, Azure Monitor, resource health, and safe triage.

### When to Use
- debug production issues
- troubleshoot container apps
- troubleshoot functions
- troubleshoot AKS
- kubectl cannot connect
- kube-system/CoreDNS failures
- pod pending
- crashloop
- node not ready
- upgrade failures
- analyze logs
- KQL
- insights
- image pull failures
- cold start issues
- health probe failures
- resource health
- root cause of errors

## azure-hosted-copilot-sdk

### Description
Build and deploy GitHub Copilot SDK apps to Azure.

### When to Use
- build copilot app
- create copilot app
- copilot SDK
- @github/copilot-sdk
- scaffold copilot project
- copilot-powered app
- deploy copilot app
- host on azure
- azure model
- BYOM
- bring your own model
- use my own model
- azure openai model
- DefaultAzureCredential
- self-hosted model
- copilot SDK service
- chat app with copilot
- copilot-sdk-service template
- azd init copilot
- CopilotClient
- createSession
- sendAndWait
- GitHub Models API

## azure-kusto

### Description
Query and analyze data in Azure Data Explorer (Kusto/ADX) using KQL for log analytics, telemetry, and time series analysis.

### When to Use
- KQL queries
- Kusto database queries
- Azure Data Explorer
- ADX clusters
- log analytics
- time series data
- IoT telemetry
- anomaly detection

## azure-messaging

### Description
Troubleshoot and resolve issues with Azure Messaging SDKs for Event Hubs and Service Bus. Covers connection failures, authentication errors, message processing issues, and SDK configuration problems.

### When to Use
- event hub SDK error
- service bus SDK issue
- messaging connection failure
- AMQP error
- event processor host issue
- message lock lost
- send timeout
- receiver disconnected
- SDK troubleshooting
- azure messaging SDK
- event hub consumer
- service bus queue issue
- topic subscription error
- enable logging event hub
- service bus logging
- eventhub python
- servicebus java
- eventhub javascript
- servicebus dotnet
- event hub checkpoint
- event hub not receiving messages
- service bus dead letter

## azure-prepare

### Description
Prepare Azure apps for deployment (infra Bicep/Terraform, azure.yaml, Dockerfiles). Use for create/modernize or create+deploy; not cross-cloud migration (use azure-cloud-migrate).

### When to Use
- "create app"
- "build web app"
- "create API"
- "create serverless HTTP API"
- "create frontend"
- "create back end"
- "build a service"
- "modernize application"
- "update application"
- "add authentication"
- "add caching"
- "host on Azure"
- "create and deploy"
- "deploy to Azure"
- "deploy to Azure using Terraform"
- "deploy to Azure App Service"
- "deploy to Azure App Service using Terraform"
- "deploy to Azure Container Apps"
- "deploy to Azure Container Apps using Terraform"
- "generate Terraform"
- "generate Bicep"
- "function app"
- "timer trigger"
- "service bus trigger"
- "event-driven function"
- "containerized Node.js app"
- "social media app"
- "static portfolio website"
- "todo list with frontend and API"
- "prepare my Azure application to use Key Vault"
- "managed identity"

## azure-quotas

### Description
Check/manage Azure quotas and usage across providers. For deployment planning, capacity validation, region selection.

### When to Use
- "check quotas"
- "service limits"
- "current usage"
- "request quota increase"
- "quota exceeded"
- "validate capacity"
- "regional availability"
- "provisioning limits"
- "vCPU limit"
- "how many vCPUs available in my subscription"

## azure-rbac

### Description
Helps users find the right Azure RBAC role for an identity with least privilege access, then generate CLI commands and Bicep code to assign it. Also provides guidance on permissions required to grant roles.

### When to Use
- what role should I assign
- least privilege role
- RBAC role for
- role to read blobs
- role for managed identity
- custom role definition
- assign role to identity
- what role do I need to grant access
- permissions to assign roles

## azure-resource-lookup

### Description
List, find, and show Azure resources. Answers "list my VMs", "show my storage accounts", "list websites", "find container apps", "what resources do I have", and similar queries for any Azure resource type.

### When to Use
- list resources
- list virtual machines
- list VMs
- list storage accounts
- list websites
- list web apps
- list container apps
- show resources
- find resources
- what resources do I have
- list resources in resource group
- list resources in subscription
- find resources by tag
- find orphaned resources
- resource inventory
- count resources by type
- cross-subscription resource query
- Azure Resource Graph
- resource discovery
- list container registries
- list SQL servers
- list Key Vaults
- show resource groups
- list app services
- find resources across subscriptions
- find unattached disks
- tag analysis

### Do Not Use For
- deploying resources (use azure-deploy)
- creating or modifying resources
- cost optimization (use azure-cost-optimization)
- writing application code
- non-Azure clouds

## azure-resource-visualizer

### Description
Analyze Azure resource groups and generate detailed Mermaid architecture diagrams showing the relationships between individual resources.

### When to Use
- create architecture diagram
- visualize Azure resources
- show resource relationships
- generate Mermaid diagram
- analyze resource group
- diagram my resources
- architecture visualization
- resource topology
- map Azure infrastructure

## azure-storage

### Description
Azure Storage Services including Blob Storage, File Shares, Queue Storage, Table Storage, and Data Lake. Provides object storage, SMB file shares, async messaging, NoSQL key-value, and big data analytics capabilities. Includes access tiers (hot, cool, archive) and lifecycle management.

### When to Use
- blob storage
- file shares
- queue storage
- table storage
- data lake
- upload files
- download blobs
- storage accounts
- access tiers
- lifecycle management

### Do Not Use For
- SQL databases, Cosmos DB (use azure-prepare)
- messaging with Event Hubs or Service Bus (use azure-messaging)

## azure-upgrade

### Description
Assess and upgrade Azure workloads between plans, tiers, or SKUs within Azure. Generates assessment reports and automates upgrade steps.

### When to Use
- upgrade Consumption to Flex Consumption
- upgrade Azure Functions plan
- migrate hosting plan
- upgrade Functions SKU
- move to Flex Consumption
- upgrade Azure service tier
- change hosting plan
- upgrade function app plan
- migrate App Service to Container Apps

## azure-validate

### Description
Pre-deployment validation for Azure readiness. Run deep checks on configuration, infrastructure (Bicep or Terraform), permissions, and prerequisites before deploying.

### When to Use
- validate my app
- check deployment readiness
- run preflight checks
- verify configuration
- check if ready to deploy
- validate azure.yaml
- validate Bicep
- test before deploying
- troubleshoot deployment errors
- validate Azure Functions
- validate function app
- validate serverless deployment

## entra-app-registration

### Description
Guides Microsoft Entra ID app registration, OAuth 2.0 authentication, and MSAL integration.

### When to Use
- create app registration
- register Azure AD app
- configure OAuth
- set up authentication
- add API permissions
- generate service principal
- MSAL example
- console app auth
- Entra ID setup
- Azure AD authentication

### Do Not Use For
- Azure RBAC or role assignments (use azure-rbac)
- Key Vault secrets (use azure-keyvault-expiration-audit)
- Azure resource security (use azure-security)

## microsoft-foundry

### Description
Deploy, evaluate, and manage Foundry agents end-to-end: Docker build, ACR push, hosted/prompt agent create, container start, batch eval, prompt optimization, prompt optimizer workflows, agent.yaml, dataset curation from traces.

### When to Use
- deploy agent to Foundry
- hosted agent
- create agent
- invoke agent
- evaluate agent
- run batch eval
- optimize prompt
- improve prompt
- prompt optimization
- prompt optimizer
- improve agent instructions
- optimize agent instructions
- optimize system prompt
- deploy model
- Foundry project
- RBAC
- role assignment
- permissions
- quota
- capacity
- region
- troubleshoot agent
- deployment failure
- create dataset from traces
- dataset versioning
- eval trending
- create AI Services
- Cognitive Services
- create Foundry resource
- provision resource
- knowledge index
- agent monitoring
- customize deployment
- onboard
- availability

### Do Not Use For
- Azure Functions, App Service, general Azure deploy (use azure-deploy)
- general Azure prep (use azure-prepare)

## agent-customization

### Description
**WORKFLOW SKILL** — Create, update, review, fix, or debug VS Code agent customization files (.instructions.md, .prompt.md, .agent.md, SKILL.md, copilot-instructions.md, AGENTS.md).

### When to Use
- saving coding preferences
- troubleshooting why instructions/skills/agents are ignored or not invoked
- configuring applyTo patterns
- defining tool restrictions
- creating custom agent modes or specialized workflows
- packaging domain knowledge
- fixing YAML frontmatter syntax

### Do Not Use For
- general coding questions (use default agent)
- runtime debugging or error diagnosis
- MCP server configuration (use MCP docs directly)
- VS Code extension development

### Invokes
- file system tools (read/write customization files)
- ask-questions tool (interview user for requirements)
- subagents for codebase exploration

### Note
For SINGLE OPERATIONS: For quick YAML frontmatter fixes or creating a single file from a known pattern, edit the file directly — no skill needed.

## microsoft-foundry-agent-framework-code-gen

### Description
Generate, create, scaffold, build, enhance, fix, or debug AI agent and workflow code for Microsoft Foundry using Microsoft Agent Framework SDK.

### When to Use
- create Foundry agent code
- build agent app for Foundry
- scaffold agent project
- generate agent code with Agent Framework
- fix agent code
- enhance agent
- add tools to agent
- make app agentic
- multi-agent workflow for Foundry

### Do Not Use For
- deploy agent to Foundry (use microsoft-foundry skill deploy)
- manage Foundry resources, RBAC, quotas (use microsoft-foundry skill)
