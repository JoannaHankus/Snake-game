import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "D:\\Programy\\spyder\\WPy-3662\\python-3.6.6.amd64\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "D:\\Programy\\spyder\\WPy-3662\\python-3.6.6.amd64\\tcl\\tk8.6"
executables = [cx_Freeze.Executable("run.py")]

cx_Freeze.setup(


    name="A bit Racey",
    options= {"build_exe": {"packages": ["pygame"],
                            "include_files":["racecar.png",
                                             "Wood_Hit_Metal_Crash.wav",
                                             "Jazz_Me_Blues.wav",
                                             "bg.png",
                                             "snaked1.png",
                                             "snaked2.png",
                                             "intro.png",
                                             "apple.png",
                                             "block.png",
                                             "headleft.png",
                                             "headright.png",
                                             "headdown.png",
                                             "headup.png",
                                             "bgLvl2.png",
                                             "bgLvl3.png",
                                             "bgLvl4.png",
                                             "Hair_Ripping.wav"]}},
    executables = executables
)