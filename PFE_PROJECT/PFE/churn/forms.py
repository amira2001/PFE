from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SuperuserLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_superuser:
            raise forms.ValidationError(
                "Only superusers can access this page."
            )


class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'
class PredictionForm(forms.Form):

    CHOICES_Click_Rate =[('Low', 'Low'),('Medium', 'Medium'),('High', 'High')]
    CHOICES_Products_Purchased = [('Mobile', 'Mobile'),('Internet', 'Internet'),('Mobile, Internet', 'Mobile, Internet')]
    CHOICES_Profile =[('Business','Business'),('Personal', 'Personal')]
    CHOICES_gender = [('Male', 'Male'),('Female', 'Female')]
    CHOICES_Contract_Type =[('Prepaid', 'Prepaid'),('Postpaid', 'Postpaid')]
    AGE_CHOICES = [(str(i), str(i)) for i in range(19, 71)]
    CHOICES_Income_Level = [('25,000 or less', '25,000 or less'),('25,000-50,000', '25,000-50,000'),('50,000-75,000', '50,000-75,000'),('75,000-100,000', '75,000-100,000'),('100,000+', '100,000+')]
    CHOICES_Device_Type = [('Smartphone', 'Smartphone'),('Desktop', 'Desktop'),('Tablet', 'Tablet')]
    CHOICES_Plan_Type = [('Unlimited', 'Unlimited'),('Limited', 'Limited')]
    CHOICES_Monthly_Spend = [('1000', '1000'),('1500', '1500'),('2000', '2000'),('2500', '2500'),('3000', '3000'),('3500', '3500'),('4000', '4000'),('4500','4500'),('5000', '5000'),('5500', '5500'),('6000', '6000'),('6500', '6500'),('7000', '7000')]
    CHOICES_Preferred_Communication_Channel = [('SMS', 'SMS'),('Calls', 'Calls'),('App Notifications', 'App Notifications')]
    CHOICES_Customer_Satisfaction_Score = [('1/10', '1/10'),('2/10', '2/10'),('3/10', '3/10'),('4/10', '4/10'),('5/10', '5/10'),('6/10', '6/10'),('7/10', '7/10'),('8/10','8/10'),('9/10', '9/10'),('10/10', '10/10')]
    WILAYA_CHOICES = [
        ('Relizane', 'Relizane'),
        ('Blida', 'Blida'),
        ('Algiers', 'Algiers'),
        ('Constantine', 'Constantine'),
        ('Tiaret', 'Tiaret'),
        ("M'Sila", "M'Sila"),
        ('Djelfa', 'Djelfa'),
        ('Tipaza', 'Tipaza'),
        ('Oran', 'Oran'),
        ('Annaba', 'Annaba'),
        ('Skikda', 'Skikda'),
        ('Boumerdès', 'Boumerdès'),
        ('Mascara', 'Mascara'),
        ('Jijel', 'Jijel'),
        ('Ghardaïa', 'Ghardaïa'),
        ('Sétif', 'Sétif'),
        ('Chlef', 'Chlef'),
        ('Bordj Bou Arréridj', 'Bordj Bou Arréridj'),
        ('Saïda', 'Saïda'),
        ('Tlemcen', 'Tlemcen'),
        ('Naâma', 'Naâma'),
        ('Aïn Defla', 'Aïn Defla'),
        ('El Bayadh', 'El Bayadh'),
        ('Béjaïa', 'Béjaïa'),
        ('Béchar', 'Béchar'),
        ('Laghouat', 'Laghouat'),
        ('Ouargla', 'Ouargla'),
        ('Tébessa', 'Tébessa'),
        ('Biskra', 'Biskra'),
        ('Oum El Bouaghi', 'Oum El Bouaghi'),
        ('Guelma', 'Guelma'),
        ('Batna', 'Batna'),
        ('Mostaganem', 'Mostaganem'),
        ('Tizi Ouzou', 'Tizi Ouzou'),
        ('Sidi Bel Abbès', 'Sidi Bel Abbès'),
        ('Aïn Témouchent', 'Aïn Témouchent'),
        ('Tissemsilt', 'Tissemsilt'),
        ('El Oued', 'El Oued'),
    ]
    CHOICES_Occupation = [('Engineer', 'Engineer'),('Teacher', 'Teacher'),('Doctor', 'Doctor'),('Accountant', 'Accountant'),('Lawyer', 'Lawyer'),('Nurse', 'Nurse'),('IT Technician', 'IT Technician'),('Salesperson','Salesperson')]



    choice_field_Click_Rate = forms.ChoiceField(label='Click Rate', choices=CHOICES_Click_Rate)
    choice_field_Products_Purchased = forms.ChoiceField(label='Products Purchased', choices=CHOICES_Products_Purchased)
    choice_field_Profile = forms.ChoiceField(label='Profile', choices=CHOICES_Profile)
    choice_field_Gender = forms.ChoiceField(label='gender', choices=CHOICES_gender)
    choice_field_Contract_Type = forms.ChoiceField(label='Contract Type', choices=CHOICES_Contract_Type)
    age = forms.ChoiceField(label='Age', choices=AGE_CHOICES)
    choice_field_Income_Level = forms.ChoiceField(label='Income Level', choices=CHOICES_Income_Level)
    choice_field_Device_Type = forms.ChoiceField(label='Device Type', choices=CHOICES_Device_Type)
    choice_field_Plan_Type = forms.ChoiceField(label='Plan Type', choices=CHOICES_Plan_Type)
    choice_field_Avg_Monthly_Spend = forms.ChoiceField(label='Avg. Monthly Spend', choices=CHOICES_Monthly_Spend)
    choice_Preferred_Communication_Channel = forms.ChoiceField(label='Preferred Communication Channel', choices=CHOICES_Preferred_Communication_Channel)
    contract_start_date = forms.DateField(label='Contract Start Date', widget=DateInput(), input_formats=['%Y-%m-%d'])
    choice_field_Customer_Satisfaction_Score = forms.ChoiceField(label='Customer Satisfaction Score', choices=CHOICES_Customer_Satisfaction_Score)
    wilaya = forms.ChoiceField(label='Wilaya', choices=WILAYA_CHOICES)
    choice_field_Occupation = forms.ChoiceField(label='Occupation', choices=CHOICES_Occupation)


    # Ajoutez plus de champs selon vos besoins

