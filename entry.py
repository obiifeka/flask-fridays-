class Person:
    def __init__(self, name, age):
          self.name = name
          self.age = age
    
            
    def setSchool(self,school):
        self.school = school
    def getSchool(self):
        return self.school
        
            
    def random(self):
        print("my name is", self.name)
        print("my age is", self.age)

  
each_person = Person("Obi", 30)
each_person.setSchool("Oxford")

print(each_person.age)
each_person.random()
print(each_person.getSchool())