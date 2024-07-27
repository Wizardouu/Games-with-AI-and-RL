class arc_const_object:
    def __init__(self,old_dom, new_dom, element_1, element_2):
        self.old_domain = old_dom
        self.new_domain = new_dom
        self.removed_element = list(set(old_dom) - set(new_dom))
        self.elm1 = element_1
        self.elm2 = element_2
        self.output_file = "arc_consistency_log.txt"
        #self.step = step
    
    def is_before(self, other):
        if self.elm1[0] <= other[0]:
            return True
        elif self.elm1[0] == other[0] and self.elm1[1] <= other[1]:
            return True
        else:
            return False


    def print_ac3(self):
        #print(f"Step: {self.step}")
        if (self.old_domain == self.new_domain):
            print(f"Arc-Consistent between ({self.elm1[0]},{self.elm1[1]}) and ({self.elm2[0]},{self.elm2[1]})\n")
            print("No domain Change\n\n")
        else:
            print(f"NOT Arc-Consistent between ({self.elm1[0]},{self.elm1[1]}) and ({self.elm2[0]},{self.elm2[1]})\n")
            print(f"To become Arc-Consistency removed element {self.removed_element} from domain of cell ({self.elm1[0]},{self.elm1[1]})\n")
            print(f"The domain of the cell ({self.elm1[0]},{self.elm1[1]})before remove {self.old_domain} \n")
            print(f"So the new domain of the cell ({self.elm1[0]},{self.elm1[1]}): {self.new_domain}\n\n")



        
    
