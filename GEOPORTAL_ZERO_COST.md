# GEOPORTAL SaaS: PLAN ZERO PRESUPUESTO
## Totalmente gratuito mientras crece

---

## 1. COSTO OPERATIVO MENSUAL

| Componente | Costo | Cómo |
|-----------|-------|------|
| **Frontend** | $0 | Vercel free tier |
| **Backend** | $0 | Railway free tier ($5/mes crédito) |
| **PostgreSQL + PostGIS** | $0 | Railway free tier (5GB) |
| **Redis Cache** | $0 | Valkey free tier en Railway |
| **Google Earth Engine** | $0 | API gratuita para research |
| **Auth0** | $0 | Free tier (7,500 users) |
| **Stripe** | 2.9% + $0.30 | Solo cuando hay pagos |
| **Email** | $0 | Sendgrid free tier |
| **Domain** | $0 | Usar subdomain de Railway/Vercel (upgrade después) |
| **DNS** | $0 | Cloudflare free |
| **Monitoring** | $0 | Sentry free tier |
| **TOTAL/MES** | **$0** | 100% gratuito |

**Nota importante:** Railway da $5/mes en créditos free tier. Eso cubre todo.

---

## 2. CÓMO FUNCIONA GRATIS

### Frontend: Vercel Free
```
✅ Deploya automáticamente desde GitHub
✅ HTTPS + CDN incluido
✅ Ilimitado en bandwidth
✅ Limit: 100 GB bandwidth/mes (suficiente para miles de usuarios)

URL: geomon.vercel.app
```

### Backend: Railway Free ($5/mes crédito)
```
✅ FastAPI runner
✅ PostgreSQL 5GB
✅ Redis pequeño
✅ Automático con GitHub

Crédito mensual: $5
Costo estimado: $2-3/mes (muy bajo)
Restante: $2-3 para buffer

URL: api.geomon.up.railway.app
```

### Database: PostgreSQL + PostGIS (Gratuito)
```
✅ Instalado en Railway free tier
✅ 5GB almacenamiento (más que suficiente)
✅ PostGIS extension (gratis, es parte de PostgreSQL)
✅ 1 base de datos

CREATE EXTENSION postgis;
→ Ahora tienes GIS full-stack
```

### APIs Externas: 100% Gratis
```
Google Earth Engine       → Free forever para research
Auth0                    → Free tier (7,500 users)
Sendgrid                 → Free tier (100 emails/día)
Stripe                   → Free, pagas solo con transacciones
Cloudflare DNS           → Free tier
Sentry                   → Free tier (error tracking)
OpenStreetMap Nominatim  → Free geocoding
```

---

## 3. ARQUITECTURA (ZERO COST)

```
USUARIO ESCRIBE EN NAVEGADOR:
"Analizar deforestación en Envigado 2021-2024"
        ↓
FRONTEND (React + Vite)
Deploy: Vercel (GRATIS)
URL: geomon.vercel.app
        ↓ HTTPS (gratis)
BACKEND (FastAPI)
Deploy: Railway ($5/mes crédito FREE)
URL: api.geomon.up.railway.app
        ├─ PostgreSQL 5GB (Railway, GRATIS)
        ├─ PostGIS extension (GRATIS)
        ├─ Redis small (Railway, GRATIS)
        └─ Claude Agent con function calling
        ↓
HERRAMIENTAS (todas GRATIS):
  ├─ Google Earth Engine API (GRATIS)
  ├─ Nominatim geocoding (GRATIS)
  ├─ Global Forest Watch (GRATIS)
  └─ Lógica pura Python (GRATIS)
        ↓
RESPUESTA JSON → FRONTEND RENDERIZA → USUARIO VE RESULTADO
```

**Costo total: $0** ✅

---

## 4. COMPARATIVO: GRATIS vs PAGADO

### Opción A: Gratis (ahora)
```
Vercel Free:         geomon.vercel.app
Railway Free:        api.geomon.up.railway.app
PostgreSQL 5GB:      Incluido
Límite Users:        Hasta que Railway diga (muy alto)
Costo/mes:           $0

Cuando cresca:
→ Upgrade Vercel a $20/mes (Pro)
→ Upgrade Railway a Plan Pro (después de generar ingresos)
```

### Opción B: Con presupuesto (más caro)
```
Vercel Pro:          $20/mes
Railway Pro:         $12/mes
PostgreSQL:          $15/mes
Redis:               $5/mes
Total:               $52/mes

Tú ahora: $0 ✅
```

---

## 5. LIMITACIONES GRATIS (y cuándo afectan)

