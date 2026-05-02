## Why

Transitioning from manual cloud console configuration to Infrastructure as Code (IaC) ensures that the Vertex AI RAG corpus setup is reproducible, version-controlled, and consistently deployable. This move reduces the risk of manual configuration drift and enables automated environment provisioning.

## What Changes

- Introduction of IaC templates (e.g., Terraform or Pulumi) for Vertex AI RAG resources.
- Formalization of the RAG corpus configuration in version control.
- Documentation on how to provision the RAG infrastructure using the new IaC scripts.

## Capabilities

### New Capabilities
- `iac-provisioning`: The ability to provision and manage Vertex AI RAG resources using Infrastructure as Code.

### Modified Capabilities
- `gcp-rag-agent`: Modification to ensure it remains compatible with IaC-managed resource names and locations.

## Impact

- New dependency on an IaC tool (e.g., Terraform).
- Changes to the internal `config.py` to support dynamic resource identifiers provided by IaC.
- Potential impact on CI/CD pipelines to include infrastructure provisioning steps.
