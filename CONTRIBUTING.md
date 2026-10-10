# Contributing

Thanks for helping. Issues and pull requests are welcome.

## Ground rules

- **Structure, not content.** Templates hold headings, placeholders (`{{...}}`) and `<!-- guide: ... -->` notes. No real project, company, customer or person.
- **Synthetic fixtures only.** Anything under `tests/fixtures/` is made up. Never add real documents, transcripts, emails or links.
- **Never overwrite a user's file.** The installer writes a `*.starter.*` file next to anything that exists. Keep it that way.
- **Partner documents are read-only.** Tools may read a mapped source; they never edit it.
- **No dependencies.** The tools run on the Python standard library (3.10 or later) so they work in any repo.

## Before you open a pull request

```bash
python3 tests/test_pack.py     # must end with "0 failed"
```

Add a test for any behaviour you change. A new detection rule needs a fixture file that it finds, and a check that it does not misfire on the existing fixture.

## Adding a role or an overlay

1. Add the role to `ROLES` in `tools/docmap.py`: its template files (mode `new`), its overlay (modes `adopt` and `extend`), and one line on what it is.
2. Add `templates/overlays/<role>.md`. Start it with `**Source of truth:** {{SOURCE}}` and hold only what a partner's own document usually lacks.
3. Add detection rules in `NAME_RULES`, `DIR_RULES` or `TITLE_RULES` if the role has common file names.
4. Update the tables in `README.md` and add tests.
