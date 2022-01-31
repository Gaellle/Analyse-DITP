import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go


st.title('Analyse des écarts d’avancement de réformes prioritaires entre départements ')


st.markdown('La Ministre souhaite disposer d’une note d’analyse visant à vérifier si le baromètre de l’action publique permet une réduction des disparités territoriales dans l’éxecution de réformes.')
st.markdown('L’objectif est démontrer l’hypothèse selon laquelle la transparence a des vertus de convergence dans les départements.')

# datas + sélecteur
df_1 = pd.read_csv('internet.csv')
detail_1 = pd.read_csv('internet-detail.csv')
df_2 = pd.read_csv('sante.csv')
detail_2 = pd.read_csv('sante-detail.csv')
df_3 = pd.read_csv('velo.csv')
detail_3 = pd.read_csv('velo-detail.csv')
df_4 = pd.read_csv('service.csv')
detail_4 = pd.read_csv('service-detail.csv')
df_5 = pd.read_csv('handicap.csv')
detail_5 = pd.read_csv('handicap-detail.csv')

departements = df_1.libelle_departement.unique()
reformes = ['Assurer une bonne couverture en internet fixe et en téléphonie mobile pour tous les Français d’ici 2022',\
    'Doubler le nombre de maisons de santé et de centres de santé dans les territoires',\
    'Déployer le plan vélo',\
    'Déployer une offre France Services dans tous les territoires',\
    'Simplifier l’accès aux droits des personnes handicapées']


# choix de la réforme
reforme = st.radio ('Sélectionnez une réforme', reformes )
st.header(reforme)

# menu déroulant 'choix du departement'
departement = st.selectbox('Sélectionnez un département', departements)

    
def graphs_internet(departement): 
    
    # Préparation des données
    df_dept = df_1[df_1['libelle_departement']==departement].reset_index(drop = True)
    df_det_dept = detail_1[detail_1['libelle_departement']==departement].reset_index(drop = True)

    value1 = int(df_dept['pourcentage_cible'])# Taux d'avancement
    value3 = int(df_dept['pourcentage_progression_derniere_maj'])# progression 20/21
    # Taux de couverture
    dates_a = [df_dept.loc[0,'date_valeur_initiale'], df_dept.loc[0,'date_valeur_actuelle'],df_dept.loc[0,'progression_derniere_maj_date']]
    values_a = [int(df_dept.loc[0,'valeur_initiale']), int(df_dept.loc[0,'valeur_actuelle']),int(df_dept.loc[0,'progression_derniere_maj'])]

    st.subheader('Taux de déploiement de la fibre')
    col1, col2  = st.columns(2)
    col1.metric('National', str(round(df_1.progression_derniere_maj.mean()))+'%')
    col2.metric('Départemental', str(round(df_dept.progression_derniere_maj.mean()))+'%')
    st.subheader('Taux de progression de la mesure 20/21')
    col3, col4  = st.columns(2)
    col3.metric('National', str(round(df_1.pourcentage_progression_derniere_maj.mean()))+'%')
    col4.metric('Départemental', str(round(df_dept.pourcentage_progression_derniere_maj.mean()))+'%')

    # Indicateurs
    fig1 = go.Figure()

    fig1.add_trace(go.Indicator(
        value = value3,
        title = {'text': "Taux de progression 20/21"},
        domain = {'row': 0, 'column': 0},
        gauge_axis_range=[0,100]))

    fig1.update_layout(
        grid = {'rows': 1, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
                                    'mode' : "number+gauge",
                                    'delta' : {'reference': 90},
                                    'number':{'suffix':'%'}}]},
                                    })

    # lineplot
    st.subheader(f'Evolution du taux de déploiement de la fibre dans le département - {departement}')

    fig3, ax = plt.subplots(figsize = (15,10))
    ax = sns.lineplot(data=df_det_dept, x = 'date', y = 'valeur', palette= 'magma')
    ax = sns.lineplot(data = pd.DataFrame(detail_1.groupby(by='date').valeur.agg('mean')), x = 'date', y = 'valeur' )
    ax.legend([f'{departement}','moyenne nationale'])
    ax.set_xlabel('')
    ax.set_ylabel("Taux de déploiement en '%' du territoire")
    ax.tick_params(axis='x', labelrotation=45)

    st.plotly_chart(fig1)
    st.pyplot(fig3.figure)

    # ccl
    st.subheader('Départements avec le plus fort taux de progression récent et leur taux de couverture')
    moy=df_1.pourcentage_progression_derniere_maj.mean()
    top_progression = df_1[df_1['pourcentage_progression_derniere_maj']>moy].sort_values(by='pourcentage_progression_derniere_maj',ascending = False)\
                  [['libelle_departement','pourcentage_progression_derniere_maj','valeur_actuelle']].reset_index(drop=True)

    top_progression

    fig1, ax = plt.subplots(figsize = (30,10))
    ax1 = plt.subplot(131)
    ax1 = sns.histplot(data = df_1, x = "valeur_actuelle", color = 'red', bins = 40)
    ax1.set_title("Actuellement")

    ax2 = plt.subplot(132)
    ax2 = sns.histplot(data = df_1, x = "progression_derniere_maj", color = 'orangered', bins = 40)
    ax2.set_title("En 2020")

    ax3 = plt.subplot(133)
    ax3 = sns.histplot(data = df_1, x = "valeur_initiale", color = 'orange', bins = 40)
    ax3.set_title("En 2017")

    st.subheader("Répartition des départements en fonction du taux de couverture")
    st.pyplot(fig1.figure)
    st.markdown ("Pour cette mesure, il semble que les départements qui avaient un certain retard concernant l'atteinte des objectifs nationaux ont tendance à progresser plus vite.")


