Feature: Ejecucion del servidor de Django
  Para las pruebas se debe verificar que se tiene acceso a la url de Django

  Scenario: Navegar a la pagina de inicio
    Given El navegador esta abierto
    When Navegue a la pagina de inicio
    Then Observare que accedi a la pagina con titulo "RouteAnvil" 
