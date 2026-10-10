# {{PROJECT_NAME}}: data model

**Version:** {{v1}} · **Last updated:** {{DATE}} · **Owner:** {{planning}} · Planning-only

<!-- guide: The ERD and the rules around the data. Keep it in step with the schema file once one exists, and name that file below so the schema, not this page, is the source of truth for column detail. If the partner already has a schema or ERD, set this role to adopt in doc-map.md and use the overlay instead. -->

## 1. Schema source
{{Path of the schema file (e.g. prisma/schema.prisma, db/schema.sql), or "this page" until one exists.}}

## 2. Entities and relationships
```mermaid
erDiagram
  {{ENTITY_A}} ||--o{ {{ENTITY_B}} : {{relationship}}
  {{ENTITY_A}} {
    string id
    {{type}} {{field}}
  }
```

| Entity | What it is | Created by | Requirement IDs |
|---|---|---|---|
| {{…}} | {{…}} | {{step or service}} | {{…}} |

## 3. Field classification
| Entity.field | Class (public / internal / personal / sensitive) | Retention | Who can read it | Synthetic in the prototype? |
|---|---|---|---|---|
| {{…}} | {{…}} | {{…}} | {{…}} | {{yes / no}} |

## 4. State machines
<!-- guide: For any entity with a status, list the states and the allowed transitions; the journey's end states usually live here. -->
| Entity | States | Allowed transitions | Who or what moves it |
|---|---|---|---|
| {{…}} | {{…}} | {{…}} | {{…}} |

## 5. Events
| Event | Emitted when | Properties | Requirement ID (MR) |
|---|---|---|---|
| {{…}} | {{…}} | {{…}} | {{…}} |

## 6. Migrations and seed data
{{How the schema changes, how to roll back, where synthetic seed data comes from.}}
