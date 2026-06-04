# Code Quality Review Rules

Bob debe verificar la calidad general del código y mejores prácticas de programación.

---

## Regla 1: Naming Conventions

**Severidad**: Low

**Descripción**: 
Usar nombres descriptivos y consistentes que revelen intención.

**Indicadores de Violación**:
- Nombres de una letra (excepto iteradores)
- Abreviaciones no estándar
- Nombres genéricos (data, info, temp, obj)
- Inconsistencia en convenciones

**Ejemplo Incorrecto**:
```python
# MALO
def calc(a, b, c):
    tmp = a * b
    res = tmp + c
    return res

x = calc(10, 20, 30)
```

**Ejemplo Correcto**:
```python
# BUENO
def calculate_total_price(unit_price, quantity, shipping_cost):
    subtotal = unit_price * quantity
    total = subtotal + shipping_cost
    return total

total_price = calculate_total_price(10, 20, 30)
```

**Convenciones por Lenguaje**:
- Python: `snake_case` para funciones/variables, `PascalCase` para clases
- JavaScript/TypeScript: `camelCase` para funciones/variables, `PascalCase` para clases
- Java: `camelCase` para métodos/variables, `PascalCase` para clases
- Constants: `UPPER_SNAKE_CASE` en todos los lenguajes

**Acción**: 
Sugerir renombrar con nombres más descriptivos.

---

## Regla 2: Function Length

**Severidad**: Medium

**Descripción**: 
Funciones deben ser cortas y hacer una sola cosa.

**Indicadores de Violación**:
- Funciones con más de 50 líneas
- Múltiples niveles de indentación (>3)
- Múltiples responsabilidades

**Ejemplo Incorrecto**:
```javascript
// MALO - Función muy larga
function processOrder(order) {
  // Validación (20 líneas)
  if (!order.items) throw new Error('No items');
  if (!order.customer) throw new Error('No customer');
  // ... más validaciones
  
  // Cálculos (20 líneas)
  let total = 0;
  for (let item of order.items) {
    total += item.price * item.quantity;
  }
  // ... más cálculos
  
  // Persistencia (20 líneas)
  db.orders.insert(order);
  db.inventory.update(order.items);
  // ... más operaciones DB
  
  // Notificaciones (20 líneas)
  sendEmail(order.customer);
  sendSMS(order.customer);
  // ... más notificaciones
}
```

**Ejemplo Correcto**:
```javascript
// BUENO - Funciones pequeñas y enfocadas
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  saveOrder(order, total);
  notifyCustomer(order);
}

function validateOrder(order) {
  if (!order.items) throw new Error('No items');
  if (!order.customer) throw new Error('No customer');
}

function calculateTotal(order) {
  return order.items.reduce((sum, item) => 
    sum + item.price * item.quantity, 0
  );
}

function saveOrder(order, total) {
  db.orders.insert({ ...order, total });
  db.inventory.update(order.items);
}

function notifyCustomer(order) {
  sendEmail(order.customer);
  sendSMS(order.customer);
}
```

**Acción**: 
Sugerir dividir función en funciones más pequeñas.

---

## Regla 3: Code Duplication (DRY)

**Severidad**: Medium

