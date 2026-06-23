# Bob Shell CI/CD Automation Lab

## Automatización Inteligente de CI/CD: Cómo IBM Bob Orquesta Code Review y DevOps con Skills Personalizadas

Este laboratorio demuestra la integración de IBM Bob Shell en pipelines CI/CD usando GitHub Actions para automatizar code review, corrección de issues y testing.

## 🎯 Objetivo

Mostrar cómo Bob Shell puede:
- **Detectar** automáticamente problemas de seguridad, arquitectura y calidad
- **Corregir** código basándose en comentarios de review
- **Generar** tests automáticamente
- **Etiquetar** PRs e issues inteligentemente
- **Acelerar** el ciclo de desarrollo en 20-40x

## 📁 Estructura del Proyecto

```
.
├── .bob/                          # Bob skills personalizadas
│   └── skills/                    # Skills en formato oficial
│       ├── sql-injection-prevention/
│       ├── solid-principles/
│       ├── security-vulnerabilities/
│       ├── architecture-patterns/
│       └── code-quality/
│
├── .github/                       # GitHub Actions workflows
│   └── workflows/
│       ├── review-pr-with-skills.yml
│       ├── fix-pr-reviews-with-bob.yml
│       ├── fix-issues-with-bob.yml
│       ├── test-pr-with-bob.yml
│       └── label-new-prs.yml
│
├── demo-app/                      # Código BUENO (main branch)
│   ├── auth/
│   │   ├── login.py              # Login seguro
│   │   └── session.py            # Sesiones seguras
│   ├── database/
│   │   └── db_manager.py         # DB con prepared statements
│   └── utils/
│       └── validators.py         # Validación robusta
│
├── demo-app-bad/                  # Código MALO (dev branch)
│   └── auth/
│       └── login_bad.py          # Múltiples vulnerabilidades
│
├── DEMO_CASE_STUDY.md            # Caso de uso detallado
├── REQUIREMENTS.md                # Requisitos y costos
├── WORKFLOWS_EXPLANATION.md       # Explicación de workflows
└── README.md                      # Este archivo
```

## 🚀 Quick Start

### 1. Prerrequisitos

- Cuenta de GitHub
- Licencia de IBM watsonx Code Assistant
- API Key de Bob Shell

### 2. Configurar Secrets

En GitHub: `Settings → Secrets and variables → Actions`

```bash
# Requerido
BOBSHELL_API_KEY=tu-api-key-de-bob

# Opcional (GitHub lo proporciona automáticamente)
GITHUB_TOKEN=automático
```

### 3. Crear Labels

```bash
gh label create "review-with-bob" --color "0E8A16" --description "Trigger Bob code review"
gh label create "fix-with-bob" --color "D93F0B" --description "Trigger Bob to fix issues"
gh label create "test-with-bob" --color "1D76DB" --description "Trigger Bob to generate tests"
```

### 4. Probar el Sistema

```bash
# Crear PR de prueba
git checkout -b test-bob-integration
echo "test" > test.txt
git add test.txt
git commit -m "Test Bob integration"
git push origin test-bob-integration
gh pr create --title "Test Bob" --body "Testing Bob integration"

# Agregar label para activar Bob
gh pr edit <PR_NUMBER> --add-label "review-with-bob"

# Ver workflow ejecutándose
gh run list --workflow=review-pr-with-skills.yml
```

## 📋 Workflows Disponibles

### 1. Review PR with Skills
**Trigger:** PR con label `review-with-bob`

Bob analiza el código usando skills personalizadas y comenta en el PR con todos los hallazgos.

### 2. Fix PR Reviews with Bob
**Trigger:** Comentario de reviewer en PR

Bob lee el comentario y automáticamente corrige el código según el feedback.

### 3. Fix Issues with Bob
**Trigger:** Issue con label `fix-with-bob`

Bob crea un PR automáticamente para resolver el issue.

### 4. Test PR with Bob
**Trigger:** PR con label `test-with-bob`

Bob genera y ejecuta tests automáticamente.

### 5. Label PRs/Issues
**Trigger:** Nuevo PR o Issue

Bob analiza el contenido y aplica labels relevantes.

## 🎓 Demo Completo

