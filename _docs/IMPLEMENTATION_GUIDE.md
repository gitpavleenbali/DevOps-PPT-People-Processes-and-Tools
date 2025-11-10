# Platform Integration Quick Start Guide

## 🎯 Overview

This guide helps you choose and implement the right platform for your requirements management needs based on your organization's current tooling and preferences.

---

## 🔷 For Siemens (Currently Using GitLab)

### ✅ Recommended Approach: GitLab-Native Requirements Management

Since Siemens is already using GitLab, we recommend leveraging GitLab's native capabilities to minimize tool sprawl and maximize integration.

### Quick Start Steps

#### 1. Verify Your GitLab Tier
```bash
# Check your GitLab tier
# Requirements feature requires GitLab Ultimate
# Free/Premium tiers can use Work Items and Issues
```

#### 2. Enable Requirements (Ultimate Tier)
- Navigate to: **Plan > Requirements**
- Click **New requirement**
- Start creating your first requirement

#### 3. Setup Work Items (All Tiers)
- Use Issues as requirements containers
- Apply labels for categorization
- Link to Epics for hierarchy
- Use milestones for releases

#### 4. Configure CI/CD Integration

Add this to your `.gitlab-ci.yml`:

```yaml
requirements_validation:
  stage: test
  rules:
    - if: '$CI_HAS_OPEN_REQUIREMENTS == "true"'
      when: manual
    - when: never
  allow_failure: false
  script:
    - mkdir -p tmp
    - echo '{"*":"passed"}' > tmp/requirements.json
  artifacts:
    reports:
      requirements: tmp/requirements.json
```

#### 5. Import Existing Requirements

Create a CSV file with format:
```csv
title,description
"User Authentication","System must support OAuth 2.0 authentication"
"Data Export","Users can export data to CSV and Excel formats"
```

Import via: **Plan > Requirements > Import CSV**

---

## 📊 Comparison at a Glance

### When to Use GitLab

✅ **Use GitLab If:**
- Already using GitLab for source control
- Want single platform for entire DevOps lifecycle
- Need tight CI/CD integration with requirements
- Prefer open-source options
- Want cost-effective solution
- Team is developer-centric

### When to Consider Azure DevOps

✅ **Use Azure DevOps If:**
- Heavy Microsoft ecosystem investment
- Need extensive work item customization
- Require Power BI integration
- Want mature process templates (CMMI, Agile, Scrum)
- Need complex reporting capabilities
- Enterprise-wide governance requirements

---

## 🚀 GitLab Implementation Roadmap (Recommended for Siemens)

### Week 1: Foundation
- [ ] Audit current GitLab tier and capabilities
- [ ] Create requirements management pilot project
- [ ] Define labeling taxonomy
- [ ] Setup requirement templates
- [ ] Train core team on GitLab requirements

### Week 2: Configuration
- [ ] Import existing requirements from CSV
- [ ] Link requirements to epics and issues
- [ ] Configure CI/CD pipeline for validation
- [ ] Setup requirement boards and views
- [ ] Create custom queries and filters

### Week 3: Integration
- [ ] Link requirements to merge requests
- [ ] Configure automated requirement satisfaction
- [ ] Setup notification rules
- [ ] Create dashboards and reports
- [ ] Document processes and workflows

### Week 4: Rollout
- [ ] Pilot with one project team
- [ ] Gather feedback and iterate
- [ ] Refine processes based on learnings
- [ ] Plan organization-wide rollout
- [ ] Create training materials

---

## 📋 Requirement Template Examples

### GitLab Requirement Template

**Title:** [REQ-ID] Brief Description

**Description:**
```markdown
## Business Context
Why this requirement exists and its business value

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Test Scenarios
1. Scenario 1: Description
2. Scenario 2: Description

## Dependencies
- Linked to: [Epic/Issue]
- Blocked by: [Issue]

## Compliance/Standards
- Standard: [e.g., ISO 27001, GDPR]
- Reference: [Link to compliance doc]
```

### GitLab Issue as Requirement Template

```markdown
## User Story
As a [user type], I want to [action] so that [benefit]

## Acceptance Criteria
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

## Technical Requirements
- Performance: [metrics]
- Security: [requirements]
- Accessibility: [standards]

## Definition of Done
- [ ] Code reviewed
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Requirement marked as satisfied
```

---

## 🔄 Migration Strategy (If Moving from Another Tool)

### Export from Legacy System
1. Export requirements to CSV/Excel
2. Map fields to GitLab structure
3. Clean and validate data

### Transform Data
```csv
# GitLab Requirements CSV Format
title,description
"Requirement Title 1","Full description with acceptance criteria"
"Requirement Title 2","Full description with acceptance criteria"
```

### Import to GitLab
1. Navigate to Plan > Requirements
2. Click Import CSV
3. Select your prepared file
4. Verify imported data
5. Link to existing work items

---

## 🎓 Training Resources

### For GitLab
- [GitLab Requirements Documentation](https://docs.gitlab.com/user/project/requirements/)
- [GitLab Work Items Guide](https://docs.gitlab.com/development/work_items/)
- [GitLab CI/CD Integration](https://docs.gitlab.com/ci/yaml/artifacts_reports/#artifactsreportsrequirements)
- [GitLab University](https://university.gitlab.com/)

### For Azure DevOps (Alternative)
- [Azure DevOps Work Items](https://docs.microsoft.com/azure/devops/boards/work-items/)
- [Azure Boards Documentation](https://docs.microsoft.com/azure/devops/boards/)
- [Azure DevOps Learning Paths](https://docs.microsoft.com/learn/azure-devops/)

---

## 💡 Best Practices for Siemens

### 1. **Leverage GitLab's Single Platform**
- Keep everything in GitLab: code, requirements, CI/CD, security
- Use native integrations rather than external tools
- Reduce tool sprawl and context switching

### 2. **Automate Requirement Validation**
- Use CI/CD pipelines to validate requirements
- Generate `requirements.json` automatically
- Link test results to requirements

### 3. **Establish Clear Hierarchy**
```
Epic (Strategic Initiative)
  └── Requirement (What needs to be delivered)
      └── Issue (How it will be implemented)
          └── Merge Request (The actual code)
              └── Test Case (Validation)
```

### 4. **Use Scoped Labels**
```
req::functional
req::non-functional
req::security
req::performance
req::compliance
status::open
status::satisfied
status::failed
priority::critical
priority::high
priority::medium
priority::low
```

### 5. **Implement Traceability**
- Link every requirement to at least one epic
- Link every MR to related requirements
- Use issue boards to visualize status
- Create milestone-based roadmaps

---

## 📞 Support & Next Steps

### Immediate Actions
1. ✅ Review the main README.md for comprehensive framework
2. ✅ Choose your platform (GitLab recommended)
3. ✅ Follow the implementation roadmap above
4. ✅ Schedule training sessions for the team
5. ✅ Start pilot with one project

### Need Help?
- Contact your GitLab Customer Success Manager
- Engage GitLab Professional Services for customization
- Join GitLab community forums for peer support

---

**Next:** Return to [RequirementManagement.md](../Requirement%20Management/RequirementManagement.md) for the complete Requirements Management Framework

---

**© 2025 Microsoft Global Delivery - Requirements Management Framework**

**Version:** 1.0  
**Last Updated:** November 11, 2025
**Author:** Pavleen Bali
