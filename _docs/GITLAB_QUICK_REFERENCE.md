# GitLab Requirements Management - Quick Reference Card

## 🦊 GitLab Requirements Cheat Sheet for Siemens

---

## Essential Commands & Workflows

### Creating Requirements (Ultimate Tier)

```bash
# Navigate in UI
Project → Plan → Requirements → New requirement

# Required Fields
Title: Short descriptive name
Description: Full requirement details (Markdown supported)
```

### Using Issues as Requirements (All Tiers)

```bash
# Create issue with template
Project → Issues → New issue → Select requirement template

# Apply labels
~req::functional ~priority::high ~status::open
```

---

## GitLab CI/CD Requirements Validation

### Basic Configuration

```yaml
# .gitlab-ci.yml
requirements_check:
  stage: test
  rules:
    - if: '$CI_HAS_OPEN_REQUIREMENTS == "true"'
      when: manual
  script:
    - mkdir tmp
    - echo '{"*":"passed"}' > tmp/requirements.json
  artifacts:
    reports:
      requirements: tmp/requirements.json
```

### Advanced Configuration (Specific Requirements)

```yaml
# Mark specific requirements
requirements_check:
  stage: test
  script:
    - mkdir tmp
    - |
      cat > tmp/requirements.json << EOF
      {
        "1": "passed",
        "2": "passed",
        "3": "failed",
        "4": "passed"
      }
      EOF
  artifacts:
    reports:
      requirements: tmp/requirements.json
```

### Dynamic Requirement Validation

```yaml
requirements_validation:
  stage: test
  script:
    - |
      # Run your tests
      pytest tests/ --junitxml=report.xml
      
      # Parse results and generate requirements.json
      python scripts/generate_requirements_report.py
  artifacts:
    reports:
      requirements: tmp/requirements.json
      junit: report.xml
```

---

## CSV Import/Export

### CSV Import Format

```csv
title,description
"User Authentication","System shall support OAuth 2.0 and SAML authentication"
"Data Encryption","All data at rest must be encrypted using AES-256"
"API Rate Limiting","API must support configurable rate limiting per endpoint"
```

### CSV Export Fields

Exported CSV includes:
- Requirement ID
- Title
- Description
- Author
- Author Username
- Created At (UTC)
- State
- State Updated At (UTC)

---

## GitLab API for Requirements

### List Requirements

```bash
curl --header "PRIVATE-TOKEN: <your_token>" \
  "https://gitlab.example.com/api/v4/projects/:id/requirements"
```

### Create Requirement

```bash
curl --request POST \
  --header "PRIVATE-TOKEN: <your_token>" \
  --header "Content-Type: application/json" \
  --data '{
    "title": "New Requirement",
    "description": "Requirement description"
  }' \
  "https://gitlab.example.com/api/v4/projects/:id/requirements"
```

### Update Requirement Status

```bash
curl --request PUT \
  --header "PRIVATE-TOKEN: <your_token>" \
  --header "Content-Type: application/json" \
  --data '{
    "state": "satisfied"
  }' \
  "https://gitlab.example.com/api/v4/projects/:id/requirements/:requirement_iid"
```

---

## Labels for Requirement Management

### Recommended Scoped Labels

```yaml
Requirement Type:
  ~req::functional
  ~req::non-functional
  ~req::security
  ~req::performance
  ~req::compliance
  ~req::usability

Status:
  ~status::draft
  ~status::open
  ~status::in-progress
  ~status::satisfied
  ~status::failed
  ~status::archived

Priority:
  ~priority::critical
  ~priority::high
  ~priority::medium
  ~priority::low

Category:
  ~category::authentication
  ~category::data-management
  ~category::reporting
  ~category::integration
  ~category::ui-ux

Compliance:
  ~compliance::gdpr
  ~compliance::iso27001
  ~compliance::sox
  ~compliance::hipaa
```

### Creating Scoped Labels

```bash
# Navigate to
Project → Settings → Labels → New label

# Format: scope::value
Name: req::functional
Description: Functional requirement
Color: #1068bf
```

---

## Requirement Linking Best Practices

### Link to Epic

```markdown
## Related Epic
Relates to #epic-123

## Parent
Part of #123
```

### Link to Issues

```markdown
## Implementation
- Closes #456
- Related to #457, #458

## Dependencies
- Blocks #459
- Blocked by #460
```

### Link to Merge Requests

```markdown
## Code Changes
- Implemented in !234
- !235 (WIP)

## Testing
- Test coverage in !236
```

---

## Board Views for Requirements

### Creating Requirement Board

```bash
# Navigate to
Project → Issues → Boards → New board

# Configure lists by:
1. Status labels (~status::*)
2. Priority labels (~priority::*)
3. Type labels (~req::*)
4. Milestones
```

### Board Automation

```bash
# Add board list automation
Settings → Automation
- Move to "In Progress" when assigned
- Move to "Satisfied" when issue closed
```

