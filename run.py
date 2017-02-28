from os import path, walk

from syllin import application

# run the app.
if __name__ == "__main__":
    # This allows for better reboot behavior when Jinja2 templates are being edited (by default, not all edits trigger
    # a server reboot)
    extra_dirs = ['syllin/templates/', ]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(extra_files=extra_files)
