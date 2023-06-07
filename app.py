from flask import Flask
from flask import render_template, request
import subprocess, os, base64
from subprocess import PIPE, Popen

app = Flask(__name__)


@app.route('/')
def Compiler():
    check = ''
    return render_template('home.html', check=check)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        code = request.form['code']
        inp = request.form['input']
        chk = request.form.get('check')

        if chk == '1':
            # If checkbox was ckecked then the input field will stay the same and checkbox will be checked.
            check = 'checked'
        else:
            # If checkbox was not ckecked then the input field will be empty and checkbox will be unchecked.
            inp = ""
            check = ''
        output = cpp_complier_output(code, inp, chk)

    return render_template('home.html', code=code, input=inp, output=output, check=check)


def cpp_complier_output(code, inp, chk):
    if not os.path.exists('test.cpp'):
        with open('test.cpp', 'w') as file_test:
            file_test.write(code)

    application = "C:\\gcc\\bin\\g++.exe"

    # result = subprocess.run([application, "test.cpp", "-o", "new.exe"], stderr=PIPE)
    result = subprocess.run([application, "test.cpp", "-o", "new.exe"], stderr=PIPE)
    check = result.returncode

    if check != 0:
        if os.path.exists('test.cpp'):
            os.remove('test.cpp')

        if os.path.exists('new.exe'):
            os.remove('new.exe')
        return result.stderr
    else:
        if chk == '1':
            inp = str.encode(inp)
            r = subprocess.run(["new"], input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            r = subprocess.run(["new"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if os.path.exists('test.cpp'):
            os.remove('test.cpp')

        if os.path.exists('new.exe'):
            os.remove('new.exe')
        outp = r.stdout
        return outp.decode("windows-1251")


if __name__ == '__main__':
    app.run()