import ptvsd
ptvsd.enable_attach("nico", address = ('0.0.0.0', 3000))

# Enable the line of source code below only if you want the application to wait until the debugger has attached to it
# ptvsd.wait_for_attach()

#The debug server has started and you can now use VS Code to attach to the application for debugging
print("Google App Engine has started, ready to attach the debugger")