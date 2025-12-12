# Testing Layers & Tooling Guide
## Complete Technical Reference: Layers, Tools, Pipelines

---

## Context: Where UTM Fits

> **Hierarchy**: URM (Requirements) → ADM (Architecture) → **UTM (Testing)**

| Phase | What | Tool |
|:------|:-----|:-----|
| **URM** | What to build (Requirements) | Jira Epics, Confluence |
| **ADM** | How to build (Architecture) | Confluence ADRs, Diagrams |
| **UTM** | How to verify (Testing) | GitLab CI, Test Suites |

**Each test traces back**: Test Case → Architecture Decision → Requirement

---

## Testing Pyramid Overview

<!-- PlantUML Diagram: UTM_02_Testing_diagram_01
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_01.puml
-->
![Utm 02 Testing Diagram 01](https://www.plantuml.com/plantuml/svg/TPJ1RjD048Rl-nH38o4GZN3Yf6roQk8u4CbDgyQfX0X2MtkShBhUZTRhf1RgaHCI1q3YWiGHYGlln1Fm28oJ5a9IlBVPV-V_PdRMnvdbnkQfP0_i35E424qkaIkMNGarvuQdSCcZgwdHkOezBRM1IjylruOYc_5OBuMQGi9bXXix1YFBrLGYl640VQtiNOxLnsusj14tyRQixhb-qw5OzpyGDunPOIb_Y9aj2SuAoYLYgC811Bn0ap7sbsBlrzVtFo1ejg7ZUVvPs1bwFZmQTyB7Uy0pse2AvxYjUdS5iYBQw-QPK9XbSC6bYBaLMatK2LSvb_04EhdLARSOJzHpCPqH1NXQ9I965U5jKg_4_0VYqsS86ctmwpuyXS4mz9-TTyB1wN1ze06LdjjiECu6HJ-N4aP5PZ652pGY4T4jIeZ6400PFuLp9AWUpgKk9efa1PHGEqIDNQAFxo1msz0V3xqIf1DGDk_qv2mOb3rQ7tEXqZriDPrxknFegOWcofOqYJPfDTBfN0fEffIgs-kj6xJ3ujxJdGyGrDimyhtn-I1yiTRLeLBpZngDreRvHIuL6duffB05rMqfowedqGoZAxqWOvjaI5Wd68iyhTvBKDyb-FOTWbeRniD1kDRKQ1QF3XkTWmrtZmhK2fNzKxjEShYzYLH7Lw_dHY_8oTpvxrZNjgr_VdaBWKErXpGFtbhaGEMmvtgjemtlKQ4iluQ7CBA5n8bQh6UpR7MIsbNTKYWxKO5UxhWwArSQzkhBcOXfunKzNrMbkM0qUzj1bz75RmVhZ2vaErXZrAVjeCEOqWHcgFKMT58-CfepNEw3Vpr7bOa5xiD8wkMspY4TlRDY7_e6ITFdcMNi65LS_h1-0m)


### Layer Comparison

| Layer | Type | Speed | Cost | Confidence | Run Frequency |
|:-----:|:-----|:-----:|:----:|:----------:|:--------------|
| **L0** | Static Analysis | ⚡⚡⚡⚡ | Free | Low | Every save |
| **L1** | Unit Tests | ⚡⚡⚡ | Free | Medium | Every commit |
| **L2** | Security Scans | ⚡⚡⚡ | Free | Medium-High | Pre-merge |
| **L3** | Functional Tests | ⚡⚡ | Low | High | CI Pipeline |
| **L4** | E2E / Integration | ⚡ | High | Very High | Release |
| **L5** | Acceptance (UAT) | ⚡ | Medium | Highest | Pre-Production |

### IaC Coverage Reality

> **⚠️ Important**: OpenTofu/Terraform is **declarative** (describes "what", not "how"). Unlike Java/Python, **line-based code coverage doesn't exist** for IaC.
>
> **What we measure instead:**
> | Coverage Type | How to Calculate | Tool |
> |:--------------|:-----------------|:-----|
> | **Resource Coverage** | Resources with assertions ÷ Total resources | `tofu test` assertion count |
> | **Scenario Coverage** | BDD scenarios tested ÷ Total scenarios | `terraform-compliance` |
> | **Module Coverage** | Modules with `.tftest.hcl` ÷ Total modules | Directory scan |
> | **Requirement Coverage** | Tests linked to requirements ÷ Total requirements | Jira traceability |

---

## 1. L0: Static Analysis

<!-- PlantUML Diagram: UTM_02_Testing_diagram_02
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_02.puml
-->
![Utm 02 Testing Diagram 02](https://www.plantuml.com/plantuml/svg/RPA_JiCm4CRtUuf3BErGYJaPw1-863fKL68toQMrujYHVIcjr9KD92GOgVfkF44V0Jk9r48h3_RvxlkT_Tb3ny9oNIguuYMLX2dPMf7Gu0gfAs55YSyYBHRMr3gR66KiNYVtOG2mP4KulObmpe9bYYCjrCP9XuaoBm3RErgHCXNPBJHz83hiFtSu5ol2H2gAVStCqY0rPIaP7umfjatD1xB9QynBZa4R9hHoiUG89qjA2yoDBGMpr0i0cMClQMFARlleRw6nz_FzYXjoVK2CmhgXhOIIcM3V5V4SwZQQnTgd0l4fb5wYUTvX__MEd2kfEMvsJbbZSeoL5QctWroJ3hofByQPSEuoiplbfBLXfBnxbCLToh6fcYKfHrwuU_CTZpeVZfNn5nXuIzSOZeLahR7k7A0pcSCbq1ccTQCbTFfM_L_xH_bOwvE7wvIj3eP-3l_i5m)


| Tool | Purpose | Example Finding |
|:-----|:--------|:----------------|
| `tofu fmt` | Enforce code style | Inconsistent indentation |
| `tofu validate` | Syntax correctness | Missing required provider |
| `tflint` | Best practices | Deprecated resource type |

### How to Implement L0 Pre-commit Hook

**File: `.pre-commit-config.yaml`**
```yaml
repos:
  - repo: local
    hooks:
      - id: tofu-fmt
        name: OpenTofu Format
        entry: tofu fmt -check -recursive
        language: system
        files: \.tf$
        pass_filenames: false

      - id: tofu-validate
        name: OpenTofu Validate
        entry: bash -c 'tofu init -backend=false && tofu validate'
        language: system
        files: \.tf$
        pass_filenames: false

      - id: tflint
        name: TFLint
        entry: tflint --recursive
        language: system
        files: \.tf$
```

**Install Hook:**
```bash
pip install pre-commit
pre-commit install
```

---

## 2. L1: Unit Tests

<!-- PlantUML Diagram: UTM_02_Testing_diagram_03
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_03.puml
-->
![Utm 02 Testing Diagram 03](https://www.plantuml.com/plantuml/svg/TPBDRXCn58NtVehBT0EB5ae8geg46XoFL96VKJEHM8o4t9cRn8h7ZlnJMggy0flks5ILODcNwXFq4R1d0fJIoAih7z_xdNDzP1qtpjUIF7CBh15AD5uYLyGkXLfnmsiuvULoRhHN5TLI6zX9MJmF50PBnzLS8bmIW5Ghjr6-fXtMVKNM3xGbDzKM6S27BQFMX3ZXGl_1_Y5CbN2GetL2pU6BS0iOwd89cT5dea93o5-SvFxwwYSSgvLt2N0BnwDiciDE_mrxc-w_StZk3azbcDa0DMJ9K5SX0A2wma8zttCpc0c9zaNpVZZk_n560aZZNQjpeTvRbB9LvcoIH-n_MBxTjgW3Ve5cqv1-32vfsg7fqpnrUF1vjV46HSA_UeEcBXAuN1Tgf85AxIkWNCe0al80nSwnz4verOx87d7SVRzv966V60sfTDCkwpnDuVJCGtHOg4no5Mp4U7hMeebTRDCc6_H6_tc--W5ZxtulO3pDcmsmWtwFRN6SSMlX9QHSo49HVOQ6pn5ESALDswGtcR2J9jrsdxkxxviWIPDchA8XqhYALJkKa2DKLVpglm0)


**Example: Payment Gateway Module Test**

```hcl
# tests/payment_gateway_test.tftest.hcl

mock_provider "azurerm" {}

variables {
  gateway_name    = "payment-gw-test"
  environment     = "dev"
  enable_tls      = true
}

run "verify_gateway_configuration" {
  command = plan

  assert {
    condition     = azurerm_api_management.gateway.sku_name == "Developer"
    error_message = "Dev environment must use Developer SKU"
  }

  assert {
    condition     = azurerm_api_management.gateway.protocols.enable_http == false
    error_message = "HTTP must be disabled, only HTTPS allowed"
  }
}
```

---

## 3. L2: Security Scanning

<!-- PlantUML Diagram: UTM_02_Testing_diagram_04
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_04.puml
-->
![Utm 02 Testing Diagram 04](https://www.plantuml.com/plantuml/svg/VLFDRjD06BplKtmaHrJ9pOyWHKArtPXOJPEgjjIBBzlrbtWLUnsjruGMzSW9f4g5KmLgopDmu7do0l08U3SASIibtejdDVFjpAnzM2WgLPcbv8LAC4DWACiKgI35Z8ivbJI32yfcKvcN8dRpD9VGzFfwrHWIcQ9YcY9y901UBjIQQHvoNUCoAkFdj9RRxdUjQi_PSjGr8OghQlwmTG01ib9oTGa1eq9mCGKlpHU4R5mq_jv_ktt6GraqW1OGkFO8cllzrvrEp_WmXXeiGJRBtqV2zGDmKB0aet9MH6BVigoNCCzJpZYkHhY3u_ywDIcGHI94AUaabna4TX16mhug9K8nHyOdd1bLw0KwnnENNp-3nqLSPLXDzlpHqJhq6uKVrC55MbLIyrab-mLk5OipcgxSdFaXD5shtMivAyqYuGfhYli76F1fOjW3_zq0caVjRiUojh0VuGHZNcQ6VzAl33clUbrhs_2VCCmNXZiSdw-RhNEVXbxUFS8fdsFA1OBD5C-54Tjkw8z7kyClVtm1PpXsZoEn7c6qPczN1ykxXp-_R-3SFXj5OYpIIoFJS5UuvVTFS6e7WI7hbotfgky1zlRUcjiZrJLl036New6nI4px6wZBrKWR8Rez3VH1X1oYYFLl-Gy)


**Common Findings**

| Finding | Severity | Fix |
|:--------|:---------|:----|
| Storage account public access | Critical | `allow_blob_public_access = false` |
| SQL Server no encryption | High | `transparent_data_encryption = true` |
| Missing tags | Medium | Add required tags |
| Outdated API version | Low | Update to latest API |

### How to Integrate L2 Security into GitLab

**GitLab Security Dashboard Integration:**
```yaml
# .gitlab-ci.yml
checkov-scan:
  stage: security
  image: bridgecrew/checkov:latest
  script:
    - checkov -d . --output cli --output junitxml --output-file-path . --framework terraform
  artifacts:
    reports:
      junit: results_junitxml.xml
    paths:
      - results_junitxml.xml
    when: always
  allow_failure: false  # BLOCKS pipeline on Critical/High

tfsec-scan:
  stage: security
  image: aquasec/tfsec:latest
  script:
    - tfsec . --format junit --out tfsec-results.xml --severity-threshold HIGH
  artifacts:
    reports:
      junit: tfsec-results.xml
  allow_failure: false
```

**Jira Integration - Auto-Create Finding:**
```python
# scripts/create_security_finding.py
import requests

def create_jira_finding(finding):
    jira_api = "https://your-org.atlassian.net/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": "UTM"},
            "issuetype": {"name": "Bug"},
            "summary": f"[L2-SEC] {finding['check_id']}",
            "description": finding['description'],
            "priority": {"name": "Critical" if finding['severity'] == "CRITICAL" else "High"},
            "labels": ["security", "automated", "L2"]
        }
    }
    requests.post(jira_api, json=payload, auth=("user", "token"))
```

---

## 4. L3: Compliance Testing

<!-- PlantUML Diagram: UTM_02_Testing_diagram_05
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_05.puml
-->
![Utm 02 Testing Diagram 05](https://www.plantuml.com/plantuml/svg/TLEnRjim5Dpv5Q_sqWuEdDXfwmv599aA3AYkOCcR5vPc5DOKQP0KMYF8s2xTahL0f_nOlg2VK9AARJL59K0WnNllxjr95yOIRPjQe1VscjKCADEDO4GYi-5oIpIfuHEXcqghHguJ9PI6VehztK5eHYsHbM1mWm1I9UqU6Ivqsy5IejVFOMV929yFtRluFrIt25bkNVziz0uILMy59v8oA9cnN5RmCfvENo5qrD7x_Ul-0MPoszWU40EpURuieJyTuzVfQQ0FEdebqvfSALr3BeXSoQrxddmsIeQgF8lc1sZAY6qqWvGBPbRovAhT1s2AezAB_4l0mnquMO1bnMKByzj-_6PoFemx6knUmu0U9bl9oskcdMbGxAGbNqDvyl53_W_B_G_8bU1q1miNd0d0nJB3XJClIKT9sfsML9Mtgoq8q3AwF1mlMCMLX8KpLNDgtVgf7JvYvin-KNhJ8PlZyd1QCDfeRdSkICF4Vkm29yzaF_xyvcaQOPy8YcLMxjFk2Cw9CV3u_SvbBbtGJTilZmettIb-EnvFZl4GBW8q5efksbIYMGRzP3YQdCLUGFiH30RlVH38X-7NmIpKMXRsGGn25qok_O_n1m)


**Example: Payment System Compliance**

```gherkin
# features/payment_compliance.feature

Feature: Payment System Security Compliance

  Scenario: TLS Must Be Enforced
    Given I have azurerm_api_management defined
    Then it must have protocols
    And its value enable_http must be false

  Scenario: Required Tags Present
    Given I have resource that supports tags defined
    Then it must have tags
    And its value must contain "environment"
    And its value must contain "cost-center"

  Scenario: Restricted Regions Only
    Given I have resource that supports location defined
    Then its value must match regex "^(westeurope|northeurope)$"
```

### How to Implement L3 Compliance Testing

**Project Structure:**
```
├── modules/
│   └── payment-gateway/
├── features/                    # BDD Feature Files
│   ├── security.feature
│   ├── tagging.feature
│   └── networking.feature
└── .gitlab-ci.yml
```

**GitLab Pipeline Step:**
```yaml
compliance:
  stage: compliance
  script:
    - tofu plan -out=plan.tfplan
    - tofu show -json plan.tfplan > plan.json
    - terraform-compliance -p plan.json -f features/ --junit-xml compliance.xml
  artifacts:
    reports:
      junit: compliance.xml
```

**Confluence Policy Documentation:**
```
Page: /spaces/UTM/pages/Compliance-Policies

| Policy ID | Rule | Feature File | Last Validated |
|-----------|------|--------------|----------------|
| POL-001 | TLS Required | security.feature | 2025-12-10 |
| POL-002 | Tags Required | tagging.feature | 2025-12-10 |
| POL-003 | EU Regions Only | networking.feature | 2025-12-10 |
```

---

## 5. L4: Integration Testing

<!-- PlantUML Diagram: UTM_02_Testing_diagram_06
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_06.puml
-->
![Utm 02 Testing Diagram 06](https://www.plantuml.com/plantuml/svg/XPEzJiCm58LtFyMbBAq0iJ1bG4Gf4P6GgC1Yw6QIIx7gsfP_GB3n12mCR8oLU0AUXnU0H-2wFz2M0h8KoLTVpZa-JWvy42x4aM8RuGf723Mwg51eveTIM-7422v4FHmu4tLJ66KSR9Q7QJ4MP508ntiPL3hWm8aWZGQEFaWzW5AP6sXpT3IdKOSnaWkobbRe0AsFvySn51Nqf4KbDRP0UDglGkCN-9AO89ml8szFz--l3t1YKNDp6QTCkPR9xwAR-kHzniXxPv_aCZXB7Vmu0nDraDTad2mPvnEwp22G2qWj0so1i5RTBe0busNYydu6XSCqEqMXwE5DT3NwRvOYv7tOcOdE0QYwddHFOh0nUDRW8f-qPv7pP0o56Lc50HSvoZ0BcqAS2oMRD6uVSTxRXhnNGIsKyfsrIVWaYJNQuuhtl83axJrINmH6HHbNgsceEsT-QwMBAV3_XHJf8unsxH6Ng-XE_VuiWz2YoYRNEiyDxPxmVhSKKdMMNg7BFa3Tf7_Y4m)


**Example: Payment Gateway Integration Test**

```go
// tests/integration/payment_gateway_test.go

func TestPaymentGatewayDeployment(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../../modules/payment-gateway",
        Vars: map[string]interface{}{
            "environment":  "test",
            "gateway_name": "payment-gw-integration",
            "enable_tls":   true,
        },
    })

    // Clean up after test
    defer terraform.Destroy(t, terraformOptions)

    // Deploy infrastructure
    terraform.InitAndApply(t, terraformOptions)

    // Get outputs
    gatewayUrl := terraform.Output(t, terraformOptions, "gateway_url")

    // Validate: Health endpoint responds
    statusCode, _ := http_helper.HttpGet(t, gatewayUrl+"/health", nil)
    assert.Equal(t, 200, statusCode)
}
```

---

## 6. L5: Acceptance Testing (UAT)

<!-- PlantUML Diagram: UTM_02_Testing_diagram_07
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_07.puml
-->
![Utm 02 Testing Diagram 07](https://www.plantuml.com/plantuml/svg/TP91Qzim5CVl-XHlxJdGDIsi7OpQmYw3BGcsCnZaeYWlheWY6KdkMaQFEvLjb5uBk-o-wpvFly3s4Ih9RM8AjGz6yk-zz___fHFhc77jMf9NxWpN21nDAv4fObT2DSomDSmPNzL6jsf1jTG6TlCil3t287TCrHBXAm78jN9FP7p8LO_bp2oUO_jqc1tk-RtqXL5NX3ZXVFyFXySmjMWWuHmRFvGZL6YTK3KXMnax_t_z-0FJfDe1PiCNTkdUy6W_ZPEZ18_SNaFQMg7GMYWvAcQ4jh4YfJtivdStyd5ErxBQ0FTtt__z_GcbgDLWl5p6t-KuIExf2RLGNJROzQy-JxBIkwFvaEPl7LwuuxdqtdloybPn9xHYSgO-CIaMBAnYTJuTRVLDq2orMOSaPegU8Lz5Pf8L-OQPMZONKhZBcIhmNE2NpaEPf1kamDhu7Fo8cIfRuJ0YHNRwpCZztJV8BeG3QZna18iSBTxxY5zdRmuEZdeUUeVqXCD7TB4asLeOQKYbvlwArFv0wYwYqLRRP0n9qnXzpcJdBQORJdKmUDTbIRf4mpfe8UG4rI9SwmS)


---

## 7. Tool Matrix

<!-- PlantUML Diagram: UTM_02_Testing_diagram_08
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_08.puml
-->
![Utm 02 Testing Diagram 08](https://www.plantuml.com/plantuml/svg/TPB1Ri8m38RlVGeFpjDAMmRq11Gc8J4D3NQQfYa4qqPDaofrcRg9TrzeWQ5AIowny_lp7olZWfYXCfFE7IMO8N0qfKIcd28LAcU6PR1bF8sDBjKkqb8Rw3xDJ_j6aLi5Yn5-780dhUYYgvTpl55odULQeQAsrelyUT-rkUa_tOwEGu8amWOB4Yg6ZTQI9qmes5QmP1KQnxaOwIpT4DR4IF0ET0SpFneDwuxlfFSbx3Fwk0O79iME4JQPlHJANXvlMRqGtfGWI_A6Ws3oU4CYQwOkp3HFFtEZ3sA7fbNlMI_8IoEeiepUV1W4euR14-IfFfnR5yYRan67giNmGuZixAHWYgEbJ0UZlZizEq5Zs5wRx9vV9JNePJLvUCLOjrX120j561ix7wqiRERt0zTjO9iJxFgioNTf4ABbeebMYyluMyX-21FECQUplSZrHzxPtZDJ9PD_XJQragpwCY9EcYvhbAX4cTNGCQhTwKF-0W)


### Tool Comparison

| Layer | Tool | Language | Speed | Best For |
|:-----:|:-----|:---------|:-----:|:---------|
| L0 | tflint | Go | ⚡⚡⚡⚡ | Terraform linting |
| L1 | tofu test | HCL | ⚡⚡⚡ | Native IaC unit tests |
| L2 | checkov | Python | ⚡⚡⚡ | Multi-framework security |
| L2 | tfsec | Go | ⚡⚡⚡⚡ | Terraform-specific SAST |
| L3 | terraform-compliance | Python | ⚡⚡ | BDD compliance tests |
| L4 | Terratest | Go | ⚡ | Real infrastructure tests |

---

## 8. Pipeline Architecture

### 8.1 Complete CI/CD Flow

<!-- PlantUML Diagram: UTM_02_Testing_diagram_09
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_09.puml
-->
![Utm 02 Testing Diagram 09](https://www.plantuml.com/plantuml/svg/TLF1Zfim4BtxAznmZae2wIOvL0k6JL59WXAoKeykcSsYW8sCMQcgLkgzjswbIfMgNljv_OJQG1AIg72PuOtzthmPRaj9XQpo3BsIZv03Ja1K6L26odtA2YfeZZ_IPByJl69RmZCki77dwxTJ8I2HbEqom9yHndUSoKDb_Q3dJcr2nVQoR4WiVsIgR-v_g9uHagbKznEU5nb85GIlYOUZj80iPO3GIKBlx--NNvWiv_CWxc5QjY4sRZoBJCOrTosY5mde9ppFKudVSRwlYwELVyH3SwfKYfpA6WfDvmowfrcwfH9Qq3q3mvGTJX4j_qpVzp_OtGIXLnVKaV9WV6CxRphgmi4KRvZI5aCfo-QkmH4b_0a4tG5UGS65R1kzlwRwXjS-sQo2-4DTen9i3FonRK-wNCCf9e-GxFbJGpHqpZ3vK4BI8kuLnyjNxN4K1iw2-0VB8souDvEHwNPePi2KQ3MzAAEiiJjq5YScIp614FH1cQudKsGfPKbhi7NTsmySB69_jdBYOBcegrIE3SyQsQRPRS-UAXU5fYxRgTWd9_MwLuKoikILIA2nceI-KdR9-FCBzlmeN3PUgX0RnBGcmswJ7XGP_uJNakvIjcjCZvtP4L_dV0-TeQxdo_V-vUb8y6sLo9ItDgsMdXRJhdA__xPP6zGiZyxLO94Uhewr_QYUWSwK9qZxecCb6Q5RO5lzo_y3)


### 8.2 GitLab CI/CD Configuration

```yaml
# .gitlab-ci.yml - Complete Testing Pipeline

stages:
  - validate      # L0
  - test          # L1
  - security      # L2
  - compliance    # L3
  - integration   # L4
  - deploy

# L0: STATIC ANALYSIS
format-check:
  stage: validate
  script:
    - tofu fmt -check -recursive -diff

validate:
  stage: validate
  script:
    - tofu init -backend=false
    - tofu validate

lint:
  stage: validate
  script:
    - tflint --init
    - tflint --recursive

# L1: UNIT TESTS
unit-tests:
  stage: test
  script:
    - tofu test -junit-xml=unit-test-results.xml
  coverage: '/Coverage: (\d+\.?\d*)%/'

# L2: SECURITY SCANNING
checkov-scan:
  stage: security
  script:
    - checkov -d . --framework terraform
  allow_failure: false  # Block on Critical/High

tfsec-scan:
  stage: security
  script:
    - tfsec . --severity-threshold HIGH

# L3: COMPLIANCE TESTING
compliance:
  stage: compliance
  script:
    - tofu plan -out=plan.tfplan
    - tofu show -json plan.tfplan > plan.json
    - terraform-compliance -p plan.json -f features/

# L4: INTEGRATION TESTS
integration-tests:
  stage: integration
  script:
    - cd tests/integration
    - go test -v -timeout 30m
  when: manual

# DEPLOYMENT
deploy-staging:
  stage: deploy
  script:
    - tofu apply -auto-approve
  environment: staging

deploy-production:
  stage: deploy
  script:
    - tofu apply -auto-approve
  environment: production
  when: manual
```

---

## 9. Use Case: Payment System

### 9.1 System Overview

<!-- PlantUML Diagram: UTM_02_Testing_diagram_10
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_10.puml
-->
![Utm 02 Testing Diagram 10](https://www.plantuml.com/plantuml/svg/TP9VJi904CRVznGZF9Eeg0zg3FqV8v4653J6Xw6TG4ExIxPJXHXku8Fn0Xx2Yta4kuiOeY7DDZlpVJFpsyrsIaRDLP6BFPvIGP2Ghd92ASfP9kUeiO0n9hE9LfLCFPKh3SqmCD-MOruxS4Bm8W129Vd7T-YrW-DziTfo9ggOAqcITtW1t1tJLa9mnZb1ZCl2D1WiIwO279rCCwQ4Aqr2R4WQNn_ldt-i3S0IOkSUclvHS18Ud34j-7ISroMMvi69Bo52fcTSFXflD3BP8UPPYfmf2GFIJrb2LXmwNQDkHiHQ9LIMIbinxlSye_h8ECPoNU6xTaYLPWnTDR6vRYyo9zl2Vds3OC6a9UOMEBYxgU_02zjU-0_OHJc3cjgsSfthAvCCDLOf-6Jkf8QsMjXtRdqpA1f1gtLXuUjbzvRL_6nKG_xk3PmDpara-viY6wqxYWx9rBoURm)


### 9.2 Testing at Each Layer

| Layer | What We Test | Example |
|:-----:|:-------------|:--------|
| **L0** | Code format, syntax | HCL files are valid |
| **L1** | API Gateway config, SKU | Gateway uses correct SKU |
| **L2** | TLS enabled, no public access | Storage is encrypted |
| **L3** | Tags present, region restricted | Only EU regions allowed |
| **L4** | End-to-end payment flow | Payment API returns 200 |
| **L5** | Business acceptance | €1000 payment succeeds |

---

## 10. Decision Flow

### 10.1 When to Run Each Layer

<!-- PlantUML Diagram: UTM_02_Testing_diagram_11
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_11.puml
-->
![Utm 02 Testing Diagram 11](https://www.plantuml.com/plantuml/svg/RPBBJiCm44Nt_ef1RD85uhsX2uhILaAqeagBM1jdcbXDni6P8ENliUEw5AYyiEovvyx3dhGiBNTr9Swun1f1eUqgb2JQdQP6Mbd3XrIxmfgEyjHKniBvVEQN4AovGdWlaO0DP1t1JAeIDjWoB6IFLeZ1NZoa9aT8Iqa5ZeLuyDB55IHhbgpLQ2pq5fBKrBNcnn6mDqnwR4S286Yl8NaZpKu9uBMhx7A9ja38yBDpwVvIaRjnEL1rLdC_i84Eg2jvAJNzHoDyEzJKL5gImZqU339q8seHDh8uXKU3EqYUYR6mhaj31uSOldTDFMsEhwVOLARtbQsioJlbiPzmowRP7x1osHCoHncdXX0km8sq1qD3QwTHolLMd3A95glCZLNcVSGFS4H_Wn4BxmUlBu7RKu4v9g9-hjtdMSilp3qmo8DOJDpkl-Gt)


---

## 10. Autonomous System Architecture

> **Goal**: Transform manual processes into **autonomous tools** that secure **90% of the quality baseline** without human intervention.

### 10.1 Process → Tool Embedding

<!-- PlantUML Diagram: UTM_02_Testing_diagram_12
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_12.puml
-->
![Utm 02 Testing Diagram 12](https://www.plantuml.com/plantuml/svg/TPFVRjCm5CRlynI7LKWWqQX_sJe9j3JDfg6scPOM2QathdFQcZfsPJk32EqM9BX0OXAtk-6I1-1vzWBi4N2SJYj395V-ykMSdxzZ7sb3bCapxZqoAymGAAgS8n6UNZEn8OfaC2TqlLGo5saekLHGEuxATyUXa1eYbXpXWmTmB8MvSxh7kzpnKgBIXxPMs8ww3Qlr_zFgqlCCCxR-xVMFxt2c94MjuURZDvX8oI7AvfYcJ2pX1GIvaK9cCjUG5DfWvddtU7ktrrTVO1ICfy4GpixZC4gIFI3wJgg5ZNQlrNTy3dIlwLjGbH43LAOu4oqVNXFEKc8GT24CUJyJRH_ESm4QQQwOAO2kaAxrJ7Hy21MMpbTC4J2Chj5OlUl3TECgX58iU8w2OaNHB7UwWtlpyzFlNryX6lMZ0PoE9p5CudXO8LTYhR_VwpPsYJSAwrHc6JEmahBay9SsEpAlK-ON6Py9HrFcPBV5fB3m7Atj7WP6X2gfgpOFcTm8Wkaa7iUZU9f0yYQPH2FdBLMeDQE3JgUtGtJ2p93CuOnja3DXGrIvq42s09HmNcoXSXUB1cOqyiLVI7ebtsdWx0B1UaZLxr-sgy_GQpo6Vf14mzDn14aKJi-ZWRENeZri1_kTuFaENYnu0Ktxaq1CRGwhF2C2tkRfCaDXPkB9D9Wy0qoNzdOGZVffLSprtfwRUltbTXw7TgOfMnHUjIm_k5GEOO0RBWlFhKhPqHn2G5SCBr1xtX6AjBo9Vm0)


### 10.2 Autonomous Tooling Matrix

| Process | Manual Effort | Autonomous Tool | Baseline Secured |
|:--------|:--------------|:----------------|:----------------:|
| **Code Formatting** | Run `tofu fmt` manually | pre-commit hook | ✅ 100% |
| **Syntax Validation** | Run `tofu validate` | GitLab CI L0 stage | ✅ 100% |
| **Security Scanning** | Run Checkov/tfsec | GitLab CI L2 stage | ✅ 100% |
| **Compliance Testing** | Write & run tests | GitLab CI L3 stage | ✅ 100% |
| **Defect Creation** | Manual Jira ticket | Jira Automation Rule | ✅ 100% |
| **Traceability Links** | Manual linking | Jira Automation + API | ✅ 95% |
| **Dashboard Updates** | Export/Import | Confluence JQL Macros | ✅ 100% |
| **Quality Gates** | Manual approval | GitLab rules + `allow_failure: false` | ✅ 100% |
| **UAT/Business Review** | Human judgment | N/A - Requires humans | ❌ 0% |

**Result**: **~90% of quality processes are autonomous**

### 10.3 GitLab → Jira → Confluence Integration Flow

```yaml
# Complete Autonomous Integration

# 1. GitLab CI/CD Variables (Project Settings → CI/CD → Variables)
variables:
  JIRA_URL: "https://customer.atlassian.net"
  JIRA_TOKEN: $JIRA_API_TOKEN  # Stored as masked variable
  CONFLUENCE_URL: "https://customer.atlassian.net/wiki"

# 2. Post-Pipeline: Update Jira automatically
.update_jira: &update_jira
  after_script:
    - |
      curl -X POST "$JIRA_URL/rest/api/3/issue/$JIRA_ISSUE/comment" \
        -H "Authorization: Basic $JIRA_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"body": "Pipeline '$CI_PIPELINE_ID': '$CI_JOB_STATUS'"}'

# 3. Quality Gate with Jira Integration
security-scan:
  stage: security
  script:
    - checkov -d . --output json > results.json
    - python scripts/create_jira_findings.py --file results.json
  <<: *update_jira
```

### 10.4 Jira Automation Rules (No-Code Setup)

> **Location**: Jira → Project Settings → Automation → Create Rule

**Rule 1: Auto-Transition on Pipeline Success**
```yaml
Trigger: Incoming Webhook (from GitLab)
Condition: webhookData.status == "success"
Actions:
  - Transition Issue to: "Ready for Review"
  - Add Comment: "✅ All tests passed - Pipeline {{webhookData.pipeline_id}}"
```

**Rule 2: Auto-Escalate on Security Finding**
```yaml
Trigger: Issue Created
Condition: Labels contains "security" AND Labels contains "critical"
Actions:
  - Set Priority: Highest
  - Assign to: Security Team
  - Send Slack: #security-alerts
```

**Rule 3: Auto-Update Requirement Coverage**
```yaml
Trigger: Scheduled (Daily 6 AM)
Actions:
  - Run JQL: project = URM AND type = Requirement
  - For each requirement:
    - Count linked test cases (status = Pass)
    - Update custom field "Test Coverage"
```

### 10.5 Confluence Live Dashboard Setup

```markdown
# UTM Quality Dashboard (Confluence Page)

## 🎯 Autonomous Metrics (Live)

### Pipeline Status
{jira:jql=project = UTM AND type = "Pipeline Run" AND created >= -7d|columns=key,summary,status,created}

### Open Security Findings
{jira:jql=project = UTM AND type = Defect AND labels = security AND status != Closed|count=true}

### Requirement Coverage
{chart:type=pie}
|| Status || Count ||
| Fully Tested | {jira:jql=project=URM AND "Test Coverage" >= 100%|count=true} |
| Partially Tested | {jira:jql=project=URM AND "Test Coverage" >= 50% AND "Test Coverage" < 100%|count=true} |
| Not Tested | {jira:jql=project=URM AND "Test Coverage" < 50%|count=true} |
{chart}

### Quality Gate History
{jira:jql=project = UTM AND type = "Quality Gate" AND created >= -30d|columns=key,summary,status,resolution|max=20}
```

### 10.6 Autonomous System Benefits

<!-- PlantUML Diagram: UTM_02_Testing_diagram_13
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_13.puml
-->
![Utm 02 Testing Diagram 13](https://www.plantuml.com/plantuml/svg/TPBFJXin48Vl-nG3Q2-fK3TT5efK98Ap2pa0LJOlu7YdYPlrEF8Vf0XnHnnGLUYPH-YhyGXubwLDH2jBFlXdpVTvniVMSUEyggCjDqU58D3u6Zb5TY5foGrNCELYCJFQKyLqhGti57cprcxewNSK3guZW4AJwwvzOccU9U7iv3y5RgB8ILSZF3yztCB0EqrQQM-XN5c72iQNeoZgQcy_F_tw0HCP54j-9Mbcju5Rc8pESzWPPaMMfot_d9FdDNmrMg2rS0HxCDVUs8yLNuLu3N84_GoK9E_mBUtrkjeXF4pZNgzH_2jm_nkO9Yk378bLosUN5sNWx-NxHR_bdtd52N9ZmZl7t66ebEtsaxXZgt1KRSPV-d6B7gcbqLTX1kGQVF8E_t074yC5ygcifNlbJyO35XfGi29bnNe3M2Xb-Am1x2Ux1ty4kiUlnOTP_E4V0cdsJk3n9vGel0dmC5EBjIHiBSgS1OV1y6JuUSDXZcBHz794ugrlRgCHfs5l9v4aCI1zqqPWrSemhPQrv2GQnLCVlXavnEfLwHYfQlxi2m)


---

## 11. Coverage Testing Deep Dive for Declarative IaC

> **Challenge**: OpenTofu/Terraform is a **declarative language** that describes "what" state to achieve, not "how" to execute it. Traditional line-based code coverage (like JaCoCo for Java or pytest-cov for Python) **does not exist** for IaC because there is no execution flow to trace.

### 11.1 The IaC Coverage Problem

<!-- PlantUML Diagram: UTM_02_Testing_diagram_14
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_14.puml
-->
![Utm 02 Testing Diagram 14](https://www.plantuml.com/plantuml/svg/TPB1RXCn48RlVeeXEPHAYIXj2Yq7rDJPY5H9MhMHAjHmc7YdMIkENTdUX0Zr2U366N7ZmNW27g6sqnNR8dQbtTMlV-R_FBCdpgFrvLAn5xwW9O4WMof2pTn2wZkqk8GPYiNScbBdt2XZeTdFubrpM18UzLmHV640VQDzvKmNkwzv1ThykMsV7sI7Uq4x_K_KFMDU-j3_zuzlS5riO68nbruQZGg6KXDmioABSu8-IkNWDXGFa3Fs5wtnv-VtNp1OtWMVbok2OT3BK3BLByzmXIsusFZ2w1Rmvcu3qC5WT17OZjvskcyISK9lP9z9b9v0nTZP9hsdEW291QmBAOgaEB2eftf4w4fBxnAaWyVQ75x1nFX7TbU5yNZEfy1VeKT2uR_47_Ym1H-xe_0ykpeVRu5x6OVcw-oeqpck0VV82Ijd13avQKDusBaFFSO6AF64CSAjCkiaRU6zWHrRwfsgxNEqk8TBSgNooN6PNK6JxnqSxv_MWkjB4jL-l37AJJNlZiVd4rWR6wOcVH6tLRLAON7uxPj2vZdfJrRE2z-E85kz_JxwM3nlzSrEIEVnHtu0)


### 11.2 Custom IaC Coverage Methodology (Dual Metrics)

Since native line coverage doesn't exist, we developed a **custom dual-metric coverage system**:

| Metric | What It Measures | How to Calculate |
|:-------|:-----------------|:-----------------|
| **Scenario Coverage** | Test execution quality | `Pass Rate = Passed Tests / (Passed + Failed) × 100%` |
| **Line Coverage** | Code structure testing | Weighted formula based on Variables, Resources, Attributes |

#### 11.2.1 Scenario Coverage (Test Pass Rate)

Measures **how well your tests execute** across all testing layers.

<!-- PlantUML Diagram: UTM_02_Testing_diagram_15
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_15.puml
-->
![Utm 02 Testing Diagram 15](https://www.plantuml.com/plantuml/svg/PL5HIWCn4FsVKuo8KFV7Lbk5b4BBqeBG3sdr0EDss8PcaoMP5GizWRyUm2jw12T5i5JozTxBlFSocIQXA5tZu4Ast31M73l7v27jh6yfKeElLEtg63g_AOCB4IyNytm0n8fZ_Fxw_C1rnPwY3LY6DuvKCvRagiwHsE013i-S1EVlN7MPEC0n5iogypXp3e_oalOSqnZCiczmBJfQOMymGb4nNMT-OF35MpbZR_Ms6aSh-pFbpcYVfdMMVCMgzK-qeS57Brp7OqNi_St1OUR9xPDD1p2blbjmnQbpejry4CPewwq0udCGSWRlVssLUQAKU6DmE5Am8Eio66ImtjcspQWFx3UOVJJeP4cQzN-94tMwKVy95iN3wAeenhgvq09CrIJ_sWy)


**Tools to Measure Scenario Coverage:**

| Layer | Tool | Output Format | Pass/Fail Detection |
|:------|:-----|:--------------|:--------------------|
| L0 | `tofu validate` | Exit code | `0` = pass |
| L1 | `tofu test` | JUnit XML | `<testcase>` results |
| L2 | `checkov --output junitxml` | JUnit XML | `passed/failed` count |
| L3 | `terraform-compliance --junit-xml` | JUnit XML | Scenario results |
| L4 | Terratest | Go test output | `PASS/FAIL` |

#### 11.2.2 Line Coverage for Declarative IaC (Custom Approach)

Since OpenTofu is declarative, we measure **code structure coverage** using static analysis:

<!-- PlantUML Diagram: UTM_02_Testing_diagram_16
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_16.puml
-->
![Utm 02 Testing Diagram 16](https://www.plantuml.com/plantuml/svg/ZPFDIiD058NtynJN5a71d_vfMq5nEgOg516jYk9ccaxRO39J9ZUYY2iVm8KBbovy2VU-YI-WZ-1C9jLO54msTmw7UxwS8PinSer9598P78b8W2zq4WekINmHo37NF88Uzo-6MYMoprIeD1JRddrp3Yryv78O2hWX06qbSU9C7tARy_fSzwTj5LRrLaf6Q_qHTKi81cZsVpmzt0DBObGHT08fWAbBeVbGmC3OTpaZv1kcK7v_kN-xUuPzUd3e5O37Re9YVQlAceqK8-Kf7FfSmX8EO1248ZwNtXLgxkCQ77CTy9xH5k10n2hHlXqfeWvw2OhORIrRmbnm9GkcUxHpUkQYizbyRQDUewk_X9jrk3Jomma4CqKOXAwHHVz_97IQf9gHd7YxsplTrED6ABRgpPLIAyT1n-Fm6hPKn0C99o8OZj1GV8N1woDK5xuvxBcI9x12sKLCOzGo34OxxAX3kwuIUu9YsMlKQiqSny-BNJ-NSra5Ph_3ceTbcEigv65Ui_6bqgnRdHAuwrvSt9YqJoQtO3LN1Cdwi8e58cHJoBxz9Ju1)


**Weighted Formula:**

```
Line Coverage = (Variables_Tested×2 + Resources_Tested×3 + Attributes_Tested×1) 
                ÷ (Total_Variables×2 + Total_Resources×3 + Total_Attributes×1) × 100%
```

| Component | Weight | Justification |
|:----------|:------:|:--------------|
| **Resources** | 3 | Core infrastructure - highest deployment impact |
| **Variables** | 2 | Input validation critical for security/correctness |
| **Attributes** | 1 | Implementation details - lower impact |

**Example Calculation (Storage Account Module):**

```
Module: azurerm_storage_account

Variables:   4 total, 4 tested = 100% × 2 = 2.0
Resources:   2 total, 2 tested = 100% × 3 = 3.0
Attributes: 10 total, 8 tested =  80% × 1 = 0.8

Line Coverage = (2.0 + 3.0 + 0.8) / (2×1 + 3×1 + 1×1) = 5.8/6 = 96.7%
```

### 11.3 Coverage Types Summary for IaC

| Coverage Type | How to Calculate | Tool | When to Use |
|:--------------|:-----------------|:-----|:------------|
| **Resource Coverage** | Resources with assertions ÷ Total resources | `tofu test` assertion count | Measure module completeness |
| **Scenario Coverage** | BDD scenarios passed ÷ Total scenarios | `terraform-compliance` | Measure policy compliance |
| **Module Coverage** | Modules with `.tftest.hcl` ÷ Total modules | Directory scan | Track testing progress |
| **Requirement Coverage** | Tests linked to requirements ÷ Total requirements | Jira traceability | Trace to business needs |
| **Variable Coverage** | Variables with validation ÷ Total variables | Static analysis | Measure input protection |

### 11.4 Implementing Custom Coverage Reports

**PowerShell Script for IaC Coverage Analysis:**

```powershell
# calculate-coverage.ps1
param([string]$ModulePath)

# Parse Terraform files
$tfFiles = Get-ChildItem -Path $ModulePath -Filter "*.tf" -Recurse
$testFiles = Get-ChildItem -Path $ModulePath -Filter "*.tftest.hcl" -Recurse

# Count elements
$variables = (Select-String -Path $tfFiles -Pattern 'variable\s+"' -AllMatches).Matches.Count
$resources = (Select-String -Path $tfFiles -Pattern 'resource\s+"' -AllMatches).Matches.Count
$outputs = (Select-String -Path $tfFiles -Pattern 'output\s+"' -AllMatches).Matches.Count

# Count tested elements (from test files)
$testedVars = (Select-String -Path $testFiles -Pattern 'var\.' -AllMatches).Matches.Count
$testedRes = (Select-String -Path $testFiles -Pattern 'assert\s*{' -AllMatches).Matches.Count

# Calculate weighted coverage
$totalWeight = ($variables * 2) + ($resources * 3) + ($outputs * 1)
$testedWeight = ([Math]::Min($testedVars, $variables) * 2) + ([Math]::Min($testedRes, $resources) * 3)
$coverage = [Math]::Round(($testedWeight / $totalWeight) * 100, 1)

Write-Output "Module: $ModulePath"
Write-Output "Variables: $variables | Resources: $resources | Outputs: $outputs"
Write-Output "Line Coverage: $coverage%"
```

---

## 12. Fuzz Testing for Infrastructure as Code

> **What is Fuzz Testing?** Fuzz testing (or fuzzing) exposes unhandled errors by sending **random, malformed, or boundary-case inputs** to a system. For IaC, this means testing modules with invalid parameters to ensure they fail gracefully.

### 12.1 Why Fuzz Testing Matters for IaC Modules

<!-- PlantUML Diagram: UTM_02_Testing_diagram_17
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_17.puml
-->
![Utm 02 Testing Diagram 17](https://www.plantuml.com/plantuml/svg/TPA_SjGm48TxFyNcA3DXZkG2IGecTyQNeGZ7X10QDtlMdYDEbZpI-fY4IKd7qAI5IKVBE_44UGJMkZyuPB0hIp_h-tQrnu7HSrEPP8ilgI8eo3U6q2PXhcsD7YkOOZ4llMkiIfrn7fwCi_Rj93mLZBOq19yJWB6pl4x69xdfP0lqwj_ORhgNxVTbRVGVr4sIi6Ov__xksoyODzVNS4w1jItXhNTJGnNC9FuQKpXrIWe8IV9NgdT_T_iJJiYIryKgq0CCS3fv9V235uFXywWKtNhls7ai2OP58IQy-Y6txmCfc5x1VdyRiAwDBf2riy24LSYjnAdc0B5COl815XhXASyMwCEQbxQrTDH-__WA7pHVkeOVr1Npew7ufVszmzrHn-zSU489WG9yyavwuAaKaTmkJK5HRTnL07QhVUEMghbDNINYQ0iIEMVYwjQQzSZj-vVezbZiPD9sxbbsC1WSTimkq6YrRCfKcFCWPX_bF93BRpYteqOR1JFKHdZPU7AMhLmhiln0hcoaYvQ9r8ONxTeRszbv6Jjp16ySB3R8pLwKEu8Bz1fbD3eHs9PneS9PfTjF6P9ZiggT_Zy)


### 12.2 IaC Fuzz Testing Strategy

For declarative IaC, fuzz testing is implemented through **variable validation rules**, **preconditions**, and **postconditions**:

| Technique | When Evaluated | What It Catches |
|:----------|:---------------|:----------------|
| **Variable Validation** | Before plan generation | Invalid input formats, wrong values |
| **Precondition** | Before resource creation | Configuration assumptions |
| **Postcondition** | After resource creation | Deployment guarantees |
| **Check Block** | After apply (non-blocking) | Runtime validation |

### 12.3 Example: Region Restriction Fuzz Testing

**Scenario**: A Storage Account module should ONLY deploy to `westeurope` or `northeurope`. If a team passes `eastus` or an invalid region, the deployment should **fail immediately**.

**Module: `modules/storage-account/variables.tf`**

```hcl
variable "location" {
  description = "Azure region for the storage account"
  type        = string

  # FUZZ TEST: Reject invalid regions
  validation {
    condition     = contains(["westeurope", "northeurope"], lower(var.location))
    error_message = "Location must be 'westeurope' or 'northeurope'. EU data residency required."
  }
}

variable "storage_account_name" {
  description = "Name of the storage account"
  type        = string

  # FUZZ TEST: Reject names that don't match Azure naming rules
  validation {
    condition     = length(var.storage_account_name) >= 3 && length(var.storage_account_name) <= 24
    error_message = "Storage account name must be 3-24 characters."
  }

  validation {
    condition     = can(regex("^[a-z0-9]+$", var.storage_account_name))
    error_message = "Storage account name must contain only lowercase letters and numbers."
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string

  # FUZZ TEST: Only allow known environments
  validation {
    condition     = contains(["dev", "test", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, test, staging, prod."
  }
}
```

**Test File: `modules/storage-account/tests/fuzz_test.tftest.hcl`**

```hcl
# Fuzz Test: Invalid region should fail
run "fuzz_invalid_region_eastus" {
  command = plan

  variables {
    location             = "eastus"  # Invalid - not in allowed list
    storage_account_name = "testaccount"
    environment          = "dev"
  }

  expect_failures = [
    var.location  # This variable should fail validation
  ]
}

run "fuzz_invalid_region_typo" {
  command = plan

  variables {
    location             = "west-europe"  # Invalid - typo with hyphen
    storage_account_name = "testaccount"
    environment          = "dev"
  }

  expect_failures = [
    var.location
  ]
}

run "fuzz_invalid_name_uppercase" {
  command = plan

  variables {
    location             = "westeurope"
    storage_account_name = "TestAccount"  # Invalid - contains uppercase
    environment          = "dev"
  }

  expect_failures = [
    var.storage_account_name
  ]
}

run "fuzz_invalid_name_special_chars" {
  command = plan

  variables {
    location             = "westeurope"
    storage_account_name = "test-account"  # Invalid - contains hyphen
    environment          = "dev"
  }

  expect_failures = [
    var.storage_account_name
  ]
}

run "fuzz_invalid_environment" {
  command = plan

  variables {
    location             = "westeurope"
    storage_account_name = "testaccount"
    environment          = "production"  # Invalid - should be "prod"
  }

  expect_failures = [
    var.environment
  ]
}
```

### 12.4 Advanced Fuzz Testing with Preconditions

For more complex validation that requires resource context:

**Module: `modules/storage-account/main.tf`**

```hcl
data "azurerm_resource_group" "target" {
  name = var.resource_group_name
}

resource "azurerm_storage_account" "this" {
  name                     = var.storage_account_name
  resource_group_name      = data.azurerm_resource_group.target.name
  location                 = var.location
  account_tier             = var.account_tier
  account_replication_type = var.replication_type

  lifecycle {
    # PRECONDITION: Resource group must be in same region as storage account
    precondition {
      condition     = data.azurerm_resource_group.target.location == var.location
      error_message = "Storage account must be in the same region as the resource group (${data.azurerm_resource_group.target.location})."
    }

    # PRECONDITION: Production must use GRS replication
    precondition {
      condition     = var.environment != "prod" || contains(["GRS", "RAGRS", "GZRS"], var.replication_type)
      error_message = "Production storage accounts must use geo-redundant replication (GRS, RAGRS, or GZRS)."
    }

    # POSTCONDITION: Verify HTTPS-only is enforced
    postcondition {
      condition     = self.https_traffic_only_enabled == true
      error_message = "Storage account must enforce HTTPS-only traffic."
    }
  }
}
```

### 12.5 Fuzz Testing CI/CD Integration

**GitLab Pipeline Stage for Fuzz Testing:**

```yaml
# .gitlab-ci.yml
fuzz-tests:
  stage: test
  script:
    - echo "Running fuzz tests for all modules..."
    - |
      for module in modules/*/; do
        if [ -d "$module/tests" ]; then
          echo "Testing $module"
          cd $module
          tofu init -backend=false
          tofu test -filter="*fuzz*" || exit 1
          cd ../..
        fi
      done
  rules:
    - if: $CI_MERGE_REQUEST_ID
      changes:
        - modules/**/*.tf
        - modules/**/*.tftest.hcl
```

### 12.6 Fuzz Testing Checklist

| Test Case | Validation Type | Example |
|:----------|:----------------|:--------|
| Invalid region | `contains()` validation | `eastus` when only EU allowed |
| Typos | `regex()` validation | `west-europe` instead of `westeurope` |
| Case sensitivity | `lower()` + validation | `WestEurope` vs `westeurope` |
| Length limits | `length()` validation | Name too short/long |
| Special characters | `regex()` validation | Hyphens, underscores where not allowed |
| Missing required tags | `can()` + lookup | Environment tag missing |
| Wrong data types | `type` constraint | String passed instead of number |
| Null/empty values | `nullable = false` | Empty string for required field |
| Cross-resource validation | `precondition` | RG region ≠ Storage region |
| Runtime guarantees | `postcondition` | HTTPS not enforced |

---

## 13. Functional and Non-Functional Testing for IaC

### 13.1 Testing Categories Overview

<!-- PlantUML Diagram: UTM_02_Testing_diagram_18
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_18.puml
-->
![Utm 02 Testing Diagram 18](https://www.plantuml.com/plantuml/svg/TPFFRjD04CRl-nH3Ue53998ufO146bnRHAhSYgOtBflra5fPxvhTCMbKzHcuSA6N7Yln13mFBq0VWVMVsCOgzcbslvtlzytQnvQueJoLx1bTOOeWqEGIkM9sawYC6vx2YelDskXSnRwMsi1161HlHs5G45ThYN3304AjQAyi7tRRqGfkuhvix4-2wKktzlu_LhUCKKAk_-Fzmqy8SoKeqOfB-6eXqchOMLcYfKIj6MkX1e_ttnyWl8pyvU8icfyEWDkoTCv7hxpvOSbJWWrED5f82BRQR41eKtIHkzadjTz84Sa5_f8dnirBaUtiPKR7kK30wymTmnXqJbbEiyRGBv9qm7xV_VZpwnj4Pz6mXnTLVAFWoFDUT_W-w2riKKg8zvveFckJEef5MLiKkS4PV4IPy9N43fuLtDLj-pvDRugsmbx2mOaN78QZjuJNz6ObtHrrW2wLwrpAuVdfw4LrPjHi-phD78XoKzcB9hLet8WMYd1jUE7TgBnQDMbKSo4metzQJMkHrqlon3TXwzn5d6au3IPFnxaenfVG3Yu4LuN5kBA8saZdrSHRa4emxcIs17DdlBD9lTccgEubaOM7VuLYKolA2EMb3uVltDHPr1GEch5ZL77nd_u5)


### 13.2 Functional Testing for IaC

| Test Type | What It Validates | Layer | Tools |
|:----------|:------------------|:-----:|:------|
| **Unit Tests** | Individual resource configuration | L1 | `tofu test`, mock_provider |
| **Compliance Tests** | Policy adherence (tags, regions) | L3 | `terraform-compliance` |
| **Integration Tests** | Full stack deployment | L4 | Terratest |
| **Acceptance Tests** | Business requirements met | L5 | Manual + automated scripts |

**Example: Functional Test for Payment Gateway**

```hcl
# Functional Test: Verify payment gateway creates correct resources
run "functional_gateway_creates_correct_sku" {
  command = plan

  variables {
    gateway_name = "payment-gw"
    environment  = "prod"
  }

  # Functional assertion: Correct SKU for production
  assert {
    condition     = azurerm_api_management.gateway.sku_name == "Premium"
    error_message = "Production gateway must use Premium SKU"
  }
}

run "functional_gateway_creates_required_apis" {
  command = apply

  # Functional assertion: All required APIs exist
  assert {
    condition     = length(azurerm_api_management_api.payment) >= 3
    error_message = "Payment gateway must have at least 3 APIs configured"
  }
}
```

### 13.3 Non-Functional Testing for IaC

| Test Type | What It Validates | Tools |
|:----------|:------------------|:------|
| **Security** | Vulnerabilities, misconfigurations | Checkov, tfsec |
| **Performance** | Response time, throughput | Terratest + load testing |
| **Cost** | Monthly cost estimation | Infracost |
| **Reliability** | Redundancy, availability zones | Custom assertions |
| **Compliance** | Regulatory requirements | terraform-compliance |

**Example: Non-Functional Security Test**

```yaml
# Non-functional: Security scanning with Checkov
checkov-nonfunctional:
  stage: security
  script:
    - checkov -d . --framework terraform --check CKV_AZURE_*
  artifacts:
    reports:
      junit: checkov-results.xml
```

---

## 14. From User Stories to Acceptance Testing

### 14.1 Traceability Flow: Requirements → Tests → Acceptance

<!-- PlantUML Diagram: UTM_02_Testing_diagram_19
Original source archived in _archive/plantuml-source/UTM_02_Testing_diagram_19.puml
-->
![Utm 02 Testing Diagram 19](https://www.plantuml.com/plantuml/svg/TPF1RjD048RlVegXFQTAavGqEQ2wMnT53RIADv6GSjckns5LUntjheKYr6Cvm0N15SGHYSVg4_08p6wSOWh4f_bdDFFjp9yJwuHnTLb4JznhB14achf0eIDxe_HQ6572jP0tArFLEcDLKHdOFq_yrwemA9tGgmBXRGHmNcctgmo_wBPLAuN97fVrM3yvwf9s-fzHjr7abAF-Fxzz_W1pYmPILvaDtB_x11oj0oOiXYYM4jT48n6OKGwD4a6VnpoAVeFkKQUlC4-J6QJySlPg3uIb4FQ7PtqsEWw40NKljY1WBJObQWSEHRdK4tWZAB2485O8gANPh1rcIvrMa0adG5bOcyhHECoQrio_ua-0Zn0pbbpn-2LBWCqcF9bDub0UCzhAyN0GFssH71w4L_kHjKKBQPfqs8kBfUuTm0Lk0Wzce7I85g8kt5Bt3o2kC-MWg5QMKCLrqI3HxB-Glly0dgGSM9mcQQZYH78w71rrJriad7MwtSCnB6Yz-SQ3x3elTSZr7d84IFx8qT2MiCds7xBY0QqPzXZf_ijTUqaURiiLSzW_J8u7Wr6BQqfCSwtydSWJpLrKfK5MEbUhfPuIM8go9cVGlgJGT5bBkwJCqTXx1AnQwKwLvysGVrpjVQYR9UbyohUtzIoisn_rsZiAv4K1SkV24kaSNhswXBIPiXLcAB8Dv6JuArDbjVJ8kyu1W8pPwJpphXZ36UPAeuqey1htsdFKQ0GzEk9RbOZ6C2dN1NhRKZ4FyZpe2r6eB5H79wWp_-__1G)


### 14.2 Example: User Story to UAT Mapping

**User Story (Jira Epic: URM-EPIC-042):**
> As a **payment application team**, I want **storage accounts to be encrypted with customer-managed keys**, so that **our payment data is protected per PCI-DSS requirements**.

**Acceptance Criteria:**

| AC # | Criteria | Testable Requirement |
|:----:|:---------|:---------------------|
| AC-1 | Storage account uses SSE with CMK | Encryption source = `Microsoft.Keyvault` |
| AC-2 | CMK stored in designated Key Vault | Key Vault ID matches approved vault |
| AC-3 | Key rotation enabled (90 days) | Key rotation policy configured |
| AC-4 | Diagnostic logs sent to Log Analytics | `diagnostic_settings` resource exists |

**Test Cases Derived:**

| TC ID | Type | Maps to AC | Test |
|:------|:-----|:-----------|:-----|
| TC-001 | L1 Unit | AC-1 | Assert encryption source = KeyVault |
| TC-002 | L1 Unit | AC-2 | Assert key_vault_key_id references approved vault |
| TC-003 | L2 Security | AC-1, AC-2 | Checkov CKV_AZURE_43 passes |
| TC-004 | L3 Compliance | AC-3 | BDD: Key rotation policy configured |
| TC-005 | L4 Integration | AC-4 | Terratest: Verify diagnostic settings created |
| TC-006 | L5 UAT | All | Manual: PO reviews deployed storage |

**Acceptance Test Implementation:**

```hcl
# tests/acceptance/storage_pci_test.tftest.hcl

# AC-1: Storage uses SSE with CMK
run "acceptance_sse_cmk_enabled" {
  command = plan

  assert {
    condition     = azurerm_storage_account.payment.customer_managed_key[0].key_vault_key_id != null
    error_message = "AC-1 FAILED: Storage must use customer-managed key encryption"
  }
}

# AC-2: CMK stored in designated Key Vault
run "acceptance_approved_keyvault" {
  command = plan

  variables {
    approved_keyvault_id = "/subscriptions/xxx/resourceGroups/security-rg/providers/Microsoft.KeyVault/vaults/pci-keyvault"
  }

  assert {
    condition     = contains(azurerm_storage_account.payment.customer_managed_key[0].key_vault_key_id, var.approved_keyvault_id)
    error_message = "AC-2 FAILED: CMK must be from approved PCI Key Vault"
  }
}
```

**BDD Compliance Test (AC-3):**

```gherkin
# features/pci_compliance.feature

Feature: PCI-DSS Storage Compliance

  @AC-3
  Scenario: Key rotation must be enabled
    Given I have azurerm_key_vault_key defined
    Then it must have rotation_policy
    And its value expire_after must be "P90D"

  @AC-4
  Scenario: Diagnostic logs must be configured
    Given I have azurerm_storage_account defined
    Then I should have azurerm_monitor_diagnostic_setting defined
    And its name must contain "payment-storage-diag"
```

### 14.3 UAT Sign-Off Checklist

| Checkpoint | Responsible | Evidence |
|:-----------|:------------|:---------|
| All test cases pass (L1-L4) | DevOps | CI/CD pipeline green |
| Security scan clean | Security | Checkov report |
| Compliance scenarios pass | Compliance | BDD report |
| Integration tests pass | DevOps | Terratest output |
| Business owner review | Product Owner | Manual inspection |
| Sign-off documented | Product Owner | Jira ticket transition |

---

## Quick Reference

### Test Commands Cheat Sheet

```bash
# L0: Static Analysis
tofu fmt -check -recursive
tofu validate
tflint --recursive

# L1: Unit Tests
tofu test

# L2: Security
checkov -d . --framework terraform
tfsec .

# L3: Compliance
tofu plan -out=plan.tfplan
tofu show -json plan.tfplan > plan.json
terraform-compliance -p plan.json -f features/

# L4: Integration
cd tests/integration && go test -v -timeout 30m
```

### Quality Gate Summary

| Gate | Layer | Blocking? | Criteria |
|:----:|:-----:|:---------:|:---------|
| Pre-commit | L0 | ✅ | Format + Validate + Lint pass |
| Pre-merge | L1, L2 | ✅ | Unit pass, Coverage ≥80%, No Critical/High |
| Pre-deploy | L3 | ✅ | All compliance scenarios pass |
| Release | L4 | ✅ | Integration tests pass |
| Pre-prod | L5 | ✅ | UAT sign-off |

---

*Document ID: UTM-02 | Version: 2.1 | Last Updated: December 2025*
