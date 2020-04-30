# function decorator to display 
# annotated message before function execution
def entry_deco(msg):
    def func_wrapper(func):
        def wrapped(*args, **kwargs):
            print('{}'.format(msg))
            rslt = func(*args, **kwargs)
            return rslt
        return wrapped
    return func_wrapper