| Limitación | Free | Cuándo importa | Solución |
|-----------|------|----------------|----------|
| Railway bandwidth | Limitado | 1000+ usuarios pesados | Upgrade a $12 |
| Vercel bandwidth | 100GB/mes | 10,000+ usuarios | Upgrade a $20 |
| PostgreSQL 5GB | 5GB almacenamiento | Con historial 20+ años | Expandir PostgreSQL |
| Requests/min | No hay limite real | N/A | N/A |
| Uptime | 99%+ | Bajo uso OK | OK |
| Cold starts | Si (5-10s inicial) | Primero pedido lento | OK en producción |

**Realidad:** Con usuarios reales pagando ($9/mes), puedes hacer upgrade en mes 2 sin problema.

---

## 6. PLAN DE SCALING (Gratuito → Pagado)

### MES 1-3: GRATIS
```
Usuarios: 1-20
Ingresos: $0-180
Gastos: $0
Margen: $0

Setup:
- Railway free
- Vercel free
- Todo local
```

### MES 4-6: HYBRID ($15/mes después de ingresos)
```
Usuarios: 20-100
Ingresos: $180-900
Gastos: $15/mes (upgrade Vercel a $20, Railway sigue free)
Margen: $165-885

Setup:
- Vercel Pro ($20/mes)
- Railway free (aún con crédito)
- PostgreSQL expandido
```

### MES 7+: FULL PAID ($52/mes)
```
Usuarios: 100+
Ingresos: $900+
Gastos: $52/mes
Margen: $848+

Setup:
- Vercel Pro ($20)
- Railway Pro ($12)
- PostgreSQL Pro ($15)
- Redis ($5)
```

**La progresión:** Gratis → $20 → $52. Escalas conforme creces.

---

## 7. SETUP ZERO PRESUPUESTO (Paso a paso)

### PASO 1: Crear Cuentas (30 minutos)
```
1. GitHub cuenta (si no tienes)
2. Vercel account (conectar GitHub)
3. Railway account (conectar GitHub)
4. Google Cloud account (Earth Engine, gratis)
5. Auth0 account (free tier)
6. Stripe account (free)
```

### PASO 2: Deploy Backend Automático (15 minutos)
```
1. Railway dashboard
2. "New Project" → "Deploy from GitHub"
3. Seleccionar repo geomon
4. Railway auto-detecta Python
5. Railway auto-crea PostgreSQL
6. Variables de entorno (.env)
7. Deploy automático

Resultado: api.geomon.up.railway.app funcional
```

### PASO 3: Deploy Frontend Automático (10 minutos)
```
1. Vercel dashboard
2. "New project" → Import from GitHub
3. Seleccionar repo geomon/frontend
4. Vercel auto-detecta Vite
5. Build settings: npm run build
6. Deploy automático

Resultado: geomon.vercel.app funcional
```

### PASO 4: PostgreSQL + PostGIS (10 minutos)
```
En Railway:
1. Crear Plugin: PostgreSQL
2. Railway asigna credenciales automáticas
3. Conectar desde FastAPI (SQLAlchemy)
4. En Python:
   from sqlalchemy import create_engine
   engine = create_engine("postgresql://...")

En PostgreSQL:
1. SSH a Railway
2. psql -d geomon
3. CREATE EXTENSION postgis;
4. Listo ✅
```

---

## 8. REPOSITORIO GITHUB (MISMO)

```
geomon/
├─ frontend/          ← Vercel auto-deploya
│  ├─ src/
│  ├─ package.json
│  └─ vite.config.js
│
├─ backend/           ← Railway auto-deploya
│  ├─ app/
│  ├─ requirements.txt
│  ├─ Procfile        ← Railway lo lee
│  └─ main.py
│
├─ .env.example
└─ README.md
```

**Clave:** Railway y Vercel leen `.env` y `requirements.txt` automáticamente. No necesitas hacer nada.

---

## 9. PRIMERAS 10 SEMANAS (GRATIS)

| Semana | Tarea | Costo | Deploy |
|--------|-------|-------|--------|
| 1-2 | Frontend UI | $0 | Vercel auto |
| 3-4 | Backend + DB | $0 | Railway auto |
| 5 | GEE Integration | $0 | Railway auto |
| 6 | Change Detection | $0 | Railway auto |
| 7 | Claude Agent | $0 | Railway auto |
| 8 | Auth + Stripe | $0 | Railway auto |
| 9 | Landing page | $0 | Vercel auto |
| 10 | Launch | $0 | Todo auto |

**Total: $0 en 10 semanas.** ✅

