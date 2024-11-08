from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
import flask_monitoringdashboard as dashboard
import os
from qiskit import QuantumCircuit, Aer, execute
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import QFT
from web3 import Web3
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
Talisman(app)
dashboard.bind(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Connect to Ethereum network (replace with your own endpoint)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR-PROJECT-ID'))

# Contract ABI and address (replace with your own contract details)
contract_abi = json.loads('[{"inputs":[{"internalType":"string","name":"result","type":"string"}],"name":"storeResult","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"results","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
contract_address = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Initialize machine learning model
ml_model = RandomForestClassifier(n_estimators=100, random_state=42)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.password_hash = bcrypt.generate_password_hash('Mynxie4417').decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

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
        user = User(username)
        if username == 'ianmcinturff' and user.check_password(password):
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
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=1000)
    result = job.result()
    counts = result.get_counts(circuit)
    
    # Store result on blockchain
    store_on_blockchain(str(counts))
    
    return jsonify(counts)

@app.route('/qft_demo')
@login_required
def qft_demo():
    qft = QFT(4)
    qft.measure_all()
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qft, backend, shots=1000)
    result = job.result()
    counts = result.get_counts(qft)
    
    # Store result on blockchain
    store_on_blockchain(str(counts))
    
    return jsonify(counts)

@app.route('/grover_demo')
@login_required
def grover_demo():
    def oracle(x):
        return x == '101'
    problem = AmplificationProblem(oracle, is_good_state=oracle)
    grover = Grover(quantum_instance=Aer.get_backend('qasm_simulator'))
    result = grover.amplify(problem)
    
    # Store result on blockchain
    store_on_blockchain(str(result.assignment_probability))
    
    return jsonify({
        'most_likely': result.top_measurement,
        'probability': result.assignment_probability
    })

@app.route('/ml_quantum_demo')
@login_required
def ml_quantum_demo():
    # Generate quantum data
    n_samples = 1000
    n_qubits = 4
    
    X = []
    y = []
    
    for _ in range(n_samples):
        circuit = QuantumCircuit(n_qubits, n_qubits)
        # Apply random gates
        for i in range(n_qubits):
            if np.random.random() > 0.5:
                circuit.h(i)
            if np.random.random() > 0.5:
                circuit.x(i)
        circuit.measure_all()
        
        backend = Aer.get_backend('qasm_simulator')
        job = execute(circuit, backend, shots=1)
        result = job.result()
        counts = result.get_counts(circuit)
        state = list(counts.keys())[0]
        
        X.append([int(bit) for bit in state])
        y.append(sum(int(bit) for bit in state) % 2)  # Simple classification task
    
    X = np.array(X)
    y = np.array(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    ml_model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = ml_model.predict(X_test)
    
    # Calculate accuracy
    accuracy = np.mean(y_pred == y_test)
    
    return jsonify({
        'accuracy': accuracy,
        'n_samples': n_samples,
        'n_qubits': n_qubits
    })

def store_on_blockchain(result):
    # Replace with your own account and private key
    account = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    private_key = 'YOUR-PRIVATE-KEY'
    
    nonce = w3.eth.get_transaction_count(account)
    
    # Build transaction
    txn = contract.functions.storeResult(result).build_transaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"Transaction receipt: {tx_receipt}")

if __name__ == '__main__':
    app.run(debug=True)