def graphs_sante(departement):
    # Préparation des données
    detail_2_a = detail_2[detail_2.unite == 'maisons de santé']
    detail_2_b = detail_2[detail_2.unite == 'centres de santé']
    
    df_dept_a = df_2[(df_2['libelle_departement']==departement)&(df_2['unite']=='maisons de santé')].reset_index(drop = True)
    df_dpt_b = df_2[(df_2['libelle_departement']==departement)&(df_2['unite']=='centres de santé')].reset_index(drop = True)

    # Taux d'avancement
    value1 = int(df_dept_a['pourcentage_cible'])
    value2 = int(df_dpt_b['pourcentage_cible'])

    # progression 20/21
    value3 = int(df_dept_a['pourcentage_progression_derniere_maj'])
    value4 = int(df_dpt_b['pourcentage_progression_derniere_maj'])

    # Nombre d'établissmeents et évolutions
    dates_a = [df_dept_a.loc[0,'date_valeur_initiale'], df_dept_a.loc[0,'date_valeur_actuelle'],df_dept_a.loc[0,'progression_derniere_maj_date']]
    dates_b = [df_dpt_b.loc[0,'date_valeur_initiale'], df_dpt_b.loc[0,'date_valeur_actuelle'],df_dpt_b.loc[0,'progression_derniere_maj_date']]

    values_a = [int(df_dept_a.loc[0,'valeur_initiale']), int(df_dept_a.loc[0,'valeur_actuelle']),int(df_dept_a.loc[0,'progression_derniere_maj'])]
    values_b = [int(df_dpt_b.loc[0,'valeur_initiale']), int(df_dpt_b.loc[0,'valeur_actuelle']),int(df_dpt_b.loc[0,'progression_derniere_maj'])]


    # Indicateurs

    
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        value = value1, title = {'text': "maisons de santé"},
        domain = {'row': 0, 'column': 0}, gauge_axis_range=[0,100]))

    fig.add_trace(go.Indicator(
        value = value2, title = {'text': "centres de santé"},
        domain = {'row': 0, 'column': 1}, gauge_axis_range=[0,100]))

    fig.add_trace(go.Indicator(
        value = value3,  title = {'text': "Progression pour les maisons de santé"},
        domain = {'row': 1, 'column': 0}, gauge_axis_range=[0,100]))

    fig.add_trace(go.Indicator(
        value = value4, title = {'text': " et les centres de santé"},
        domain = {'row': 1, 'column': 1}, gauge_axis_range=[0,100]))

    fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
                                    'mode' : "number+gauge",
                                    'delta' : {'reference': 90},
                                    'number':{'suffix':'%'}}]},
                                    })

    # Répartition nombre d'établissements
    detail_2_a = detail_2[detail_2.unite == 'maisons de santé']
    detail_2_b = detail_2[detail_2.unite == 'centres de santé']
    df_2_a = df_2[df_2.unite == 'maisons de santé']
    df_2_b = df_2[df_2.unite == 'centres de santé']

    
       # Taux d'avancement
    fig5, ax = plt.subplots(figsize = (30,10))

    ax1 = plt.subplot(131)
    ax1 = sns.scatterplot(data = df_2, x = "valeur_actuelle", y = "cible",palette = 'magma', hue = 'unite')
    ax1.set_title("Actuellement")

    ax2 = plt.subplot(132)
    ax2 = sns.scatterplot(data = df_2, x = "progression_derniere_maj", y = "cible",palette = 'magma', hue = 'unite')
    ax2.set_title("En 2020")

    ax3 = plt.subplot(133)
    ax3 = sns.scatterplot(data = df_2, x = "valeur_initiale", y = "cible",palette = 'magma', hue = 'unite')
    ax3.set_title("En 2017")

    st.subheader(f"Taux de d'avancement et de progression 20/21  - {departement}")
    st.plotly_chart(fig)
    st.subheader("Nombre d'établissements de santé dans les départements par rapport à la cible")
    st.pyplot(fig5.figure)
    ## Conclusion

    st.markdown("On voit nettement qu'entre 2017 et 2021 (et entre 2020 et 2021 pour les maisons de santé), le nuage forme d'avantage une ligne. Ce qui montre bien une certaine unité des départements à converger vers leur cible. Avec beaucoup moins dde département très éloignés de la cible.")


