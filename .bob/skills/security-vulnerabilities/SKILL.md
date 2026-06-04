# Security Vulnerabilities Review Rules

Bob debe identificar vulnerabilidades de seguridad comunes en el código.

---

## Regla 1: SQL Injection

**Severidad**: Critical

**Descripción**: 
Nunca concatenar strings para construir queries SQL. Siempre usar prepared statements o ORMs.

**Indicadores de Violación**:
- Concatenación de strings en queries SQL
- Uso de `format()` o template strings con input del usuario
- Queries dinámicas sin sanitización

**Ejemplo Incorrecto**:
```python
# VULNERABLE
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# VULNERABLE
query = "SELECT * FROM users WHERE id = " + user_id
```

**Ejemplo Correcto**:
```python
# SEGURO - Prepared statement
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    return db.execute(query, (username,))

# SEGURO - ORM
user = User.objects.filter(username=username).first()
```

**Acción**: 
Bloquear el PR y requerir uso de prepared statements o ORMs.

---

## Regla 2: Cross-Site Scripting (XSS)

**Severidad**: Critical

**Descripción**: 
Nunca insertar input del usuario directamente en HTML sin sanitización.

**Indicadores de Violación**:
- `innerHTML`, `dangerouslySetInnerHTML` con input del usuario
- Renderizado de HTML sin escape
- Uso de `eval()` con input del usuario

**Ejemplo Incorrecto**:
```javascript
// VULNERABLE
element.innerHTML = userInput;

// VULNERABLE
<div dangerouslySetInnerHTML={{__html: userComment}} />

// VULNERABLE
eval(userCode);
```

**Ejemplo Correcto**:
```javascript
// SEGURO - textContent
element.textContent = userInput;

// SEGURO - React escapa automáticamente
<div>{userComment}</div>

// SEGURO - Sanitización
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
element.innerHTML = clean;
```

**Acción**: 
Bloquear el PR y requerir sanitización o uso de métodos seguros.

---

## Regla 3: Hardcoded Credentials

**Severidad**: Critical

**Descripción**: 
Nunca hardcodear passwords, API keys, tokens o secrets en el código.

**Indicadores de Violación**:
- Variables con nombres como `password`, `api_key`, `secret`, `token`
- Strings que parecen passwords o keys
- Conexiones a DB con credenciales hardcodeadas

**Ejemplo Incorrecto**:
```python
# VULNERABLE
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "mypassword123"

# VULNERABLE
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="admin",
    password="admin123"
)
```

**Ejemplo Correcto**:
```python
# SEGURO - Variables de entorno
import os
API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# SEGURO - Archivo de configuración (no commiteado)
from config import get_secret
API_KEY = get_secret("API_KEY")
```

**Acción**: 
Bloquear el PR inmediatamente. Requerir uso de variables de entorno o secret managers.

---

## Regla 4: Insecure Deserialization

**Severidad**: High

**Descripción**: 
Nunca deserializar datos no confiables sin validación.

**Indicadores de Violación**:
- `pickle.loads()` con input del usuario
- `eval()`, `exec()` con input externo
- `JSON.parse()` sin validación

**Ejemplo Incorrecto**:
```python
# VULNERABLE
import pickle
data = pickle.loads(user_input)

# VULNERABLE
result = eval(user_expression)
```

**Ejemplo Correcto**:
```python
# SEGURO - JSON con validación
import json
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"}
    }
}

data = json.loads(user_input)
validate(instance=data, schema=schema)
```

**Acción**: 
Sugerir usar JSON en lugar de pickle, y siempre validar datos deserializados.

---

## Regla 5: Path Traversal

**Severidad**: High

**Descripción**: 
Validar y sanitizar rutas de archivos para prevenir acceso a archivos no autorizados.

**Indicadores de Violación**:
- Concatenación directa de rutas con input del usuario
- Falta de validación de `../` en rutas
- Acceso a archivos sin verificar permisos

**Ejemplo Incorrecto**:
```python
# VULNERABLE
def read_file(filename):
    path = f"/uploads/{filename}"
    with open(path, 'r') as f:
        return f.read()

# Usuario puede pasar: ../../../../etc/passwd
```

**Ejemplo Correcto**:
```python
# SEGURO
import os
from pathlib import Path

def read_file(filename):
    # Validar que no contenga path traversal
    if '..' in filename or filename.startswith('/'):
        raise ValueError("Invalid filename")
    
    # Usar path seguro
    base_dir = Path("/uploads")
    file_path = (base_dir / filename).resolve()
    
    # Verificar que esté dentro del directorio permitido
    if not str(file_path).startswith(str(base_dir)):
        raise ValueError("Access denied")
    
    with open(file_path, 'r') as f:
        return f.read()
```

**Acción**: 
Sugerir validación de rutas y uso de Path.resolve() para normalizar.

---

## Regla 6: Weak Cryptography

**Severidad**: High

**Descripción**: 
Usar algoritmos criptográficos modernos y seguros.

