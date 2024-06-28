from django.shortcuts import render,HttpResponse , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.conf import settings
import os
from .forms import PredictionForm
from django.views.decorators.csrf import csrf_exempt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder,OrdinalEncoder,StandardScaler
import pickle
import polars as pl 
from .prediction_model import Model
# Create your views here.


@login_required
def Dashboard(request):
    excel_path = os.path.join(settings.BASE_DIR, 'churn/static/files/customer_data_algeria.xlsx')
    
    # Lire le fichier Excel avec pandas
    df = pl.read_excel(excel_path)
    df = pd.DataFrame(df.to_dicts())
    # Convertir le DataFrame en liste de dictionnaires
    data_size = df.shape[0]
    top_produit = df['Products Purchased'].value_counts().idxmax()
    top_Contrat = df['Contract Type'].value_counts().idxmax()
    top_appareil = df['Device Type'].value_counts().idxmax()
    top_canal = df['Preferred Communication Channel'].value_counts().idxmax()

    profil_counts = df['Profile'].value_counts()
    profil_lebels = profil_counts.index.tolist()
    profil_data = profil_counts.tolist()

    location_counts = df['Location'].value_counts()
    location_labels = location_counts.index.tolist()
    location_data = location_counts.tolist()

    clic_counts = df['Click Rate'].value_counts()
    clic_labels = clic_counts.index.tolist()
    clic_data = clic_counts.tolist()

    age_counts = df['Age'].value_counts().sort_index()
    age_labels = age_counts.index.tolist()
    age_data = age_counts.tolist()

    gender_counts = df['Gender'].value_counts()
    gender_labels = gender_counts.index.tolist()
    gender_data = gender_counts.tolist()

    level_counts = df['Income Level'].value_counts()
    level_labels = level_counts.index.tolist()
    level_data = level_counts.tolist()

    plan_counts = df['Plan Type'].value_counts()
    plan_labels = plan_counts.index.tolist()
    plan_data = plan_counts.tolist()
    context = {
        'data_size': data_size,
        'top_produit':top_produit,
        'top_Contrat':top_Contrat,
        'top_appareil':top_appareil,
        'top_canal':top_canal,
        'profil_lebels':profil_lebels,
        'profil_data':profil_data,
        'location_labels':location_labels,
        'location_data':location_data,
        'clic_labels':clic_labels,
        'clic_data':clic_data,
        'age_labels':age_labels,
        'age_data':age_data,
        'gender_labels':gender_labels,
        'gender_data':gender_data,
        'level_labels':level_labels,
        'level_data':level_data,
        'plan_labels':plan_labels,
        'plan_data':plan_data
    }
    return render(request, 'dashboard.html',context)
    
def count_churn(df,feature):
    df_sum = df.groupby(by=[feature,'Churn Status'])['Churn Status'].agg(['count'])
    chart_data = []
    for type_feature , churn_stat in df_sum.index:
        chart_data.append({
            'type_feature': type_feature,
            'churn_status': churn_stat,
            'value': df_sum.at[(type_feature,churn_stat),'count']
        })
    return chart_data


@login_required
def analyseChurn(request):
    excel_path = os.path.join(settings.BASE_DIR, 'churn/static/files/customer_data_algeria.xlsx')
    
    # Lire le fichier Excel avec pandas
    df = pd.read_excel(excel_path)
    churn_yes = df['Churn Status'].value_counts(normalize=True).get('Yes', 0)
    churn_no = df['Churn Status'].value_counts(normalize=True).get('No', 0)
        
    # Convertir les proportions en pourcentages
    churn_yes = (churn_yes * 100).round(2)
    churn_no = (churn_no * 100).round(2)
    client_yes = df['Churn Status'].value_counts().get('Yes', 0)
    client_no = df['Churn Status'].value_counts().get('No', 0)

    data_profil = count_churn(df,'Profile')
    data_device = count_churn(df,'Device Type')
    data_product = count_churn(df,'Products Purchased')
    data_canal = count_churn(df,'Preferred Communication Channel')
    data_contract = count_churn(df,'Contract Type')
    data_incomeL = count_churn(df,'Income Level')
    data_gender = count_churn(df,'Gender')
    context ={
        'churn_yes':churn_yes,
        'churn_no':churn_no,
        'client_yes':client_yes,
        'client_no':client_no,
        'data_profil':data_profil,
        'data_device':data_device,
        'data_product':data_product,
        'data_canal':data_canal,
        'data_contract':data_contract,
        'data_incomeL':data_incomeL,
        'data_gender':data_gender
    }
    return render(request,'analyseChurn.html',context)

# views.py



