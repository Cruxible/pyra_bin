from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'console'

executables = [
    Executable('py3_11_repeater.py', base=base, target_name = 'pyra_repeater')
]

setup(name='pyra_repeater',
      version = '1.0',
      description = 'auto-messanger',
      options = {'build_exe': build_options},
      executables = executables)
