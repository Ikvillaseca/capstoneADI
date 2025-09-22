Feature: Gestión de pasajeros
  Como dueño del negocio
  Quiero gestionar los pasajeros que solicitan las empresas que sean llevados
  Para poder asignar pasajeros a la flota de vehículos

  Scenario: Ver página de pasajeros
    Given El navegador esta abierto
    When Navegue a la pagina de pasajeros
    Then Observare que accedi a la pagina con titulo "Lista de Pasajeros"