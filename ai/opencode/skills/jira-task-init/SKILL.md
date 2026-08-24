---
name: jira-task-init
description: Generate comprehensive initial overview comment for Jira tasks
metadata:
  audience: project-managers
  workflow: jira
---

## What I do
- Validate Jira task ID format and existence
- Gather comprehensive data from Jira MCP and codebase analysis
- Perform comprehensive technical assessment including codebase complexity, implementation approaches, and dependency analysis
- Generate comprehensive overview comment with 5 structured fields covering task complexity, dependencies, risks, and impact
- Apply enhanced validation rules for content quality
- Preview formatted comment and require user confirmation
- Post analysis as Jira comment when approved

## When to use me
Use this for initial assessment and planning on newly assigned Jira tasks. It generates a comprehensive overview comment covering task complexity, dependencies, risks, and impact to establish a solid foundation before work begins.

---

## Validation Schema

```yaml
validation_schema:
  required_fields: [Risk_Impact_Analysis, Dependencies, Potentially_Impacted_Areas, Known_Risks, Unknowns_Assumptions]
  format_requirements:
    format_pattern: "Field: Content"
    no_markdown: true
  field_validations:
    Risk_Impact_Analysis:
      required: true
      min_length: 50
      validation_rules:
        - Must contain both technical and business considerations
        - Technical keywords: performance, security, integration, compatibility
        - Business keywords: timeline, budget, user impact, business risk
        - Validation: Check for presence of both technical and business keywords
    Dependencies:
      required: true
      min_length: 30
      validation_rules:
        - Must include actionable dependency information
        - Internal dependencies: JIRA tickets, blocked tasks
        - External dependencies: APIs, third-party services
        - Resource dependencies: team availability, environment setup
    Potentially_Impacted_Areas:
      required: true
      min_length: 30
      validation_rules:
        - Must identify specific systems or user flows
        - Service impact: backend services, databases, APIs
        - User impact: frontend components, user workflows, performance
    Known_Risks:
      required: true
      min_length: 30
      validation_rules:
        - Must identify specific, assessable risks
        - Technical risks: performance, security, integration
        - Project risks: timeline, resource availability
        - Each risk should have potential impact level
    Unknowns_Assumptions:
      required: true
      min_length: 20
      validation_rules:
        - Must clearly state unknowns or working assumptions
        - Technical unknowns: performance characteristics, data volume
        - Business unknowns: user behavior, regulatory requirements
        - Scope assumptions: clear boundaries and exclusions
```

---

## Process Flow

1. **Initial Validation**: Checks if Jira task ID follows correct format (PROJECT-123)
2. **Ticket Existence Verification**: Uses `jira_get_issue` to confirm ticket exists and is accessible
3. **Data Gathering**:
    - JIRA MCP server for ticket details, context, and related tickets
    - Perform comprehensive technical assessment including codebase complexity, implementation approaches, and dependency analysis
    - Analyze GitHub CLI for related PRs, review status, and code activity
    - Review Git commands for current branch status, recent commits, and changes analysis
4. **Content Analysis**: Generates content for each of the five overview fields enhanced with technical insights
5. **Format Generation**: Creates overview comment following Output Format specification
6. **Enhanced Validation**: Applies enhanced validation rules for content quality and compliance
7. **Preview**: Shows formatted output ready for Jira
8. **User Confirmation**: Requires explicit approval
9. **Posting**: Uses `jira_add_comment` to add comment if confirmed

---

## Jira MCP Integration

### Core Commands Used

#### **jira_get_issue**
- **Description**: Retrieves detailed information about a specific Jira issue
- **Usage**: `jira_get_issue(issueKey="PROJ-123")`
- **Purpose**: Get full ticket details including description, assignee, status, comments, and attachments. Used in step 2 of the skill's process to verify ticket existence and gather initial data.

#### **jira_search_issues**
- **Description**: Searches for Jira issues using JQL (Jira Query Language)
- **Usage**: `jira_search_issues(jql="project = PROJ AND status = Open", maxResults=50)`
- **Purpose**: Find and filter issues by project, status, assignee, etc. Used in the data gathering phase to identify related tickets, blockers, or dependencies.

#### **jira_add_comment**
- **Description**: Adds a comment to a Jira issue
- **Usage**: `jira_add_comment(issueKey="PROJ-123", comment="Analysis complete", format="plain")`
- **Purpose**: Add notes, updates, or analysis to tickets. Used in step 9 of the skill to post the generated overview comment after user confirmation.

---

## Enhanced Validation Rules

### **Technical and Business Keyword Validation:**
- ✅ Risk & Impact Analysis must contain both technical AND business keywords
- ✅ Technical keywords: performance, security, integration, compatibility, scalability, database, API
- ✅ Business keywords: timeline, budget, user impact, business risk, ROI, stakeholders, requirements
- ❌ Validation fails if only one type of keyword is present

