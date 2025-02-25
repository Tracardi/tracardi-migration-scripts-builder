# Tracardi migration script builder

#### v0.1.0

This is a simple Python-based console app for constructing Elasticsearch migration scripts for Tracardi.

# Setup

In the repo's directory, run ```pip install -r requirements.txt```

In environmental variables, include variable `ELASTIC_HOST`, containing Elasticsearch instance IP, port and username
with password if needed.

# Usage

After setup, run `main.py`. Provide the codenames of both old and new Tracardi version (just hit Enter if the previous
version has no codename, at least one is required though). Provide a name for the migration data file,
then `<given-name>.json` file should be created in the `tmp` directory. Move created file to Tracardi and let Tracardi
Migration Engine handle the rest for you. Script has to be specified though, since it arrives in form:

```
// some commented line of code;\n
// other commented line of code;\n
```

`//` have to be removed wherever you find it reasonable for the line to be executed (if casting or re-assigning is
required).

Sometimes, changes has to be reviewed by Tracardi developer. For this purpose, here's the structure of the migration
schema:

```json
{
  "id": "67ffc4208b8e52cac124962528ade4b55659531a",
  "copy_index": {
    "from_index": "tracardi-session",
    "to_index": "tracardi-session",
    "multi": true,
    "script": "Map row = new HashMap();\nrow.putAll(ctx._source);\n//row.context.storage.local.tracardi-profile-id = <type text>;\nctx._source = [:];\nctx._source.putAll(row);"
  },
  "worker": "reindex",
  "conflicts": null,
  "asynchronous": true
}
```

- `from_index` property defines the name of the index to move data from
- `to_index` property defines the name of the target index
- `multi` indicates if given index is a multi index or not
- `script` is just a Painless script to reindex data
- `worker` is a name of needed worker function from tracardi/worker repo
- `custom_worker_required` is an array of type changes that cannot be handled by Painless scripting language
- `asynchronous` indicates whether the worker should execute its task apart from other workers, or in a synchronous
  chain - in the second case, schemas are executed in the order they have been put in the migration file.