def graphs_velo(departement):
    df_velo = df_3[df_3['libelle_departement']==departement].reset_index(drop = True)
    value1 = int(df_velo['pourcentage_cible'])
    value3 = int(df_velo['pourcentage_progression_derniere_maj'])
    dates_a = [df_velo.loc[0,'date_valeur_initiale'], df_velo.loc[0,'date_valeur_actuelle'],df_velo.loc[0,'progression_derniere_maj_date']]
    values_a = [int(df_velo.loc[0,'valeur_initiale']), int(df_velo.loc[0,'valeur_actuelle']),int(df_velo.loc[0,'progression_derniere_maj'])]

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        value = value1,
        title = {'text': "Taux d'avancement"},
        domain = {'row': 0, 'column': 0},
        gauge_axis_range=[0,100]))

    fig.add_trace(go.Indicator(
        value = value3,
        title = {'text': "Taux de progression 20/21"},
        domain = {'row': 0, 'column': 1},
        gauge_axis_range=[0,100]))

    fig.update_layout(
        grid = {'rows': 1, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
                                    'mode' : "number+gauge",
                                    'delta' : {'reference': 90},
                                    'number':{'suffix':'%'}}]},
                                    })

    fig6, ax = plt.subplots(figsize = (30,10))
    fig6.suptitle('Kilomètres de réseau cyclabre sécurisés', fontsize=16)

    ax1 = plt.subplot(131)
    ax1 = sns.scatterplot(data = df_3, x = "valeur_actuelle", y = "cible",color = 'limegreen')
    ax1.set_title("Actuellement")

    ax2 = plt.subplot(132)
    ax2 = sns.scatterplot(data = df_3, x = "progression_derniere_maj", y = "cible", color = 'darkcyan')
    ax2.set_title("En 2020")

    ax3 = plt.subplot(133)
    ax3 = sns.scatterplot(data = df_3, x = "valeur_initiale", y = "cible",color = 'tomato')
    ax3.set_title("En 2017 (valeur initiale)")

    fig7, ax = plt.subplots(figsize = (20,8))

    ax1 = plt.subplot(121)
    ax1 = sns.histplot(df_3.pourcentage_cible,color = 'limegreen',shrink=0.8,  multiple="dodge", kde=True, bins = 20)
    ax1.set_title("Actuellement")
    ax1.set_ylim(ymax = 65)

    ax2 = plt.subplot(122)
    ax2 = sns.histplot(data = df_3["progression_derniere_maj"]/df_3['cible']*100,color = 'darkcyan', shrink=0.8,  multiple="dodge", kde=True, bins = 20)
    ax2.set_title("en 2020")
    ax2.set_ylim(ymax = 65)

    st.subheader(f"Taux de d'avancement et de progression 20/21 de l'aménagement cyclable sécurisé - {departement}")
    st.plotly_chart(fig)
    st.subheader("Kilomètres de réseau cyclable sécurisés par rapport à la cible")
    st.pyplot(fig6.figure)
    st.subheader("Histogramme du taux d'avancement par département")
    st.pyplot(fig7.figure)
    ## Conclusion

    st.markdown("On observe qu'entre 2020 et 2021, il y a d'avantage de disparité entre les départeents concernant le taux d'avancement. Cependant, c'est une évolution positive car il y a eu final d'avantage de départements à avoir atteint la cible et donc aussi moins de départements dans la tranche 80-95.")


