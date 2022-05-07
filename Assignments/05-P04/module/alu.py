class Alu(object):
    def __init__(self, registers):
        self.lhs = None
        self.rhs = None
        self.op = None
        self.registers = registers
        self.ops = {"ADD": self.add, "SUB": self.sub, "MUL": self.mul, "DIV": self.div}

    def exec(self, op):
        self.lhs = self.registers[0].read()
        self.rhs = self.registers[1].read()
        self.op = op.upper()
        ans = self.ops[self.op](self.lhs, self.rhs)
        self.registers[0].write(ans)
    
    def add(self, l, r):
        return l + r

    def sub(self, l, r):
        return l - r

    def mul(self, l, r):
        return l * r

    def div(self, l, r):
        if r == 0:
            return 0
        return l / r

    def __str__(self):
        return f"{self.lhs} {self.op} {self.rhs}"
