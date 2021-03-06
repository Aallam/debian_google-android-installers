import re, os.path, glob
import maintscript.buildtools_install, maintscript.buildtools_postinst, maintscript.buildtools_postrm, maintscript.buildtools_config, maintscript.buildtools_templates, maintscript.buildtools_dirs, maintscript.buildtools_control, maintscript.buildtools_lintianoverrides, maintscript.buildtools_rules

pkg_dir = ""

def get(soup,pif):
    pkg_dir = os.path.join(glob.glob(os.path.expanduser(pif))[0], '')
    # Get build-tools list
    buildtools_list = soup.findAll('build-tool') 

    # Show results
    latest = buildtools_list[0]
    for bt in buildtools_list:
        if int(bt.revision.major.string) < int (latest.revision.major.string):
            gen(latest)
            latest = bt
            if bt == buildtools_list[-1]:
                gen(latest)
        elif int(bt.revision.minor.string) > int (latest.revision.minor.string):
            latest = bt
        elif int(bt.revision.micro.string) > int (latest.revision.micro.string):
            latest = bt

def gen(buildtools):            
        archive = buildtools.archives.archive.url.string
        sha1 =  buildtools.archives.archive.checksum.string
        api_level = buildtools.revision.major.string
        binary = "google-android-build-tools-"+api_level+"-installer"
        install = pkg_dir+"debian/"+binary+".install"
        postinst = pkg_dir+"debian/"+binary+".postinst"
        postrm = pkg_dir+"debian/"+binary+".postrm"
        config = pkg_dir+"debian/"+binary+".config"
        templates = pkg_dir+"debian/"+binary+".templates"
        dirs = pkg_dir+"debian/"+binary+".dirs"
        overrides = pkg_dir+"debian/"+binary+".lintian-overrides"
        control = pkg_dir+"debian/control"
        rules = pkg_dir+"debian/rules"
        sha1sum = pkg_dir+"for-postinst/default/"+archive+".sha1"
        current_sha1sum = ""
    
        version = api_level+"."+buildtools.revision.minor.string+"."+buildtools.revision.micro.string
        print(("\033[1;32m- Google build tools "+api_level+" for Android \033[0m ("+version+")"))

        # Generate/Update <package>.install
        if os.path.isfile(install):
            f = open(install)
            current_sha1sum = re.search(r"build-tools_r.+-linux.zip.sha1",f.readlines()[1]).group()
            if current_sha1sum == archive+".sha1":
                print("\033[0;32mOK\033[0m "+binary+".install")
            else:
                print("\033[0;33mOUTDATED\033[0m "+binary+".install")
                f.seek(0)
                i = f.read()
                o = open(install,"w")
                o.write(i.replace(current_sha1sum, archive+".sha1"))
                print(":... \033[0;34mUPDATED\033[0m from "+current_sha1sum+" to "+archive+".sha1")
                o.close()
        else:
            print("\033[0;31mNOT EXIST\033[0m "+binary+".install")
            maintscript.buildtools_install.generate(install,api_level,archive)       

        # Generate/Update <archive>.sha1
        current_sha1sum_file = pkg_dir+"for-postinst/default/"+current_sha1sum
        generate_sha1 = False
        if current_sha1sum != "":
           if os.path.isfile(current_sha1sum_file):
               f = open(current_sha1sum_file)
               current_sha1 = re.search(r'\b[0-9a-f]{5,40}\b',f.readlines()[0]).group()
               if current_sha1sum_file != sha1sum:
                   # Remove outdated sha1 file
                   try:
                       os.remove(current_sha1sum_file)
    	           except OSError:
                       pass
                   # Generate new sha1 file
                   if os.path.isfile(sha1sum):
                       print("\033[0;32mOK\033[0m "+archive+".sha1")
                   else:
                       generate_sha1 = True
               elif current_sha1 != sha1:
                   generate_sha1 = True
           else:
               generate_sha1 = True
        else:
           generate_sha1 = True

        # Generate SHA1 if needed
        if generate_sha1 == True:
            i = open(pkg_dir+"for-postinst/default/"+archive+".sha1", "w+")
            i.write(sha1+"  "+archive)
            i.close()
            print ":... \033[0;34mGENERATED\033[0m "+archive+".sha1"
    
        # Generate/Update <package>.postinst
        if os.path.isfile(postinst):
            f = open(postinst)
            match = re.search(r"build-tools_r.+-linux.zip",f.readlines()[7]).group()
            if match == archive:
                print("\033[0;32mOK\033[0m "+binary+".postinst")
            else:
                print("\033[0;33mOUTDATED\033[0m "+binary+".postinst")
                f.seek(0)
                i = f.read()
                o = open(postinst,"w")
                o.write(i.replace(match, archive))
                print(":... \033[0;34mUPDATED\033[0m from revision  to "+archive)
                o.close()
        else:
            print("\033[0;31mNOT EXIST\033[0m "+binary+".postinst")
            maintscript.buildtools_postinst.generate(postinst,api_level,archive,version)
    
        # Generate <package>.postrm
        if os.path.isfile(postrm):
           print("\033[0;32mOK\033[0m "+binary+".postrm")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".postrm")
           maintscript.buildtools_postrm.generate(postrm,api_level)

        #Generate <package>.config
        if os.path.isfile(config):
           print("\033[0;32mOK\033[0m "+binary+".config")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".config")
           maintscript.buildtools_config.generate(config,api_level)

        # Generate <package>.templates
        if os.path.isfile(templates):
           print("\033[0;32mOK\033[0m "+binary+".templates")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".templates")
           maintscript.buildtools_templates.generate(templates,api_level)

        # Generate <package>.dirs
        if os.path.isfile(dirs):
           print("\033[0;32mOK\033[0m "+binary+".dirs")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".dirs")
           maintscript.buildtools_dirs.generate(dirs,api_level)

        #Generate <package>.lintian-overrides
        if os.path.isfile(overrides):
           print("\033[0;32mOK\033[0m "+binary+".lintian-overrides")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".lintian-overrides")
           maintscript.buildtools_lintianoverrides.generate(overrides,api_level)

        # Add package to d/control
        if "build-tools-"+api_level+"-" in open(control).read():
           print("\033[0;32mOK\033[0m "+binary+" in d/control")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+" in d/control")
           maintscript.buildtools_control.generate(control,api_level,archive)

        # Add package to d/rules
        maintscript.buildtools_rules.generate(rules,api_level,version)
