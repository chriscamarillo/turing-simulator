def alpha_pos(key: str):
    assert key.isupper()
    return ord(key) - ord('A')

class Rotor:
    def __init__(self, cipher: str, notch: str, position: str):
        self.cipher = cipher
        self.notch = notch
        self.position = alpha_pos(position)

    def onnotch(self):
        return self.cipher[self.position] is self.notch

    def encode(self, key):
        result = self.cipher[(self.position + alpha_pos(key)) % len(self.cipher)]
        # print('<A> starts from', self.cipher[self.position])
        print(key, '->', result)
        return result

    def tick(self):
        self.position = (self.position + 1) % 26

class Enigma:
    def __init__(self, reflector: Rotor, l_rotor: Rotor, m_rotor: Rotor, r_rotor: Rotor, plugs: str):
        self.reflector = reflector
        self.l_rotor = l_rotor
        self.m_rotor = m_rotor
        self.r_rotor = r_rotor
        self.plugs = plugs

    def transform(self, text: str) -> str:
        return ''.join([self.push(c) for c in text])

    def push(self, key: str) -> str:
        self.update_rotors()
        i = self.r_rotor.encode(key)
        j = self.m_rotor.encode(i)
        k = self.l_rotor.encode(j)
        reflected = self.reflector.encode(k)
        l = self.l_rotor.encode(reflected)
        m = self.m_rotor.encode(l)
        final = self.r_rotor.encode(m)
        print()
        return final

    def plugboard_replace(self, key: str) -> str:
        pass

    def update_rotors(self):
        if self.m_rotor.onnotch():
            self.l_rotor.tick()
        if self.r_rotor.onnotch():
            self.m_rotor.tick()
        self.r_rotor.tick()


id = Rotor('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'A', 'A')
rotorI = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 'F')
rotorII = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E', 'U')
rotorIII = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V', 'N')
reflB = Rotor('YRUHQSLDPXNGOKMIEBFZCWVJAT', 'A', 'A')

mock_I = Rotor('ABCD', 'A', 'A')
mock_II = Rotor('CADB', 'A', 'C')
mock_III = Rotor('DCBA', 'A', 'B')
mock_reflect = Rotor('CDAB', 'A', 'A')

def main():
    plugs = 'EJ.OY.IV.AQ.KW.FX.MT.PS.LU.BD'
    machine_alice = Enigma(reflB, rotorI, rotorII, rotorIII, plugs)
    text = 'O'
    print('result:', machine_alice.transform(text))


if __name__ == '__main__':
    main()