def graphs_service(departement):
    df_service = df_4[df_4['libelle_departement']==departement].reset_index(drop = True)

    value1 = int(df_service['pourcentage_cible'])
    value3 = int(df_service['pourcentage_progression_derniere_maj'])
    dates_a = [df_service.loc[0,'date_valeur_initiale'], df_service.loc[0,'date_valeur_actuelle'],df_service.loc[0,'progression_derniere_maj_date']]
    values_a = [int(df_service.loc[0,'valeur_initiale']), int(df_service.loc[0,'valeur_actuelle']),int(df_service.loc[0,'progression_derniere_maj'])]

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        value = value1,
        title = {'text': "Taux d'avancement"},
        domain = {'row': 0, 'column': 0},
        gauge_axis_range=[0,100]))

    fig.add_trace(go.Indicator(
        value = value3,
        title = {'text': "Taux de progression 20/21"},
        domain = {'row': 0, 'column': 1},
        gauge_axis_range=[0,100]))

    fig.update_layout(
        grid = {'rows': 1, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
                                    'mode' : "number+gauge",
                                    'delta' : {'reference': 90},
                                    'number':{'suffix':'%'}}]},
                                    })

    # Evolution des labellisations par département

    df_det_dept = detail_4[detail_4['libelle_departement']==departement].reset_index(drop = True)

    fig8, ax = plt.subplots(figsize = (15,10))
    ax = sns.lineplot(data=df_det_dept, x = 'date', y = 'valeur', palette = 'viridis')
    ax = sns.lineplot(data = pd.DataFrame(detail_4.groupby(by='date').valeur.agg('mean')), x = 'date', y = 'valeur' )
    ax.legend([f'{departement}','moyenne nationale'])
    ax.set_ylabel('Nombre de labellisations')
    ax.tick_params(axis='x', labelrotation=45)

    fig9, ax = plt.subplots(figsize = (30,10))
    ax1 = plt.subplot(131)
    ax1 = sns.scatterplot(data = df_4, x = "valeur_actuelle", y = "cible",color = 'indigo')
    ax1.set_title("Actuellement")

    ax2 = plt.subplot(132)
    ax2 = sns.scatterplot(data = df_4, x = "progression_derniere_maj", y = "cible", color = 'mediumaquamarine')
    ax2.set_title("En 2020")

    ax3 = plt.subplot(133)
    ax3 = sns.scatterplot(data = df_4, x = "valeur_initiale", y = "cible",color = 'gold')
    ax3.set_title("En 2020 (valeur initiale)")

    fig10, ax = plt.subplots(figsize = (20,8))

    ax1 = plt.subplot(121)
    ax1 = sns.histplot(df_4.pourcentage_cible,color = 'indigo',shrink=0.8,  multiple="dodge", kde=True, bins = 20)
    ax1.set_title("Actuellement (1er trimestre 2022)")
    ax1.set_ylim(ymax = 19)

    ax2 = plt.subplot(122)
    ax2 = sns.histplot(data = df_4["progression_derniere_maj"]/df_4['cible']*100,color = 'mediumaquamarine', shrink=0.8,  multiple="dodge", kde=True, bins = 20)
    ax2.set_title("En 2020")
    ax2.set_ylim(ymax = 19)

    st.subheader(f"Taux de d'avancement et de progression 20/21 des labellisations France services - {departement}")
    st.plotly_chart(fig)
    st.pyplot(fig8.figure)
    st.subheader("Nombre de labellisations France services par rapport à la cible")
    st.pyplot(fig9.figure)
    st.subheader("Histogramme du taux d'avancement par département")
    st.pyplot(fig10.figure)

    st.markdown("Une évolution que l'on ne peut juger que sur 2 années mais une évolution très rapide puisque 45% des départements ont aujourd'hui un taux d'avancement élevé (+ de 80%).")
    st.markdown("Entre 2020 et 2022, il y a un étalement des valeurs vers des taux plus élevés. On va donc dans le sens d'une convergence des départements pour cette mesure.")

