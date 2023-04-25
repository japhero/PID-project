class Person:
  def __init__(self, age,name="BALLS"):
    self.name = name
    self.age = age
    self.d = 4

  def myfunc(self):
    print("Hello my name is " + self.name)

p1 = Person(36)
p1.myfunc()