### **Cross-field Validation:**
- ✅ Dependencies should align with Potentially Impacted Areas
- ✅ Known Risks should be reflected in Risk & Impact Analysis
- ✅ Unknowns/Assumptions should relate to dependencies and risks
- ❌ Validation fails if fields conflict or are inconsistent

### **Content Quality Validation:**
- ✅ Risk assessments should include specific impact levels (high/medium/low)
- ✅ Dependencies should include actionable contact information or next steps
- ✅ Impacted areas should specify systems, users, or business processes
- ✅ Known risks should include probability and potential mitigation strategies
- ❌ Validation fails if content is too generic or lacks specificity

### **Risk Assessment Validation:**
- ✅ Must include both technical and business risk perspectives
- ✅ Should consider short-term and long-term impacts
- ✅ Include dependency risks and external factors
- ✅ Consider resource availability and timeline implications
- ❌ Validation fails if risk assessment is incomplete or one-sided

---

## Output Format

The generated overview comment follows this exact format:

The generated overview comment must follow this exact format:

```
Risk & Impact Analysis: `[Comprehensive risk and impact analysis text]`
Dependencies: `[List of dependencies with details]`
Potentially Impacted Areas: `[Areas potentially affected by this work]`
Known Risks: `[Identified risks with assessments]`
Unknowns / Assumptions: `[Unknowns and assumptions being made]`
```

### **Key Requirements:**
- Each line follows the exact pattern: `Field: Content`
- Content should be comprehensive but concise
- No additional markdown formatting or bullet points
- All five fields must be present

### **Field-Specific Requirements:**

**Risk & Impact Analysis:**
- Minimum 50 characters
- Comprehensive overview of risks and impacts
- Business and technical considerations
- Clear assessment of overall project impact

**Dependencies:**
- Minimum 30 characters
- Covers technical, resource, and external dependencies
- Specific and actionable information with technical implementation details
- Includes JIRA tickets, PRs, external systems, and code contracts

**Potentially Impacted Areas:**
- Minimum 30 characters
- Identifies affected systems/services and specific code modules
- Includes user-facing impacts where relevant
- Mentions performance or scalability implications with technical basis

**Known Risks:**
- Minimum 30 characters
- Identifies specific risks with potential impact and technical basis
- Covers technical complexity risks and implementation challenges
- Includes probability/impact where possible with code analysis backing

**Unknowns / Assumptions:**
- Minimum 20 characters
- Clearly states unknowns or assumptions
- Relevant to the work being performed
- Identifies scope boundaries

---

## Validation Rules

### **Format Validation:**
- ✅ Field name exactly as specified
- ✅ Colon followed by space
- ✅ No additional formatting or bullet points
- ❌ Validation fails if format deviates

### **Content Validation:**
- ✅ All fields meet minimum character requirements
- ✅ Content is relevant and specific
- ✅ Technical details are accurate
- ✅ Dependencies are actionable
- ❌ Validation fails if content is too brief or irrelevant

---

## Error Handling

If any data source is unavailable:
- Note the missing data source clearly
- Proceed with available information
- Indicate which sections may have incomplete information
- Suggest manual verification steps

If JIRA task ID format is invalid:
- Provide clear error message with correct format example (PROJECT-123)
- Suggest verifying task ID before proceeding

If ticket existence verification fails:
- Clearly indicate ticket not found or access denied
- Suggest verifying ticket ID and permissions
- Provide option to proceed with manual input if appropriate

If content generation fails:
- Provide templates for each field type
- Offer manual input options
- Include guidance on meeting content requirements

### **Enhanced Validation Error Handling:**

**Keyword Validation Errors:**
- Missing business keywords: Suggest adding timeline, budget, user impact, or business risk
- Missing technical keywords: Recommend adding performance, security, integration, or compatibility
- Provide comprehensive keyword lists for both categories

**Cross-field Validation Errors:**
- Dependencies vs Impact areas misaligned: Suggest reviewing dependency scope
- Risks not reflected in analysis: Recommend updating Risk & Impact Analysis
- Inconsistent assumptions: Request clarification on scope boundaries

**Content Quality Errors:**
- Vague risk assessments: Provide templates with specific impact level examples
- Generic dependencies: Suggest including specific contact information or next steps
- Unclear impacted areas: Request specific systems, users, or business processes
- Incomplete risk analysis: Recommend adding probability and mitigation strategies

**Risk Assessment Errors:**
- One-sided perspective: Suggest adding missing technical or business view
- Missing timeframe: Recommend including short-term and long-term impacts
- Incomplete consideration: Request dependency risks and external factors
- Resource implications missing: Suggest adding timeline and resource considerations
