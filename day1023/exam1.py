# 클래스
class Student :
    # 생성자( 인스턴스가 생성될때 자동호출되는 메소드 )
    # def __init__(self, 멤버변수... ):
    #       self.멤버변수1 = 멤버변수1 
    def __init__(self,name,korean,math,english,science):
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        sel.science = science
    
    # def 메소드명(self, 매개변수...)
    def get_sum(self):
        return self.korean+self.math+self.english+self.science
    def get_average(self):
        return self.get_sum()/4
    def to_string(self):
        return "{} \t {} \t {}".format(self.name,self.get_sum(), self.get_average())
    def __str__(self):
        return "{} \t {} \t {}".format(self.name,self.get_sum(), self.get_average())
    def __eq__(self,value):
        return self.get_sum() == value.get_sum()
    def __ne__(self,value):
        return self.get_sum() != value.get_sum()
    def __gt__(self,value):
        return self.get_sum()!=value.get_sum()
    def __ge__(self,value):
        return self.get_sum() >=value.get_sum()
    def __lt__(self,value):
        return self.get_sum() < value.get_sum()
    def __le___(self,value):
        return self.get_sum() <= value.get_sum()
            
# 일반함수 vs 클래스 내 메소드?
# 
def get_sum2():
    pass
# 생성자를 이용한 인스턴스 생성
students = [
    Student("황소연", 90, 100, 89, 94),
    Student("황소연", 90, 100, 89, 94),
    Student("황소연", 90, 100, 89, 94),
    Student("황소연", 90, 100, 89, 94),
    Student("황소연", 90, 100, 89, 94),
    Student("황소연", 90, 100, 89, 94)
]

print( students[0].korean )


print(str(students[0]))

print (students[0]== students[1])
