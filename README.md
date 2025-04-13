# Visualització d'Accuracy Ponderada

## Descripció
Eina simple per visualitzar com varia l'accuracy global d'un model basat en l'accuracy ponderada de dos subgrups (predominant i minoritari). Ideada per a facilitar un debat ètic sobre la representativitat i els grups minoritaris en algorismes d'intel·ligència artificial.

## Característiques
- Permet modificar l'accuracy de cada subgrup (predominant i minoritari)
- Ajusta la distribució (pes) de cada subgrup a la població
- Calcula automàticament l'accuracy ponderada total
- Representa visualment la proporció d'encerts i errors per cada grup

## Requisits
```
streamlit
numpy
matplotlib
pandas
```

## Execució
```bash
streamlit run app.py
```
