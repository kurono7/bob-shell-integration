# Skill: SQL Injection Prevention

## Description
Identifies and prevents SQL injection vulnerabilities by ensuring all database queries use parameterized statements or prepared statements instead of string concatenation.

## When to Use
- When reviewing code that constructs SQL queries
- When analyzing database access layers or repositories
- When auditing legacy code for security vulnerabilities
- During pre-deployment security reviews
- When implementing new database operations

## Guidelines

### 1. Identify Query Construction Patterns
Look for any code that builds SQL queries, including:
- Direct SQL string construction
- ORM query builders
- Stored procedure calls
- Dynamic query generation
- Raw SQL execution

### 2. Detect Dangerous Patterns
Flag queries that use string manipulation:
- String concatenation operators: `+`, `+=`, `concat()`
- String interpolation: f-strings, template literals `${}`, string templates
- String formatting: `format()`, `sprintf()`, `%` operator
- Direct variable insertion in SQL strings

### 3. Verify Proper Parameterization
Ensure all queries use safe methods:
- Prepared statements with placeholders: `?`, `:param`, `$1`
- ORM methods that automatically parameterize
- Query builders with explicit parameter binding
- Parameterized stored procedure calls

### 4. Validate Dynamic Identifiers
For dynamic table/column names:
- Maintain whitelist of allowed identifiers
- Validate against whitelist before use
- Never allow user input directly in identifiers
- Use ORM schema definitions when possible

### 5. Review Input Handling
Even with parameterization, verify:
- Input validation exists (type, format, length)
- Type checking is performed
- Length limits are enforced
- Business logic validation is applied

## Examples

### Bad Example - String Concatenation (Python)
```python
# VULNERABLE: Direct string concatenation
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# Attack: username = "admin' OR '1'='1"
# Result: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```

### Good Example - Parameterized Query (Python)
```python
# SECURE: Using parameterized query
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    return db.execute(query, (username,))

# Attack attempt is safely escaped
```

### Bad Example - String Interpolation (JavaScript)
```javascript
// VULNERABLE: Template literal with user input
async function getProduct(productId) {
  const query = `SELECT * FROM products WHERE id = ${productId}`;
  return await db.query(query);
}
```

### Good Example - Parameterized Query (JavaScript)
```javascript
// SECURE: Using parameterized query
async function getProduct(productId) {
  const query = 'SELECT * FROM products WHERE id = $1';
  return await db.query(query, [productId]);
}
```

### Bad Example - Dynamic Table Name (Java)
```java
// VULNERABLE: Table name from user input
public List<Record> getData(String tableName) {
    String query = "SELECT * FROM " + tableName;
    return jdbcTemplate.query(query, new RecordMapper());
}
```

### Good Example - Whitelist Validation (Java)
```java
// SECURE: Whitelist validation for table names
private static final Set<String> ALLOWED_TABLES = 
    Set.of("users", "products", "orders");

public List<Record> getData(String tableName) {
    if (!ALLOWED_TABLES.contains(tableName)) {
        throw new IllegalArgumentException("Invalid table name");
    }
    // Safe to use after validation
    String query = "SELECT * FROM " + tableName;
    return jdbcTemplate.query(query, new RecordMapper());
}
```

### Bad Example - ORM Misuse (Python/Django)
```python
# VULNERABLE: Using raw() with f-string
def search_users(name):
    return User.objects.raw(
        f"SELECT * FROM users WHERE name LIKE '%{name}%'"
    )
```

### Good Example - ORM Proper Use (Python/Django)
```python
# SECURE: Using ORM query methods
def search_users(name):
    return User.objects.filter(name__icontains=name)

# Or with parameterized raw query
def search_users_raw(name):
    return User.objects.raw(
        "SELECT * FROM users WHERE name LIKE %s",
        [f'%{name}%']
    )
```

## Common Pitfalls

### Pitfall 1: Partial Parameterization
```python
# STILL VULNERABLE: Table name not parameterized
table = user_input
query = f"SELECT * FROM {table} WHERE id = ?"
db.execute(query, (user_id,))
```
**Why it's dangerous**: Attacker can inject malicious table names or SQL commands.
**Fix**: Validate table name against whitelist before using it.

### Pitfall 2: Trusting "Internal" Data
```python
# VULNERABLE: Assuming internal data is safe
role = get_role_from_session()  # Could be manipulated
query = f"SELECT * FROM users WHERE role = '{role}'"
```
**Why it's dangerous**: Session data can be tampered with.
**Fix**: Always parameterize, regardless of data source.

