def generate(install,api_level):
    f = open("script/maintscript/google-android-build-tools-X-installer.lintian-overrides.ex")
    i = f.read()
    o = open(install, "w")
    i = i.replace("$X",api_level)
    o.write(i)
    o.close()
    print ":... \033[0;34mGENERATED\033[0m google-android-build-tools-"+api_level+"-installer.lintian-overrides"