---

## Quick Actions (Slash Commands)

```markdown
# In issue/requirement description or comment

/assign @username           # Assign to user
/label ~req::functional     # Add label
/unlabel ~status::draft     # Remove label
/milestone %v1.0           # Set milestone
/due 2025-12-31            # Set due date
/estimate 3d               # Set time estimate
/relate #123               # Link to another issue
/epic &456                 # Link to epic
/close                     # Close issue
/reopen                    # Reopen issue
/weight 5                  # Set weight/complexity
```

---

## Search & Filter Syntax

### Basic Search

```bash
# In Issues search box
req::functional status::open

# Advanced filters
label:~req::functional
milestone:%Q4-2025
author:@pavleen
assignee:@john
```

### Advanced Query Language

```bash
# Issue search
label = ~req::functional AND
label = ~priority::high AND
milestone = %Q4-2025

# Quick filters in URL
?label_name[]=req::functional&state=opened
```

---

## Automation Scripts

### Bulk Requirement Creation

```python
import requests

GITLAB_URL = "https://gitlab.example.com"
PROJECT_ID = "123"
PRIVATE_TOKEN = "your_token"

requirements = [
    {"title": "REQ-001", "description": "User authentication"},
    {"title": "REQ-002", "description": "Data encryption"},
    {"title": "REQ-003", "description": "API rate limiting"},
]

for req in requirements:
    response = requests.post(
        f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/requirements",
        headers={"PRIVATE-TOKEN": PRIVATE_TOKEN},
        json=req
    )
    print(f"Created: {req['title']}")
```

### Export Requirements to JSON

```python
import requests
import json

response = requests.get(
    f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/requirements",
    headers={"PRIVATE-TOKEN": PRIVATE_TOKEN}
)

with open('requirements_export.json', 'w') as f:
    json.dump(response.json(), f, indent=2)
```

---

## Notifications Configuration

### Email Notifications

```bash
# Navigate to
User Settings → Notifications → Project overrides

# Configure for requirements:
- New issue created
- Issue status changed
- Mentioned in issue
- Assigned to issue
```

### Webhook for Requirements

```bash
# Project Settings → Webhooks
URL: https://your-webhook-endpoint.com/gitlab
Trigger: Issues events
SSL verification: Enable
```

---

## Reporting & Metrics

### Issue Board Insights

```bash
# Navigate to
Project → Issues → Boards → Select board → Show insights

# Metrics available:
- Requirements by status
- Requirements by priority
- Requirements by milestone
- Burndown charts
```

### Custom Dashboards

```bash
# Using GitLab API + BI Tool
1. Export data via API
2. Connect to Power BI / Tableau
3. Create custom visualizations
```

---

## Integration with External Tools

### Jira Integration

```bash
# Project Settings → Integrations → Jira
- Map GitLab requirements to Jira issues
- Sync status updates
- Bi-directional linking
```

### Slack Integration

```bash
# Project Settings → Integrations → Slack notifications
# Notify channel on:
- New requirements
- Status changes
- Comments on requirements
```

---

## Troubleshooting

### Common Issues

**Problem:** Requirements feature not visible
**Solution:** Verify GitLab Ultimate license is active

**Problem:** CI job not updating requirement status
**Solution:** Check `requirements.json` format and artifact path

**Problem:** CSV import fails
**Solution:** Verify CSV format matches: title,description headers

**Problem:** Requirements not linking to issues
**Solution:** Use correct syntax: #issue-number in description

---

## GitLab Version Compatibility

| Feature | Minimum GitLab Version |
|---------|----------------------|
| Requirements | 12.10 (Ultimate) |
| Work Items | 15.0 |
| requirements.json | 13.0 |
| CSV Import/Export | 12.10 |
| API Support | 13.2 |

---

## Pro Tips

1. **Use Description Templates**: Create `.gitlab/issue_templates/requirement.md`
2. **Automate Everything**: Leverage CI/CD for requirement validation
3. **Use Milestones**: Group requirements by release/sprint
4. **Enable Time Tracking**: Use `/estimate` and `/spend` for effort tracking
5. **Create Roadmaps**: Use epics + milestones for strategic planning
6. **Regular Exports**: Backup requirements via API regularly
7. **Use Boards**: Visualize requirement status with custom boards
8. **Link Liberally**: Connect requirements to all related work items

---

## Need More Help?

- 📚 [GitLab Requirements Docs](https://docs.gitlab.com/user/project/requirements/)
- 💬 [GitLab Forum](https://forum.gitlab.com/)
- 🎓 [GitLab University](https://university.gitlab.com/)
- 📧 Support: support@gitlab.com

---

**Print this page and keep it handy!**

---

**© 2025 Microsoft Global Delivery - Requirements Management Framework**

**Version:** 1.0  
**Last Updated:** November 11, 2025
