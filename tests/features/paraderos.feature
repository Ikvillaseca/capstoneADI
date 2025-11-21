Feature: H.U.4 - Gestión de paraderos
  Como dueño del negocio
  Quiero gestionar los paraderos
  Para mantener puntos de recogida confiables

  Scenario: Ver pagina de paraderos
    Given Navegue a la pagina de paraderos
    Then Observare que accedi a la pagina con titulo "Lista de Paraderos"

  Scenario: Agregar paraderos
    Given Navegue a la pagina de paraderos
    When Agregue los datos de un paradero
      | nombre                            | direccion                                           |
      | Duoc UC Sede Maipu                | Av. Esquina Blanca 501, Maipú, Región Metropolitana |
      | Estación Central - Acceso Alameda | Av. Libertador B. O'Higgins 3170, Santiago          |
      | Terminal San Borja                | San Borja 123, Independencia, Santiago              |
    Then Observare que los paraderos se agregaron a la lista