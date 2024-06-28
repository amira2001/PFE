class Model:
    def __init__(self):
        pass

    def predict(self, data):
        customer_satisfaction_score = data['customer_satisfaction_score'].iloc[0]
        age = data['age'].iloc[0]
        avg__monthly_spend = data['avg__monthly_spend'].iloc[0]
        print('hhhhhhhhhh')
        print(customer_satisfaction_score)
        print(age)
        print(avg__monthly_spend)
        if customer_satisfaction_score < 4:
            if age < 36 and avg__monthly_spend< 4000:
                prediction = 0
            elif age < 36 and avg__monthly_spend >= 4000:
                prediction = 2
            elif age >= 36:
                prediction = 3
        else:
            if 4 <= customer_satisfaction_score <= 6:
                prediction = 5
            else:
                if age < 36 and avg__monthly_spend < 4000:
                    prediction = 4
                elif age < 36 and avg__monthly_spend >= 4000:
                    prediction = 1
                elif age >= 36:
                    prediction = 6

        return prediction