def graphs_handi(departement):
    df_handicap = df_5[df_5['libelle_departement']==departement].reset_index(drop = True)
    value1 = int(df_handicap['pourcentage_cible'])
    value3 = int(df_handicap['pourcentage_progression_derniere_maj'])
    dates_a = [df_handicap.loc[0,'date_valeur_initiale'], df_handicap.loc[0,'date_valeur_actuelle'],df_handicap.loc[0,'progression_derniere_maj_date']]
    values_a = [int(df_handicap.loc[0,'valeur_initiale']), int(df_handicap.loc[0,'valeur_actuelle']),int(df_handicap.loc[0,'progression_derniere_maj'])]
    df_det_dept = detail_5[detail_5['libelle_departement']==departement].reset_index(drop = True)

    fig11, ax = plt.subplots(figsize = (10,8))
    ax = sns.lineplot(data=df_det_dept, x = 'date', y = 'valeur', palette = 'viridis')
    ax = sns.lineplot(data = pd.DataFrame(detail_5.groupby(by='date').valeur.agg('mean')), x = 'date', y = 'valeur' )
    ax.legend([f'{departement}','moyenne nationale'])
    ax.set_ylabel('Nombre de mois e, moyenne')
    ax.tick_params(axis='x', labelrotation=45)


    fig12, ax = plt.subplots(figsize = (30,10))
    ax1 = plt.subplot(131)
    ax1 = sns.histplot(data = df_5, x = "valeur_actuelle", color = 'red', bins = 20)
    ax1.axvline(3, 0,30)
    ax1.set_title("Actuellement")

    ax2 = plt.subplot(132)
    ax2 = sns.histplot(data = df_5, x = "progression_derniere_maj", color = 'orangered', bins = 20)
    ax2.axvline(3, 0,30)
    ax2.set_title("En 2020")

    ax3 = plt.subplot(133)
    ax3 = sns.histplot(data = df_5, x = "valeur_initiale", color = 'orange', bins = 20)
    ax3.axvline(3, 0,30)
    ax3.set_title("En 2017 (ou année valeur initiale)")

    fig13, ax = plt.subplots(figsize = (30,10))
    ax1 = plt.subplot(131)
    ax1 = sns.boxplot(data = df_5, y = "valeur_actuelle", color = 'red')
    ax1.set_title("Actuellement")

    ax2 = plt.subplot(132)
    ax2 = sns.boxplot(data = df_5, y = "progression_derniere_maj", color = 'orangered')
    ax2.set_title("En 2020")

    ax3 = plt.subplot(133)
    ax3 = sns.boxplot(data = df_5, y = "valeur_initiale", color = 'orange')
    ax3.set_title("En 2017 (ou année valeur initiale)")

    st.subheader(f'Evolution temps de traitement des demandes AAH - {departement}')
    st.pyplot(fig11.figure)
    st.subheader("Durée moyenne de traitement pour les demandes d’allocation adulte handicapé (mois)")
    st.pyplot(fig12.figure)
    st.pyplot(fig13.figure)

    st.markdown("Il s'agit d'une donnée qu'on ne peut que difficilement comparer à une cible car l'avancement peut varier en positif comme en négatif d'une prise de mesure à l'autre.")
    st.markdown("Si aujourd'hui, il semble y avoir beaucoup de département dont l'objectif est atteint, il y en a aussi beaucoup qui font moins bien qu'avant.")
    st.markdown("Et tout cela peut changer lors de la prochaine mesure courant 2022.")


if reforme == 'Assurer une bonne couverture en internet fixe et en téléphonie mobile pour tous les Français d’ici 2022':
    graphs_internet(departement)
elif reforme ==  'Doubler le nombre de maisons de santé et de centres de santé dans les territoires':
    graphs_sante(departement)
elif reforme == 'Déployer le plan vélo':
    graphs_velo(departement)
elif reforme == 'Déployer une offre France Services dans tous les territoires':
    graphs_service(departement)
elif reforme == 'Simplifier l’accès aux droits des personnes handicapées':
    graphs_handi(departement)