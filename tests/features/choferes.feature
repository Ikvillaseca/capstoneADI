Feature: H.U.2 - Gestión de choferes
  Como dueño del negocio
  Quiero gestionar los datos de los choferes registrados en la empresa

  Scenario: Ver página de choferes
    Given Navegue a la pagina de choferes
    Then Observare que accedi a la pagina con titulo "Lista de Choferes"

  Scenario: Agregar choferes
    Given Navegue a la pagina de choferes
    When Agregue los datos de un chofer
      | rut        | nombre  | apellido  | tipo_licencia       | direccion | fecha_ultimo_control | fecha_proximo_control |
      | 19083514-6 | Juanito | Perez     | Licencia Clase A1   | Calle 1   | 18-11-2025           | 18-11-2026            |
      | 17219852-K | Mariela | Marianela | Licencia Clase A1   | Calle 1   | 18-11-2025           | 18-11-2026            |
      | 20417796-1 | Maximo  | Orlando   | Licencia Clase A1   | Calle 1   | 18-11-2025           | 18-11-2026            |
    Then Observare que los choferes se agregaron a la lista