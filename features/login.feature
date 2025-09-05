Feature: Login de usuarios

  Scenario: Usuario accede correctamente
    Given el usuario tiene cuenta
    When intenta acceder al sitio con su usuario y contraseña
    Then logra acceder al sitio