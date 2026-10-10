# Overlay: data model

**Source of truth:** {{SOURCE}}

<!-- guide: This overlay holds only what the source lacks. Never copy the source here, and never edit a partner document from a build session. In extend mode, these sections are meant to be pasted into the source once the partner agrees; until then this file is what the agent reads alongside it. Delete a section once the source covers it, and say where in the "Covered by the source" table. -->

The source (a Prisma or SQL schema, DBML, an ERD image or a doc) stays the model. This overlay records what the project changes and what the schema does not say.

## Entities this project touches
| Entity / table | Change (new / extend / read-only / unchanged) | Requirement IDs | Owner |
|---|---|---|---|
| {{…}} | {{…}} | {{…}} | {{partner / us}} |

## What we add
```mermaid
erDiagram
  {{EXISTING_ENTITY}} ||--o{ {{NEW_ENTITY}} : {{relationship}}
```

## Field classification
| Entity.field | Class (public / internal / personal / sensitive) | Retention | Who can read it | Synthetic in the prototype? |
|---|---|---|---|---|
| {{…}} | {{…}} | {{…}} | {{…}} | {{yes / no}} |

## Migrations
| Migration | Reversible? | Rollback | Partner sign-off |
|---|---|---|---|
| {{…}} | {{…}} | {{…}} | {{…}} |

## Seed and fixture data
{{Where synthetic data comes from; never real records.}}