def transforme(cust):
    print(cust)
    df = pd.DataFrame(cust,index=[0])
    ordinal_encoder = OrdinalEncoder(categories=[['Low','Medium','High']])
    df['click_rate'] = ordinal_encoder.fit_transform(df[['click_rate']]).astype(int)
    df.profile = (df.profile == 'Business').astype(int)
    df.gender = (df.gender == 'Female').astype(int)
    df.contract_type = (df.contract_type == 'Postpaid').astype(int)
    df.plan_type = (df.plan_type == 'Unlimited').astype(int)
    mapping_wilayas = {
    'Relizane':48,
    'Blida':9,
    'Algiers':16,
    'Constantine':25,
    'Tiaret':14,
    "M'Sila":28,
    'Djelfa':17,
    'Tipaza':42,
    'Oran':31,
    'Annaba':23,
    'Skikda':21,
    'Boumerdès':35,
    'Mascara':29,
    'Jijel':18,
    'Ghardaïa':47,
    'Sétif':19,
    'Chlef':2,
    'Bordj Bou Arréridj':34,
    'Saïda':20,
    'Tlemcen':13,
    'Naâma':45,
    'Aïn Defla':44,
    'El Bayadh':32,
    'Béjaïa':6,
    'Béchar':8,
    'Laghouat':3,
    'Ouargla':30,
    'Tébessa':12,
    'Biskra':7,
    'Oum El Bouaghi':41,
    'Guelma':24,
    'Batna':5,
    'Mostaganem':27,
    'Tizi Ouzou':15,
    'Sidi Bel Abbès':22,
    'Aïn Témouchent':46,
    'Tissemsilt':38,
    'El Oued':39
    }
    df['location']=df['location'].map(mapping_wilayas)
    ordinal_encoder_product = OrdinalEncoder(categories=[['Internet','Mobile','Mobile, Internet']])
    df['products_purchased'] = ordinal_encoder_product.fit_transform(df[['products_purchased']]).astype(int)
    ordinal_encoder_device = OrdinalEncoder(categories=[['Desktop','Smartphone','Tablet']])
    df['device_type'] = ordinal_encoder_device.fit_transform(df[['device_type']]).astype(int)
    ordinal_encoder_channel = OrdinalEncoder(categories=[['App Notifications','Calls','SMS']])
    df['preferred_communication_channel'] = ordinal_encoder_channel.fit_transform(df[['preferred_communication_channel']]).astype(int)
    ordinal_encoder_income = OrdinalEncoder(categories=[['100,000+','25,000 or less','25,000-50,000','50,000-75,000','75,000-100,000']])
    df['income_level'] = ordinal_encoder_income.fit_transform(df[['income_level']]).astype(int)
    df['age'] = df['age'].astype(int)
    df['avg__monthly_spend'] = df['avg__monthly_spend'].astype(int)
    ordinal_encoder_occupation = OrdinalEncoder(categories=[['Engineer', 'Teacher', 'Doctor', 'Accountant', 'Lawyer', 'Nurse', 'IT Technician', 'Salesperson']])
    df['occupation'] = ordinal_encoder_occupation.fit_transform(df[['occupation']]).astype(int)
    from datetime import datetime
    # Convertir la colonne de dates en format de date approprié
    df['contract_start_date'] = pd.to_datetime(df['contract_start_date'])
    end_of_2023 = datetime(2023, 12, 31)

    # Calcul de la durée de la relation client jusqu'à la fin de décembre 2023
    df['contract_start_date'] = (end_of_2023 - df['contract_start_date']).dt.days
    df['customer_satisfaction_score'] = df['customer_satisfaction_score'].str.split('/').str[0].astype(int)

    to_scale =['age','avg__monthly_spend','contract_start_date','click_rate','products_purchased','location','income_level','device_type','preferred_communication_channel','customer_satisfaction_score','occupation']
    
    '''scaler_path = os.path.join(settings.BASE_DIR, 'churn/static/files/scaler2.pkl')
    with open(scaler_path, 'rb') as file:
        scaler = pickle.load(file)
    df[to_scale] = scaler.transform(df[to_scale].values) '''  
    return df 



modele_path = os.path.join(settings.BASE_DIR, 'churn/static/files/final_model.sav')
with open(modele_path, 'rb') as file:
    model = pickle.load(file)    
    model = Model()


@csrf_exempt
def Predict(request):
    if request.method == 'POST':
            form = PredictionForm(request.POST)
            if form.is_valid():
                # Traiter les données du formulaire ici
                click_rate = form.cleaned_data['choice_field_Click_Rate']
                products_purchased = form.cleaned_data['choice_field_Products_Purchased']
                profile = form.cleaned_data['choice_field_Profile']
                gender = form.cleaned_data['choice_field_Gender']
                contract_type = form.cleaned_data['choice_field_Contract_Type']
                age = form.cleaned_data['age']
                income_level = form.cleaned_data['choice_field_Income_Level']
                device_type = form.cleaned_data['choice_field_Device_Type']
                plan_type = form.cleaned_data['choice_field_Plan_Type']
                avg__monthly_spend = form.cleaned_data['choice_field_Avg_Monthly_Spend']
                preferred_communication_channel = form.cleaned_data['choice_Preferred_Communication_Channel']
                contract_start_date = form.cleaned_data['contract_start_date']
                customer_satisfaction_score = form.cleaned_data['choice_field_Customer_Satisfaction_Score']
                location = form.cleaned_data['wilaya']
                occupation = form.cleaned_data['choice_field_Occupation']
                
                cust = {'click_rate':click_rate,'products_purchased':products_purchased,'profile':profile,'gender':gender,'contract_type':contract_type,'age':age,'location':location,'income_level':income_level,
                'device_type': device_type,'plan_type':plan_type,'avg__monthly_spend':avg__monthly_spend,'preferred_communication_channel':preferred_communication_channel,'contract_start_date':contract_start_date,
                'customer_satisfaction_score':customer_satisfaction_score,'occupation':occupation}
                														
                cust = transforme(cust)

                prediction = model.predict(cust) + 1

                profils_churn = [1, 3, 4]
                profils_non_churn = [2, 5, 7]
                text = "profil mixte"
                if prediction in profils_churn :
                     text = "profil churn"
                if prediction in profils_non_churn :
                     text = "profil non churn"
                return render(request, 'prediction.html', {'form': form,'prediction':prediction,'text':text})
    else:
            form = PredictionForm()
    
    return render(request, 'prediction.html', {'form': form})




def user_logout(request):
    logout(request)
    # Rediriger l'utilisateur vers une page appropriée (par exemple, la page d'accueil)
    return redirect('login')  # Assurez-vous d'importer 'redirect' depuis django.shortcuts

