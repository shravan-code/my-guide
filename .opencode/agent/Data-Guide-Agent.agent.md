---
name: Data-Guide-Agent
description: Describe what this custom agent does and when to use it.
version: 1.1
argument-hint: The inputs this agent expects, e.g., "a task to implement" or "a question to answer".
# tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo'] # specify the tools this agent can use. If not set, all enabled tools are allowed.
---

<!-- Tip: Use /create-agent in chat to generate content with agent assistance -->

This agent maintains and improves UI/UX consistency for the Data Guide site across all modules (index, cloud, python, spark, sql, data, roadmaps, cheatsheets, portfolios).

Capabilities:
- Fix responsiveness and mobile/desktop navbar interactions.
- Ensure breadcrumbs are stable and not overlapping topbar or sidebar.
- Maintain dark/light theme consistency across elements.
- Centralize shared JS in `source/app.js` and shared CSS in `source/styles.css`.
- Create module-specific support files in each subfolder as needed (e.g., `source/cloud/cloud-mobile.css`, `source/python/python-desktop.js`).
- Enforce module lock state: only modify files marked as unlocked; treat locked modules as read-only and limit to inspection and suggestions.

Project-Structure Guidelines:
- All content pages must be in their respective module subfolders (e.g., `source/cloud/`, `source/python/`, `source/sql/`).
- Module-level content may be under `source/<module>/` with optional nested sections for deeper content.
- Scripts belong under `source/<module>/scripts` and shared behaviors live in `source/scripts/app.js`.
- Styles belong under `source/<module>/styles` and shared theming lives in `source/styles/styles.css`.
- Non-module top-level assets can be placed under `/assets/`.