---

## 10. CUÁNDO PAGAR (La verdad)

### Necesitas presupuesto cuando:
```
✅ >1000 usuarios activos/mes
✅ >100GB bandwidth Vercel/mes
✅ >5GB datos PostgreSQL
✅ Quieres dominio custom (geomon.app)
✅ Quieres mejorar uptime a 99.99%
```

### En realidad:
```
Con 50 usuarios pagos ($9/mes):
- Ingresos: $450/mes
- Gastos: $0
- Margen: 100%

Con 100+ usuarios:
- Puedes permitirte upgrade a $52/mes
- Aún tienes 80%+ margen
```

---

## 11. CÓMO ACTUALIZAR CUANDO TENGAS INGRESOS

### Mes 3: Primer upgrade ($20)
```
Cuando veas $200+ en el banco:
1. Upgrade Vercel a Pro ($20/mes)
   - Mejor performance
   - Más bandwidth
   - Soporte prioritario

Costo: $20/mes
Ingresos: $180-300/mes (si todo va bien)
Margen: Aún 80%+
```

### Mes 6: Full upgrade ($52)
```
Cuando veas $500+ acumulado:
1. Vercel Pro: $20
2. Railway Pro: $12
3. PostgreSQL expandido: $15
4. Redis: $5
Total: $52/mes

Ingresos en mes 6: $450+/mes
Margen: 88%

Reinviertes en:
- Marketing (blog, ads)
- Features nuevas
- Soporte
```

---

## 12. DOMINIO GRATIS TEMPORAL

**Opción A: Subdominio gratuito (ahora)**
```
URL: geomon.vercel.app (Vercel)
URL: api.geomon.up.railway.app (Railway)
Totalmente funcional
Costo: $0
```

**Opción B: Dominio gratis con Freenom (ahora)**
```
.tk / .ml / .ga domains
geomon.tk
Costo: $0
Nota: No ideal para SaaS profesional, pero válido para MVP
```

**Opción C: Dominio custom (después de ingresos)**
```
Cuando tengas $100+ en caja:
- Compra geomon.app en Namecheap ($10/año)
- Cuesta 1 pago de usuario
- Vale mucho la pena
```

---

## 13. TEMPLATE PARA SONNET/OPUS (MISMO)

El template de prompts de la versión anterior funciona exactamente igual:

```
# TAREA: [Nombre]

## CONTEXTO
GeoMonitor (SaaS forestal, ZERO presupuesto)

## OBJETIVO
[Qué necesito]

## REQUIREMENTS
- Code unit tested
- Production-ready
- Sin presupuesto = sin dependencias pagas

## DELIVERABLE
1. Código
2. Tests
3. README
```

**Claude no necesita saber que es gratis. Sigue siendo production-ready.**

---

## 14. RESUMEN: ZERO COST = VENTAJA

✅ **Presión baja:** Si falla, no pierdes dinero
✅ **Escalable:** Upgrade cuando necesites
✅ **Aprendizaje:** Cambias stack si necesitas
✅ **Risk zero:** Comienzas sin riesgo
✅ **Ingreso pure:** Todo lo que ganes es margen

---

## 15. DIFERENCIAS CON VERSIÓN ANTERIOR

| Aspecto | Versión anterior | Zero cost |
|--------|------------------|-----------|
| **Vercel** | Pro ($20) | Free |
| **Railway** | $7/starter | Free ($5 crédito) |
| **PostgreSQL** | $15 | Free (en Railway) |
| **Redis** | $5 | Free (en Railway) |
| **Domain** | Considerado | Subdominio free |
| **Total/mes** | $27 | **$0** |

**Cambio único:** todo es free tier. Nada más cambia.

---

## 16. PLAN ES IDÉNTICO

- Mismas 10 semanas
- Mismo stack (React, FastAPI, PostgreSQL, Claude)
- Mismo template de prompts
- Mismo repositorio GitHub
- **Única diferencia:** $0 en lugar de $27

**Ejecución:**
1. Sigue plan original
2. Usa free tiers de Vercel + Railway
3. Cuando tengas ingresos → upgrade
4. Listo ✅

---

## RESUMEN EJECUTIVO

Hoy: **GRATIS**
- Vercel free
- Railway free
- PostgreSQL free
- APIs externas gratis

Después (mes 3-6): **$20-52** (con ingresos)
- Upgrade cuando tengas dinero
- Costo muy bajo
- Margen muy alto

**El plan funciona igual. Solo sin dinero de bolsillo inicial.**

¿Preguntas antes de empezar?