Ver [DEMO_CASE_STUDY.md](DEMO_CASE_STUDY.md) para:
- Flujo completo de demostración
- Problemas intencionados en el código
- Resultados esperados
- Métricas de mejora

## 🔧 Skills Personalizadas

Las skills en `.bob/skills/` guían el análisis de Bob:

1. **sql-injection-prevention** - Previene SQL injection
2. **solid-principles** - Verifica principios SOLID
3. **security-vulnerabilities** - Detecta vulnerabilidades
4. **architecture-patterns** - Valida patrones de arquitectura
5. **code-quality** - Verifica calidad general

### Crear Nueva Skill

```bash
# Crear directorio
mkdir -p .bob/skills/my-new-skill

# Crear SKILL.md
cat > .bob/skills/my-new-skill/SKILL.md << 'EOF'
# Skill: My New Skill

## Description
[Description here]

## When to Use
- [Scenario 1]
- [Scenario 2]

## Guidelines
[Guidelines here]
EOF
```

Ver `../bob-skills-global/skill-creator/SKILL.md` para guía completa.

## 📊 Resultados Esperados

### Antes de Bob (Manual)
- Tiempo de review: 2-4 horas
- Issues encontrados: 10-15
- Tiempo de fix: 4-8 horas
- **Ciclo completo: 1-2 días**

### Después de Bob (Automatizado)
- Tiempo de review: 5-10 minutos
- Issues encontrados: 50+
- Tiempo de fix: 10-20 minutos
- **Ciclo completo: 30-60 minutos**

### Mejora
- **Velocidad**: 20-40x más rápido
- **Cobertura**: 3-5x más issues detectados
- **Consistencia**: 100%
- **Costo**: Reduce tiempo de developers en 80%

## 📚 Documentación

- [DEMO_CASE_STUDY.md](DEMO_CASE_STUDY.md) - Caso de uso completo
- [REQUIREMENTS.md](REQUIREMENTS.md) - Requisitos y costos
- [WORKFLOWS_EXPLANATION.md](WORKFLOWS_EXPLANATION.md) - Explicación detallada de workflows
- [.bob/skills/README.md](.bob/skills/README.md) - Guía de skills

## 🐛 Issues de Ejemplo

Ver [DEMO_ISSUES.md](DEMO_ISSUES.md) para issues de ejemplo que puedes crear para probar los workflows.

## 💡 Casos de Uso

### Caso 1: Review Automático
1. Developer crea PR
2. Agrega label `review-with-bob`
3. Bob analiza y comenta con hallazgos
4. Developer corrige basándose en feedback

### Caso 2: Fix Automático
1. Reviewer comenta: "Esta función tiene SQL injection"
2. Bob lee el comentario
3. Bob corrige el código automáticamente
4. Bob responde al comentario explicando el fix

### Caso 3: Resolver Issue
1. Se crea issue: "Login permite SQL injection"
2. Se agrega label `fix-with-bob`
3. Bob crea PR con la solución
4. Bob comenta en el issue con link al PR

## 🔒 Seguridad

- Todos los secrets están protegidos en GitHub
- Bob usa prepared statements para prevenir SQL injection
- Skills personalizadas validan seguridad en cada PR
- CodeQL analiza vulnerabilidades automáticamente

## 📈 Métricas

El laboratorio incluye código con:
- **15+ vulnerabilidades de seguridad**
- **20+ violaciones de SOLID**
- **10+ problemas de arquitectura**
- **30+ problemas de calidad**

Bob detectará y reportará todos estos problemas automáticamente.

## 🤝 Contribuir

Para agregar nuevas skills o mejorar workflows:

1. Fork el repositorio
2. Crea una branch: `git checkout -b feature/nueva-skill`
3. Sigue la estructura oficial de skills
4. Crea PR con descripción detallada

## 📞 Soporte

- **Bob Shell**: https://bob.ibm.com
- **IBM watsonx**: https://www.ibm.com/watsonx
- **GitHub Actions**: https://docs.github.com/actions

## 📄 Licencia

Este es un proyecto de demostración para fines educativos.

---

**Nota**: Este laboratorio requiere licencia de IBM watsonx Code Assistant para funcionar. El código con malas prácticas es intencional para demostración.