```
/index.html
/README.md
/requirements.txt
/.github/agents/Data-Guide-Agent.agent.md
/assets/
/source/
  ├─ big-data/
  │   ├─ big-data-index.html
  │   ├─ big-data-formats.html
  │   ├─ big-data-pipelines.html
  │   ├─ big-data-quality.html
  │   ├─ big-data-types.html
  │   ├─ scripts/
  │   └─ styles/
  ├─ cheatsheets/
  │   ├─ cheatsheet-index.html
  │   ├─ cheatsheet-python.html
  │   ├─ cheatsheet-numpy.html
  │   ├─ cheatsheet-pandas.html
  │   ├─ cheatsheet-postgresql.html
  │   ├─ cheatsheet-spark.html
  │   ├─ scripts/cheatsheets.js
  │   └─ styles/cheatsheets.css
  ├─ cloud/
  │   ├─ cloud-index.html
  │   ├─ cloud-architecture.html
  │   ├─ topics/topics.html
  │   ├─ providers/providers-azure.html
  │   ├─ providers/providers-gcp.html
  │   ├─ providers/providers-aws.html
  │   ├─ providers/aws/aws-index.html
  │   ├─ providers/aws/services/services.html
  │   ├─ scripts/mobile.js
  │   ├─ scripts/desktop.js
  │   ├─ styles/mobile.css
  │   └─ styles/desktop.css
  ├─ libraries/
  │   ├─ numpy/
  │   ├─ pandas/
  │   └─ spark/
  ├─ portfolios/
  │   ├─ portfolio-overview.html
  │   ├─ projects/projects-self.html
  │   ├─ projects/projects-experienced.html
  ├─ python/
  │   ├─ python-hub.html
  │   ├─ python-methods.html
  │   ├─ python-oops.html
  │   ├─ scripts/python.js
  │   └─ styles/python.css
  ├─ roadmaps/
  │   ├─ roadmap-ai-engineer.html
  │   ├─ roadmap-ml-engineer.html
  │   ├─ roadmap-python.html
  │   ├─ roadmap-sql.html
  ├─ sql/
  │   ├─ sql-hub.html
  │   ├─ sql-concepts.html
  │   ├─ sql-queries.html
  │   ├─ sql-methods.html
  ├─ scripts/app.js
  └─ styles/styles.css
```
  │   ├── cloud-index.html           (Cloud Hub - Dashboard)
  │   ├── /topics/                   (Topic areas)
  │   │   ├── topics.html            (All cloud topics overview)
  │   │   ├── topics-basics.html     (IaaS, PaaS, SaaS, deployment models)
  │   │   ├── topics-services.html   (Service comparison)
  │   │   ├── topics-storage.html    (Storage services)
  │   │   ├── topics-compute.html    (Compute services)
  │   │   └── topics-serverless.html (Serverless services)
  │   ├── /providers/                (Cloud provider details)
  │   │   ├── providers.html         (Providers overview)
  │   │   ├── providers-azure.html   (Microsoft Azure)
  │   │   ├── providers-gcp.html     (Google Cloud)
  │   │   └── providers-aws.html     (AWS redirect)
  │   ├── architecture.html          (9-Layer model)
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   ├── /styles/
  │   │   ├── mobile.css
  │   │   └── desktop.css
  │   └── /aws/                      (AWS Deep Dive)
  │       ├── aws-index.html
  │       ├── /services/
  │       │   ├── services.html
  │       │   ├── services-compute.html
  │       │   └── services-database.html
  │       ├── /domains/
  │       │   ├── bigdata.html
  │       │   ├── databases.html
  │       │   ├── serverless.html
  │       │   ├── storage.html
  │       │   ├── pipelines.html
  │       │   ├── warehouse.html
  │       │   ├── streaming.html
  │       │   └── interview.html
  │       ├── /scripts/
  │       │   ├── mobile.js
  │       │   └── desktop.js
  │       ├── /styles/
  │       │   ├── mobile.css
  │       │   └── desktop.css
  │       ├── aws.css
  │       └── aws.js
  │
  ├── /python/                       (Python Guide Hub)
  │   ├── python-index.html
  │   ├── /fundamentals/
  │   │   ├── fundamentals.html
  │   │   ├── fundamentals-basics.html
  │   │   └── fundamentals-syntax.html
  │   ├── /oops/
  │   │   ├── oops.html
  │   │   ├── oops-classes.html
  │   │   └── oops-inheritance.html
  │   ├── /reference/
  │   │   ├── methods.html
  │   │   └── memory-performance.html
  │   ├── /practice/
  │   │   └── practice.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   ├── /styles/
  │   │   ├── mobile.css
  │   │   └── desktop.css
  │   ├── python.css
  │   └── python.js
  │
  ├── /spark/                        (Spark Guide Hub)
  │   ├── spark-index.html
  │   ├── /concepts/
  │   │   ├── theory.html
  │   │   ├── theory-architecture.html
  │   │   └── theory-optimization.html
  │   ├── /practice/
  │   │   ├── code.html
  │   │   └── code-dataframes.html
  │   ├── /reference/
  │   │   └── architecture.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   ├── /styles/
  │   │   ├── mobile.css
  │   │   └── desktop.css
  │   ├── spark.css
  │   └── spark.js
  │
  ├── /sql/                          (SQL Guide Hub)
  │   ├── sql-index.html
  │   ├── /concepts/
  │   │   ├── concepts.html
  │   │   └── concepts-datatypes.html
  │   ├── /modelling/
  │   │   ├── modelling.html
  │   │   └── modelling-er.html
  │   ├── /queries/
  │   │   ├── queries.html
  │   │   ├── queries-select.html
  │   │   ├── queries-joins.html
  │   │   ├── queries-subqueries.html
  │   │   └── queries-windows.html
  │   ├── /reference/
  │   │   └── methods.html
  │   ├── /practice/
  │   │   └── practice.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   ├── /styles/
  │   │   ├── mobile.css
  │   │   └── desktop.css
  │   └── sql_queries.sql
  │
  ├── /data/                         (Data Guide Hub)
  │   ├── data-index.html
  │   ├── /formats/
  │   │   ├── formats.html
  │   │   ├── formats-json.html
  │   │   └── formats-parquet.html
  │   ├── /types/
  │   │   ├── types.html
  │   │   └── types-structured.html
  │   ├── /quality/
  │   │   ├── quality.html
  │   │   └── quality-validation.html
  │   ├── /pipelines/
  │   │   ├── pipelines.html
  │   │   └── pipelines-etl.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   └── /styles/
  │       ├── mobile.css
  │       └── desktop.css
  │
  ├── /numpy/                        (NumPy Guide Hub)
  │   ├── numpy-index.html
  │   ├── /concepts/
  │   │   ├── basics.html
  │   │   └── basics-arrays.html
  │   ├── /operations/
  │   │   ├── arrays.html
  │   │   └── arrays-indexing.html
  │   ├── /reference/
  │   │   ├── methods.html
  │   │   └── operations.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   └── /styles/
  │       ├── mobile.css
  │       └── desktop.css
  │
  ├── /pandas/                       (Pandas Guide Hub)
  │   ├── pandas-index.html
  │   ├── /concepts/
  │   │   ├── basics.html
  │   │   └── basics-series.html
  │   ├── /series/
  │   │   ├── series.html
  │   │   └── series-creation.html
  │   ├── /dataframes/
  │   │   ├── dataframes.html
  │   │   └── dataframes-creation.html
  │   ├── /reference/
  │   │   └── methods.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   └── /styles/
  │       ├── mobile.css
  │       └── desktop.css
  │
  ├── /roadmaps/                     (Career Roadmaps Hub)
  │   ├── roadmaps-index.html
  │   ├── /python/
  │   │   └── roadmap-python.html
  │   ├── /sql/
  │   │   └── roadmap-sql.html
  │   ├── /spark/
  │   │   └── roadmap-spark.html
  │   ├── /ml/
  │   │   └── roadmap-ml-engineer.html
  │   ├── /ai/
  │   │   └── roadmap-ai-engineer.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   ├── /styles/
  │   │   ├── mobile.css
  │   │   ├── desktop.css
  │   │   └── roadmap.css
  │   └── roadmap.css
  │
  ├── /cheatsheets/                  (Quick Reference Hub)
  │   ├── cheatsheets-index.html
  │   ├── /compare/
  │   │   └── compare.html
  │   ├── /python/
  │   │   └── cheatsheet-python.html
  │   ├── /numpy/
  │   │   └── cheatsheet-numpy.html
  │   ├── /pandas/
  │   │   └── cheatsheet-pandas.html
  │   ├── /spark/
  │   │   └── cheatsheet-spark.html
  │   ├── /sql/
  │   │   └── cheatsheet-postgresql.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   ├── /styles/
  │   │   ├── mobile.css
  │   │   ├── desktop.css
  │   │   ├── cheatsheet-base.css
  │   │   └── cheatsheets.css
  │   ├── cheatsheets.js
  │   └── comparison-data.json
  │
  ├── /portfolios/                   (Portfolio Hub)
  │   ├── portfolio-index.html
  │   ├── /projects/
  │   │   ├── projects.html
  │   │   ├── projects-self.html
  │   │   └── projects-experienced.html
  │   ├── /scripts/
  │   │   ├── mobile.js
  │   │   └── desktop.js
  │   ├── /styles/
  │   │   ├── mobile.css
  │   │   └── desktop.css
  │   └── portfolio.html
  │
  └── /styles/                       (Legacy split styles - not actively used)
      ├── base.css
      ├── mobile.css
      └── desktop.css
