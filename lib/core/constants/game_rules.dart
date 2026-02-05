//Rules of the game

/// Calcula cuántas respuestas correctas se necesitan para pasar un nodo.
///
/// Reglas:
/// - Nodos 1-10 (Fácil): 1 de 3 correctas
/// - Nodos 11-20 (Medio): 2 de 3 correctas
/// - Nodos 21-30 (Difícil): 3 de 5 correctas
///
/// Lanza [ArgumentError] si [nodeId] no está entre 1 y 30.
int getRequiredCorrectAnswers(int nodeId) {
  if (nodeId < 1 || nodeId > 30 ){
    throw ArgumentError('Node ID must be between 1 and 30, got $nodeId');
  }
  if (nodeId >= 1 && nodeId <= 10) {
    return 1;
  } else if (nodeId >= 11 && nodeId <= 20) {
    return 2;
  } else {
    return 3;
  }
}

// Calcula cuántas preguntas hay en un nodo.
///
/// Reglas:
/// - Nodos 1-10 (Fácil): 3 preguntas
/// - Nodos 11-20 (Medio): 2 de 3 preguntas
/// - Nodos 21-30 (Difícil): 5 preguntas
///
/// Lanza [ArgumentError] si [nodeId] no está entre 1 y 30.
int getTotalQuestions(int nodeId){
  if (nodeId < 1 || nodeId > 30 ){
    throw ArgumentError('Node ID must be between 1 and 30, got $nodeId');
  }
  if (nodeId >= 1 && nodeId <= 10) {
    return 3;
  } else if (nodeId >= 11 && nodeId <= 20) {
    return 3;
  } else {
    return 5;
  }
}