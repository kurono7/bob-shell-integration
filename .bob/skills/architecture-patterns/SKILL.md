# Architecture Patterns Review Rules

Bob debe verificar que el código siga patrones de arquitectura sólidos y escalables.

---

## Regla 1: Separation of Concerns

**Severidad**: High

**Descripción**: 
Separar lógica de negocio, presentación y acceso a datos en capas distintas.

**Indicadores de Violación**:
- Lógica de negocio en controladores/vistas
- Queries SQL en componentes de UI
- Validación mezclada con presentación

**Ejemplo Incorrecto**:
```typescript
// MALO - Todo mezclado en el componente
function UserProfile() {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    // Acceso a datos en UI
    fetch('/api/users/1')
      .then(res => res.json())
      .then(data => {
        // Lógica de negocio en UI
        if (data.age < 18) {
          data.isMinor = true;
        }
        setUser(data);
      });
  }, []);
  
  return <div>{user?.name}</div>;
}
```

**Ejemplo Correcto**:
```typescript
// BUENO - Separación de capas

// services/userService.ts - Acceso a datos
export class UserService {
  async getUser(id: number): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
  }
}

// domain/userDomain.ts - Lógica de negocio
export class UserDomain {
  static isMinor(user: User): boolean {
    return user.age < 18;
  }
}

// components/UserProfile.tsx - Presentación
function UserProfile() {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    userService.getUser(1).then(setUser);
  }, []);
  
  const isMinor = user ? UserDomain.isMinor(user) : false;
  
  return <div>{user?.name} {isMinor && '(Minor)'}</div>;
}
```

**Acción**: 
Sugerir extraer lógica a servicios, dominios y repositorios apropiados.

---

## Regla 2: Dependency Injection

**Severidad**: Medium

**Descripción**: 
Usar inyección de dependencias en lugar de instanciación directa para mejorar testabilidad.

**Indicadores de Violación**:
- `new` dentro de clases
- Dependencias hardcodeadas
- Singletons globales

**Ejemplo Incorrecto**:
```python
# MALO
class OrderService:
    def __init__(self):
        self.db = Database()  # Dependencia hardcodeada
        self.email = EmailService()
    
    def create_order(self, order):
        self.db.save(order)
        self.email.send_confirmation(order)
```

**Ejemplo Correcto**:
```python
# BUENO
class OrderService:
    def __init__(self, db: Database, email: EmailService):
        self.db = db
        self.email = email
    
    def create_order(self, order):
        self.db.save(order)
        self.email.send_confirmation(order)

# Uso con DI container
container = Container()
container.register(Database, MySQLDatabase)
container.register(EmailService, SMTPEmailService)
order_service = container.resolve(OrderService)
```

**Acción**: 
Sugerir usar inyección de dependencias y considerar un DI container.

---

## Regla 3: Repository Pattern

**Severidad**: Medium

**Descripción**: 
Abstraer acceso a datos usando el patrón Repository para desacoplar lógica de negocio de la persistencia.

**Indicadores de Violación**:
- Queries SQL directas en servicios
- Lógica de negocio mezclada con acceso a datos
- Múltiples formas de acceder a la misma entidad

**Ejemplo Incorrecto**:
```typescript
// MALO
class UserService {
  async getUser(id: number) {
    // Acceso directo a DB en servicio
    const result = await db.query('SELECT * FROM users WHERE id = ?', [id]);
    return result[0];
  }
  
  async updateUser(id: number, data: any) {
    await db.query('UPDATE users SET name = ? WHERE id = ?', [data.name, id]);
  }
}
```

**Ejemplo Correcto**:
```typescript
// BUENO
interface IUserRepository {
  findById(id: number): Promise<User | null>;
  save(user: User): Promise<void>;
  update(user: User): Promise<void>;
}

class UserRepository implements IUserRepository {
  async findById(id: number): Promise<User | null> {
    const result = await db.query('SELECT * FROM users WHERE id = ?', [id]);
    return result[0] ? this.mapToUser(result[0]) : null;
  }
  
  async save(user: User): Promise<void> {
    await db.query('INSERT INTO users ...', [user]);
  }
  
  async update(user: User): Promise<void> {
    await db.query('UPDATE users ...', [user]);
  }
}

class UserService {
  constructor(private userRepo: IUserRepository) {}
  
  async getUser(id: number): Promise<User | null> {
    return this.userRepo.findById(id);
  }
}
```

