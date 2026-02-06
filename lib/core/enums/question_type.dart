/// Este enum representa tipos de preguntas.
///
/// Uso:
/// - QuestionEngine: Selecciona la colección de Firestore según el tipo.
/// - QuestionScreen: Renderiza el widget apropiado según el tipo.
///
/// Valores:
/// - multipleChoice: 4 opciones, 1 correcta.
/// - trueFalse: 2 opciones, 1 correcta.
/// - multiSelect: 4-6 opciones, 2+ correctas.
///
/// Nota: Para el MVP solo se implementa multipleChoice.
///
enum QuestionType {
  multipleChoice,
  trueFalse,
  multiSelect
}
