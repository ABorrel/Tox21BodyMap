from os import system, path, remove, chdir, getcwd, listdir

def runRCMD(cmd, out = 0):

    chdir("./../R/")
    print cmd
    if out == 0:
        system(cmd)
        output = 0
    else:
        import subprocess
        output = subprocess.check_output(cmd, shell=True)
    chdir("./../py/")
    return output






def histExpresion(pfilin):

    cmd = "./histExpression.R " + pfilin
    runRCMD(cmd)
