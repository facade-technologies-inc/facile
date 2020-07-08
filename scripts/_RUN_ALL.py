if __name__ == "__main__":
    import os

    scripts = [
        "01_normalize_packages.py",
        "02_extra_downloads.py",
        "03_build_icon_resource.py",
        "04_build_rc.py",
        "05_build_ui.py",
    ]

    for script in scripts:
        if script.endswith(".py"):
            os.system("python {}".format(script))
        else:
            os.system(script)