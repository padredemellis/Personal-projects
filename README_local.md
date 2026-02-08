# 📄 Documentación Actualizada - COMPLETA



**Versión:** 2.1  
**Fecha:** 2026-02-06  
**Autores:** Emanuel Romero  
**Documento de:** Decisiones Arquitectónicas y Justificaciones Técnicas

---

## Índice

1. [Introducción](#introducción)
2. [Cambios Fundamentales en las Reglas de Negocio](#cambios-fundamentales-en-las-reglas-de-negocio)
3. [Decisiones de Arquitectura de Datos](#decisiones-de-arquitectura-de-datos)
4. [Decisiones de Lógica de Negocio](#decisiones-de-lógica-de-negocio)
5. [Decisiones de Experiencia de Usuario](#decisiones-de-experiencia-de-usuario)
6. [Decisiones de Seguridad y Transacciones](#decisiones-de-seguridad-y-transacciones)
7. [Estructura del Proyecto](#estructura-del-proyecto)
8. [Casos de Uso Definidos](#casos-de-uso-definidos)
9. [Constantes del Juego](#constantes-del-juego)
10. [Decisiones de Implementación](#decisiones-de-implementación)
11. [Progreso de Implementación](#progreso-de-implementación)
12. [Próximos Pasos](#próximos-pasos)

---

## Introducción

Este documento complementa la documentación técnica original del MVP de Trivia, registrando todas las decisiones arquitectónicas tomadas durante la fase de diseño detallado e implementación.

### Objetivo del Documento

- Documentar cambios en las reglas de negocio respecto al diseño original
- Justificar decisiones técnicas tomadas
- Registrar preguntas críticas y sus respuestas
- Servir como referencia para el equipo de desarrollo
- Facilitar futuras refactorizaciones
- **Trackear progreso de implementación**

### Contexto

Durante la fase de refinamiento arquitectónico, se identificaron contradicciones y gaps en el diseño original que requerían decisiones explícitas. Este documento registra el proceso de toma de decisiones, las justificaciones técnicas, y el progreso de implementación.

---

## Cambios Fundamentales en las Reglas de Negocio

### 1. Sistema de Vidas Global vs Game Over por Nodo

**Documentación Original:**
- Un jugador responde preguntas de un nodo
- Si falla 3 veces → Game Over total
- No hay concepto de "vidas globales"
- No hay dificultad progresiva

**Nueva Visión (Pivote):**
- Sistema de vidas que persiste entre nodos
- La dificultad cambia según el número de nodo
- Perder en un nodo ≠ Game Over (solo pierdes 1 vida)
- Game Over ocurre cuando vidas = 0

**Justificación del Cambio:**

Este cambio representa un **pivote en las reglas de negocio** motivado por:

1. **Experiencia de Usuario Mejorada:**
   - El sistema original era demasiado punitivo (3 errores = perder todo)
   - El nuevo sistema permite progreso gradual y reduce frustración
   - Aumenta el tiempo de juego y engagement del usuario

2. **Modelo de Progresión Más Escalable:**
   - Permite implementar mecánicas futuras (tienda, power-ups)
   - Las vidas se convierten en un recurso gestionable
   - Facilita monetización futura (comprar vidas, revivir, etc.)

3. **Mayor Profundidad de Juego:**
   - Introduce decisiones estratégicas (¿intento nodos difíciles o conservo vidas?)
   - Crea tensión narrativa (última vida = alto riesgo)
   - Permite diferentes estilos de juego (conservador vs arriesgado)

**Impacto en la Arquitectura:**

Este cambio requirió rediseñar:
- El modelo de datos `Player` (agregar campo `lives`)
- La lógica de `GameEngine` (evaluar vidas antes de iniciar nodo)
- Los casos de uso (separar `FailNodeUseCase` de `GameOverUseCase`)
- La persistencia de datos (guardar vidas en Firestore)

---

### 2. Sistema de Dificultad Progresiva

**Decisión Tomada:**

**Dificultad = Umbral de Éxito (Opción A)**

**Reglas Implementadas:**
- **Nodos 1-10 (Fácil):** Requieren 1 de 3 respuestas correctas para pasar
- **Nodos 11-20 (Medio):** Requieren 2 de 3 respuestas correctas para pasar
- **Nodos 21-30 (Difícil):** Requieren 3 de 5 respuestas correctas para pasar

**Alternativas Consideradas:**

| Opción | Descripción | ¿Por qué NO se eligió? |
|--------|-------------|------------------------|
| **Opción B: Dificultad = Complejidad de Preguntas** | Preguntas más difíciles en nodos avanzados, mismo umbral | Requiere clasificar manualmente 1500 preguntas (50 por tema × 6 temas × 5 niveles de dificultad). Fuera del alcance del MVP. |
| **Opción C: Dificultad = Ambas** | Preguntas MÁS duras Y umbrales MÁS exigentes | Combina la complejidad de B con el desarrollo de A. Sobrecarga técnica para el MVP. |

**Justificación de la Elección:**

1. **Simplicidad de Implementación:**
   - El umbral se calcula con una función simple (`getRequiredCorrectAnswers(nodeId)`)
   - No requiere curación manual de preguntas
   - Las preguntas pueden ser del mismo pool (random por tema)

2. **Progresión Clara para el Usuario:**
   - El jugador entiende inmediatamente el desafío ("necesito 2 de 3")
   - La dificultad es objetiva, no subjetiva
   - Permite mostrar feedback claro ("llevas 1 de 2 correctas")

3. **Escalabilidad Futura:**
   - Si más adelante queremos agregar Opción B, podemos hacerlo sin romper la lógica existente
   - Podemos introducir un campo `difficulty` en las preguntas gradualmente
   - La arquitectura soporta ambas mecánicas simultáneamente

**Relación con Personajes (Fuera del MVP):**

Se decidió que en futuras versiones:
- Cada rango de dificultad desbloquea un personaje
- El personaje "hace las preguntas" (diseño narrativo)
- Para el MVP: los personajes NO se implementan

**Pregunta Crítica Resuelta:**

> **¿Puede cambiar la dificultad de un nodo con el tiempo?**

**Respuesta:** NO. Para el MVP, la dificultad es **determinística** basada en el `nodeId`. Esto permite cálculo dinámico y evita almacenar datos redundantes.

---

## Decisiones de Arquitectura de Datos

### 3. Persistencia del Estado de Partida

**Pregunta Crítica:**

> **Escenario:** Jugador está en Nodo 15, respondió 1 correcta y 1 incorrecta, cierra la app.  
> **¿Qué debe pasar cuando vuelve a abrir la app?**

**Decisión Tomada:**

✅ **Partidas guardables en medio de un nodo**

El jugador debe poder continuar exactamente donde estaba.

**Alternativa Descartada:**

❌ Un nodo es una sesión atómica (si cierras la app, pierdes el progreso del nodo)

**Justificación:**

1. **Experiencia de Usuario:**
   - Los usuarios móviles frecuentemente interrumpen apps (llamadas, notificaciones, batería)
   - Perder progreso por interrupciones genera frustración
   - La competencia (apps de trivia populares) permite guardar progreso

2. **Modelo de Juego:**
   - Si un nodo puede tener 5 preguntas (nodos 21-30), forzar completitud atómica es excesivo
   - Permite sesiones de juego más cortas y flexibles
   - Reduce la presión sobre el usuario

3. **Viabilidad Técnica:**
   - Firestore soporta esta funcionalidad nativamente
   - El costo de almacenamiento es mínimo (una sesión = ~1KB)
   - Permite sincronización multi-dispositivo

**Implementación:**

Se creó el modelo `GameSession` que persiste:

```
GameSession:
- sessionId: string (identificador único)
- userId: string (quién está jugando)
- currentNodeId: int (1-30)
- correctCount: int (respuestas correctas hasta ahora)
- incorrectCount: int (respuestas incorrectas hasta ahora)
- questionsShownIds: lista de strings (preguntas ya mostradas)
- answersGiven: mapa {questionId: bool} (historial de respuestas)
- attemptNumber: int (¿primer, segundo, tercer intento del nodo?)
- createdAt: fecha/hora
- lastUpdated: fecha/hora
```

**Pregunta Crítica Resuelta:**

> **¿Por qué `answersGiven` si ya tienes `questionsShownIds`?**

**Respuesta:**

- **`questionsShownIds`:** Previene mostrar la MISMA pregunta dos veces en el MISMO intento
- **`answersGiven`:** Implementa el sistema anti-repetición GLOBAL (una pregunta correcta no se vuelve a mostrar nunca)

**Ejemplo:**
```
Usuario responde pregunta "q_123" correctamente → answersGiven["q_123"] = true
Usuario falla el nodo y lo reintenta → "q_123" NO aparece
Usuario responde pregunta "q_456" incorrectamente → answersGiven["q_456"] = false
Usuario falla el nodo y lo reintenta → "q_456" PUEDE aparecer de nuevo
```

---

### 4. Modelo de Datos: ¿Guardar `requiredCorrect` en GameSession?

**Pregunta Crítica:**

> **¿Necesitas guardar `requiredCorrect` y `totalQuestionsNeeded` en la sesión, o los calculas con `game_rules.getRequiredCorrectAnswers(currentNodeId)`?**

**Decisión Tomada:**

✅ **Opción B: CALCULAR dinámicamente (para el MVP)**

**Plan Futuro:** Migrar a Opción A (guardarlo) en versiones posteriores.

**Estructura de GameSession (MVP):**

```
GameSession en Firestore:
{
  sessionId: "session_abc123",
  userId: "user_xyz",
  currentNodeId: 15,
  correctCount: 1,
  incorrectCount: 1,
  questionsShownIds: ["q_245", "q_891"],
  answersGiven: {
    "q_245": true,
    "q_891": false
  },
  attemptNumber: 1,
  createdAt: "2026-02-05T10:30:00Z",
  lastUpdated: "2026-02-05T10:35:00Z"
}

// En el código:
int requiredCorrect = GameRules.getRequiredCorrectAnswers(session.currentNodeId); // Retorna 2
```

**Justificación:**

**Para el MVP (Opción B - Calcular):**

✅ **Ventajas:**
- Menos datos en Firestore (más barato, más rápido)
- Fuente única de verdad (DRY - Don't Repeat Yourself)
- Cambiar las reglas afecta a todos instantáneamente
- Más simple de implementar

❌ **Desventajas:**
- Si cambias las reglas, afectas sesiones en progreso
- Ejemplo: Usuario empezó nodo 15 con reglas "2/3", cambias a "3/5", inconsistencia
- Dependencia: siempre necesitas `game_rules.dart` para interpretar la sesión

**Por qué es aceptable para el MVP:**

1. **Las reglas NO cambiarán durante el desarrollo del MVP** (período de 3 semanas)
2. **No habrá usuarios reales** durante el MVP (solo pruebas del equipo)
3. **Es más simple y rápido de implementar** (prioridad: velocidad de desarrollo)

**Plan de Migración Futura:**

Cuando el juego esté en producción con usuarios reales:

1. Agregar campos a `GameSession`:
   ```dart
   requiredCorrect: int
   totalQuestionsNeeded: int
   ```

2. Migración de datos:
   - Script para actualizar sesiones existentes
   - Calcular valores basados en `currentNodeId` y guardarlos

3. Modificar `StartNodeUseCase` para guardar estos valores al crear la sesión

**Ventajas de migrar después del MVP:**

- Respeta las reglas originales de sesiones antiguas
- Permite ajustar dificultades según feedback de usuarios sin romper partidas en progreso
- Más fácil auditar: "¿Con qué reglas jugó este usuario?"

---

### 5. Firestore: Transacciones Atómicas

**Pregunta Crítica:**

> **¿Qué operaciones DEBEN ser atómicas?**

**Decisión Tomada:**

Marcadas como ATÓMICAS:
- ✅ Responder una pregunta (actualizar contador + marcar pregunta usada)
- ✅ Fallar un nodo (restar vida + resetear sesión + actualizar progreso)
- ✅ Completar un nodo (sumar puntos + desbloquear siguiente + guardar progreso)

**Nivel de Transaccionalidad Elegido:**

Se implementará usando `Firestore.runTransaction()` para las operaciones críticas.

**Justificación:**

**Escenario Crítico Analizado:**

```
Usuario completa Nodo 10 (último del rango fácil)
Sistema debe:
1. Sumar 100 puntos
2. Marcar nodo 10 como completado
3. Desbloquear nodo 11
4. Dar recompensa de monedas (100)
5. Borrar la sesión activa
6. Actualizar estadísticas

[CRASH después del paso 3]

Resultado SIN transacción:
✓ Puntos sumados
✓ Nodo 10 marcado completo
✓ Nodo 11 desbloqueado
✗ NO recibió monedas (pérdida de recompensa)
✗ Sesión NO borrada (basura en Firestore)
✗ Estadísticas NO actualizadas

¿Esto es aceptable? NO.
```

**Pregunta de Diseño:**

> **¿Necesitas una operación `completeNodeTransaction()` que haga TODAS las escrituras atómicas?**

**Respuesta: SÍ, usando Opción C (Balance)**

**Opción C: Todo en el Player, Sesión aparte**

```dart
// Pseudocódigo
Future<void> completeNode() async {
  // Transacción atómica para datos críticos del jugador
  await Firebase.runTransaction(() {
    updatePlayer({
      points: currentPoints + earnedPoints,
      completedNodes: [...completedNodes, currentNodeId],
      unlockedNodes: [...unlockedNodes, currentNodeId + 1],
      coins: currentCoins + coinsReward,
      stats: updatedStats
    });
  });
  
  // La sesión se borra después (sin transacción)
  // Si esto falla, no afecta datos del jugador
  // Un job de limpieza periódico eliminará sesiones huérfanas
  await deleteSession(sessionId);
}
```

**Justificación de la Opción C:**

✅ **Ventajas:**
- Balance entre consistencia y velocidad
- Protege datos críticos del jugador (puntos, progreso, monedas)
- No bloquea múltiples documentos (más rápido que Opción A)
- Más simple que implementar job de recuperación (Opción B)

❌ **Desventajas Aceptables:**
- Puede quedar "basura" de sesiones en Firestore
- Requiere un job de limpieza periódico (pero no crítico)

**¿Por qué esto es aceptable?**

1. **La sesión es un dato transitorio**, no crítico
2. **No afecta la experiencia del usuario** si queda una sesión huérfana
3. **Fácil de limpiar** con un Cloud Function semanal:
   ```
   DELETE sessions WHERE lastUpdated < NOW() - 7 days
   ```

**Implementación en `SessionRepository`:**

```
SessionRepository tendrá:
- createSession(userId, nodeId)
- getActiveSession(userId)
- updateSessionProgress(sessionId, updates) // CON transacción
- deleteSession(sessionId) // SIN transacción
- completeNodeTransaction(playerId, nodeData) // Transacción del Player
```

---

## Decisiones de Lógica de Negocio

### 6. Separación de Responsabilidades: Validación de Respuesta vs Superación de Nodo

**Contexto:**

Se identificaron DOS responsabilidades diferentes:

**Responsabilidad A:**
```
Dada una respuesta del jugador y la respuesta correcta,
¿es correcta o incorrecta?
```

**Responsabilidad B:**
```
Dado el historial de respuestas de un nodo,
¿el jugador superó el umbral requerido?
```

**Decisión de Asignación:**

| Responsabilidad | Componente Responsable | ¿Qué necesita saber? |
|----------------|------------------------|---------------------|
| Validar si una respuesta es correcta | **QuestionEngine** | La pregunta + respuesta del jugador + respuesta correcta |
| Contar cuántas respuestas correctas llevas | **GameSession** (modelo de datos) | Historial de respuestas de la sesión actual |
| Decidir si superaste el nodo | **GameEngine** | Reglas del nodo (umbral) + estado de la sesión (contadores) |
| Aplicar consecuencias (restar vida) | **GameEngine** | Vidas actuales del jugador + reglas de penalización |

**Justificación:**

1. **Principio de Responsabilidad Única (SRP):**
   - Cada componente tiene una responsabilidad clara y delimitada
   - Facilita testing (puedes probar `QuestionEngine` sin `GameEngine`)
   - Reduce acoplamiento entre módulos

2. **Escalabilidad Futura:**
   
   **¿Esta separación permite agregar verdadero/falso o "elige 2 de 4"?**
   
   **Respuesta: SÍ (con modificaciones menores)**
   
   - `QuestionEngine.validateAnswer()` puede recibir diferentes tipos de respuestas
   - `GameEngine` no cambia (sigue evaluando umbrales)
   - Solo necesitas extender el modelo `Question`

3. **Flujo de Responsabilidades:**

```
Usuario selecciona respuesta "B"
  ↓
QuestionScreen captura evento
  ↓
GameController.onAnswerSelected("B")
  ↓
SubmitAnswerUseCase.execute()
  ├→ QuestionEngine.validateAnswer("B", "A") → INCORRECTA
  ├→ GameSession actualiza incorrectCount++
  ├→ GameEngine.checkNodeStatus(session) → TODAVÍA JUGANDO
  └→ Retorna resultado al Controller
  ↓
Controller actualiza UI
```

**Componente NO Responsable:**

- ❌ **Player:** NO valida respuestas (solo almacena estado)
- ❌ **QuestionRepository:** NO valida respuestas (solo lee/escribe datos)
- ❌ **UI (QuestionScreen):** NO decide si la respuesta es correcta

---

### 7. Lógica de "Restar Vida": ¿Dónde vive?

**Flujo de Causalidad:**

```
Jugador responde mal las preguntas del nodo
→ No alcanzó el umbral de correctas
→ Falló el nodo
→ Se resta vida
```

**Pregunta Crítica:**

> **¿"Restar vida" es una consecuencia automática de fallar un nodo, una acción que el controlador decide, o un efecto secundario que cualquiera puede disparar?**

**Decisión Tomada:**

✅ **Una consecuencia automática de fallar un nodo (regla de negocio)**

**Componente Responsable:**

**GameEngine** tiene la "verdad" sobre las vidas y ejecuta la lógica de penalización.

**Justificación:**

1. **Es una Regla del Juego:**
   - "Fallar un nodo cuesta 1 vida" es una regla de negocio, no una decisión de UI
   - Debe vivir en la capa de dominio (`GameEngine`), no en el controlador
   - Permite cambiar la regla en un solo lugar

2. **Centralización de Lógica:**
   - Si en el futuro hay múltiples formas de perder vidas (temporizador, power-ups), todas pasan por `GameEngine`
   - Evita duplicar lógica entre `FailNodeUseCase`, `TimeoutUseCase`, etc.

3. **Separación de Concerns:**
   - El controlador NO decide cuándo restar vidas (solo coordina)
   - El `Player` NO decide cuándo restar vidas (solo almacena el valor)
   - El `GameEngine` decide cuándo Y cómo restar vidas

**Pseudocódigo del Flujo:**

```
CUANDO jugador falla un nodo:

  1. QuestionEngine detecta que no alcanzó el umbral
     → Notifica a SubmitAnswerUseCase
  
  2. SubmitAnswerUseCase consulta a GameEngine
     → gameEngine.evaluateNodeFailure(session, player)
  
  3. GameEngine ejecuta lógica de negocio:
     → player.loseLife() // Método interno del modelo Player
     → if (player.lives == 0) { triggerGameOver() }
     → Retorna evento: {tipo: "NODE_FAILED", livesRemaining: 2}
  
  4. GameEngine persiste cambios (transacción)
     → Firebase.updatePlayer({lives: 2})
     → Firebase.deleteSession() // Limpia sesión actual
  
  5. GameEngine retorna evento al UseCase
     → {tipo: "NODE_FAILED", livesRemaining: 2, canRetry: true}
  
  6. UseCase retorna al Controller
  
  7. Controller actualiza UI
     → Muestra animación de "vida perdida"
     → Si livesRemaining > 0: navega a MapScreen
     → Si livesRemaining == 0: navega a GameOverScreen
```

**Validación de Integridad:**

**Pregunta:** ¿Qué pasa si Firebase falla en el paso 4?

**Respuesta: Flujo Pesimista (Decidido anteriormente)**

```dart
Future<void> onNodeFailed() async {
  showLoadingScreen(); // UI bloqueada, el usuario espera
  
  try {
    await Firebase.runTransaction(() {
      player.loseLife();
      updatePlayer();
      deleteSession();
    });
    
    showNodeFailedScreen(livesRemaining: player.lives);
  } catch (e) {
    // Firebase falló
    showErrorDialog("No se pudo guardar tu progreso. Reintenta.");
    // NO se actualiza la UI como si hubiera perdido vida
    // El usuario puede reintentar la operación
  }
}
```

**Justificación del Flujo Pesimista:**

- ✅ Más seguro (datos consistentes siempre)
- ✅ El usuario ve un error claro si algo falla
- ❌ Más lento (el usuario espera a la transacción)
- ✅ Para el MVP, la consistencia > velocidad

---

### 8. Cálculo de Precondiciones: ¿Quién valida si puedes iniciar un nodo?

**Escenario Crítico:**

```
Jugador tiene 1 vida restante.
Intenta el nodo 12.
Falla.
```

**¿Qué debe pasar?**

**Decisión Tomada:**

1. Se resta la vida → lives = 0
2. Es Game Over
3. El jugador vuelve al menú

**Reglas Definidas:**

1. **"Puedes reintentar un nodo siempre que tengas vidas"** (vidas = intentos)
2. **El límite de intentos son las vidas** (no hay límite por nodo individual)
3. **Si fallas con 0 vidas → Game Over**

**Precondiciones para `iniciarNodo(nodoId)`:**

```
PARA iniciar un nodo, el jugador DEBE:
- [✓] Tener vidas > 0
- [✓] Haber completado el nodo anterior (o ser el nodo 1)
- [✓] NO estar en otra sesión activa

SI no cumple "vidas > 0":
  → Mostrar "Game Over - Reiniciar juego?"

SI no cumple "nodo anterior completado":
  → Mostrar mensaje "Completa el nodo X primero"
  → Deshabilitar el botón del nodo en el mapa

SI ya tiene sesión activa:
  → Preguntar "¿Continuar partida guardada o empezar de nuevo?"
```

**¿DÓNDE se verifica esto?**

**Decisión:** **En ambos momentos**

1. **Cuando el jugador toca el nodo (UI):**
   - Para deshabilitar botones (UX)
   - Para mostrar mensajes informativos
   - Validación del lado del cliente (Flutter)

2. **Cuando termina el intento (Backend):**
   - Para prevenir estados inconsistentes
   - Para bloquear intentos maliciosos
   - Validación del lado del servidor (Firebase Security Rules)

**Seguridad: Cliente vs Servidor**

**Decisión Tomada:**

✅ **Opción C: Verificar en ambos lados (doble check)**

**Nivel de Implementación para el MVP:**

- ✅ **OBLIGATORIO:** Validación en cliente (Flutter)
- ✅ **IMPLEMENTADO:** Firebase Security Rules básicas

**Firebase Security Rules Mínimas:**

```javascript
// Firestore Security Rules
match /game_sessions/{sessionId} {
  // Solo usuarios autenticados pueden crear sesiones
  allow create: if request.auth != null 
                && request.resource.data.userId == request.auth.uid;
  
  // Solo el dueño puede actualizar su sesión
  allow update: if request.auth.uid == resource.data.userId
                && request.resource.data.lives >= 0; // Previene vidas negativas
}

match /players/{playerId} {
  // Solo el jugador puede modificar sus datos
  allow update: if request.auth.uid == playerId
                && request.resource.data.lives >= 0
                && request.resource.data.lives <= 3; // Máximo 3 vidas
}
```

**Esto previene:**
- ✅ Usuarios no autenticados
- ✅ Modificar sesiones de otros jugadores
- ✅ Poner vidas negativas
- ✅ Tener más de 3 vidas (hack)

**Justificación:**

**¿Por qué AMBOS lados?**

1. **Cliente (Flutter):**
   - Mejora UX (feedback inmediato)
   - Previene errores de usuario
   - Reduce carga en Firestore (no envías requests inválidas)

2. **Servidor (Security Rules):**
   - Previene hacking (modificar código Flutter)
   - Garantiza integridad de datos
   - Cumple con mejores prácticas de seguridad

**Complejidad vs Seguridad:**

- Para el MVP, las reglas básicas son suficientes (5 líneas)
- NO se implementará validación server-side compleja (Cloud Functions)
- Se monitoreará en producción y se ajustará si es necesario

---

## Decisiones de Experiencia de Usuario

### 9. Restauración de Sesiones: `RestoreSessionUseCase`

**Escenario:**

```
Usuario cierra la app mientras jugaba Nodo 15 (1 correcta, 1 incorrecta)
Vuelve a abrir la app al día siguiente
```

**Pregunta Crítica:**

> **¿Qué experiencia de usuario quieres?**

**Decisión Tomada:**

✅ **Opción B + Ambos componentes necesarios**

**Experiencia de UX Elegida:**

**Restauración Manual con Banner:**

```
1. Usuario abre la app
2. RestoreSessionUseCase busca automáticamente sesión activa
3. Si existe:
   → Muestra HomeScreen con banner: "Continuar partida en Nodo 15?"
   → Opciones: [Continuar] [Empezar de nuevo]
4. Si NO existe:
   → Muestra HomeScreen normal
```

**Justificación:**

**¿Por qué NO Restauración Automática?**

❌ **Opción A descartada:**
- Usuario abre la app → Ya está en la pregunta donde estaba
- **Problema:** Puede ser confuso si pasó mucho tiempo
- **Problema:** No da control al usuario (puede querer reiniciar)
- **Problema:** Si abrió la app "de casualidad", lo mete en medio del juego

**¿Por qué NO Expiración de Sesiones (todavía)?**

⚠️ **Opción C pospuesta:**
- Si pasaron más de 24 horas → Borra la sesión
- **Razón para posponer:** Agrega complejidad innecesaria al MVP
- **Decisión:** Implementar en v1.1 (después del MVP)
- **Para el MVP:** Las sesiones NO expiran

**Componentes Necesarios:**

```
[ ✓ ] Crearé RestoreSessionUseCase (se ejecuta en main.dart al iniciar)
[ ✓ ] StartNodeUseCase manejará la restauración manual (cuando el usuario elija "Continuar")
[ ✓ ] Necesito AMBOS
```

**Flujo Detallado:**

```
main.dart inicia la app
  ↓
RestoreSessionUseCase.execute()
  ├→ Busca en Firestore: getActiveSession(currentUserId)
  ├→ Si existe sesión:
  │   └→ Retorna: {hasActiveSession: true, nodeId: 15, progress: "1/3"}
  └→ Si NO existe:
      └→ Retorna: {hasActiveSession: false}
  ↓
GameController recibe resultado
  ├→ Si hasActiveSession == true:
  │   └→ Actualiza estado: showRestoreBanner = true
  └→ Si hasActiveSession == false:
      └→ Navega a HomeScreen normal
  ↓
HomeScreen renderiza
  ├→ Si showRestoreBanner:
  │   └→ Muestra banner: "Continuar en Nodo 15? (1 de 3 correctas)"
  │       [Continuar] → Llama StartNodeUseCase.restoreSession()
  │       [Empezar de nuevo] → Llama deleteSession() + navega a MapScreen
  └→ Si NO:
      └→ Muestra botón "Jugar" normal
```

**Beneficios de esta Aproximación:**

1. **Usuario tiene control** (elige continuar o empezar de nuevo)
2. **No es intrusivo** (solo un banner, no te mete automáticamente)
3. **Informa al usuario** (muestra progreso: "1 de 3 correctas")
4. **Simple de implementar** (no requiere lógica de expiración)

---

## Decisiones de Escalabilidad

### 10. Tipos de Preguntas: Preparación para Verdadero/Falso

**Contexto:**

Se identificó que el modelo actual de `Question` (4 opciones múltiples) se "rompe" si se agregan otros tipos (verdadero/falso, selección múltiple).

**Opciones Evaluadas:**

**Opción A: Campo Tipo en Question**
```dart
class Question {
  String id;
  String text;
  QuestionType type; // multipleChoice, trueFalse, multiSelect
  dynamic options;   // List<String> o bool o Map
  dynamic correctAnswer; // String, bool, o List<String>
}
```
- ✅ Más simple ahora
- ❌ `dynamic` puede dar problemas de tipo

**Opción B: Herencia/Polimorfismo**
```dart
abstract class Question { ... }
class MultipleChoiceQuestion extends Question { ... }
class TrueFalseQuestion extends Question { ... }
```
- ✅ Más robusto, type-safe
- ❌ Más código inicial

**Opción C: Separación por Colección**
```
Firestore:
/questions_multiple_choice
/questions_true_false
/questions_multi_select
```
- ✅ Más flexible, queries especializadas
- ❌ Múltiples queries, más complejo

**Decisión Tomada:**

✅ **Opción C: Separación por Colección (para escalabilidad)**

**Justificación:**

**Para el MVP:**
- Solo se implementa `/questions_multiple_choice`
- Las preguntas tienen 4 opciones
- Estructura simple y directa

**Cuando agregue verdadero/falso:**
- Crear nueva colección `/questions_true_false`
- El `QuestionEngine` decide de qué colección leer según el tipo de nodo
- NO necesitas modificar las preguntas existentes
- Puedes mezclar tipos en un mismo nodo (si quieres)

**Ventajas a Largo Plazo:**

1. **Separación de Concerns:**
   - Cada tipo de pregunta tiene su propia estructura óptima
   - No necesitas campos `dynamic` (más seguro)

2. **Performance:**
   - Queries más rápidas (solo lees del tipo que necesitas)
   - Índices especializados por tipo

3. **Escalabilidad:**
   - Agregar un nuevo tipo NO afecta los existentes
   - Puedes tener reglas de validación diferentes por tipo

**Cambios Necesarios al Agregar Verdadero/Falso:**

```
1. Crear colección Firestore:
   /questions_true_false/{questionId}
   
2. Crear modelo Dart:
   class TrueFalseQuestion {
     String id;
     String text;
     bool correctAnswer; // true o false
     String category;
   }
   
3. Modificar QuestionEngine:
   Question getRandomQuestion(String theme, QuestionType type) {
     if (type == QuestionType.multipleChoice) {
       return questionRepo.getFromCollection('questions_multiple_choice');
     } else if (type == QuestionType.trueFalse) {
       return questionRepo.getFromCollection('questions_true_false');
     }
   }
   
4. NO necesitas cambiar:
   - GameEngine (sigue evaluando umbrales)
   - GameSession (sigue guardando IDs de preguntas)
   - UI básica (solo cambias el widget de opciones)
```

**Costo de esta Decisión:**

- ⚠️ Más colecciones en Firestore (pero el costo es mínimo)
- ⚠️ Necesitas poblar múltiples colecciones (pero puedes hacerlo gradualmente)

**Beneficio:**

- ✅ Arquitectura preparada para crecer sin refactorización mayor

---

## Decisiones de Implementación

### 11. Sistema de Recompensas: Fijo vs Progresivo

**Contexto:**

Durante la implementación de `calculateCoinsReward()`, surgió la pregunta sobre si la recompensa debería ser progresiva por nodo o fija por rango.

**Decisión Original del Documento:**
> **Sistema: FIJO por rango de dificultad**

**Confusión Durante Implementación:**

El desarrollador implementó inicialmente un sistema progresivo con bucles, pensando que:
```
"Si estoy en el nivel 15, se deberían sumar los anteriores al puntaje"
```

**Aclaración de Responsabilidades:**

| Componente | Responsabilidad |
|------------|----------------|
| `calculateCoinsReward(nodeId)` | Calcula cuánto **vale** completar ESE nodo específico |
| `CompleteNodeUseCase` | **Suma** la recompensa al total del jugador |
| `Player.coins` | **Almacena** el total acumulado |

**Reafirmación de la Decisión:**

✅ **Sistema FIJO confirmado:**
```
Nodos 1-10: 100 monedas cada uno
Nodos 11-20: 200 monedas cada uno
Nodos 21-30: 300 monedas cada uno
```

**Alternativa descartada durante implementación:**
```
Sistema progresivo:
Nodo 1: 100
Nodo 2: 110
Nodo 3: 120
...
```

**Razones para mantener FIJO:**
1. ✅ Ya se había decidido en el documento
2. ✅ Más simple de implementar
3. ✅ Claro para el usuario
4. ✅ Puede cambiarse después del MVP con datos reales

**Implementación Final:**

```dart
int calculateCoinsReward(int nodeId) {
  if (nodeId < 1 || nodeId > 30) {
    throw ArgumentError('Node ID must be between 1 and 30, got $nodeId');
  }
  if (nodeId >= 1 && nodeId <= 10) {
    return 100;
  } else if (nodeId >= 11 && nodeId <= 20) {
    return 200;
  } else {
    return 300;
  }
}
```

**Lección aprendida:**
- Separar responsabilidades entre calcular valor individual vs acumular totales
- El principio de responsabilidad única aplica a nivel de función

---

### 12. Estados del Juego: Granularidad Apropiada

**Contexto:**

Durante la implementación de `GameState`, surgió la pregunta sobre el nivel de granularidad de los estados.

**Decisión Inicial:**

Se definieron 6 estados:
```
idle, playing, loading, nodeCompleted, nodeFailed, gameOver
```

**Problema Identificado:**

El estado `playing` era ambiguo, cubriendo:
1. "Usuario tocó el botón play"
2. "Usuario está en el mapa seleccionando nodo"
3. "Usuario está respondiendo preguntas"

**Análisis de Alternativas:**

| Opción | Estados | Ventaja | Desventaja |
|--------|---------|---------|------------|
| **A: Separar "navigating"** | 7 estados | Clara separación mapa vs preguntas | Un estado adicional |
| **B: "playing" amplio** | 6 estados | Más simple | Menos granular, lógica extra en controller |
| **C: Estados por pantalla** | 7 estados | Mapeo 1:1 estado-pantalla | Nombres más largos |

**Decisión Tomada:**

✅ **Opción A: Agregar estado `navigating`**

**Estados finales:**
```dart
enum GameState {
  idle,           // HomeScreen
  navigating,     // MapScreen (seleccionando nodo)
  playing,        // QuestionScreen (respondiendo preguntas)
  loading,        // Cargando datos
  nodeCompleted,  // Pantalla de éxito
  nodeFailed,     // Pantalla de fallo
  gameOver        // Pantalla de Game Over
}
```

**Justificación:**

1. **Claridad:** Cada estado representa UNA situación específica
2. **Debugging:** Fácil identificar en qué punto del flujo está el usuario
3. **Escalabilidad:** Patrón claro para agregar más pantallas
4. **Balance:** No es demasiado complejo (7 estados) ni demasiado simple

**Mapeo Estado → Pantalla:**
```
idle → HomeScreen
navigating → MapScreen
playing → QuestionScreen
loading → LoadingWidget (overlay)
nodeCompleted → NodeCompletedScreen
nodeFailed → NodeFailedScreen
gameOver → GameOverScreen
```

**Flujo Típico:**
```
idle → loading → navigating → loading → playing → loading → 
nodeCompleted → navigating
```

**Beneficios de la Decisión:**
- ✅ No hay ambigüedad sobre qué está haciendo el usuario
- ✅ El `GameController` puede tomar decisiones basadas en estados claros
- ✅ Facilita implementación de analytics (tracking por estado)

---

### 13. Funciones vs Constantes en `game_rules.dart`

**Contexto:**

Durante la implementación del archivo `game_rules.dart`, surgió la pregunta sobre si valores fijos deberían ser constantes o funciones.

**Opciones Evaluadas:**

**Opción A: Todas constantes**
```dart
const int POINTS_PER_CORRECT = 10;
const int INITIAL_LIVES = 3;
```

**Opción B: Todas funciones**
```dart
int getPointsPerCorrectAnswer() => 10;
int getInitialLives() => 3;
```

**Opción C: Mixto**
- Constantes para valores que NUNCA cambiarán
- Funciones para valores que PODRÍAN tener lógica

**Decisión Tomada:**

✅ **Opción B: Todas funciones**

**Justificación:**

1. **Consistencia:** Todo en `game_rules.dart` se usa de la misma forma
2. **Escalabilidad:** Fácil agregar lógica después sin cambiar la interfaz
   - Ejemplo: `getPointsPerCorrectAnswer()` podría depender de dificultad
   - Ejemplo: `getAvailableThemes()` podría leer de Firebase
3. **Documentación:** Las funciones pueden documentarse con `///`
4. **API unificada:** No hay que pensar "¿es constante o función?"

**Implementación:**
```dart
int getPointsPerCorrectAnswer() => 10;
int getInitialLives() => 3;
List<String> getAvailableThemes() => ["Cine", "Videojuegos", ...];
int getQuestionsPerTheme() => 50;
```

**Nota sobre Performance:**
- Para el MVP, el overhead de llamada a función es negligible
- Si se detectan problemas de performance, se optimiza después
- Dart puede inline funciones simples en compilación

**Lección aprendida:**
- Priorizar escalabilidad y consistencia sobre micro-optimización prematura
- YAGNI aplica, pero también "prepararse para el cambio"

---

## Estructura del Proyecto

### 14. Organización de Carpetas Definitiva

Basándose en las decisiones tomadas, la estructura final del proyecto es:

```
arquitectura_trivia/
│
├── lib/
│   ├── main.dart                    # Punto de entrada
│   │
│   ├── core/                        # Configuración global
│   │   ├── constants/
│   │   │   ├── game_rules.dart      # ✅ COMPLETADO - Lógica de dificultad
│   │   │   └── firebase_collections.dart
│   │   ├── enums/
│   │   │   ├── difficulty.dart      # ✅ COMPLETADO - easy, medium, hard
│   │   │   ├── game_state.dart      # ✅ COMPLETADO - idle, navigating, playing, etc.
│   │   │   └── question_type.dart   # ⬜ PENDIENTE - multipleChoice, trueFalse (futuro)
│   │   └── errors/
│   │       └── app_exceptions.dart
│   │
│   ├── data/                        # Capa de datos (Firebase)
│   │   ├── models/
│   │   │   ├── player.dart
│   │   │   ├── node.dart
│   │   │   ├── question.dart
│   │   │   └── game_session.dart    # CON answersGiven
│   │   ├── repositories/
│   │   │   ├── player_repository.dart
│   │   │   ├── question_repository.dart  # Múltiples colecciones
│   │   │   └── session_repository.dart   # CON completeNodeTransaction()
│   │   └── services/
│   │       └── firebase_service.dart
│   │
│   ├── domain/                      # Lógica de negocio
│   │   ├── engines/
│   │   │   ├── game_engine.dart     # Responsable de vidas, umbrales, recompensas
│   │   │   └── question_engine.dart # Selección, validación, anti-repetición
│   │   └── usecases/
│   │       ├── start_node_usecase.dart       # Verifica precondiciones
│   │       ├─�� restore_session_usecase.dart  # Busca sesión activa
│   │       ├── submit_answer_usecase.dart    # Coordina validación
│   │       ├── complete_node_usecase.dart    # Transacción atómica
│   │       ├── fail_node_usecase.dart        # Resta vida, limpia sesión
│   │       └── game_over_usecase.dart        # Calcula recompensa, resetea
│   │
│   ├── presentation/                # UI (Flutter)
│   │   ├── controllers/
│   │   │   └── game_controller.dart # Coordina UseCases
│   │   ├── screens/
│   │   │   ├── home_screen.dart             # Con banner de restauración
│   │   │   ├── map_screen.dart              # Con validación de precondiciones
│   │   │   ├── question_screen.dart
│   │   │   └── game_over_screen.dart
│   │   └── widgets/
│   │       ├── node_widget.dart
│   │       ├── question_card.dart
│   │       ├── lives_display.dart
│   │       └── restore_banner.dart          # Nuevo
│   │
│   └── utils/
│       └── logger.dart
│
├── firebase/
│   └── firestore.rules              # Security Rules (validación servidor)
│
├── pubspec.yaml
└── README.md
```

**Justificación de Cambios vs Estructura Original:**

| Carpeta/Archivo | Cambio | Justificación |
|----------------|--------|---------------|
| `core/enums/question_type.dart` | **NUEVO** | Preparación para múltiples tipos de preguntas |
| `core/enums/game_state.dart` | **MODIFICADO** | Agregado estado `navigating` |
| `data/models/game_session.dart` | **MODIFICADO** | Agregado `answersGiven` para anti-repetición global |
| `domain/usecases/restore_session_usecase.dart` | **NUEVO** | Necesario para restauración manual de sesiones |
| `domain/usecases/game_over_usecase.dart` | **NUEVO** | Separado de `fail_node` (diferentes responsabilidades) |
| `presentation/widgets/restore_banner.dart` | **NUEVO** | Widget para mostrar opción de continuar partida |

---

## Casos de Uso Definidos

### 15. UseCases Completos del Sistema

Basándose en las decisiones, estos son TODOS los casos de uso del MVP:

#### 1. `StartNodeUseCase`

**Responsabilidad:** Iniciar un nodo (verificar precondiciones y crear sesión)

**Precondiciones verificadas:**
- Jugador tiene vidas > 0
- Nodo anterior está completado (excepto nodo 1)
- NO hay sesión activa

**Flujo:**
```
1. Validar precondiciones (usando GameEngine)
2. Si hay sesión activa:
   → Preguntar al usuario: ¿Continuar o empezar de nuevo?
3. Si no hay sesión:
   → Crear nueva GameSession
   → Calcular requiredCorrect y totalQuestions (desde game_rules)
   → Persistir sesión en Firestore
4. Retornar: {success: true, sessionId: "..."}
```

---

#### 2. `RestoreSessionUseCase`

**Responsabilidad:** Buscar sesión activa al iniciar la app

**Flujo:**
```
1. Obtener userId del usuario actual
2. Buscar en Firestore: sessions WHERE userId == currentUser AND completed == false
3. Si existe sesión:
   → Retornar: {hasActiveSession: true, nodeId: X, progress: "1/3"}
4. Si NO existe:
   → Retornar: {hasActiveSession: false}
```

---

#### 3. `SubmitAnswerUseCase`

**Responsabilidad:** Procesar la respuesta del jugador

**Flujo:**
```
1. Obtener pregunta desde QuestionRepository
2. Validar respuesta usando QuestionEngine
   → questionEngine.validateAnswer(userAnswer, correctAnswer)
3. Actualizar GameSession:
   → Si correcta: correctCount++
   → Si incorrecta: incorrectCount++
   → Agregar a questionsShownIds
   → Agregar a answersGiven
4. Verificar estado del nodo usando GameEngine:
   → gameEngine.checkNodeStatus(session)
   → Resultados posibles:
      - STILL_PLAYING (necesita más respuestas)
      - NODE_COMPLETED (alcanzó umbral)
      - NODE_FAILED (agotó intentos)
5. Persistir cambios (transacción)
6. Retornar: {isCorrect: bool, nodeStatus: status, nextAction: action}
```

---

#### 4. `CompleteNodeUseCase`

**Responsabilidad:** Finalizar un nodo exitosamente

**Flujo (Transacción Atómica - Opción C):**
```
1. Calcular recompensas:
   → points = correctCount * 10
   → coins = GameRules.calculateCoinsReward(nodeId)
   
2. Ejecutar transacción en Player:
   await Firebase.runTransaction(() {
     - Sumar puntos
     - Marcar nodo como completado
     - Desbloquear siguiente nodo (nodeId + 1)
     - Sumar monedas
     - Actualizar estadísticas
   });
   
3. Borrar sesión (SIN transacción):
   → sessionRepository.deleteSession(sessionId)
   
4. Retornar: {
     success: true,
     pointsEarned: X,
     coinsEarned: Y,
     nextNodeUnlocked: Z
   }
```

---

#### 5. `FailNodeUseCase`

**Responsabilidad:** Procesar fallo de nodo (restar vida)

**Flujo (Transacción Atómica):**
```
1. Verificar vidas actuales del jugador
2. Ejecutar transacción:
   await Firebase.runTransaction(() {
     - player.loseLife() (vidas--)
     - updatePlayer({lives: newLives})
     - deleteSession() // Limpia intento fallido
   });
   
3. Evaluar resultado:
   → Si lives > 0: {canRetry: true, livesRemaining: X}
   → Si lives == 0: Llamar a GameOverUseCase
   
4. Retornar resultado
```

---

#### 6. `GameOverUseCase`

**Responsabilidad:** Procesar fin de juego (vidas = 0)

**Flujo:**
```
1. Calcular progreso del jugador:
   → nodesCompleted = player.completedNodes.length
   
2. Calcular recompensa final:
   → coins = nodesCompleted * 50 (por nodo completado)
   
3. Ejecutar transacción:
   await Firebase.runTransaction(() {
     - Resetear vidas a 3
     - Resetear puntaje a 0
     - Sumar monedas de recompensa
     - Mantener nodos completados (progreso permanente)
     - Actualizar estadística: gamesPlayed++
   });
   
4. Retornar: {
     totalNodesCompleted: X,
     coinsEarned: Y,
     canContinueFrom: lastCompletedNode + 1
   }
```

**Nota sobre "Resetear Puntaje":**

Se decidió que al Game Over:
- ✅ **Vidas se resetean** (vuelves a tener 3)
- ✅ **Puntaje se resetea** (vuelve a 0)
- ✅ **Nodos completados SE MANTIENEN** (no pierdes progreso)
- ✅ **Monedas se SUMAN** (recompensa permanente)

**Justificación:**
- El puntaje es una métrica de "esta sesión de juego"
- Los nodos completados son progreso permanente (no retrocedes)
- Las monedas son el "tesoro" que guardas para la tienda (fuera del MVP)

---

## Constantes del Juego

### 16. Valores Numéricos Definidos

Basándose en todas las decisiones, estos son los valores definitivos:

```
CONSTANTES DEL JUEGO:

Vidas:
- Vidas iniciales: 3
- Vidas máximas: 3
- Costo por fallar nodo: 1 vida

Temas:
- Temas disponibles: ["Cine", "Videojuegos", "Deportes", "Historia", "Arte", "Literatura"]
- Total de temas: 6
- Preguntas por tema: 50
- Total de preguntas en el sistema: 300 (6 temas × 50 preguntas)

Nodos:
- Total de nodos: 30
- Distribución:
  * Nodos 1-10: Dificultad FÁCIL (1 de 3 correctas)
  * Nodos 11-20: Dificultad MEDIA (2 de 3 correctas)
  * Nodos 21-30: Dificultad DIFÍCIL (3 de 5 correctas)

Puntos:
- Puntos por respuesta correcta: 10
- Puntos NO se acumulan entre Game Overs (se resetean)

Recompensas de Monedas:
- Sistema: FIJO por rango de dificultad

Fórmula:
  Si nodeId entre 1-10:  100 monedas
  Si nodeId entre 11-20: 200 monedas
  Si nodeId entre 21-30: 300 monedas

- Recompensa por Game Over: nodesCompleted × 50 monedas
- Las monedas SE ACUMULAN (no se resetean)

Progresión:
- Desbloqueo: Secuencial (completar nodo X desbloquea X+1)
- NO se puede saltar nodos
- Al Game Over, mantienes nodos completados
```

**Decisión sobre Recompensa de Monedas:**

**Elegida: FIJA por rango**

**Alternativa descartada:** Progresiva (nodo 1 = 100, nodo 2 = 110, etc.)

**Justificación:**
- Más simple de implementar (if/else en lugar de fórmula)
- Más clara para el usuario (sabe cuánto ganará)
- Suficiente diferenciación entre rangos (100 vs 200 vs 300)
- Si se necesita más granularidad, se puede cambiar en el futuro

---

## Responsabilidades de GameEngine

### 17. Contrato Completo del GameEngine

Basándose en las decisiones, el `GameEngine` es responsable de:

#### 1. ✅ Calcular si un nodo fue superado

**Entrada:** 
- `GameSession` (con correctCount, incorrectCount)
- `requiredCorrect` (calculado desde game_rules)

**Lógica:**
```
if (correctCount >= requiredCorrect) {
  return NodeStatus.COMPLETED;
} else if (questionsShown >= totalQuestionsNeeded) {
  return NodeStatus.FAILED;
} else {
  return NodeStatus.PLAYING;
}
```

---

#### 2. ✅ Determinar si es Game Over

**Entrada:** `Player` (con campo lives)

**Lógica:**
```
if (player.lives == 0) {
  return true;
}
return false;
```

---

#### 3. ✅ Calcular puntos ganados

**Entrada:** `correctCount`

**Lógica:**
```
points = correctCount * POINTS_PER_CORRECT;
return points;
```

---

#### 4. 🆕 Calcular recompensa de monedas al completar nodo

**Entrada:** `nodeId`

**Lógica:**
```
if (nodeId >= 1 && nodeId <= 10) {
  return 100;
} else if (nodeId >= 11 && nodeId <= 20) {
  return 200;
} else if (nodeId >= 21 && nodeId <= 30) {
  return 300;
}
```

---

#### 5. 🆕 Determinar si el jugador puede intentar un nodo

**Entrada:** 
- `Player` (con lives, completedNodes)
- `nodeId` (nodo que quiere intentar)

**Precondiciones:**
```
1. player.lives > 0
2. Si nodeId == 1: siempre puede
   Si nodeId > 1: (nodeId - 1) debe estar en completedNodes
3. NO debe existir una sesión activa
```

**Retorna:** `{canStart: bool, reason: string}`

---

#### 6. 🆕 Calcular el siguiente nodo a desbloquear

**Entrada:** `currentNodeId`

**Lógica:**
```
nextNode = currentNodeId + 1;
if (nextNode > 30) {
  return null; // Juego completado
}
return nextNode;
```

**Nota:** NO se pueden saltar nodos. Siempre es secuencial.

---

#### 7. 🆕 Determinar cuántas preguntas faltan en el nodo actual

**Entrada:** `GameSession`

**Lógica:**
```
questionsAnswered = session.questionsShownIds.length;
totalNeeded = GameRules.getTotalQuestions(session.currentNodeId);
remaining = totalNeeded - questionsAnswered;
return remaining;
```

**Para la UI:** "Pregunta 2/3"

---

#### 8. 🆕 Validar que un intento es posible

**Entrada:** 
- `Player`
- `nodeId`

**Lógica:**
```
if (player.lives == 0) {
  return {canAttempt: false, reason: "No tienes vidas"};
}

if (nodeId > 1 && !player.completedNodes.contains(nodeId - 1)) {
  return {canAttempt: false, reason: "Completa el nodo anterior primero"};
}

return {canAttempt: true};
```

**Reintentos de nodo:**
- ✅ Se puede reintentar el mismo nodo infinitas veces (mientras tenga vidas)
- ✅ Cada intento cuesta 1 vida (si fallas)
- ✅ Si fallas con 0 vidas → Game Over

---

### Restricciones del GameEngine

El `GameEngine` **NO debe**:

- ❌ Conocer Firebase (no hace queries ni escrituras)
- ❌ Tener estado interno (es stateless, funciones puras)
- ❌ Decidir qué pregunta mostrar (eso es `QuestionEngine`)
- ❌ Actualizar modelos directamente (solo retorna valores calculados)
- ❌ Manejar UI (solo lógica de negocio)

**Principio:** El `GameEngine` es un conjunto de **funciones puras** que toman datos de entrada y retornan decisiones de