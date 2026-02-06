import 'package:lost_library/core/enums/dificulty.dart';
// ============================================
// REGLAS DEL JUEGO
// ============================================
// Este archivo contiene todas las reglas de negocio del juego
// como valores fijos. NO debe tener lógica de Firebase ni UI.

/// Calcula cuántas respuestas correctas se necesitan para pasar un nodo.
///
/// Reglas:
/// - Nodos 1-10 (Fácil): 1 de 3 correctas
/// - Nodos 11-20 (Medio): 2 de 3 correctas
/// - Nodos 21-30 (Difícil): 3 de 5 correctas
///
/// Lanza [ArgumentError] si [nodeId] no está entre 1 y 30.
int getRequiredCorrectAnswers(int nodeId) {
  if (nodeId < 1 || nodeId > 30) {
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

/// Calcula cuántas preguntas hay en un nodo.
///
/// Reglas:
/// - Nodos 1-10 (Fácil): 3 preguntas
/// - Nodos 11-20 (Medio): 3 preguntas
/// - Nodos 21-30 (Difícil): 5 preguntas
///
/// Lanza [ArgumentError] si [nodeId] no está entre 1 y 30.
int getTotalQuestions(int nodeId) {
  if (nodeId < 1 || nodeId > 30) {
    throw ArgumentError('Node ID must be between 1 and 30, got $nodeId');
  }
  if ((nodeId >= 1 && nodeId <= 10) || (nodeId >= 11 && nodeId <= 20)) {
    return 3;
  } else {
    return 5;
  }
}

/// Sirve para obtener la dificultad de un nodo
/// segun el lugar donde se encuentre el nodo
///
/// Retorna:
/// - Difficulty.easy para nodos 1-10
/// - Difficulty.medium para nodos 11-20
/// - Difficulty.hard para nodos 21-30
///
/// Lanza [ArgumentError] si [nodeId] no está entre 1 y 30.
Difficulty getDifficulty(int nodeId) {
  if (nodeId < 1 || nodeId > 30) {
    throw ArgumentError('Node ID must be between 1 and 30, got $nodeId');
  }
  if (nodeId >= 1 && nodeId <= 10) {
    return Difficulty.easy;
  } else if (nodeId >= 11 && nodeId <= 20) {
    return Difficulty.medium;
  } else {
    return Difficulty.hard;
  }
}

/// Sirve para obtener recompensas por superar un nodo
///
/// Reglas:
/// - Nodos 1-10 (Fácil): obtener 100 coins
/// - Nodos 11-20 (Medio): obtener 200 coins
/// - Nodos 21-30 (Difícil): obtenes 300 coins
///
/// Lanza [ArgumentError] si [nodeId] no está entre 1 y 30.
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

/// Retorna los puntos que se otorgan por cada respuesta correcta.
///
/// Valor: 10 puntos
int getPointsPerCorrectAnswer() => 10;

/// Retorna la cantidad de vidas con las que inicia el jugador.
///
/// Valor: 3 vidas
int getInitialLives() => 3;

/// Retorna la lista de temas disponibles para las preguntas.
///
/// Temas:
/// - Cine
/// - Videojuegos
/// - Deportes
/// - Historia
/// - Arte
/// - Literatura
List<String> getAvailableThemes() => [
  "Cine",
  "Videojuegos",
  "Deportes",
  "Historia",
  "Arte",
  "Literatura",
];

/// Retorna la cantidad de preguntas que debe haber por cada tema.
///
/// Valor: 50 preguntas por tema
int getQuestionsPerTheme() => 50;
