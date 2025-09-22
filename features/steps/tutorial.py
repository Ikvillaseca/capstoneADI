from behave import given,when,then

@given("tenemos behave instalado")
def step_impl(context):
    pass

@when("implementamos una prueba")
def step_impl(context):
    assert True is not False

@then("behave lo probara por nosotros")
def step_impl(context):
    assert context.failed is True