**Acción**: 
Sugerir crear repositorios para abstraer acceso a datos.

---

## Regla 4: Service Layer

**Severidad**: Medium

**Descripción**: 
Encapsular lógica de negocio en una capa de servicios.

**Indicadores de Violación**:
- Lógica de negocio en controladores
- Controladores con más de 20 líneas
- Lógica duplicada entre controladores

**Ejemplo Incorrecto**:
```python
# MALO - Lógica en controlador
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    
    # Validación en controlador
    if not data.get('items'):
        return {'error': 'No items'}, 400
    
    # Cálculos en controlador
    total = sum(item['price'] * item['quantity'] for item in data['items'])
    
    # Acceso a datos en controlador
    order = Order(user_id=data['user_id'], total=total)
    db.session.add(order)
    db.session.commit()
    
    # Lógica de negocio en controlador
    if total > 100:
        send_email(data['user_id'], 'Big order!')
    
    return {'id': order.id}, 201
```

**Ejemplo Correcto**:
```python
# BUENO - Lógica en servicio

# services/order_service.py
class OrderService:
    def __init__(self, order_repo, email_service):
        self.order_repo = order_repo
        self.email_service = email_service
    
    def create_order(self, user_id, items):
        # Validación
        if not items:
            raise ValueError('No items')
        
        # Lógica de negocio
        total = self._calculate_total(items)
        order = Order(user_id=user_id, total=total, items=items)
        
        # Persistencia
        self.order_repo.save(order)
        
        # Reglas de negocio
        if total > 100:
            self.email_service.send_big_order_notification(user_id)
        
        return order
    
    def _calculate_total(self, items):
        return sum(item['price'] * item['quantity'] for item in items)

# controllers/order_controller.py
@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        order = order_service.create_order(
            request.json['user_id'],
            request.json['items']
        )
        return {'id': order.id}, 201
    except ValueError as e:
        return {'error': str(e)}, 400
```

**Acción**: 
Sugerir extraer lógica de negocio a servicios.

---

## Regla 5: DTO (Data Transfer Objects)

**Severidad**: Low

**Descripción**: 
Usar DTOs para transferir datos entre capas y validar input.

**Indicadores de Violación**:
- Pasar diccionarios/objetos genéricos entre capas
- Falta de validación de tipos
- Exposición de modelos de DB directamente

**Ejemplo Incorrecto**:
```typescript
// MALO
app.post('/api/users', (req, res) => {
  const user = req.body; // Cualquier estructura
  userService.createUser(user);
  res.json(user); // Expone modelo interno
});
```

**Ejemplo Correcto**:
```typescript
// BUENO
// dtos/CreateUserDto.ts
export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  name: string;
  
  @IsEmail()
  email: string;
  
  @IsInt()
  @Min(18)
  age: number;
}

// dtos/UserResponseDto.ts
export class UserResponseDto {
  id: number;
  name: string;
  email: string;
  
  static fromUser(user: User): UserResponseDto {
    return {
      id: user.id,
      name: user.name,
      email: user.email
      // No expone password_hash, etc.
    };
  }
}

app.post('/api/users', async (req, res) => {
  const dto = plainToClass(CreateUserDto, req.body);
  await validate(dto);
  
  const user = await userService.createUser(dto);
  res.json(UserResponseDto.fromUser(user));
});
```

**Acción**: 
Sugerir crear DTOs para validación y transferencia de datos.

---

## Regla 6: Event-Driven Architecture

**Severidad**: Low

**Descripción**: 
Usar eventos para desacoplar componentes en operaciones asíncronas.

**Indicadores de Violación**:
- Llamadas síncronas a múltiples servicios
- Acoplamiento fuerte entre módulos
- Operaciones lentas bloqueando requests

**Ejemplo Incorrecto**:
```python
# MALO - Acoplamiento fuerte
def create_user(user_data):
    user = User(**user_data)
    db.save(user)
    
    # Múltiples operaciones síncronas
    email_service.send_welcome_email(user)
    analytics_service.track_signup(user)
    crm_service.create_contact(user)
    
    return user
```