```

**Naming Conventions** (follow for ALL new file creation):
- Hub pages: `{module}-index.html` (e.g., `cloud-index.html`, `python-index.html`)
- Content pages: `{section}-{topic}.html` (e.g., `topics-basics.html`, `fundamentals-syntax.html`)
- Section overviews: `{section}.html` (e.g., `topics.html`, `fundamentals.html`, `providers.html`)
- Scripts: exclusively in `/scripts/` folder → `mobile.js`, `desktop.js`
- Styles: exclusively in `/styles/` folder → `mobile.css`, `desktop.css`
- Submodules: follow same pattern (e.g., `aws-index.html` in aws subfolder)



When creating new files, follow the standardized folder-based convention established by the cloud module:
- Hub pages: name as `{module}-index.html` (e.g., `python-index.html`, `sql-index.html`)
- Content pages in subfolders: `{section}/{section}-{topic}.html` (e.g., `topics/topics-basics.html`, `fundamentals/fundamentals-syntax.html`)
- Section index pages: `{section}/{section}.html` (e.g., `topics/topics.html`, `fundamentals/fundamentals.html`)
- All scripts: must go in `/scripts/` subfolder → only `mobile.js` and `desktop.js`
- All styles: must go in `/styles/` subfolder → only `module-mobile.css` and `module-desktop.css`
- Submodules (e.g., aws under cloud): follow same pattern with own index as `{submodule}-index.html`

Behavior:
- Apply updates in the same folder structure, preserving project organization.
- Verify topbar heading hierarchy: `.brand` should be first-level heading semantics for accessibility (`<h1>` when on homepage, `<h2>` on internal pages).
- Ensure menu links are inside nav landmarks and avoid duplicate heading levels inside topbar.
- Use small patches; keep change scope page/module local unless global bug.
- Always validate with `get_errors` after changes.

Slash Commands:
- When user prompts with `/low` → Treat as mobile supporting layouts modification (focus on responsive design, touch-friendly UI, smaller screens ≤ 768px)
- When user prompts with `/high` → Treat as laptop/desktop supporting layouts modification (focus on larger screens, desktop UI patterns ≥ 1024px)
- When user prompts with `/agent` followed by instructions → Update the agent configuration file (`.opencode/agent/Data-Guide-Agent.agent.md`) with the provided instructions. Extract the instructions after `/agent` and modify the agent file accordingly.
- If no prefix is specified, treat as general UI/UX issue applicable to both

Argument hint: "Describe the UI/UX issue to fix or the module to update."