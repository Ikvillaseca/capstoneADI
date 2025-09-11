from behave import given, when, then

@when('I visit "{url}"')
def step_impl(context, url):
    context.browser.get(context.get_url(url))