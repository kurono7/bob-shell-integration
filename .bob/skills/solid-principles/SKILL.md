# SOLID Principles Review Rules

Bob debe verificar que el código siga los principios SOLID de diseño orientado a objetos.

---

## Regla 1: Single Responsibility Principle (SRP)

**Severidad**: High

**Descripción**: 
Cada clase/módulo/función debe tener una única responsabilidad. Si una clase hace múltiples cosas no relacionadas, viola SRP.

**Indicadores de Violación**:
- Nombres de clase con "And", "Manager", "Handler", "Util"
- Clases con más de 300 líneas
- Métodos con más de 50 líneas
- Múltiples razones para cambiar la clase

**Ejemplo Incorrecto**:
```typescript
class UserManager {
  createUser(data) { /* ... */ }
  sendEmail(user) { /* ... */ }
  generateReport(user) { /* ... */ }
  validatePassword(password) { /* ... */ }
  logActivity(action) { /* ... */ }
}
```

**Ejemplo Correcto**:
```typescript
class UserService {
  createUser(data) { /* ... */ }
}

class EmailService {
  sendEmail(user) { /* ... */ }
}

class ReportGenerator {
  generateReport(user) { /* ... */ }
}

class PasswordValidator {
  validate(password) { /* ... */ }
}

class ActivityLogger {
  log(action) { /* ... */ }
}
```

**Acción**: 
Sugerir dividir la clase en clases más pequeñas, cada una con una responsabilidad única.

---

## Regla 2: Open/Closed Principle (OCP)

**Severidad**: Medium

**Descripción**: 
Las entidades deben estar abiertas para extensión pero cerradas para modificación. Usa herencia, interfaces o composición en lugar de modificar código existente.

**Indicadores de Violación**:
- Múltiples `if/else` o `switch` para tipos
- Modificar clases existentes para agregar funcionalidad
- Código que requiere cambios en múltiples lugares para nueva funcionalidad

**Ejemplo Incorrecto**:
```python
class PaymentProcessor:
    def process(self, payment_type, amount):
        if payment_type == "credit_card":
            # procesar tarjeta
        elif payment_type == "paypal":
            # procesar paypal
        elif payment_type == "bitcoin":
            # procesar bitcoin
        # Agregar nuevo método requiere modificar esta clase
```

**Ejemplo Correcto**:
```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        # procesar tarjeta

class PayPalPayment(PaymentMethod):
    def process(self, amount):
        # procesar paypal

class PaymentProcessor:
    def process(self, payment_method: PaymentMethod, amount):
        payment_method.process(amount)
```

**Acción**: 
Sugerir usar polimorfismo, strategy pattern o factory pattern para hacer el código extensible.

---

## Regla 3: Liskov Substitution Principle (LSP)

**Severidad**: High

**Descripción**: 
Los objetos de una subclase deben poder reemplazar objetos de la superclase sin romper la aplicación.

**Indicadores de Violación**:
- Subclases que lanzan excepciones no esperadas
- Subclases que no implementan métodos de la superclase
- Subclases que cambian el comportamiento esperado
- Uso de `instanceof` o `type()` para verificar tipos

**Ejemplo Incorrecto**:
```java
class Bird {
    void fly() {
        // volar
    }
}

class Penguin extends Bird {
    @Override
    void fly() {
        throw new UnsupportedOperationException("Penguins can't fly");
    }
}
```

**Ejemplo Correcto**:
```java
interface Bird {
    void move();
}

class FlyingBird implements Bird {
    void move() {
        fly();
    }
    
    void fly() {
        // volar
    }
}

class Penguin implements Bird {
    void move() {
        swim();
    }
    
    void swim() {
        // nadar
    }
}
```

**Acción**: 
Sugerir rediseñar la jerarquía de clases o usar composición en lugar de herencia.

---

## Regla 4: Interface Segregation Principle (ISP)

**Severidad**: Medium

**Descripción**: 
Los clientes no deben depender de interfaces que no usan. Divide interfaces grandes en interfaces más pequeñas y específicas.

**Indicadores de Violación**:
- Interfaces con muchos métodos (>5)
- Clases que implementan interfaces pero dejan métodos vacíos
- Métodos que lanzan `NotImplementedException`

**Ejemplo Incorrecto**:
```typescript
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  getPaid(): void;
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { throw new Error("Robots don't eat"); }
  sleep() { throw new Error("Robots don't sleep"); }
  getPaid() { throw new Error("Robots don't get paid"); }
}
```

**Ejemplo Correcto**:
```typescript
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

interface Payable {
  getPaid(): void;
}

class Human implements Workable, Eatable, Sleepable, Payable {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
  getPaid() { /* ... */ }
}

class Robot implements Workable {
  work() { /* ... */ }
}
```

**Acción**: 
Sugerir dividir la interfaz en interfaces más pequeñas y específicas.

---

## Regla 5: Dependency Inversion Principle (DIP)

**Severidad**: High

**Descripción**: 
Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones. Las abstracciones no deben depender de detalles.

**Indicadores de Violación**:
- Instanciación directa de clases concretas con `new`
- Dependencias hardcodeadas
- Falta de inyección de dependencias
- Acoplamiento fuerte entre módulos

**Ejemplo Incorrecto**:
```python
class MySQLDatabase:
    def save(self, data):
        # guardar en MySQL

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Dependencia hardcodeada
    
    def create_user(self, user):
        self.db.save(user)
```

**Ejemplo Correcto**:
```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        # guardar en MySQL

class PostgreSQLDatabase(Database):
    def save(self, data):
        # guardar en PostgreSQL

class UserService:
    def __init__(self, database: Database):  # Inyección de dependencia
        self.db = database
    
    def create_user(self, user):
        self.db.save(user)

# Uso
db = MySQLDatabase()
service = UserService(db)
```

**Acción**: 
Sugerir usar inyección de dependencias, interfaces/abstracciones, y dependency injection containers.

---

## Checklist de Review SOLID

Bob debe verificar:

- [ ] ¿Cada clase tiene una única responsabilidad clara?
- [ ] ¿Se puede extender funcionalidad sin modificar código existente?
- [ ] ¿Las subclases pueden reemplazar a sus superclases?
- [ ] ¿Las interfaces son pequeñas y específicas?
- [ ] ¿Se usan abstracciones en lugar de implementaciones concretas?
- [ ] ¿Hay inyección de dependencias en lugar de instanciación directa?
- [ ] ¿El código es testeable y desacoplado?

---

## Excepciones Permitidas

- **Scripts pequeños** (<100 líneas): Pueden violar SRP si son simples
- **DTOs/Models**: Pueden tener múltiples propiedades sin violar SRP
- **Builders/Factories**: Pueden tener múltiples métodos relacionados
- **Código legacy**: Documentar violaciones pero no bloquear si refactoring es muy costoso