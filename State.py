class State(object):
    def __init__(self, state_type, next_state=None):
        """If state_type='Start', then a next_state must be provided."""
        if state_type not in ('Accept', 'Push', 'Pop', 'Read', 'Start'):
            raise SystemExit(state_type + " is not a valid State type!")
        if state_type == 'Start' and not next_state:
            raise SystemExit("Start states must be provided a next_state!")
        self.state_type = state_type
        self.transitions = list()
        self.next_state = next_state

    def add_transition(self, next_state, character=None):
        """Adds a transition to the list of the state's acceptable
        transitions.  A transition consists of at least a  next state, and a
        character depending on the type of the state."""
        transition = {'char': character, 'next': next_state}
        self.transitions.append(transition)

    def get_next_state(self, character=None):
        """Retrieves the next state that the PDA should go to, based on the
        current state's type, and an input from either the tape or stack."""       
        if self.state_type == "Start":
            return self.next_state

        if self.state_type == "Read":
            if character == "":
                return self.transitions[0]['next']

            for transition in self.transitions:
                if transition['char'] == character:
                    return transition['next']

        if self.state_type == "Push":
            return self.transitions[0]['next']

        if self.state_type == "Pop":
            for transition in self.transitions:
                if transition['char'] == character:
                    return transition['next']

    def action(self, tape, stack,step = 0, current_state="first",rule_num=0, verbose=True):
        """If state_type is Read, Push, or Pop, the respective action is taken
        and the get_next_state() retrieves the next state in the PDA.  The
        action() function of the next state is then called.
        If state_type is Start, next state's action() function is called.
        If state_type is Accept, the state simply prints a message."""
        if verbose:
            if current_state=="first":
                print ("Step#    State Rule  Stack        Input Left")
                print ("0    q_0    0    ----         TAPE:  "+tape)
            if current_state == "q-2":  
                if tape[0] == "b":
                    rule_num=4
                    current_state = "q-2"
                else:
                    current_state = "q-3"
                    rule_num=5
            elif current_state == "q-1":
                if tape[0] == "a":
                    rule_num=2
                    current_state = "q-1"
                elif tape[0] == "b":
                    rule_num=3
                    current_state = "q-2"
            elif current_state == "q-0":
                current_state = "q-1"
                rule_num=1
            if current_state!="first":
                if step<10:
                    print (step,end="    ")
                else:
                    print (step,end="   ")
                print (current_state,end="    ")
                print (rule_num,end="    ")
                if stack:
                    print("STACK: ", stack[-1],end="    ")
                else:
                    print("STACK: ", stack, end="    ")
                print("TAPE: ", tape)
        try:
            if self.state_type == "Start":
                current_state="q-0"
                rule_num=0
                #if verbose:
                    #print("START -> next_state")
                self.get_next_state().action(tape, stack, step+1,current_state,rule_num,
                                             verbose)
            elif self.state_type == "Read":
                #if verbose:
                    #print("READ " + tape[0] + "")
                self.get_next_state(character=tape[0]).action(tape[1:], stack, step+1,
                                                              current_state,rule_num,
                                                              verbose)
            elif self.state_type == "Push":
                char = self.transitions[0]['char']
                stack.append(char)
                #if verbose:
                 #  print("PUSH " + char + "")
                self.get_next_state().action(tape, stack, step+1,current_state,
                                             rule_num, verbose)
            elif self.state_type == "Pop":
                char = stack.pop()
                #if verbose:
                 #   print("POP " + char + "")
                self.get_next_state(character=char).action(tape, stack, step+1,
                                                           current_state,rule_num, verbose)
            elif self.state_type == "Accept":
                print("Tape accepted!")
                if verbose:
                    print("FINAL TAPE: ", tape)
                    print("FINAL STACK: ", stack)
            else:
                pass
        except:
            print("Tape NOT accepted!")
            if verbose:
                print("FINAL TAPE: ", tape)
                print("FINAL STACK: ", stack)
