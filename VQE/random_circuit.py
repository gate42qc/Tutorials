import numpy as np
import random
from pyquil import Program
from pyquil.gates import RX, RZ, CZ, RY


class AnsatzCircuitGenerator:
    """
    creates an instence of the state preparation circuit for VQE input

    constructor takes arguments to specify the qubits and the  
    circuit depth

    two methods apply entangling gates and single qubit rotation gates on specified qubits.
    the 'generate' method does the work utilizing the other two methods
    PRAGMA PRESERVE_BLOCK and PRAGMA END_PRESERVE_BLOCK make sure to apply 
    necessary operations without the compiler optimizing for gates
    """
    def __init__(self, qubits, depth):
        self.qubits = qubits
        self.depth = depth
    
    def generate_first_layer(self, thetas) -> Program:
        p = Program()
        p.inst(self._apply_random_gates(thetas))
            
        return Program('PRAGMA PRESERVE_BLOCK') + p + Program('PRAGMA END_PRESERVE_BLOCK')
    
    def generate(self, thetas) -> Program:
        p = Program()
        p.inst(self._entangle())
        p.inst(self._apply_random_gates(thetas))

        return Program('PRAGMA PRESERVE_BLOCK') + p + Program('PRAGMA END_PRESERVE_BLOCK')
    
    def _apply_random_gates(self, thetas):
        random.seed(99999)
        gates = []
        L = len(thetas)
        for i in range(len(self.qubits)):
            j = random.randint(0, len(thetas))
            gate = random.choice([RZ(thetas[(i+j)%L], self.qubits[i]), 
                                  RX(thetas[(i+j)%L], self.qubits[i]), 
                                  RY(thetas[(i+j)%L], self.qubits[i])])
            gates.append(gate)
            
        return gates
        
    def _entangle(self):
        return [CZ(self.qubits[i], self.qubits[i+1]) for i in range(len(self.qubits)-1)]
    
    
def get_ansatz_circuit_generator(qubits, depth):
    """
    function to create the circuit for VQE ansatz state
    :param qubits: list, numbers in the list specify the qubits to apply gates
    :param depth: int, to specify the depth of the circuit
    """
    generator = AnsatzCircuitGenerator(qubits, 2)
    def get_random_circuit(thetas):
        vqe_ansatz = Program()
        vqe_ansatz += generator.generate_first_layer(thetas[:len(qubits)])
        for k in range(depth):
            vqe_ansatz += generator.generate(thetas[len(qubits):]) #thetas[k:k+2]
        return vqe_ansatz
    
    return get_random_circuit