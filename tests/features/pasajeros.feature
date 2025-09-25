Feature: Gestión de pasajeros
  Como dueño del negocio
  Quiero gestionar los pasajeros que solicitan las empresas que sean llevados
  Para poder asignar pasajeros a la flota de vehículos

  Scenario: Ver página de pasajeros
    When Navegue a la pagina de pasajeros
    Then Observare que accedi a la pagina con titulo "Lista de Pasajeros"

  Scenario: Navegar a pagina "Agregar un pasajero"

    Given Navegue a la pagina de pasajeros
    When Agregue los datos de un pasajero
      | rut        | nombre  | apellido  | telefono     | empresa_trabajo |
      | 19083514-6 | Juanito | Perez     | +56909021679 | Fontabella      |
      | 17219852-k | Mariela | Marianela | +56958116233 | Cites           |
      | 20417796-1 | Maximo  | Orlando   | +56997496356 | FudFud          |
    Then Observare que los pasajeros se agregaron a la lista
    
    
  