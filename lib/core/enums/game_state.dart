/// Representar en qué estado se encuentra el juego en un momento dado.
///
/// Uso:
/// El GameController (en la capa de presentación) usará este enum para saber qué pantalla mostrar.
///
/// Valores:
/// - idle: El juego está en reposo (pantalla principal, esperando acción del usuario)
/// - navigating: MapScreen (seleccionando nodo)
/// - playing: El jugador está activamente respondiendo preguntas
/// - loading: Cargando datos (Firestore, transiciones)
/// - nodeCompleted: El jugador completó un nodo exitosamente
/// - nodeFailed: El jugador falló un nodo (perdió una vida)
/// - gameOver: El jugador perdió todas las vidas
enum GameState {
  idle,
  navigating,
  playing,
  loading,
  nodeCompleted,
  nodeFailed,
  gameOver
}