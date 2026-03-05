# CoPilotTest

## File Access Module

The `file_access` module fixes the **Consumption File Type Failure** by providing
utilities that validate file types and enable file access for users.

### Usage

```python
from file_access import enable_file_access

result = enable_file_access("alice", "report.pdf")
if result["access_granted"]:
    print(result["reason"])  # Access granted to 'report.pdf' for user 'alice'.
else:
    print(result["reason"])  # Explains why access was denied.
```

### Allowed File Types

| Category | Extensions |
|----------|-----------|
| text     | `.txt`, `.csv`, `.log` |
| document | `.pdf`, `.docx`, `.xlsx` |
| image    | `.png`, `.jpg`, `.jpeg`, `.gif` |
| data     | `.json`, `.xml`, `.yaml`, `.yml` |

You can restrict access to specific categories by passing `allowed_types`:

```python
result = enable_file_access("bob", "data.json", allowed_types=["data"])
```

### Running Tests

```bash
python -m pytest test_file_access.py -v
```