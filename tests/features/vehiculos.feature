Feature: H.U.1 - Gestión de vehículos
  Como administrador
  Quiero gestionar los vehículos de la flota
  Para mantener sus datos actualizados

  Scenario: Ver pagina de vehiculos
    Given Navegue a la pagina de vehiculos
    Then Observare que accedi a la pagina con titulo "Lista de Vehículos"

  Scenario: Agregar vehiculos
    Given Navegue a la pagina de vehiculos
    When Agregue los datos de un vehiculo
      | patente | marca | modelo  | anio | capacidad | fecha_revision_tecnica | fecha_proximo_revision |
      | ABCD12  | Kia   | Morning | 2020 | 9         | 10-10-2024             | 10-10-2026             |
    Then Observare que los vehiculos se agregaron a la lista