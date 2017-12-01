import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
	name="Checkers",
	options={"build_exe": {"packages":["pygame"],
													"include_files":["board.png"]}},
	executables = executables
)