from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from qiskit import QuantumCircuit, Aer, execute

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@login_required
def control_room():
    return render_template('control_room.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'ianmcinturff' and password == 'Mynxie4417':
            user = User(username)
            login_user(user)
            return redirect(url_for('control_room'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/quantum_demo')
@login_required
def quantum_demo():
    # Create a quantum circuit
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)  # Apply Hadamard gate to qubit 0
    circuit.cx(0, 1)  # Apply CNOT gate with control qubit 0 and target qubit 1
    circuit.measure([0, 1], [0, 1])

    # Execute the circuit on a simulator
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=1000)
    result = job.result()
    counts = result.get_counts(circuit)

    return jsonify(counts)

if __name__ == '__main__':
    app.run(debug=True)