**Descripción**: 
Evitar duplicación de código (Don't Repeat Yourself).

**Indicadores de Violación**:
- Bloques de código idénticos o muy similares
- Lógica repetida en múltiples lugares
- Copy-paste programming

**Ejemplo Incorrecto**:
```python
# MALO - Código duplicado
def get_active_users():
    users = db.query("SELECT * FROM users WHERE active = 1")
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })
    return result

def get_admin_users():
    users = db.query("SELECT * FROM users WHERE role = 'admin'")
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })
    return result
```

**Ejemplo Correcto**:
```python
# BUENO - Código reutilizable
def map_users_to_dto(users):
    return [{
        'id': user.id,
        'name': user.name,
        'email': user.email
    } for user in users]

def get_users_by_condition(condition):
    users = db.query(f"SELECT * FROM users WHERE {condition}")
    return map_users_to_dto(users)

def get_active_users():
    return get_users_by_condition("active = 1")

def get_admin_users():
    return get_users_by_condition("role = 'admin'")
```

**Acción**: 
Sugerir extraer código común a funciones reutilizables.

---

## Regla 4: Magic Numbers and Strings

**Severidad**: Low

**Descripción**: 
Reemplazar números y strings mágicos con constantes nombradas.

**Indicadores de Violación**:
- Números literales en código (excepto 0, 1, -1)
- Strings repetidos
- Valores sin contexto

**Ejemplo Incorrecto**:
```typescript
// MALO
function calculateDiscount(price: number, customerType: string) {
  if (customerType === 'premium') {
    return price * 0.15;
  } else if (customerType === 'regular') {
    return price * 0.05;
  }
  return 0;
}

if (user.age < 18) {
  // ...
}
```

**Ejemplo Correcto**:
```typescript
// BUENO
const CUSTOMER_TYPES = {
  PREMIUM: 'premium',
  REGULAR: 'regular'
} as const;

const DISCOUNT_RATES = {
  PREMIUM: 0.15,
  REGULAR: 0.05,
  NONE: 0
} as const;

const MINIMUM_AGE = 18;

function calculateDiscount(price: number, customerType: string) {
  if (customerType === CUSTOMER_TYPES.PREMIUM) {
    return price * DISCOUNT_RATES.PREMIUM;
  } else if (customerType === CUSTOMER_TYPES.REGULAR) {
    return price * DISCOUNT_RATES.REGULAR;
  }
  return DISCOUNT_RATES.NONE;
}

if (user.age < MINIMUM_AGE) {
  // ...
}
```

**Acción**: 
Sugerir extraer valores a constantes con nombres descriptivos.

---

## Regla 5: Comments and Documentation

**Severidad**: Low

**Descripción**: 
Código debe ser auto-explicativo. Comentarios deben explicar "por qué", no "qué".

**Indicadores de Violación**:
- Comentarios que repiten el código
- Código comentado (dead code)
- Falta de documentación en APIs públicas
- Comentarios obsoletos

**Ejemplo Incorrecto**:
```java
// MALO
// Incrementa i en 1
i++;

// Loop through users
for (User user : users) {
    // Check if user is active
    if (user.isActive()) {
        // Add to list
        activeUsers.add(user);
    }
}

// Old implementation
// function oldWay() { ... }
```

**Ejemplo Correcto**:
```java
// BUENO
i++;  // Código auto-explicativo, no necesita comentario

// Filtra usuarios activos
List<User> activeUsers = users.stream()
    .filter(User::isActive)
    .collect(Collectors.toList());

/**
 * Calcula el precio con descuento aplicando reglas de negocio complejas.
 * 
 * NOTA: El descuento se aplica ANTES de impuestos debido a regulación fiscal
 * vigente desde 2024 (ver ticket JIRA-1234).
 * 
 * @param basePrice Precio base sin descuentos
 * @param customer Cliente con información de membresía
 * @return Precio final con descuento aplicado
 */
public double calculateDiscountedPrice(double basePrice, Customer customer) {
    // Implementación
}
```

**Acción**: 
Sugerir remover comentarios obvios, eliminar código comentado, y agregar documentación donde sea necesario.

---

## Regla 6: Error Handling

**Severidad**: High

**Descripción**: 
Manejar errores apropiadamente, no silenciarlos.

**Indicadores de Violación**:
- Try-catch vacíos
- Catch genérico sin logging
- Retornar null en lugar de lanzar excepción
- No propagar errores

**Ejemplo Incorrecto**:
```python
# MALO
try:
    result = risky_operation()
except:
    pass  # Silencia error

def get_user(id):
    try:
        return db.get(id)
    except:
        return None  # Pierde información del error
```

**Ejemplo Correcto**:
```python
# BUENO
import logging

try:
    result = risky_operation()
except SpecificException as e:
    logging.error(f"Operation failed: {e}", exc_info=True)
    raise  # Re-lanza para que caller maneje

def get_user(id):
    try:
        return db.get(id)
    except DatabaseError as e:
        logging.error(f"Failed to get user {id}: {e}")
        raise UserNotFoundError(f"User {id} not found") from e
```

**Acción**: 
Sugerir logging apropiado y manejo explícito de errores.

---

## Regla 7: Nested Conditionals

**Severidad**: Medium

**Descripción**: 
Evitar anidamiento excesivo de condicionales.

**Indicadores de Violación**:
- Más de 3 niveles de indentación
- Múltiples if-else anidados
- Lógica difícil de seguir

**Ejemplo Incorrecto**:
```javascript
// MALO
function processPayment(user, amount) {
  if (user) {
    if (user.isActive) {
      if (amount > 0) {
        if (user.balance >= amount) {
          if (user.paymentMethod) {
            // Procesar pago
            return true;
          } else {
            return false;
          }
        } else {
          return false;
        }
      } else {
        return false;
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}
```

**Ejemplo Correcto**:
```javascript
// BUENO - Guard clauses
function processPayment(user, amount) {
  if (!user) return false;
  if (!user.isActive) return false;
  if (amount <= 0) return false;
  if (user.balance < amount) return false;
  if (!user.paymentMethod) return false;
  
  // Procesar pago
  return true;
}

// O mejor aún, con excepciones
function processPayment(user, amount) {
  validateUser(user);
  validateAmount(amount);
  validateBalance(user, amount);
  validatePaymentMethod(user);
  
  return executePayment(user, amount);
}
```

**Acción**: 
Sugerir usar guard clauses o extraer validaciones a funciones.

---

## Regla 8: Variable Scope

**Severidad**: Low

**Descripción**: 
Declarar variables en el scope más pequeño posible.

**Indicadores de Violación**:
- Variables declaradas al inicio de funciones largas
- Variables usadas solo en un bloque pero declaradas fuera
- Variables globales innecesarias

**Ejemplo Incorrecto**:
```python
# MALO
def process_data():
    result = None
    temp = None
    counter = 0
    
    # 50 líneas de código...
    
    if condition:
        temp = calculate()
        result = temp * 2
    
    return result
```

**Ejemplo Correcto**:
```python
# BUENO
def process_data():
    # 50 líneas de código...
    
    if condition:
        temp = calculate()
        result = temp * 2
        return result
    
    return None
```

**Acción**: 
Sugerir mover declaraciones de variables más cerca de su uso.

---

## Regla 9: Immutability

**Severidad**: Low

**Descripción**: 
Preferir inmutabilidad cuando sea posible.

**Indicadores de Violación**:
- Mutación de parámetros
- Uso de `let` cuando `const` es suficiente
- Modificación de objetos compartidos

**Ejemplo Incorrecto**:
```javascript
// MALO
function addDiscount(product, discount) {
  product.price = product.price * (1 - discount);  // Muta parámetro
  return product;
}

let total = 0;  // Debería ser const
total = calculateTotal();
```

**Ejemplo Correcto**:
```javascript
// BUENO
function addDiscount(product, discount) {
  return {
    ...product,
    price: product.price * (1 - discount)
  };
}

const total = calculateTotal();
```

**Acción**: 
Sugerir usar const y evitar mutaciones.

---

## Regla 10: Code Complexity

**Severidad**: High

**Descripción**: 
Mantener complejidad ciclomática baja (<10).

**Indicadores de Violación**:
- Múltiples if/else/switch
- Loops anidados
- Múltiples return statements
- Lógica booleana compleja

**Ejemplo Incorrecto**:
```python
# MALO - Complejidad ciclomática: 15
def calculate_price(product, customer, season, promo_code):
    price = product.base_price
    
    if customer.is_premium:
        if season == 'winter':
            price *= 0.8
        elif season == 'summer':
            price *= 0.9
        else:
            price *= 0.95
    else:
        if season == 'winter':
            price *= 0.9
        elif season == 'summer':
            price *= 0.95
    
    if promo_code:
        if promo_code == 'SAVE10':
            price *= 0.9
        elif promo_code == 'SAVE20':
            price *= 0.8
        elif promo_code == 'SAVE30':
            price *= 0.7
    
    if customer.orders_count > 10:
        price *= 0.95
    
    return price
```

**Ejemplo Correcto**:
```python
# BUENO - Complejidad reducida
SEASONAL_DISCOUNTS = {
    ('premium', 'winter'): 0.8,
    ('premium', 'summer'): 0.9,
    ('premium', 'other'): 0.95,
    ('regular', 'winter'): 0.9,
    ('regular', 'summer'): 0.95,
}

PROMO_DISCOUNTS = {
    'SAVE10': 0.9,
    'SAVE20': 0.8,
    'SAVE30': 0.7,
}

def calculate_price(product, customer, season, promo_code):
    price = product.base_price
    price = apply_seasonal_discount(price, customer, season)
    price = apply_promo_discount(price, promo_code)
    price = apply_loyalty_discount(price, customer)
    return price

def apply_seasonal_discount(price, customer, season):
    customer_type = 'premium' if customer.is_premium else 'regular'
    season_key = season if season in ['winter', 'summer'] else 'other'
    discount = SEASONAL_DISCOUNTS.get((customer_type, season_key), 1.0)
    return price * discount

def apply_promo_discount(price, promo_code):
    discount = PROMO_DISCOUNTS.get(promo_code, 1.0)
    return price * discount

def apply_loyalty_discount(price, customer):
    return price * 0.95 if customer.orders_count > 10 else price
```

**Acción**: 
Sugerir refactorizar usando estrategias, tablas de lookup, o extraer funciones.

---

## Checklist de Code Quality Review

Bob debe verificar:

- [ ] ¿Los nombres son descriptivos y consistentes?
- [ ] ¿Las funciones son cortas (<50 líneas)?
- [ ] ¿No hay código duplicado?
- [ ] ¿Los magic numbers están en constantes?
- [ ] ¿Los comentarios explican "por qué", no "qué"?
- [ ] ¿Los errores se manejan apropiadamente?
- [ ] ¿No hay anidamiento excesivo?
- [ ] ¿Las variables tienen el scope mínimo?
- [ ] ¿Se prefiere inmutabilidad?
- [ ] ¿La complejidad ciclomática es baja?

---

## Métricas de Calidad

Bob debe reportar:
- **Complejidad Ciclomática**: <10 (bueno), 10-20 (aceptable), >20 (refactorizar)
- **Longitud de Función**: <50 líneas (bueno), 50-100 (revisar), >100 (dividir)
- **Duplicación**: <3% (excelente), 3-5% (bueno), >5% (mejorar)
- **Cobertura de Tests**: >80% (bueno), 60-80% (aceptable), <60% (insuficiente)