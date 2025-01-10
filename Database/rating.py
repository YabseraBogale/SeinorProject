import sqlite3

class Rating():
    def __init__(self) -> None:
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()

    def InsertingRating(self,UID,RatedUserID,RateValue):
        try:
            statment="Insert Into Rating(UID,ratedUserID,rateValue) values(?,?,?)"
            self.pointer.execute(statment,(UID,RatedUserID,RateValue))
            self.connection.commit()
            return True
        except Exception as e:
            return False

    def SumRatingOfUser(self,RatedUserID):
        try:
            statment="Select Sum(rateValue) from Rating where ratedUserID=?"
            self.pointer.execute(statment,(RatedUserID,))
            result=self.pointer.fetchone()
            if result is None:
                return 0
            return result[0]
        except Exception as e:
            return 0
    
    def MinRatingOfUser(self,RatedUserID):
        try:
            statment="Select MIN(rateValue) from Rating where ratedUserID=?"
            self.pointer.execute(statment,(RatedUserID,))
            result=self.pointer.fetchone()
            if result is None:
                return 0
            return result[0]
        except Exception as e:
            return e
    
    def AverageRatingOfUser(self,RatedUserID):
        try:
            return self.SumRatingOfUser(RatedUserID)/5
        except Exception as e:
            return e
        
    def CountOfRatingOfUser(self,RatedUserID):
        try:
            statment="Select Count(rateValue) from Rating where ratedUserID=?"
            self.pointer.execute(statment,(RatedUserID,))
            result=self.pointer.fetchone()
            if result is None:
                return 0
            return result[0]
        except Exception as e:
            return e
    
    def BayesianRatingOfUser(self,RatedUserID):
        try:
            avaerage=self.AverageRatingOfUser(RatedUserID)
            numberOfReview=self.CountOfRatingOfUser(RatedUserID)
            sum=self.SumRatingOfUser(RatedUserID)
            min=self.MinRatingOfUser(RatedUserID)
            return self.truncate_float(((avaerage*min)+sum)/(min+numberOfReview),2)
        except Exception as e:
            return e
    
    def truncate_float(self,float_number, decimal_places):
        multiplier = 10 ** decimal_places
        return int(float_number * multiplier) / multiplier
