def generate(control,api_level,archive):
    f = open("script/maintscript/google-android-build-tools-X-installer.control.ex")
    i = f.read()
    o = open(control, "a")
    i = i.replace("$X",api_level).replace("$Y",archive)
    o.write(i)
    o.close()
    print ":... \033[0;34mGENERATED\033[0m add google-android-build-tools-"+api_level+"-installer to d/control"