**Ejemplo Correcto**:
```python
# BUENO - Event-driven
from events import EventBus

def create_user(user_data):
    user = User(**user_data)
    db.save(user)
    
    # Emitir evento
    EventBus.publish('user.created', user)
    
    return user

# Handlers desacoplados
@EventBus.subscribe('user.created')
def send_welcome_email(user):
    email_service.send_welcome_email(user)

@EventBus.subscribe('user.created')
def track_signup(user):
    analytics_service.track_signup(user)

@EventBus.subscribe('user.created')
def sync_to_crm(user):
    crm_service.create_contact(user)
```

**Acción**: 
Sugerir usar eventos para operaciones asíncronas y desacoplamiento.

---

## Regla 7: API Versioning

**Severidad**: Medium

**Descripción**: 
Versionar APIs para mantener compatibilidad hacia atrás.

**Indicadores de Violación**:
- Cambios breaking en APIs existentes
- Falta de versionado en endpoints
- Modificación de contratos sin deprecation

**Ejemplo Incorrecto**:
```python
# MALO - Cambio breaking
@app.route('/api/users/<id>')
def get_user(id):
    # Cambió de devolver objeto a devolver array
    return jsonify([user.to_dict()])  # Breaking change!
```

**Ejemplo Correcto**:
```python
# BUENO - Versionado
@app.route('/api/v1/users/<id>')
def get_user_v1(id):
    return jsonify(user.to_dict())

@app.route('/api/v2/users/<id>')
def get_user_v2(id):
    # Nueva versión con cambios
    return jsonify({
        'data': user.to_dict(),
        'meta': {'version': 2}
    })
```

**Acción**: 
Sugerir versionar APIs y mantener versiones antiguas durante período de deprecation.

---

## Regla 8: Error Handling Strategy

**Severidad**: Medium

**Descripción**: 
Implementar manejo de errores consistente en toda la aplicación.

**Indicadores de Violación**:
- Try-catch sin logging
- Errores genéricos sin contexto
- Falta de error boundaries
- Stack traces en producción

**Ejemplo Incorrecto**:
```javascript
// MALO
async function getUser(id) {
  try {
    return await api.get(`/users/${id}`);
  } catch (e) {
    return null; // Silencia error
  }
}
```

**Ejemplo Correcto**:
```javascript
// BUENO
class AppError extends Error {
  constructor(message, statusCode, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
  }
}

async function getUser(id) {
  try {
    return await api.get(`/users/${id}`);
  } catch (error) {
    logger.error('Failed to fetch user', { id, error });
    
    if (error.response?.status === 404) {
      throw new AppError('User not found', 404);
    }
    
    throw new AppError('Failed to fetch user', 500);
  }
}

// Global error handler
app.use((error, req, res, next) => {
  logger.error(error);
  
  if (error.isOperational) {
    res.status(error.statusCode).json({
      error: error.message
    });
  } else {
    res.status(500).json({
      error: 'Internal server error'
    });
  }
});
```

**Acción**: 
Sugerir implementar estrategia de error handling consistente.

---

## Checklist de Architecture Review

Bob debe verificar:

- [ ] ¿Hay separación clara entre capas (UI, Service, Data)?
- [ ] ¿Se usa inyección de dependencias?
- [ ] ¿Hay repositorios para acceso a datos?
- [ ] ¿La lógica de negocio está en servicios?
- [ ] ¿Se usan DTOs para validación y transferencia?
- [ ] ¿Hay versionado de APIs?
- [ ] ¿El manejo de errores es consistente?
- [ ] ¿Se usan eventos para desacoplamiento?
- [ ] ¿El código es testeable?
- [ ] ¿La arquitectura es escalable?

---

## Patrones Recomendados por Tipo de Aplicación

### REST API:
- Controller → Service → Repository
- DTOs para input/output
- Middleware para autenticación
- Global error handler

### Microservicios:
- Event-driven architecture
- API Gateway
- Service discovery
- Circuit breaker pattern

### Frontend (React/Vue):
- Component → Hook/Composable → Service
- State management (Redux/Pinia)
- Error boundaries
- Code splitting

### Monolito Modular:
- Bounded contexts
- Shared kernel mínimo
- Event bus interno
- Módulos independientes