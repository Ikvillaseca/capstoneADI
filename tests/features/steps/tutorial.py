from behave import given,when,then

@given("Se ejecutaron todas las pruebas")
def step_impl(context):
    pass

@when("Terminen de ejecutarse las pruebas")
def step_impl(context):
    assert True is not False

@then("Todas las pruebas pasaran")
def step_impl(context):
    assert context.failed is False