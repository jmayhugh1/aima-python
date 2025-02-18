
from logic4e_modify_v01 import *

## Alices pass her public to first and Bob passer her public info to second
'''takes thea cnf and converts to form ppsat can understand'''
def cnf_to_ppsat(clause):
    clause = str(clause).replace(' | ', " ").replace('~','-')
    clauses = clause.split(' & ')
    clauses = [("(" + c if c[0] != '(' else c) for c in clauses]
    clauses = [ (c + ")" if c[-1] != ')' else c).replace('((','(').replace('))',')') for c in clauses ]
    return '"' + " ".join(clauses).strip() + '"'

def ppsat_to_cnf(clause : str):
    '''
    passed in the form {A B C D}
    '''
    if not clause:
        return None
    clause = clause[1:-1]
    clause = clause.replace(" ", " & ")
    return to_cnf(clause)
    
    
    pass
    
def ppsat_wrappet(master, agent):
    ## run the ./ppsat with args for 
    pass
class AgentKB(KB):
    def __init__(self, master: KB, sentence=None, mode=0):
        self.public = []
        self.private = []
        self.master = master
        if sentence:
            self.tell_public(sentence) if mode == 0 else self.tell_private(sentence)
            
    '''
    tell accepts a sentence and a mode, if mode is 0 then the sentence is added to public knowledge base
    if mode is 1 then the sentence is added to private knowledge base
    '''
    def tell(self, sentence, mode = 0):
        """Add the sentence to the KB."""
        if mode == 0:
            self.tell_public(sentence)
        else:
            self.tell_private(sentence)
    def tell_private(self, sentence):
        self.private.extend(conjuncts(to_cnf(sentence)))
    def tell_public(self, sentence):
        self.public.extend(conjuncts(to_cnf(sentence)))
    
    def ask_master(self):
        """Return True if the KB entails query, else return False."""
        return self.ask_master(self.master)
    def _ask_master(self, master):
        ## create a connection with
        agent_clauses = ""
        master_clauses = ""
        for c in self.public:
            agent_clauses += cnf_to_ppsat(c) + " "
        for c in self.private:
            agent_clauses += cnf_to_ppsat(c) + " "
        for c in master.public:
            master_clauses += cnf_to_ppsat(c) + " "
        for c in master.private:
            master_clauses += cnf_to_ppsat(c) + " "
        print("self clauses:", agent_clauses)
        print("master clauses:", master_clauses)
        ## now go up a file and 
            
        
        
        
        
            

    def ask_generator(self, query):
        """Yield the empty substitution {} if KB entails query; else no results."""
        clauses = self.public + self.private
        if tt_entails(Expr('&', *clauses), query):
            yield {}

    def ask_if_true(self, query):
        """Return True if the KB entails query, else return False."""
        for _ in self.ask_generator(query):
            return True
        return False

    def retract(self, sentence):
        """Remove the sentence's clauses from the KB."""
        for c in conjuncts(to_cnf(sentence)):
            if c in self.public:
                self.clauses.remove(c)
            if c in self.private:
                self.clauses.remove(c)
    ## in order to use share we need both KB parties to be sitting in serber, the calling kb will be Alice and the other will be Bob
    
    
    
        
        
def ppsat_to_cnf_test():
    t1 = ppsat_to_cnf('{A B C D}')
    print("Test 1: {A B C D}  -->", t1)
    
    t2 = ppsat_to_cnf("{A}")
    print("Test 2: {A}  -->", t2)
    
    
    
def cnf_tests():

    # Test 1: Biconditional negation conversion using '<=>'
    t1 = to_cnf('~(P11 <=> P12)')
    print(type(t1))
    print("Test 1: ~(P11 <=> P12)  -->", t1)
    print("Formatted:", cnf_to_ppsat(t1))

    # Test 2: Forward implication conversion using '==>'
    # Expected conversion: A ==> B  becomes  B | ~A
    t2 = to_cnf('A ==> B')
    print("Test 2: A ==> B       -->", t2)
    print("Formatted:", cnf_to_ppsat(t2))

    # Test 3: Reverse implication conversion using '<=='
    # Expected conversion: A <== B  becomes  A | ~B
    t3 = to_cnf('A <== B')
    print("Test 3: A <== B       -->", t3)
    print("Formatted:", cnf_to_ppsat(t3))

    # Test 4: Biconditional conversion using '<=>'
    # Expected conversion: A <=> B becomes (A | ~B) & (B | ~A)
    t4 = to_cnf('A <=> B')
    print("Test 4: A <=> B       -->", t4)
    print("Formatted:", cnf_to_ppsat(t4))

    # Test 5: Exclusive OR conversion using '^'
    # Expected conversion: A ^ B becomes (A & ~B) | (~A & B)
    t5 = to_cnf('A ^ B')
    print("Test 5: A ^ B         -->", t5)
    print("Formatted:", cnf_to_ppsat(t5))

    # Test 6: Standard logical operators
    # Example: ~(A | B) should convert to ~A & ~B using De Morgan's law.
    t6 = to_cnf('~(A | B)')
    print("Test 6: ~(A | B)      -->", t6)
    print("Formatted:", cnf_to_ppsat(t6))

    # Test 7: A more complex expression combining various operators
    t7 = to_cnf('(A ==> B) & ~(C <=> D) | (E ^ F)')
    print("Test 7: (A ==> B) & ~(C <=> D) | (E ^ F)  -->", t7)
    print("Formatted:", cnf_to_ppsat(t7))

    # Test 8: Expression already in CNF should remain unchanged.
    t8 = to_cnf('(A | ~B) & (C | D)')
    print("Test 8: (A | ~B) & (C | D) -->", t8)
    print("Formatted:", cnf_to_ppsat(t8))

    # Test 9: Extra parentheses and whitespace.
    t9 = to_cnf('  ((A))  &  ( ~(B |  C) ) ')
    print("Test 9: ((A)) & ( ~(B | C) )  -->", t9)
    print("Formatted:", cnf_to_ppsat(t9))

    # Test 10: Nested implications.
    t10 = to_cnf('A ==> (B ==> C)')
    print("Test 10: A ==> (B ==> C)  -->", t10)
    print("Formatted:", cnf_to_ppsat(t10))

    # Test 11: Single literal (if allowed by your parser).
    # If your parser accepts a single literal as a valid expression.
    t11 = to_cnf('A')
    print("Test 11: A  -->", t11)
    print("Formatted:", cnf_to_ppsat(t11))
    
    
    pass
    
#cnf_tests()
ppsat_to_cnf_test()
    