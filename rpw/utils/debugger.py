import inspect

def debug(context):
    from rpw.ui.forms import TextInput
    print(inspect.currentframe().f_back.f_locals)
    # x = raw_input('>')
    form = TextInput('Debug').show()
    eval(form.selected)
    # while True:
        # prompt = raw_input('>')
        # eval(prompt)
