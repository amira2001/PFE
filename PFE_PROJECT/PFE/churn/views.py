from django.shortcuts import render,HttpResponse , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.conf import settings
import os
# Create your views here.


@login_required
def Dashboard(request):
    excel_path = os.path.join(settings.BASE_DIR, 'churn/static/files/customer_data_algeria.xlsx')
    
    # Lire le fichier Excel avec pandas
    df = pd.read_excel(excel_path)
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


def user_logout(request):
    logout(request)
    # Rediriger l'utilisateur vers une page appropriée (par exemple, la page d'accueil)
    return redirect('login')  # Assurez-vous d'importer 'redirect' depuis django.shortcuts

