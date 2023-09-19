CallBacksStack = {
        "OnCreateMenu": [],
        "SelectedGameObjectsChanged": [],
    }

"""
def AddCallBackToStack(CallBackName, CallBack):
    CallBacksStack[CallBackName].append(CallBack)
"""
# decorators for add callbacks to stack
def AddCallBackToStack(CallBackName,Order=float("inf")):
    def decorator(callback):
        #check if callback is callable
        if not callable(callback):
            raise TypeError("Callback must be callable")
        #check if callback is already in stack
        if callback in CallBacksStack[CallBackName]:
            raise ValueError("Callback already in stack")
        #check CallBackName is in stack
        if not CallBackName in CallBacksStack:
            raise ValueError("CallBackName not in stack")
        callback.Order = Order
        CallBacksStack[CallBackName].append(callback)
        return callback
    return decorator

def CallBacksStackCall(CallBackName, *args, **kwargs):
    #sort CallBacks by Order
    CallBacksStack[CallBackName].sort(key=lambda x: x.Order)
    for CallBack in CallBacksStack[CallBackName]:
        CallBack(*args, **kwargs)