### Pitfall 3: Second-Order SQL Injection
```python
# VULNERABLE: Storing unsanitized data, then using it
def store_username(username):
    # Stored safely with parameterization
    db.execute("INSERT INTO users (name) VALUES (?)", (username,))

def get_user_data(username):
    # VULNERABLE: Retrieved data used in query
    stored_name = db.execute("SELECT name FROM users WHERE id = ?", (user_id,))
    query = f"SELECT * FROM logs WHERE user = '{stored_name}'"
    return db.execute(query)
```
**Why it's dangerous**: Malicious data stored earlier is executed later.
**Fix**: Parameterize all queries, even with stored data.

### Pitfall 4: Escaping Instead of Parameterizing
```python
# VULNERABLE: Manual escaping is error-prone
def escape_sql(value):
    return value.replace("'", "''")

query = f"SELECT * FROM users WHERE name = '{escape_sql(username)}'"
```
**Why it's dangerous**: Easy to miss edge cases, encoding issues.
**Fix**: Use parameterized queries, not manual escaping.

### Pitfall 5: Concatenating Multiple Parameters
```python
# VULNERABLE: Building WHERE clause with concatenation
conditions = []
if name:
    conditions.append(f"name = '{name}'")
if email:
    conditions.append(f"email = '{email}'")

query = "SELECT * FROM users WHERE " + " AND ".join(conditions)
```
**Why it's dangerous**: Each condition is vulnerable.
**Fix**: Build parameterized conditions properly.

```python
# SECURE: Proper parameterized conditions
conditions = []
params = []

if name:
    conditions.append("name = ?")
    params.append(name)
if email:
    conditions.append("email = ?")
    params.append(email)

query = "SELECT * FROM users WHERE " + " AND ".join(conditions)
db.execute(query, params)
```

## Review Checklist
- [ ] All SQL queries use parameterized statements or prepared statements
- [ ] No string concatenation, interpolation, or formatting in query construction
- [ ] Dynamic identifiers (table/column names) are validated against whitelists
- [ ] Input validation exists before all database operations
- [ ] ORM methods are used correctly without raw SQL bypass
- [ ] No manual SQL escaping (use parameterization instead)
- [ ] Stored data is treated as untrusted in subsequent queries
- [ ] Error messages don't expose SQL structure or data

## Severity Levels

### Critical
- Direct string concatenation/interpolation with user input in SQL queries
- No parameterization in authentication or authorization queries
- Dynamic table/column names from user input without validation

### High
- Partial parameterization (some params safe, others not)
- Using raw SQL when ORM provides safe alternatives
- Missing input validation on database operations
- Second-order injection vulnerabilities

### Medium
- Inconsistent parameterization across codebase
- Manual SQL escaping instead of parameterization
- Overly permissive whitelists for dynamic identifiers

### Low
- Missing input validation on already-parameterized queries
- Verbose error messages that could aid attackers
- Lack of prepared statement reuse (performance issue)

## Auto-fix Suggestions

### Fix 1: String Concatenation to Parameterization
```python
# Replace this:
query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)

# With this:
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))
```

### Fix 2: Template Literal to Parameterization
```javascript
// Replace this:
const query = `SELECT * FROM products WHERE category = '${category}'`;
await db.query(query);

// With this:
const query = 'SELECT * FROM products WHERE category = $1';
await db.query(query, [category]);
```

### Fix 3: Dynamic Table Name
```python
# Replace this:
query = f"SELECT * FROM {table_name} WHERE id = ?"

# With this:
ALLOWED_TABLES = {'users', 'products', 'orders'}
if table_name not in ALLOWED_TABLES:
    raise ValueError(f"Invalid table: {table_name}")
query = f"SELECT * FROM {table_name} WHERE id = ?"
```

### Fix 4: ORM Raw Query
```python
# Replace this:
User.objects.raw(f"SELECT * FROM users WHERE name = '{name}'")

# With this:
User.objects.filter(name=name)
# Or if raw SQL is necessary:
User.objects.raw("SELECT * FROM users WHERE name = %s", [name])
```

## Testing for SQL Injection

### Test Inputs
Try these inputs to verify protection:
```
' OR '1'='1
'; DROP TABLE users; --
admin'--
' UNION SELECT * FROM passwords--
1' AND 1=1--
```

### Verification Steps
1. Attempt injection with test inputs
2. Verify query fails safely or escapes input
3. Check logs for attempted injection
4. Confirm no data leakage in errors
5. Test with automated security scanners

## Related Skills
- input-validation.md
- authentication-security.md
- database-security.md
- error-handling-security.md
- logging-security.md

## References
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- OWASP Top 10 A03:2021: https://owasp.org/Top10/A03_2021-Injection/