**Indicadores de Violación**:
- MD5, SHA1 para passwords
- DES, 3DES para encriptación
- Generación de números aleatorios con `random()` para seguridad

**Ejemplo Incorrecto**:
```python
# VULNERABLE
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# VULNERABLE
import random
token = random.randint(1000, 9999)
```

**Ejemplo Correcto**:
```python
# SEGURO - bcrypt para passwords
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# SEGURO - secrets para tokens
import secrets
token = secrets.token_urlsafe(32)

# SEGURO - SHA-256 para hashing (no passwords)
import hashlib
file_hash = hashlib.sha256(file_content).hexdigest()
```

**Acción**: 
Sugerir usar bcrypt/argon2 para passwords, secrets para tokens, y SHA-256+ para hashing.

---

## Regla 7: Insecure Direct Object References (IDOR)

**Severidad**: High

**Descripción**: 
Siempre verificar autorización antes de acceder a recursos.

**Indicadores de Violación**:
- Acceso a recursos usando IDs del usuario sin verificación
- Falta de checks de autorización
- Confiar en IDs del cliente

**Ejemplo Incorrecto**:
```python
# VULNERABLE
@app.route('/api/documents/<doc_id>')
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    return jsonify(doc.to_dict())
```

**Ejemplo Correcto**:
```python
# SEGURO
@app.route('/api/documents/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    
    # Verificar que el usuario tenga acceso
    if doc.owner_id != current_user.id:
        abort(403, "Access denied")
    
    return jsonify(doc.to_dict())
```

**Acción**: 
Sugerir agregar checks de autorización antes de acceder a recursos.

---

## Regla 8: Missing Authentication

**Severidad**: Critical

**Descripción**: 
Endpoints sensibles deben requerir autenticación.

**Indicadores de Violación**:
- Endpoints sin decoradores de autenticación
- APIs sin verificación de tokens
- Rutas admin sin protección

**Ejemplo Incorrecto**:
```python
# VULNERABLE
@app.route('/api/admin/users')
def list_users():
    return jsonify(User.query.all())
```

**Ejemplo Correcto**:
```python
# SEGURO
@app.route('/api/admin/users')
@login_required
@admin_required
def list_users():
    return jsonify(User.query.all())
```

**Acción**: 
Bloquear el PR y requerir autenticación en endpoints sensibles.

---

## Regla 9: Sensitive Data Exposure

**Severidad**: High

**Descripción**: 
No loggear ni exponer información sensible.

**Indicadores de Violación**:
- Logging de passwords, tokens, PII
- Respuestas de API con datos sensibles
- Stack traces en producción

**Ejemplo Incorrecto**:
```python
# VULNERABLE
logger.info(f"User login: {username} with password {password}")

# VULNERABLE
return jsonify({
    "user": user.to_dict(),
    "password_hash": user.password_hash,
    "ssn": user.ssn
})
```

**Ejemplo Correcto**:
```python
# SEGURO
logger.info(f"User login attempt: {username}")

# SEGURO
return jsonify({
    "user": {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
})
```

**Acción**: 
Sugerir remover logging de datos sensibles y filtrar respuestas de API.

---

## Regla 10: Insufficient Input Validation

**Severidad**: Medium

**Descripción**: 
Validar y sanitizar todo input del usuario.

**Indicadores de Violación**:
- Falta de validación de tipos
- Falta de validación de rangos
- Falta de sanitización de strings

**Ejemplo Incorrecto**:
```python
# VULNERABLE
@app.route('/api/users/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)  # No valida que sea número
    return jsonify(user.to_dict())
```

**Ejemplo Correcto**:
```python
# SEGURO
from marshmallow import Schema, fields, ValidationError

class UserIdSchema(Schema):
    user_id = fields.Int(required=True, validate=lambda x: x > 0)

@app.route('/api/users/<user_id>')
def get_user(user_id):
    try:
        validated = UserIdSchema().load({"user_id": int(user_id)})
        user = User.query.get(validated['user_id'])
        return jsonify(user.to_dict())
    except (ValueError, ValidationError):
        abort(400, "Invalid user ID")
```

**Acción**: 
Sugerir agregar validación de input usando schemas o validators.

---

## Checklist de Security Review

Bob debe verificar:

- [ ] ¿Se usan prepared statements para SQL?
- [ ] ¿Se sanitiza input antes de renderizar HTML?
- [ ] ¿No hay credenciales hardcodeadas?
- [ ] ¿Se valida input del usuario?
- [ ] ¿Se verifican permisos antes de acceder a recursos?
- [ ] ¿Endpoints sensibles requieren autenticación?
- [ ] ¿Se usa criptografía moderna (bcrypt, SHA-256+)?
- [ ] ¿No se loggea información sensible?
- [ ] ¿Se validan rutas de archivos?
- [ ] ¿Se usan HTTPS y headers de seguridad?

---

## Referencias

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE Top 25: https://cwe.mitre.org/top25/
- SANS Top 25: https://www.sans.org/top25-software-errors/