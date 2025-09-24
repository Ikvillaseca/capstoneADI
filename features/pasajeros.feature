Feature: Gestión de pasajeros
  Como dueño del negocio
  Quiero gestionar los pasajeros que solicitan las empresas que sean llevados
  Para poder asignar pasajeros a la flota de vehículos

  Scenario: Ver página de pasajeros
    When Navegue a la pagina de pasajeros
    Then Observare que accedi a la pagina con titulo "Lista de Pasajeros"

  Scenario: Agregar un pasajero
    When Navegue a la pagina de pasajero/crear
    Then Observare que accedi a la pagina con titulo "Crear Pasajero"
    
