# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 20:35:39 2023

@author: Davi
"""

import numpy as np  # type: ignore 
from math import pi
import pylab as plt  # type: ignore      
import pandas as pd
import sympy as sy
from math import ceil,atan
import math
import os
import time
from colorama import Fore
from colorama import Style

# lista_Cr = [0.46]    #asa de 2020
# lista_Ct = [0.23]    #asa de 2020
# lista_b  = [1]       #asa de 2020

# lista_Cr = [0.46,0.46]    #asa de 2021
# lista_Ct = [0.46,0.23]    #asa de 2021
# lista_b  = [0.5,1]        #asa de 2021

# lista_Cr = [0.54,0.54]    #asa de 2022
# lista_Ct = [0.54,0.24]    #asa de 2022
# lista_b  = [0.5,1.00]     #asa de 2022

# lista_Cr = [0.6,0.6]      # asa de 2023
# lista_Ct = [0.6,0.4]      # asa de 2023
# lista_b  = [0.6,1.15]

# Perfis dos estabilizadores

#n0009        = NACA 0009            
#n0012        = NACA 0012     
#n0015        = NACA 0015       
#n63015a      = NACA 63-015A          
#n64012       = NACA 64012
#BELL540      = BELL 540

# Perfis de asa

#s1223           = Selig 1223                 
#S1223RTL        = Selig 1223 RTL
#S 1210          = selig 1210 12%
#aj21s90         = AJ 2021-S90-10        perfil de 2021
#aj2190-SRTL10   = AJ 2021-S90-RTL10     perfil de 2022
#NACA 4412       = NACA 4412
#NACA 4415       = NACA 4415
#fx63137         = FX 63-0137 13.7%
#fx73cl3152      = FX 73-CL3-152
#e423            = Eppler E423 high lift airfoil
#e420            = EPPLER 420

'Esse código calcula todos os dados importantes de sua asa'
'Ele inclui uma aproximação da massa da asa de a acordo com o projeto de 2022'
'O método de calcular o MTOW é o desenvolvido por Victor e é bem antigo, então CUIDADO, pode ter erros!'

nome_da_asa = 'Protótipo'            #escolha um nome pra sua asa

nome_do_perfil='S1223RTL'

perfil_ht = 'n0015'
perfil_vt = 'n0015'


lista_Cr = [0.47]
lista_Ct = [0.47]
lista_b  = [1.1]

T = 30                         # [°C]  temperatura da asa
V = 12.5                         # [m/s] use uma velocidade um pouco acima da velocidade de decolagem ou estol

i_w    = 3                     # [°] ângulo de incidência
torção = 0                     # [°] ângulo de torção da asa
diedro = 0                     # [°] ângulo de diedro

h                = 0.35        # [m]altura da asa do avião
dist_nariz_a_asa = 0.3         # [m]
poten            = 716         # [W] potencia do motor
atrito           = 0.0658      # atrito do material das rodas

'Endplate'

Sep     = 0.2                  #[m²] área lateral de 1 endplate, caso não tenha endplate, coloque esse valor = 0
h_end   = 0.4                  #[m] altura maxima de 1 endplate, caso não tenha endplate, coloque esse valor = 0
Swetend = 0.4                  #[m²] área molhada dos endplates(eixo x)
Ced     = 0.5                  #[m] corda/raio do endplate
t_end   = 0.4                  #Espessura maxima do endplate (geometria)
Cd0ed   = 0.9                  #Cd0 do endplate (geometria)

'MTOW conservativo ou ideal'

analise = 'con'     # 'con' ou 'ide'


'Só mexer aqui embaixo caso queria uma análise mais exata porem devagar ou gráficos de temperatura'

N_g = 200              #separação do LLT
#quanto maior, mais exato é o CL, mas mais lerdo é o cálculo, use entre 10 e 200

incremento_MTOW = 0.1 #[kg] de quanto em quanto o MTOW é verificado, se quiser uma análise rápida deixe em 0.1


graf = False                   #graficos
lista_T = np.arange(5,50,1)









'__________________CÓDIGO ABAIXO, NÃO ALTERAR SE VOCÊ NÃO SOUBER O QUE ESTÁ FAZENDO__________________'















com = time.time()



rho = -3.52607427278736e-8*T**3 + 1.60215687088211e-5*T**2 - 0.00471578515074178*T + 1.2925545912127
vis = 5.63034007726774e-13*T**3 + 1.15655321938951e-11*T**2 + 9.06376414877547e-8*T + 1.32700903275642e-5

phi      = 159.52     #[kg/m³] densidade do material da asa
phil     = 159.52     #[kg/m³] densidade do material da longarina
phi_fita = 970        #[kg/m³] densidade da fita adesiva
phi_monk = 0.067812   #[kg/m²] densidade(EM AREA) do monokote (tem uma espessura de 0,00015 m)
esp      = 0.002      #[m]     Espessura da asa
espn     = 0.002      #[m]     Espessura da nervura 
Acir     = 0.01       #[%]     Área retirada do perfil com os circulos nas nervuras

P_end = (Sep*2)*(espn+0.001)*phi     #Peso dos dois endplates 

Numero_de_intecoes  = 100            #quantas vezes ele vai tentar calcular antes de desistir

R_TR = []
R_S  = []

lista_contar= range(len(lista_Cr))

'_______________________________________________________________________________________'

for i in lista_contar:
    
    Cri = lista_Cr[i]
    Cti = lista_Ct[i]
    
    if i > 0:
        bi = lista_b[i] - lista_b[i-1]
    else:
        bi  = lista_b[i]
    
    TRi=Cti/Cri
    cmaci=(2/3)*Cri*((1+TRi+(TRi**2))/(1+TRi))
    Si=bi*cmaci
    
    Si = Si*2 #isso pq os valores de b são pra só um lado
    
    R_TR.append(TRi)
    R_S.append(Si)

soma = sum(R_S)
S_real = soma
medias = []

for i in lista_contar:
    me = R_S[i]*R_TR[i]
    medias.append(me)

cima = sum(medias)

TR_eff = cima/soma

nome_do_arquivo = 'PontosPerfis/' + nome_do_perfil

'_______________________________________________________________________________________'

#dados do perfil

lista_de_perfis = pd.read_excel('Perfil_df.xlsx')

for j in range(len(lista_de_perfis)):
    if lista_de_perfis.iloc[j,1] == nome_do_perfil:
        index_do_perfil = j
        break

eq_alpha_s = (str(lista_de_perfis.iloc[index_do_perfil,2]))
eq_alpha_0 = (str(lista_de_perfis.iloc[index_do_perfil,3]))
eq_Clalpha = (str(lista_de_perfis.iloc[index_do_perfil,6]))
Cd0_asa    = str(lista_de_perfis.iloc[index_do_perfil,7])
tsob_c     = (lista_de_perfis.iloc[index_do_perfil,10])

'_______________________________________________________________________________________'

#dados do perfil dos estabilizadores

for j in range(len(lista_de_perfis)):
    if lista_de_perfis.iloc[j,1] == perfil_ht:
        index_do_perfil = j
        break

Cd0_ht        = str(lista_de_perfis.iloc[index_do_perfil,7])
tsob_c_ht     = (lista_de_perfis.iloc[index_do_perfil,10])

for j in range(len(lista_de_perfis)):
    if lista_de_perfis.iloc[j,1] == perfil_vt:
        index_do_perfil = j
        break
Cd0_vt        = str(lista_de_perfis.iloc[index_do_perfil,7])
tsob_c_vt     = (lista_de_perfis.iloc[index_do_perfil,10])


'_______________________________________________________________________________________'

#calculando corda média

lista_S = []
lista_C = []

for i in range(len(lista_b)):
    
    TR_i = lista_Ct[i]/lista_Cr[i]
    cmac=(2/3)*lista_Cr[i]*((1+TR_i+(TR_i**2))/(1+TR_i))

    if i == 0:
        S_i = lista_b[i]*cmac
    else:
        S_i = (lista_b[i]-lista_b[i-1])*cmac
    
    S_i = S_i*2
    
    lista_C.append(cmac)
    lista_S.append(S_i)

soma = sum(lista_S)
soma_cima = 0
for i in range(len(lista_C)):
    
    soma_cima = soma_cima + (lista_C[i]*lista_S[i])

cmac = soma_cima/soma

'_______________________________________________________________________________________'

#Endplate

b = lista_b[-1]*2

M = V/343

fM = 1 - 0.08*(M**1.45)

Rend = V*Ced/vis

CFed = 0.42/(math.log10(Rend)**2.58)

ftced = 1 + (2.7*(t_end)) + (100*(t_end**4))

CD0end = CFed * ftced * fM * (Swetend/S_real) * ((Cd0ed/0.004)**0.4)

fator_area = -0.980392156862763*(Sep/S_real)**2 + 2.09803921568627*(Sep/S_real) + 0.999999999999998 # AR efetivo com endplate de acordo com a altura

fator_altu = -0.980392156862763*(h_end/b)**2 + 2.09803921568627*(h_end/b) + 0.999999999999998 # AR efetivo com endplate de acordo com a altura

fator = (fator_area+fator_altu)/2

'_______________________________________________________________________________________'

#Efeito do solo no CL (Nicolai pag 259)

didiv_AR = 0.195729679631324*(2*h/b) - 2.54016228375777e-5*(2*h/b)**(-3) + 1.04883297007381*(2*h/b)*math.exp(-(2*h/b)) + 0.336121232721402

if 2*h/b > 1.9:
    
    didiv_AR = 1

M = V/343

beta = (1 - M**2)**0.5

AR = b/cmac

CLa = (2*math.pi*AR)/(2+(4+(AR**2 * beta**2 *(1+(0/beta**2))))**0.5)

AR = AR/didiv_AR

CLa2 = (2*math.pi*AR)/(2+(4+(AR**2 * beta**2 *(1+(0/beta**2))))**0.5)

solo_CL_con = CLa2/CLa

'_______________________________________________________________________________________'

#Incremento C1 do CL (Nicolai pag 62)

AR = b/cmac

C1 = 10.6264982037274*(1/(2*math.pi)**0.5)*math.exp(-((AR**2)/2)) + 0.106013870344867*math.atan(AR)*180/math.pi + 0.455690445917242*AR**2 - 5.11788525427153*AR + 7.76073604035651

if AR > 6:
    
    C1 = 0

C1 = 0

'_______________________________________________________________________________________'

#Efeito solo que já estava aqui, da valores altos de MTOW

AR = b/cmac

solo_CL_ide = 1 + (0.00211 - 0.0003 * (AR - 3)) * math.exp( 5.2*(1-h/b) ) #efeito solo

'_______________________________________________________________________________________'

#enflechamento na metade da corda

enfl = atan(((lista_Cr[0]-lista_Ct[-1])/2)/(b/2))

enfl = enfl*180/pi

'_______________________________________________________________________________________'

#Numero de Reynols

Numero_de_Reynols   = str(round(cmac*V/vis,1))

def LLT(lista_b:list,
        lista_Cr:list,
        lista_Ct:list,
        Clalpha:float,
        torção:float,
        incidencia:float,
        alpha_0:float,
        diedro:float,
        N:int):
    
    twist = torção
    Cla = Clalpha
    i_w = incidencia
    
    '__________________________________________________________________________'
    
    'Calculo das linhas que representam a asa'
    
    x=sy.symbols('x')
    
    segmentos=[]
    
    for i in range(len(lista_b)):
        if i == 0:
            linha = lista_Cr[i] + (((lista_Ct[i]-lista_Cr[i])/(lista_b[i]-0))*(x-0))
        if i > 0:     
            linha = lista_Cr[i] + (((lista_Ct[i]-lista_Cr[i])/(lista_b[i]-lista_b[i-1]))*(x-lista_b[i-1]))
        
        segmentos.append(linha)
    
    listax = np.linspace(0,lista_b[len(lista_b)-1],N) #divido N vezes
    listay = []
    listacont = np.arange(1,len(lista_b),1)
    
    for x in listax:
        
        if x < lista_b[0]:
            y = eval(str(segmentos[0]))
        
        if x > lista_b[0]:
            for i in listacont:
                if x > lista_b[i-1] and x < lista_b[i]:
                    y = eval(str(segmentos[i]))
                    
        listay.append(y)
    
    '___________________________________________________________________________'
    
    'calculo da corda média'
    
    lista_S = []
    lista_C = []
    
    for i in range(len(lista_b)):
        
        TR_i = lista_Ct[i]/lista_Cr[i]
        cmac=(2/3)*lista_Cr[i]*((1+TR_i+(TR_i**2))/(1+TR_i))
        
        if i == 0:
            S_i = lista_b[i]*cmac
        if i > 0:
            S_i = (lista_b[i]-lista_b[i-1])*cmac
            
        
        S_i = 2*S_i
        
        lista_C.append(cmac)
        lista_S.append(S_i)
    
    soma = sum(lista_S)
    soma_cima = 0
    for i in range(len(lista_C)):
        
        soma_cima = soma_cima + (lista_C[i]*lista_S[i])
        
    
    MAC = soma_cima/soma
    
    b = lista_b[len(lista_b)-1]*2
    
    Cla = Cla * 180/pi
    
    alpha_twist = twist         
    a_2d = Cla
    
    theta = np.linspace((pi / (2 * N)), (pi / 2), N, endpoint=True)
    
    alpha = np.linspace(i_w + alpha_twist, i_w, N) 

    listay = listay[::-1]
    
    c = np.array(listay)
    
    mu = c * a_2d / (4 * b)
    
    LHS = mu * (np.array(alpha) - alpha_0) *pi/180
    
    RHS = []
    for i in range(1, 2 * N + 1, 2):
        RHS_iter = np.sin(i * theta) * (1 + (mu * i) / (np.sin(list(theta))))  # .reshape(1,self.N)
        # print(RHS_iter,"RHS_iter shape")
        RHS.append(RHS_iter)
        
    
    test = np.asarray(RHS)
    x = np.transpose(test)
    inv_RHS = np.linalg.inv(x)
        
    A = np.matmul(inv_RHS, LHS) #An
        
    AR = b/MAC         #Aspect ratio
    
    CL_wing = (pi * AR * A[0]) 
    
    CL_wing = CL_wing * math.cos(diedro*math.pi/180)
    
    listay = listay[::-1]  
    
    # CL_wing = CL_wing * 1.25 #gurney flaps
    
    return(round(CL_wing,5),listax,listay)

def cma(Nome:str,
        lista_Cr:list,
        lista_Ct:list,
        lista_b:list,
        phi:float,
        phil:float,
        phi_monk:float,
        esp:float,
        espn:float,
        Acir:float):
       
    nome_do_arquivo = 'PontosPerfis/' + Nome
    
    perfil = pd.read_csv(nome_do_arquivo+'.dat',delimiter=' ')
    
    vx=[]  
    vy=[]
    
    listacontar=perfil.index
    listacontar=np.arange(1,70,1)
    
    b = lista_b[len(lista_b)-1]*2
    
    
    '___________________________________________________________________________'
    
    'calculo da corda média'
    
    lista_S = []
    lista_C = []

    for i in range(len(lista_b)):
        
        TR_i = lista_Ct[i]/lista_Cr[i]
        cmac=(2/3)*lista_Cr[i]*((1+TR_i+(TR_i**2))/(1+TR_i))
        
        if i == 0:
            S_i = lista_b[i]*cmac
        if i > 0:
            S_i = (lista_b[i]-lista_b[i-1])*cmac
        
        S_i = S_i*2
        
        lista_C.append(cmac)
        lista_S.append(S_i)

    soma = sum(lista_S)
    soma_cima = 0
    for i in range(len(lista_C)):
        
        soma_cima = soma_cima + (lista_C[i]*lista_S[i])
    
    cmac = soma_cima/soma
    
    '___________________________________________________________________________'
    
    'Calculo do TR efetivo'
    
    R_TR = []
    R_S  = []

    lista_contar= range(len(lista_Cr))

    for i in lista_contar:
        
        Cri = lista_Cr[i]
        Cti = lista_Ct[i]
        
        if i > 0:
            bi = lista_b[i] - lista_b[i-1]
        else:
            bi  = lista_b[i]
        
        TRi=Cti/Cri
        cmaci=(2/3)*Cri*((1+TRi+(TRi**2))/(1+TRi))
        Si=bi*cmaci
        
        Si = Si*2 #isso pq os valores de b são pra só um lado
        
        R_TR.append(TRi)
        R_S.append(Si)

    area_total = sum(R_S)
    medias = []

    for i in lista_contar:
        me = R_S[i]*R_TR[i]
        medias.append(me)

    cima = sum(medias)

    TR = cima/area_total
    
    '___________________________________________________________________________'
    
    'aproximações da longarina e quantidade de nervuras'
    
    Alon=area_total/2300             #[m²] Área da longarina
    q=ceil(b*12)                   #[Nº] Quantidade de nervuras
    
    '___________________________________________________________________________'
    
    'Calculo da área molhada e área das nervuras'

    if TR == 1:

        xa=perfil.iloc[:,0]
        ya=perfil.iloc[:,1]
        
        vx=list(map(lambda i: float(i)*cmac,xa))
        vy=list(map(lambda i: float(i)*cmac,ya))
        
        
        listac=range(len(vy)-1)
        ht=0
        for i in listac:
            
            h=(((vy[i+1]-vy[i])**2)+(vx[i+1]-vx[i])**2)**0.5
            
            ht=ht+h                                                     #comprimento
        
        at=0
        for i in listac:
            
            A1 = min([abs(vy[i]),abs(vy[i+1])]) * abs(vx[i+1] - vx[i])  #retangulo
            
            A2 = abs(vy[i] - vy[i+1]) * abs(vx[i+1] - vx[i])            # triangulo
            
            at=at+A1+A2
            
        area_molhada = ht * b
        
        area_lateral = at
                
    if TR != 1:             
        
        area_molhada = 0
        
        area_lateral = 0
        
        n_segmentos = len(lista_b)
        
        def calc(ht1,at1):
            for i in listac:
                
                h=(((vy[i+1]-vy[i])**2)+(vx[i+1]-vx[i])**2)**0.5            #perimetro
                
                A1 = min([abs(vy[i]),abs(vy[i+1])]) * abs(vx[i+1] - vx[i])  #retangulo
                
                A2 = abs(vy[i] - vy[i+1]) * abs(vx[i+1] - vx[i])            # triangulo
                
                at1=at1+A1+A2   #área lateral do perfil
                ht1=ht1+h       #perimetro do perfil
                
            return (ht1,at1)
                
        for k in range(n_segmentos):
            
            if k > 0:
                bi = lista_b[k] - lista_b[k-1]
            else:
                bi  = lista_b[k]
            
            b_local = round(bi * 2,3)
            
            Cr_local = lista_Cr[k]
            
            Ct_local = lista_Ct[k]
            
            x = sy.symbols('x')
            
            eq = Cr_local + ((Ct_local - Cr_local)/(b_local+0.000001)*x)
            
            ht=0
            at=0
            
            for j in listacontar:
                
                x = b_local * (j/len(listacontar))
            
                cmacd = eval(str(eq))

                vx=[]
                vy=[]
                
                ht1=0
                
                xa=perfil.iloc[:,0]
                ya=perfil.iloc[:,1]
             
                vx=list(map(lambda m: float(m)*cmacd,xa)) #mesma coisa q um for loop..
                vy=list(map(lambda m: float(m)*cmacd,ya)) #com oq tem dps do lambda

                              
                listac=range(len(vy)-1)
                
                ht1,at1=calc(0,0)
    
                ht=ht+ht1     
                at=at+at1
            
            at=at/(len(listacontar))     #área lateral do perfil média
            ht=ht/(len(listacontar))     #perimetro do perfil

            area_molhada = area_molhada + ht*b_local
            
            area_lateral = area_lateral + at
            
        area_lateral = area_lateral/n_segmentos
        
    V1 = ((area_lateral*(1-Acir))-Alon)*espn*(q-2)

    V2 = area_lateral*espn*2

    V3=area_molhada*esp
    
    m_monokote = area_molhada * phi_monk
    
    m=(V1+V2+V3)*phi
    
    ml=b*Alon*phil

    mt = m + ml + m_monokote
    
    return(mt,area_molhada)

def Calculo_do_peso(altura:float,
                    nome_do_perfil:str,
                    perfil_ht:str,
                    perfil_vt:str,
                    lista_Cr:list,
                    lista_Ct:list,
                    lista_b:list,
                    phi:float,
                    phil:float,
                    phi_fita:float,
                    phi_monk:float,
                    esp:float,
                    espn:float,
                    Acir:float,
                    mac:float,
                    dist_nariz_a_asa:float):

    
    #peso dos componentes fixos
    
    P_bequilha = 0.2
    
    CG_bequilha  = 0.1
    
    P_trem_prin = 0.2
    
    CG_trem_prin = dist_nariz_a_asa + mac*0.7
    
    P_bateria = 0.52 + 0.1218  #bateria motor + bateria servos
    
    CG_bateria = 0.2  #CG
    
    P_Helices = 0.02
    
    CG_helice = 0.0165  #CG
    
    P_motor = 0.408
    
    CG_motor = 0.061  #CG
    
    P_fios = 0.25
    
    CG_fios = dist_nariz_a_asa + mac*1/4  #CG
    
    P_servos = 4*0.06
    
    CG_servos = dist_nariz_a_asa + mac*1/4  #CG
    
    P_fixos = P_bateria + P_Helices + P_motor + P_fios + P_servos + P_bequilha + P_trem_prin
    
    b = lista_b[len(lista_b)-1]*2
    S = b * mac
    
    #peso da asa
    
    P_asa,S_wet_asa = cma(nome_do_perfil,lista_Cr,lista_Ct,lista_b,phi,phil,phi_monk,esp,espn,Acir)
    
    CG_asa = dist_nariz_a_asa + mac*1/4  #CG
    
    #peso da cauda
    
    ARh = (2/3)*(b/mac)  #aproximação de Sadraey
    
    bh = (b)/2.5           #aproximação
    
    ch = bh/ARh
    
    lista_Cr2 = [ch,ch]
    lista_Ct2 = [ch,ch]
    lista_b2 = [0,bh/2]
    
    
    P_cauda_h,S_wet_h = cma(perfil_ht,lista_Cr2,lista_Ct2,lista_b2,phi,phil,phi_monk,esp,espn,Acir)
    
    Sh  = ((bh**2)/ARh)
    
    Sv = 2*(0.6645*Sh - 0.05948) #valor aproximado vendo os outros projetos
    
    ARv = 1.5  #aproximação de Sadraey
        
    macv = (Sv/ARv)**0.5
    
    bv = Sv/macv
    
    lista_Cr3 = [macv,macv]
    lista_Ct3 = [macv,macv]
    lista_b3 = [0,bv/2]
    
    P_cauda_v,S_wet_v = cma(perfil_vt,lista_Cr3,lista_Ct3,lista_b3,phi,phil,phi_monk,esp,espn,Acir)

    #aproximação do peso da fuselagem
    
    dist_nariz_cg = dist_nariz_a_asa + mac*1/4 # [m]
    
    lh = (0.4*S*mac/Sh)              # [m]
    
    largura = 0.1 # [m]
    alt = altura/2  # [m]
    
    densidade = 1451   #[kg/m³] 
    kg_resina_por_suporte = 0.02 # [kg]
    
    diametro_interno = 0.003 # [m]
    diametro_externo = 0.005 # [m]
    
    dist_para_suporte = 0.15 # [m]
    
    area_externa_certa = math.pi*(diametro_externo**2)/4
    area_interna_certa = math.pi*(diametro_interno**2)/4
    
    area_total = area_externa_certa - area_interna_certa
    
    Comprimento_da_fuselagem_total = (dist_nariz_cg + lh) * 0.7 #ajuste de projeto
    
    CG_h = Comprimento_da_fuselagem_total + ((1/4)*ch)  #CG
    
    CG_v = Comprimento_da_fuselagem_total + ((1/4)*macv)  #CG
    
    volume_tubos_no_eixo_x = Comprimento_da_fuselagem_total * 4 * area_total
    
    qtd_de_suportes = Comprimento_da_fuselagem_total // dist_para_suporte 
    
    volume_tubos_no_eixo_y =  2 * qtd_de_suportes * largura * area_total
    
    comprimento_do_tubo_de_suporte = ((dist_para_suporte**2) + (alt**2))**0.5
    
    volume_tubos_de_suporte_vertical = 2 * qtd_de_suportes * comprimento_do_tubo_de_suporte * area_total
    
    volume_total = volume_tubos_no_eixo_x + volume_tubos_no_eixo_y + volume_tubos_de_suporte_vertical
    
    massa_fuselagem = volume_total * densidade
            
    massa_da_resina = 4 * qtd_de_suportes * kg_resina_por_suporte
    
    P_fus = massa_fuselagem + massa_da_resina
    
    CG_fus = Comprimento_da_fuselagem_total/2
    
    # entelagem de fita na fuselagem:
    
    area_molhada_lados = 2 * Comprimento_da_fuselagem_total * alt 
    
    area_molhada_horizontais = 2 * Comprimento_da_fuselagem_total * largura
    
    volume_molhado = (area_molhada_lados + area_molhada_horizontais) * 0.00015 #  0.00015 é a espessura da fita
    
    Peso_fita = 2 * volume_molhado * phi_fita
    
    CG_fita = CG_fus

    #peso total

    P_total = P_fixos + P_asa + P_cauda_h + P_cauda_v + P_fus + Peso_fita

    #CG
    
    # com 5kg no CA para ajustar
    
    CG = ((5 * ((dist_nariz_a_asa)+mac*1/4)) + (CG_bateria*P_bateria) + (CG_helice*P_Helices) + (CG_motor*P_motor) + (CG_fios*P_fios) + (CG_servos*P_servos) + (CG_asa*P_asa) + (CG_h*P_cauda_h) + (CG_v*P_cauda_v) + (CG_fus*P_fus) + (Peso_fita*CG_fita) + (P_bequilha*CG_bequilha) + (P_trem_prin*CG_trem_prin))/(P_total + 5)
    
    #area molhada total

    Swet_total = (S_wet_asa+S_wet_h+S_wet_v+area_molhada_lados+area_molhada_horizontais)
    
    return(P_total,CG,Swet_total,S_wet_asa)

def arrasto(nome_do_perfil,
        perfil_ht,
        perfil_vt,
        V:float,
        lista_b:list,
        lista_Cr:list,
        lista_Ct:list,
        Clalpha:float,
        torção:float,
        alpha_0:float,
        diedro:float,
        rho:float,
        vis:float,
        h:float,
        N:int,
        i_w:float,
        a_s:float,
        Ced:float,
        CD0end:float,
        fator:float,
        C1:float,
        dist_nariz_a_asa:float,
        Cd0_w,
        Cd0_ht,
        Cd0_vt,
        Cd0ed,
        t_cht,
        t_cvt,
        t_cw,
        CL_solo_conservativo,
        CL_solo_ideal,
        analise):
    
    '________________________________________________________________________________________'
    
    #asa
    
    b = lista_b[len(lista_b)-1]*2

    S = b * cmac
    AR = b/cmac

    Ae = AR*fator

    e=1/(1.05+(0.007*math.pi*AR)) #oswald.pdf
 
    delt_CL = (math.pi*e*Ae*(2*CD0end*(Sep/S)))**0.5
    
    CLmax,listax,listay = LLT(lista_b,lista_Cr,lista_Ct,Clalpha,torção,a_s,alpha_0,diedro,N)
    
    CLmax = CLmax + delt_CL #compensação do endplate

    CLalpha_limpo = (CLmax - 0)/(a_s - alpha_0)
    CL0 = CLmax - (CLalpha_limpo*a_s)
    
    P_asa,Swetw = cma(nome_do_perfil,lista_Cr,lista_Ct,lista_b,phi,phil,phi_monk,esp,espn,Acir)
    
    '________________________________________________________________________________________'
    
    #estabilizadores
    
    ARh = (2/3)*(b/cmac)  #aproximação de Sadraey
    
    bh = (b)/2.5           #aproximação
    
    ch = bh/ARh
    
    Sh  = ((bh**2)/ARh)
    
    Sv = 2*(0.6645*Sh - 0.05948) #valor aproximado vendo os outros projetos
    
    ARv = 1.5  #aproximação de Sadraey
        
    macv = (Sv/ARv)**0.5    
    
    bv = Sv/macv
    
    lista_Cr2 = [ch,ch]
    lista_Ct2 = [ch,ch]
    lista_b2 = [0,bh/2]
    
    P_cauda_h,Swetht = cma(perfil_ht,lista_Cr2,lista_Ct2,lista_b2,phi,phil,phi_monk,esp,espn,Acir)
    
    lista_Cr3 = [macv,macv]
    lista_Ct3 = [macv,macv]
    lista_b3 = [0,bv/2]
    
    P_cauda_v,Swetvt = cma(perfil_vt,lista_Cr3,lista_Ct3,lista_b3,phi,phil,phi_monk,esp,espn,Acir)
    
    '________________________________________________________________________________________'
    
    #fuselagem
            
    alt = 0.125
    
    df = 0.15
    
    largura = 0.1
    
    lh = (0.4*S*cmac/Sh)
    
    dist_nariz_cg = dist_nariz_a_asa + cmac*1/4 # [m]
    
    lf = (dist_nariz_cg + lh) * 0.7 #ajuste de projeto
    
    area_molhada_lados = 2 * lf * alt 
    
    area_molhada_horizontais = 2 * lf * largura
    
    Swetf = area_molhada_lados + area_molhada_horizontais
    
    '________________________________________________________________________________________'

    Re = V*cmac/vis
    Reht = V*ch/vis
    Revt = V*macv/vis
    Ref  = V*lf/vis
    Rend = V*Ced/vis
    
    '________________________________________________________________________________________'
    
    #Cd0s
    
    x = Re/10000
    
    Cd0w = eval(Cd0_w)
    
    x = Reht/10000
    
    Cd0ht = eval(Cd0_ht)
    
    x = Revt/10000
    
    Cd0vt = eval(Cd0_vt)
    
    Cd0f  = 1.2         #paralelepipedo 

    
    '________________________________________________________________________________________'
    
    M = V/343

    CFw  = 0.42/(math.log10(Re)**2.58)
    CFht = 0.42/(math.log10(Reht)**2.58)
    CFvt = 0.42/(math.log10(Revt)**2.58)
    CFf  = 0.42/(math.log10(Ref)**2.58)
    CFed = 0.42/(math.log10(Rend)**2.58)

    fM = 1 - 0.08*(M**1.45)

    fld = 1 + (60/((lf/df)**3))+(0.0025*(lf/df))

    ftcw  = 1 + (2.7*(t_cw))  + (100*(t_cw**4))
    ftcht = 1 + (2.7*(t_cht)) + (100*(t_cht**4))
    ftcvt = 1 + (2.7*(t_cvt)) + (100*(t_cvt**4))
    ftced = 1 + (2.7*(t_end)) + (100*(t_end**4))

    CD0w   = CFw  * ftcw  * fM * (Swetw/S)   * ((Cd0w/0.004)**0.4)
    CD0ht  = CFht * ftcht * fM * (Swetht/S)  * ((Cd0ht/0.004)**0.4)
    CD0vt  = CFvt * ftcvt * fM * (Swetvt/S)  * ((Cd0vt/0.004)**0.4)
    CD0f   = CFf  * fld   * fM * (Swetf/S)   * ((Cd0f/0.004)**0.4)
    CD0end = CFed * ftced * fM * (Swetend/S) * ((Cd0ed/0.004)**0.4)

    CD0_Total = CD0w + CD0ht + CD0vt + CD0f + 2*CD0end*(Sep/S)
    
    '________________________________________________________________________________________'
    
    if analise == 'con':
        
        CLalpha = CLalpha_limpo * CL_solo_conservativo
    
        CLlocal = (CLalpha * i_w) + CL0 + (C1*(i_w*math.pi/180)**2)
    
    if analise == 'ide':
        
        CLlocal = (CLalpha_limpo * i_w) + CL0 + (C1*(i_w*math.pi/180)**2)

        CLlocal = CLlocal * CL_solo_ideal

    CDi = (CLlocal**2)/(math.pi*e*Ae)  

    solo = ((16*h/b)**2)/(1+((16*h/b)**2))

    CDi_decolagem = solo*CDi
    
    CD = CDi_decolagem + CD0_Total
    
    CD_asa = CDi_decolagem + CD0w
    
    solo = x #IGNORA!!   isso só para tirar uma mensagem irritante

    return(CLalpha_limpo,CL0,CLlocal,CD,CD_asa,CD0_Total)


def CLmax_velocidade(cmac:float,
                     lista_b:list,
                     lista_Cr:list,
                     lista_Ct:list,
                     eq_Clalpha:str,
                     eq_alpha_0:str,
                     eq_alpha_s:str,
                     diedro:float,
                     vis:float,
                     N:int,
                     incremento_MTOW:float,
                     CD0end:float,
                     fator:float,
                     C1:float
                     ):
    
    lista = np.arange(5,30,incremento_MTOW)
    
    b = lista_b[len(lista_b)-1]*2
    
    AR = b/cmac
    
    Ae = AR*fator
    
    e=1/(1.05+(0.007*math.pi*AR)) #oswald.pdf
    
    delt_CL = (math.pi*e*Ae*(2*CD0end*(Sep/S)))**0.5
    
    CLmax_lista = []
    
    for velocidade in lista:
    
        Re = cmac*velocidade/vis
    
        x=Re/10000
        
        Clalpha = eval(eq_Clalpha)
        alpha_0 = eval(eq_alpha_0)
        a_s     = eval(eq_alpha_s)

        CLmax,listax,listay = LLT(lista_b,lista_Cr,lista_Ct,Clalpha,torção,a_s,alpha_0,diedro,N)
        
        CLmax = CLmax + delt_CL #compensação do endplate
        
        CLalpha = (CLmax - 0)/(a_s - alpha_0)
        CL0 = CLmax - (CLalpha*a_s)

        CLmax = (CLalpha * a_s) + CL0 + (C1*(i_w*math.pi/180)**2)
    
        Re = x    
        
        CLmax_lista.append(CLmax)
        
    return(CLmax_lista)


def simps(f,m,a,b,N=50):
    
    dx = (b-a)/N
    V = np.linspace(a,b,N+1)
    y = eval(f)
    l = dx/3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
    return l,V


def MTOW(potencia:float,
         velocidade:float,
         densidade:float,
         atrito:float,
         mac:float,
         CLa:float,
         CL0:float,
         lista_b:list,
         lista_Cr:list,
         lista_Ct:list,
         eq_Clalpha:str,
         eq_alpha_0:str,
         eq_alpha_s:str,
         diedro:float,
         CD:float,
         massa:float,
         vis:float,
         N_g:int,
         i_w:float,
         incremento_MTOW:float,
         CD0end:float,
         fator:float,
         CL_solo_conservativo:float,
         CL_solo_ideal:float,
         analise:str,
         C1:float,
         ):

    
    b = lista_b[len(lista_b)-1]*2
    S = b * mac
        
    rho = densidade
    
    mu =  atrito                   #Coeficiente de atrito []
    g = 9.81                       #Aceleração gravitacional [m/s²]
    S_max = 58 - 0.7               #Restrição de pista [m]

    Δm = incremento_MTOW
    
    h_obs = 0.7 #altura do obstaculo
    
    if analise == 'con':
        
        CLa = CLa * CL_solo_conservativo
    
    CL = (CLa * i_w) + CL0 + (C1*(i_w*math.pi/180)**2)
    
    if analise == 'ide':

        CL = CL * CL_solo_ideal

    got_mtow = False
    _trigger = False    

    V = sy.symbols('V')
    m = sy.symbols('m')
    
    T = -0.04907*(V**2) + 0.3868*V + 37.12
    
    # T = -0.08447*(V**2) + 1.053*V + 35.14      #nova hélice
    
    L = (rho * (V**2) * S * CL)/2
    D = (rho * (V**2) * S * CD)/2

    W = m*g
    Fat = mu*(W-L)                                                    #Força de atrito [N]
    
    ΣFx = T - Fat - D 
    ΣFy = str(L - W)                      
    ΣFx = str(T - Fat - D )
    
    q = .5*rho*V**2
    Equation = str(V/( g*( (T/W - mu) - (CD -mu*CL)*q/(W/S)) ) )
    
    CL_max_lista = CLmax_velocidade(mac,lista_b,lista_Cr,lista_Ct,eq_Clalpha,eq_alpha_0,eq_alpha_s,diedro,vis,N_g,incremento_MTOW,CD0end,fator,C1)

    contagem = list(np.arange(5,30,Δm))
    
    m = massa*2
    
    while got_mtow is not True:

        for V in contagem:
            if eval(ΣFy)>=0:
                V_to = V
                break
        
        indx_clmax = contagem.index(V_to)
        CL_max = CL_max_lista[indx_clmax]
        
        V_estol = ( 2*W/(rho*S*CL_max))**0.5
        ΔCL = eval(str(0.5*((V_to/V_estol)**2 - 1)*(CL*((V_estol/V_to)**2 - 0.53) + 0.38)))
        R_tr = eval(str(2*((W/S)/(rho*g*ΔCL))))
        
        try:
            
            
            SG,nada = simps(Equation,m,0,V_to)                                 #Comprimento de pista [m] [Eq. 10.8 Roskam]
            θCL = eval(str((eval(ΣFx))/W))                                     #[rad] angulo de subida   
            
            S_tr = R_tr*math.sin(θCL)*0.3048   #de ft pra metro
            
            H_tr =  S_tr*θCL/2


            if H_tr > h_obs:
                
                S_CL = 0
                
            else:
                
                S_CL = (h_obs - H_tr)/math.tan(θCL)
                

            S_total = SG + S_tr + S_CL
            
            
        except UnboundLocalError:
            for V in contagem:
                if eval(ΣFy)>=0:
                    V_to = V
                    break
                
            m-= Δm
            _trigger = True
            
            
        "Correção caso passe do limite"
        if S_total > S_max:
            m -= Δm 
            
            _trigger = True
             
        else:
            pass
             
        if _trigger is True:
            got_mtow = True
            
            MTOW = m   

            _trigger = False
            
        m += Δm
        
    MTOW=round(MTOW,3)
    angulo_de_subida = round(np.rad2deg(np.arcsin(θCL)),2)

    return(V_to,angulo_de_subida,MTOW,CL,CLa)


def analise_controle(S:float,
                     b:float,
                     mac:float,
                     CLa:float,
                     cr:float,
                     TR:float,            
                     densidade:float,
                     velocidade:float):
    
    
    CLalpha = CLa*180/math.pi

    phi0 = densidade
    
    Vc = velocidade
         
    yDr=0.4*(b/2)    #Centro de arrasto, de acordo com a linha de referência da fuselagem eixo y
    poi=0.7*(b/2)     #posição inicial do aileron em uma só asa (eixo y): entre 0.5 e 0.65
    pof=0.9*(b/2)     #posição final do aileron em uma só asa   (eixo y): entre 0.8 e 0.95
    cac=0.15          #razão entre o comprimento do aileron e o comprimeito da asa eixo(x)
    deltaa=20         #deflexão dos ailerons
    
    bank=30     #bank angle escolhido para os ailerons EM GRAUS
    treq3=2.6   #lv 3 tempo requerido para alcançar o bank angle
    treq2=1.8   #lv 2 tempo requerido para alcançar o bank angle
    treq1=1.3   #lv 1 tempo requerido para alcançar o bank angle
    Cdr=0.7     #Coeficiente de arrasto durante a rolagem (entre 0.7 e 1.2)
    
    yi=poi                         #Posição do início do aileron, eixo y(do cg até a ponta da asa)
    y0=pof                         #Posição do fim do aileron, eixo y
    
    ARh = (2/3)*(b/mac)  #aproximação de Sadraey
    
    if ARh < 3:
        ARh = 3      #recomendação
    
    Sh  = (((b/3)**2)/ARh)
    
    Sv = 0.66454*Sh - 0.05948 #valor aproximado vendo os outros projetos
    
    Ixx = 0.9905*S - 0.5633  #valor aproximado vendo os outros projetos
    
    At = -5505.191*2**cac + 64.536*cac**4 + 303.021*cac**3 + 1319.252*cac**2 + 3818.384*cac + 0.0991*cac**(1/3) + 5505.191 #graf 12.12
    At = round(At,2)

    Cl_delta_A = ((2*CLalpha*At*cr)/(S*b))*((((y0**2)/2)+(2/3)*((TR-1)/b)*(y0**3))-(((yi**2)/2)+(2/3)*((TR-1)/b)*(yi**3)))

    deltaa=deltaa/57.3 #transformação em rad

    C1=Cl_delta_A*deltaa

    LA=0.5*phi0*(Vc**2)*S*C1*b 

    Pss=(2*LA/(phi0*(S+Sh+Sv)*Cdr*(yDr**3)))**0.5

    bank1=(Ixx/(phi0*(yDr**3)*(S+Sh+Sv)*Cdr))*math.log(Pss**2) #lembrar que esse log é ln

    Pponto=(Pss**2)/(2*bank1) 

    teste = (((bank*math.pi/180)*2)/Pponto)

    if (bank1*180/3.14) >= bank:
        if teste < 0:
            tf = 5
        if teste > 0:
            tf=(((bank*math.pi/180)*2)/Pponto)**0.5    #Sadraey n fala, mas no exemplo ele transforma o bank em rad

    if (bank1*180/3.14) < bank:
        if teste < 0:
            tf = 5
        if teste > 0:
            tss=(((bank1*math.pi/180)*2)/Pponto)**0.5
            t2=(((bank*math.pi/180)*2)/Pponto)**0.5
            bank2=Pss*(t2-tss)+bank1
            tf=tss+((bank2-bank1)/Pss)

    try:
        if tf<=treq1:
            nivel = 'Muito bom, pode aumentar a corda da asa'
        if tf<=treq2 and tf>treq1:
            nivel = 'Ta ótimo, corda da asa está próxima da perfeita'
        if tf<=treq3 and tf>treq2:
            nivel = 'Difícil, diminua a corda da asa'
        if tf<=treq3+0.5 and tf>treq3:
            nivel = 'Muito difícil, diminua a corda da asa'
        if tf>treq3+0.5:
            nivel = 'Impossível, mude essa asa!'
    except:
        nivel = 'Impossível, mude essa asa!'

    return(poi,pof,cac,nivel)


Numero_de_Reynols = round(cmac*V/vis,1)

x = (Numero_de_Reynols)/10000

Clalpha = eval(eq_Clalpha)
# Clalpha = 0.075 #valor experimental
alpha_0 = eval(eq_alpha_0)
# print(alpha_0)
a_s     = eval(eq_alpha_s) * 0.9

a_s = round(a_s)


b = lista_b[len(lista_b)-1]*2
S = b*cmac
AR = b/cmac
TR = lista_Ct[len(lista_Ct)-1]/lista_Cr[0]



m,CG_vazio,Swet_total,S_wet_asa = Calculo_do_peso(h,
                    nome_do_perfil,
                    perfil_ht,
                    perfil_vt,
                    lista_Cr,
                    lista_Ct,
                    lista_b,
                    phi,
                    phil,
                    phi_fita,
                    phi_monk,
                    esp,
                    espn,
                    Acir,
                    cmac,
                    dist_nariz_a_asa)    

'____________________________Sem efeito solo(no arrasto)____________________________'

CLalpha_sem_solo,CL0_sem_solo,CLmax_sem_solo,CDmax_sem_solo,CD_asa_max_sem_solo,CD0_Total_max_sem_solo = arrasto(nome_do_perfil,
              perfil_ht,
              perfil_vt,
              V,
              lista_b,
              lista_Cr,
              lista_Ct,
              Clalpha,
              torção,
              alpha_0,
              diedro,
              rho,
              vis,
              10000,
              N_g,
              a_s,
              a_s,
              Ced,
              CD0end,
              fator,
              C1,
              dist_nariz_a_asa,
              Cd0_asa,
              Cd0_ht,
              Cd0_vt,
              Cd0ed,
              tsob_c_ht,
              tsob_c_vt,
              tsob_c,
              1,
              1,
              analise)

CLalpha_sem_solo,CL0_sem_solo,CL_sem_solo,CD_sem_solo,CD_asa_sem_solo,CD0_Total_sem_solo = arrasto(nome_do_perfil,
              perfil_ht,
              perfil_vt,
              V,
              lista_b,
              lista_Cr,
              lista_Ct,
              Clalpha,
              torção,
              alpha_0,
              diedro,
              rho,
              vis,
              10000,
              N_g,
              i_w,
              a_s,
              Ced,
              CD0end,
              fator,
              C1,
              dist_nariz_a_asa,
              Cd0_asa,
              Cd0_ht,
              Cd0_vt,
              Cd0ed,
              tsob_c_ht,
              tsob_c_vt,
              tsob_c,
              1,
              1,
              analise)

'____________________________Com efeito solo(no arrasto)____________________________'

CLalpha,CL0,CLmax,CDmax,CD_asa_max,CD0_Total_max = arrasto(nome_do_perfil,
              perfil_ht,
              perfil_vt,
              V,
              lista_b,
              lista_Cr,
              lista_Ct,
              Clalpha,
              torção,
              alpha_0,
              diedro,
              rho,
              vis,
              h,
              N_g,
              a_s,
              a_s,
              Ced,
              CD0end,
              fator,
              C1,
              dist_nariz_a_asa,
              Cd0_asa,
              Cd0_ht,
              Cd0_vt,
              Cd0ed,
              tsob_c_ht,
              tsob_c_vt,
              tsob_c,
              solo_CL_con,
              solo_CL_ide,
              analise)

CLalpha,CL0,CL,CD,CD_asa,CD0_Total = arrasto(nome_do_perfil,
              perfil_ht,
              perfil_vt,
              V,
              lista_b,
              lista_Cr,
              lista_Ct,
              Clalpha,
              torção,
              alpha_0,
              diedro,
              rho,
              vis,
              h,
              N_g,
              i_w,
              a_s,
              Ced,
              CD0end,
              fator,
              C1,
              dist_nariz_a_asa,
              Cd0_asa,
              Cd0_ht,
              Cd0_vt,
              Cd0ed,
              tsob_c_ht,
              tsob_c_vt,
              tsob_c,
              solo_CL_con,
              solo_CL_ide,
              analise)


# CD = 0.1628
# CDmax = 0.3046

# CL0 = 0.91            #XF
# CLalpha = 0.0582      #XF
# CD = 0.112            #XF

V_to,angulo_de_subida,MT,CL_g,CLa_g = MTOW(poten,
               V,
               rho,
               atrito,
               cmac,
               CLalpha,
               CL0,
               lista_b,
               lista_Cr,
               lista_Ct,
               eq_Clalpha,
               eq_alpha_0,
               eq_alpha_s,
               diedro,
               CD,
               m,
               vis,
               N_g,
               i_w,
               incremento_MTOW,
               CD0end,
               fator,
               solo_CL_con,
               solo_CL_ide,
               analise,
               C1,)

'______________________________________teste______________________________________'

# i_w2 = angulo_de_subida/2 + i_w

# CLalpha2,CL02,CL2,CD2,CD_asa2,CD0_Total2 = arrasto(nome_do_perfil,
#               perfil_ht,
#               perfil_vt,
#               V,
#               lista_b,
#               lista_Cr,
#               lista_Ct,
#               Clalpha,
#               torção,
#               alpha_0,
#               diedro,
#               rho,
#               vis,
#               h,
#               N_g,
#               i_w2,
#               a_s,
#               Ced,
#               CD0end,
#               fator,
#               C1,
#               dist_nariz_a_asa,
#               Cd0_asa,
#               Cd0_ht,
#               Cd0_vt,
#               Cd0ed,
#               tsob_c_ht,
#               tsob_c_vt,
#               tsob_c,
#               solo_CL_con,
#               solo_CL_ide,
#               analise)

# V_to_2,angulo_de_subida_2,MT,CL_g,CLa_g = MTOW(poten,
#                 V,
#                 rho,
#                 atrito,
#                 cmac,
#                 CLalpha,
#                 CL0,
#                 lista_b,
#                 lista_Cr,
#                 lista_Ct,
#                 eq_Clalpha,
#                 eq_alpha_0,
#                 eq_alpha_s,
#                 diedro,
#                 CD2,
#                 m,
#                 vis,
#                 N_g,
#                 i_w2,
#                 incremento_MTOW,
#                 CD0end,
#                 fator,
#                 solo_CL_con,
#                 solo_CL_ide,
#                 analise,
#                 C1,)

'______________________________________teste______________________________________'

poi,pof,cac,contr = analise_controle(S,
                         b,
                         cmac,
                         CLalpha,
                         lista_Cr[0],
                         TR_eff,
                         rho,
                         V)
    

#posição real do CG:

verifica = round(100*abs((cmac/4)-abs(CG_vazio-dist_nariz_a_asa))/(cmac*0.3),2) #verificação do sadraey

porc = round(100*(CG_vazio-dist_nariz_a_asa)/(cmac),2) # porcentagem do CG na corda da asa

m = m + P_end  #adicionando o peso do endplate no peso total

#ângulo de ataque total da asa:
    
alt = i_w + angulo_de_subida

if alt > a_s:
    estol = True
else:
    estol = False

print('\n______________________________')

print('\nAnálise com T = ',T,'°C')
print('            V = ',V,'m/s') 
print('\nAsa',nome_da_asa)
print('Perfil',nome_do_perfil)
print('Número de Reynolds =',Numero_de_Reynols)


print('\nDados de entrada:')

print('\nDimensões:')
print('\nLista_Cr =',lista_Cr)
print('Lista_Ct =',lista_Ct)
print('Lista_b  =',lista_b)
print('\nIncidência        =',i_w,'°')
print('Torção            =',torção,'°')
print('Diedro            =',diedro,'°')
print('Enflechamento(C/2)=',round(enfl,2),'°')
print('Altura da asa     =',h,'m')
print('Potência do motor =',poten,'W')
print('Atrito das rodas  =',atrito,)
print('Viscosidade do ar =',round(vis,9),'m²/s')
print('Densidade do ar   =',round(rho,4),'Kg/m³')
print('Distância do nariz do avião até a asa =',dist_nariz_a_asa,'m')

print('\nDados de Saída:')

print('\nMAC      =',round(cmac,3),'m')
print('CA       =',round(cmac*1/4,3),'m')
print('b        =',round(b,3),'m')
print('AR       =',round(AR,3))
print('TR       =',round(TR,3))
print('TReff    =',round(TR_eff,3))
print('S        =',round(S,3),'m²')
print('S_real   =',round(S_real,3),'m²')
print('Swet_asa =',round(S_wet_asa,3),'m²')
print('Aproximação da área molhada do avião =',round(Swet_total,3),'m²')
print('\n\u03B1s_asa  =',round(a_s,1),'°')

print('____________________________________\nSem efeito solo:\n')

print('CL%s     ='%i_w,round(CL_sem_solo,4))
print('CL0     =',round(CL0_sem_solo,4))
print('CL\u03B1     =',round(CLalpha_sem_solo,4),'(1/°)')
print('CL_max  =',round(CLmax_sem_solo,4))
print('CD%s_asa ='%i_w,round(CD_asa_sem_solo,4))
print('CD_asa_max =',round(CD_asa_max_sem_solo,4))

print('\nCD do avião:\n')

print('CD0     =',round(CD0_Total_sem_solo,4))
print('CD%s     ='%i_w,round(CD_sem_solo,4))
print('CD_max  =',round(CDmax_sem_solo,4))

print('____________________________________\nCom efeito solo:\n')

print('CL%s_g        ='%i_w,round(CL_g,4))
print('CL0          =',round(CL0,4))
print('CL\u03B1_g        =',round(CLa_g,4),'(1/°)')
print('CL_max_g     =',round(CLmax,4))
print('CD%s_asa_g    ='%i_w,round(CD_asa,4))
print('CD_asa_max_g =',round(CD_asa_max,4))

print('\nCD do avião:\n')

print('CD0_g      =',round(CD0_Total,4))
print('CD%s_g      ='%i_w,round(CD,4))
print('CD_max_g   =',round(CDmax,4))

print('\nRecomendação, o controle da aeronave está:',contr)
print('CG está em',round(porc,3),'% da corda média da asa')
print('Verificação do Sadraey:',verifica,'% quanto menor melhor!')
print('Ângulo de subida =',angulo_de_subida,'°')

if estol == True:
    print(f'{Fore.RED}CUIDADO!!! O ângulo total da asa durante a subida pode estar ultrapassando o ângulo de estol{Style.RESET_ALL}')
else:
    print(f'{Fore.CYAN}A asa não entrará em estol{Style.RESET_ALL}')
if verifica > 100:
    print(f'{Fore.RED}CUIDADO!!! O CG está muito longe do CA da asa{Style.RESET_ALL}')
else:
    print(f'{Fore.CYAN}A distância ente o CG e o CA está aceitável{Style.RESET_ALL}')


print('\nV_decolagem =',round(V_to,1),'m/s')
print('MTOW        =',round(MT,3),'Kg')
print('P_total     =',round(m,3),'Kg')
print('Carga Paga  =',round(MT - m,3),'Kg')

print('\n_______________________________')



nome_da_pasta = 'Resultado de '+nome_da_asa+' '+nome_do_perfil+' V '+str(V)+' m_s'+' e '+str(T)+' °C'

try:
    path = os.path.join(os.path.dirname(__file__)+'\Resultados',nome_da_pasta)
    os.mkdir(path)
except:
    pass

local='Resultados/'+nome_da_pasta+'/Analise'+'.txt'

f = open(local,'w')
f.write('\n______________________________')

f.write('\n\n Análise com T = '+str(T)+' °C')
f.write('\n             V = '+str(V)+' m/s')
f.write('\n\nAsa '+nome_da_asa)
f.write('\nPerfil '+nome_do_perfil)
f.write('\nNúmero de Reynolds = '+str(Numero_de_Reynols))

f.write('\n\nDados de entrada:')

f.write('\n\n Dimensões:')
f.write('\nlista_Cr = [')

for i in range(len(lista_Cr)):
    f.write(','+str(lista_Cr[i]))
    
f.write(']\n')

f.write('\nlista_Ct = [')

for i in range(len(lista_Cr)):
    f.write(','+str(lista_Ct[i]))
    
f.write(']\n')

f.write('\nlista_b  = [')

for i in range(len(lista_Cr)):
    f.write(','+str(lista_b[i]))
    
f.write(']\n')

f.write('\n\nIncidência        = '+str(i_w)+' °')
f.write('\nTorção            = '+str(torção)+' °')
f.write('\nDiedro            = '+str(diedro)+' °')
f.write('\nEnflechamento(C/2)= '+str(round(enfl,4))+' °')
f.write('\nAltura da asa     = '+str(h)+' m')
f.write('\nPotência do motor = '+str(poten)+' W')
f.write('\nAtrito das rodas  = '+str(atrito))
f.write('\nViscosidade do ar = '+str(round(vis,9))+' m²/s')
f.write('\nDensidade do ar   = '+str(round(rho,4))+' Kg/m³')
f.write('\nDistância do nariz do avião até a asa = '+str(dist_nariz_a_asa)+' m')

f.write('\n\nDados de Saída:')

f.write('\n\nMAC      = ' +str(round(cmac,3))+' m')
f.write('\nCA       = '+str(round(cmac*1/4,3))+' m')
f.write('\nb        = '+str(round(b,3))+' m')
f.write('\nAR       = '+str(round(AR,3)))
f.write('\nTR       = '+str(round(TR,3)))
f.write('\nTReff    = '+str(round(TR_eff,3)))
f.write('\nS        = '+str(round(S,3))+' m²')
f.write('\nS_real   = '+str(round(S_real,3))+' m²')
f.write('\nSwet_asa = '+str(round(S_wet_asa,3))+' m²')
f.write('\nAproximação da área molhada do avião = '+str(round(Swet_total,3))+' m²')
f.write('\n\na_asa   = '+str(round(a_s,1))+' °')

f.write('\n____________________________________\nSem efeito solo:\n')

f.write('\nCL'+str(i_w)+'     = '+str(round(CL_sem_solo,4)))
f.write('\nCL0     = '+str(round(CL0_sem_solo,4)))
f.write('\nCLa     = '+str(round(CLalpha_sem_solo,4))+' (1/°)')
f.write('\nCL_max  = '+str(round(CLmax_sem_solo,4)))
f.write('\nCD'+str(i_w)+'_asa = '+str(round(CD_asa_sem_solo,4)))
f.write('\nCD_asa_max  = '+str(round(CD_asa_max_sem_solo,4)))

f.write('\n\nCD do avião todo:\n')

f.write('\nCD0     = '+str(round(CD0_Total_sem_solo,4)))
f.write('\nCD'+str(i_w)+'     = '+str(round(CD_sem_solo,4)))
f.write('\nCD_max  = '+str(round(CDmax_sem_solo,4)))

f.write('\n____________________________________\nCom efeito solo:\n')


f.write('\nCL'+str(i_w)+'_g     = '+str(round(CL_g,4)))
f.write('\nCL0     = '+str(round(CL0,4)))
f.write('\nCLa_g     = '+str(round(CLa_g,4))+' (1/°)')
f.write('\nCL_max_g  = '+str(round(CLmax,4)))
f.write('\nCD'+str(i_w)+'_asa_g = '+str(round(CD_asa,4)))
f.write('\nCD_asa_max_g  = '+str(round(CD_asa_max,4)))

f.write('\n\nCD do avião todo:\n')

f.write('\nCD0_g    = '+str(round(CD0_Total,4)))
f.write('\nCD'+str(i_w)+'_g    = '+str(round(CD,4)))
f.write('\nCD_max_g = '+str(round(CDmax,4)))




f.write('\n\nControle: '+str(contr))
f.write('\nCG está em '+str(round(porc,3))+' % da corda média da asa')
f.write('\nVerificação do Sadraey: '+str(verifica)+' % quanto menor melhor!')
f.write('\nÂngulo de subida = '+str(angulo_de_subida)+' °')

if estol == True:
    f.write('\nCUIDADO!!! O ângulo total da asa durante a subida pode estar ultrapassando o ângulo de estol')
else:
    f.write('\nA asa não entrará em estol')

if verifica > 100:
    f.write('\nCUIDADO!!! O CG está muito longe do CA da asa')
else:
    f.write('\nA distância ente o CG e o CA está aceitável')

f.write('\n\nV_decolagem = '+str(round(V_to,1))+' m/s')
f.write('\nMTOW        = '+str(round(MT,3))+' Kg') 
f.write('\nP_total     = '+str(round(m,3))+' Kg')
f.write('\nCarga Paga  = '+str(round(MT - m,3))+' Kg')

f.write('\n\n______________________________')
f.close()

'______________________________________________________________________'


#gráficos

try:
    plt.style.use('extensys-gd')
except:
    pass


'___________________________________________________________________________________________________'

# Desenho do perfil


pontos = pd.read_csv(nome_do_arquivo+'.dat',delimiter=' ')

xa=pontos.iloc[:,0]
ya=pontos.iloc[:,1]

vx=list(map(lambda i: float(i),xa))
vy=list(map(lambda i: float(i),ya))

ymax=max(vy)
ymin=min(vy) 

local_graf = 'Resultados/'+nome_da_pasta+'/'

graf_p = plt.figure(num=None, figsize=(10.5, 7.5), dpi=200, facecolor='w', edgecolor='k')
plt.xlabel('Eixo x [m]')
plt.ylabel('Eixo z [m]')
plt.title('Gráfico do perfil')
plt.axis([-0.05,1.05,ymin-0.3,ymax+0.3])
plt.plot(vx,vy,color='b')   

graf_p.savefig(local_graf+' Desenho do perfil'+'.png')

'___________________________________________________________________________________________________'

# Desenho da asa

x=sy.symbols('x')

segmentos=[]

for i in range(len(lista_b)):
    if i == 0:
        linha = lista_Cr[i] + (((lista_Ct[i]-lista_Cr[i])/(lista_b[i]-0))*(x-0))
    if i > 0:     
        linha = lista_Cr[i] + (((lista_Ct[i]-lista_Cr[i])/(lista_b[i]-lista_b[i-1]))*(x-lista_b[i-1]))
    
    segmentos.append(linha)

listax = np.linspace(0,lista_b[len(lista_b)-1],100)
listay = []
listacont = np.arange(1,len(lista_b),1)

for x in listax:
    
    if x < lista_b[0]:
        y = eval(str(segmentos[0]))
    
    if x > lista_b[0]:
        for i in listacont:
            if x > lista_b[i-1] and x < lista_b[i]:
                y = eval(str(segmentos[i]))
                
    listay.append(y)

listax2 = []

for i in range(len(listay)):
    listax2_v = -listax[i]      
    listax2.append(listax2_v)

for i in range(len(listay)):
    listay[i] = -listay[i]


px = [-lista_b[len(lista_b)-1],-lista_b[len(lista_b)-1]]
py = [0,-lista_Ct[len(lista_Ct)-1]]

bx = [lista_b[len(lista_b)-1],lista_b[len(lista_b)-1]]
by = [0,-lista_Ct[len(lista_Ct)-1]]

cx = [-lista_b[len(lista_b)-1],lista_b[len(lista_b)-1]]
cy = [0,0]

#Desenhando a asa de 2022

cix = [-1,1]
ciy = [0,0]

esx = [-1,-1]
esy = [0,-0.24]

dix = [1,1]
diy = [0,-0.24]

rex = [-1,-0.5]
rey = [-0.24,-0.54]

rix = [0.5,1]
riy = [-0.54,-0.24]

bax = [-0.5,0.5]
bay = [-0.54,-0.54]

        
graf_a = plt.figure(num=None, figsize=(19, 13.5), dpi=200, facecolor='w', edgecolor='k')

#asa atual

plt.plot(listax,listay,color='blue')
plt.plot(listax2,listay,color='blue')
plt.plot(cx,cy,color='b')
plt.plot(px,py,color='b')
plt.plot(bx,by,color='b',label='atual')

#asa 2022

# plt.plot(cix,ciy,color='purple',label='2022')
# plt.plot(esx,esy,color='purple')
# plt.plot(dix,diy,color='purple')
# plt.plot(rex,rey,color='purple')
# plt.plot(rix,riy,color='purple')
# plt.plot(bax,bay,color='purple')

#ailerons

# plt.axvline(poi ,ymax = 0.35, linestyle = ':',color='black')
# plt.axvline(pof ,ymax = 0.35, linestyle = ':',color='black')

plt.axhline(-cmac*1/4,linestyle = '-.',label='CA')
plt.scatter(0,dist_nariz_a_asa-CG_vazio,label='CG')


# plt.title('Desenho da Asa '+nome_da_asa)
plt.axis([-0.1-lista_b[len(lista_b)-1],lista_b[len(lista_Ct)-1]+0.1,-max(lista_Cr)-0.05,0.05])
plt.xlabel('b[m]')
plt.ylabel('C[m]')
# plt.legend(bbox_to_anchor=(0.92, 0.85, 0.25, 0.1), frameon=True, shadow=True, ncol=2)
plt.legend(bbox_to_anchor=(0.98,0.15), frameon=True, shadow=True, ncol=2)
ax = plt.gca()
ax.set_aspect('equal',adjustable = 'box')
plt.show()

graf_a.savefig(local_graf+' Desenho da asa'+'.png')

'___________________________________________________________________________________________________'

'Desenho do avião todo'

'______________________________________________________'

#estabilizadores

ARh = (2/3)*(b/cmac)  #aproximação de Sadraey

bh = (b)/2.5           #aproximação

ch = bh/ARh

Sh  = ((bh**2)/ARh)

Sv = 2*(0.6645*Sh - 0.05948) #valor aproximado vendo os outros projetos

ARv = 1.5  #aproximação de Sadraey
    
macv = (Sv/ARv)**0.5    

bv = Sv/macv

lista_Cr2 = [ch,ch]
lista_Ct2 = [ch,ch]
lista_b2 = [0,bh/2]

P_cauda_h,Swetht = cma(perfil_ht,lista_Cr2,lista_Ct2,lista_b2,phi,phil,phi_monk,esp,espn,Acir)

lista_Cr3 = [macv,macv]
lista_Ct3 = [macv,macv]
lista_b3 = [0,bv/2]

P_cauda_v,Swetvt = cma(perfil_vt,lista_Cr3,lista_Ct3,lista_b3,phi,phil,phi_monk,esp,espn,Acir)

'______________________________________________________'

#fuselagem

alt = h/2

df = 0.15

largura = 0.1

lh = (0.4*S*cmac/Sh)

dist_nariz_cg = dist_nariz_a_asa + cmac*1/4 # [m]

lf = (dist_nariz_cg + lh) * 0.7 #ajuste de projeto

'______________________________________________________'

'linhas da fuselagem'

fufx = [-df/2,df/2]
fufy = [dist_nariz_a_asa,dist_nariz_a_asa]

fuex = [-df/2,-df/2]
fuey = [dist_nariz_a_asa,dist_nariz_a_asa - CG_vazio - lh]

fudx = [df/2,df/2]
fudy = [dist_nariz_a_asa,dist_nariz_a_asa - CG_vazio - lh]

futx = [-df/2,df/2]
futy = [dist_nariz_a_asa - CG_vazio - lh,dist_nariz_a_asa - CG_vazio - lh]

'linhas dos estabilizadores'

ehfx = [-bh/2,bh/2]
ehfy = [dist_nariz_a_asa - CG_vazio - lh + (ch/4), dist_nariz_a_asa- CG_vazio - lh + (ch/4)]

ehex = [-bh/2,-bh/2]
ehey = [dist_nariz_a_asa - CG_vazio - lh + (ch/4), dist_nariz_a_asa- CG_vazio - lh + (ch/4) - ch]

ehdx = [bh/2,bh/2]
ehdy = [ dist_nariz_a_asa- CG_vazio - lh + (ch/4), dist_nariz_a_asa- CG_vazio - lh + (ch/4) - ch]

ehtx = [-bh/2,bh/2] 
ehty = [ dist_nariz_a_asa- CG_vazio - lh + (ch/4) - ch, dist_nariz_a_asa- CG_vazio - lh + (ch/4) - ch]


graf_a = plt.figure(num=None, figsize=(19, 13.5), dpi=200, facecolor='w', edgecolor='k')

#fuselagem

plt.plot(fufx,fufy,color='black')
plt.plot(fuex,fuey,color='black')
plt.plot(fudx,fudy,color='black')
plt.plot(futx,futy,color='black',label='Fuselagem')

#asa atual

plt.plot(listax,listay,color='b')
plt.plot(listax2,listay,color='b')
plt.plot(cx,cy,color='b')
plt.plot(px,py,color='b')
plt.plot(bx,by,color='b',label='Asa')

plt.plot(ehfx,ehfy,color='purple')
plt.plot(ehex,ehey,color='purple')
plt.plot(ehdx,ehdy,color='purple')
plt.plot(ehtx,ehty,color='purple',label='EH')


plt.axis([-0.1-lista_b[len(lista_b)-1],lista_b[len(lista_Ct)-1]+0.1,dist_nariz_a_asa- CG_vazio - lh + (ch/4) - ch - 0.1, dist_nariz_a_asa + 0.1])
plt.axhline(-cmac*1/4,linestyle = '-.',label='CA')
plt.scatter(0,dist_nariz_a_asa-CG_vazio,label='CG',color='black',s = 150)
plt.title('Expectativa teórica do avião')
plt.xlabel('Eixo y [m]')
plt.ylabel('Eixo x [m]')
# plt.legend(bbox_to_anchor=(0.92, 0.85, 0.25, 0.1), frameon=True, shadow=True, ncol=2)
plt.legend(bbox_to_anchor=(0.98,0.15), frameon=True, shadow=True, ncol=2)
ax = plt.gca()
ax.set_aspect('equal',adjustable = 'box')
plt.show()

graf_a.savefig(local_graf+' Expectativa do avião'+'.png')

'___________________________________________________________________________________________________'

#grafico em 3D

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
    

graf_3D = plt.figure(num=None, figsize=(13.5, 10.5), dpi=200, facecolor='w', edgecolor='k')
ax = plt.axes(projection='3d')

listax = list(listax)

for j in range(2):
    for i in listax:
        if i % 2:
            tirar = listax.index(i)
            listax.pop(tirar)
            listay.pop(tirar)


for i in listax:
    
    index = listax.index(i)
    
    j = abs(listay[index])

    vxx = []
    vyy = []

    vxx = list(map(lambda k: float(k)*j,xa))
    vyy = list(map(lambda k: float(k)*j,ya))

    b_em_3d = np.linspace(i,i,len(vx))

    ax.plot3D(vxx , b_em_3d, vyy, 'blue')
    
    x2 = -i
    
    index = listax.index(i)
    
    j = abs(listay[index])
    
    vxx = []
    vyy = []

    vxx = list(map(lambda k: float(k)*j,xa))
    vyy = list(map(lambda k: float(k)*j,ya))

    b_em_3d = np.linspace(x2,x2,len(vx))

    ax.plot3D(vxx , b_em_3d, vyy, 'blue')


set_axes_equal(ax)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

graf_3D.savefig(local_graf+' Desenho da asa em 3D'+'.png')

#Polar de arrasto e gráfico L/D

lista_i = np.arange(alpha_0,a_s,0.5)
lista_CL = []
lista_CD = []
lista_L_D = []
lista_CL2 = []
lista_CD2 = []
lista_L_D2=[]

for i_ww in lista_i:

    
    CLalpha,CL0,CL,CD,CD_asa,CD0_Total = arrasto(nome_do_perfil,
                  perfil_ht,
                  perfil_vt,
                  V,
                  lista_b,
                  lista_Cr,
                  lista_Ct,
                  Clalpha,
                  torção,
                  alpha_0,
                  diedro,
                  rho,
                  vis,
                  h,
                  N_g,
                  i_ww,
                  a_s,
                  Ced,
                  CD0end,
                  fator,
                  C1,
                  dist_nariz_a_asa,
                  Cd0_asa,
                  Cd0_ht,
                  Cd0_vt,
                  Cd0ed,
                  tsob_c_ht,
                  tsob_c_vt,
                  tsob_c,
                  solo_CL_con,
                  solo_CL_ide,
                  analise)
    
    CLalpha2,CL02,CL2,CD2,CD_asa2,CD0_Total2 = arrasto(nome_do_perfil,
                  perfil_ht,
                  perfil_vt,
                  V,
                  lista_b,
                  lista_Cr,
                  lista_Ct,
                  Clalpha,
                  torção,
                  alpha_0,
                  diedro,
                  rho,
                  vis,
                  h,
                  N_g,
                  i_ww,
                  a_s,
                  Ced,
                  0,
                  1,
                  C1,
                  dist_nariz_a_asa,
                  Cd0_asa,
                  Cd0_ht,
                  Cd0_vt,
                  Cd0ed,
                  tsob_c_ht,
                  tsob_c_vt,
                  tsob_c,
                  solo_CL_con,
                  solo_CL_ide,
                  analise)

    
    lista_CL.append(CL)
    lista_CD.append(CD)
    
    lista_CL2.append(CL2)
    lista_CD2.append(CD2)
    
    lista_L_D.append(CL/CD)
    lista_L_D2.append(CL2/CD2)
    
graf_a = plt.figure(num=None, figsize=(10.5,7.5), dpi=200, facecolor='w',edgecolor='k')
plt.plot(lista_CD,lista_CL,color='b',label='Endplate')
plt.plot(lista_CD2,lista_CL2,color='black',label='Sem Endplate',linestyle='--')
plt.title('Polar de arrasto')
plt.xlabel('CD')
plt.ylabel('CL')
plt.legend(bbox_to_anchor=(1.02, 0.85, 0.25, 0.1), frameon=True, shadow=True, ncol=1)
plt.show()

graf_a.savefig(local_graf+' Polar de arrasto'+'.png')

graf_a = plt.figure(num=None, figsize=(10.5,7.5), dpi=200, facecolor='w',edgecolor='k')
plt.plot(lista_i,lista_L_D,color='b',label='Endplate')
plt.plot(lista_i,lista_L_D2,color='black',label='Sem Endplate',linestyle='--')
plt.title('Eficiência aerodinâmica')
plt.xlabel('\u03B1')
plt.ylabel('L/D')
plt.legend(bbox_to_anchor=(1.02, 0.85, 0.25, 0.1), frameon=True, shadow=True, ncol=1)
plt.show()

graf_a.savefig(local_graf+' Eficiência aerodinâmica'+'.png')

graf_a = plt.figure(num=None, figsize=(10.5,7.5), dpi=200, facecolor='w',edgecolor='k')
plt.plot(lista_i,lista_CL,color='b',label='Endplate')
plt.plot(lista_i,lista_CL2,color='black',label='Sem Endplate',linestyle='--')
plt.title('CL vs \u03B1')
plt.xlabel('\u03B1')
plt.ylabel('CL')
plt.legend(bbox_to_anchor=(1.02, 0.85, 0.25, 0.1), frameon=True, shadow=True, ncol=1)
plt.show()

graf_a.savefig(local_graf+' CL vs alpha'+'.png')

graf_a = plt.figure(num=None, figsize=(10.5,7.5), dpi=200, facecolor='w',edgecolor='k')
plt.plot(lista_i,lista_CD,color='b',label='Endplate')
plt.plot(lista_i,lista_CD2,color='black',label='Sem Endplate',linestyle='--')
plt.title('CD vs \u03B1')
plt.xlabel('\u03B1')
plt.ylabel('CD')
plt.legend(bbox_to_anchor=(1.02, 0.85, 0.25, 0.1), frameon=True, shadow=True, ncol=1)
plt.show()

graf_a.savefig(local_graf+' CD vs alpha'+'.png')

# plt.figure(num=None, figsize=(10.5,7.5), dpi=200, facecolor='w',edgecolor='k')
# plt.plot(lista_CD,lista_CL,color='b')
# plt.xlabel('CD')
# plt.ylabel('CL')
# plt.show()

# plt.figure(num=None, figsize=(10.5,7.5), dpi=200, facecolor='w',edgecolor='k')
# plt.plot(lista_CL,lista_L_D,color='b')
# plt.xlabel('CL')
# plt.ylabel('L/D')
# plt.show()

# plt.figure(num=None, figsize=(10.5,7.5), dpi=200, facecolor='w',edgecolor='k')
# plt.plot(lista_i,lista_CL,color='b')
# plt.xlabel('\u03B1')
# plt.ylabel('CL')
# plt.axis([0,a_s,0.6,2])
# plt.show()

# plt.figure(num=None, figsize=(10.5,7.5), dpi=200, facecolor='w',edgecolor='k')
# plt.plot(lista_i,lista_CD,color='b')
# plt.xlabel('\u03B1')
# plt.ylabel('CD')
# plt.axis([0,a_s,0,round(CDmax+0.05,2)])
# plt.show()

'___________________________________________________________________________________________________'

# L em função da temperatura:

lista_T=list(lista_T)    

if graf == True:

    lista_MTOW = []
    lista_LsoD = []
    remover=[]
    
    print('\nCarregando...')
    
    for T in lista_T:
        
        print('\nT =',T,'°C')

        rho = -3.52607427278736e-8*T**3 + 1.60215687088211e-5*T**2 - 0.00471578515074178*T + 1.2925545912127
        vis = 5.63034007726774e-13*T**3 + 1.15655321938951e-11*T**2 + 9.06376414877547e-8*T + 1.32700903275642e-5
        
        Numero_de_Reynols = round(cmac*V/vis,1)

        x = (Numero_de_Reynols)/10000

        Clalpha = eval(eq_Clalpha)

        alpha_0 = eval(eq_alpha_0)

        a_s     = eval(eq_alpha_s)

        a_s = 0.9*a_s

        b = lista_b[len(lista_b)-1]*2
        S = b*cmac
        AR = b/cmac
        TR = lista_Ct[len(lista_Ct)-1]/lista_Cr[0]

        m,CG_vazio,Swet_total,S_wet_asa = Calculo_do_peso(h,
                            nome_do_perfil,
                            perfil_ht,
                            perfil_vt,
                            lista_Cr,
                            lista_Ct,
                            lista_b,
                            phi,
                            phil,
                            phi_fita,
                            phi_monk,
                            esp,
                            espn,
                            Acir,
                            cmac,
                            dist_nariz_a_asa)    



        CLalpha,CL0,CLmax,CDmax,Lmax,Dmax = arrasto(nome_do_perfil,
                      perfil_ht,
                      perfil_vt,
                      V,
                      lista_b,
                      lista_Cr,
                      lista_Ct,
                      Clalpha,
                      torção,
                      alpha_0,
                      diedro,
                      rho,
                      vis,
                      h,
                      N_g,
                      a_s,
                      a_s,
                      Ced,
                      CD0end,
                      fator,
                      C1,
                      dist_nariz_a_asa,
                      Cd0_asa,
                      Cd0_ht,
                      Cd0_vt,
                      tsob_c_ht,
                      tsob_c_vt,
                      tsob_c,
                      solo_CL_con,
                      solo_CL_ide,
                      analise)

        CLalpha,CL0,CL,CD,L,D = arrasto(nome_do_perfil,
                      perfil_ht,
                      perfil_vt,
                      V,
                      lista_b,
                      lista_Cr,
                      lista_Ct,
                      Clalpha,
                      torção,
                      alpha_0,
                      diedro,
                      rho,
                      vis,
                      h,
                      N_g,
                      i_w,
                      a_s,
                      Ced,
                      CD0end,
                      fator,
                      C1,
                      dist_nariz_a_asa,
                      Cd0_asa,
                      Cd0_ht,
                      Cd0_vt,
                      tsob_c_ht,
                      tsob_c_vt,
                      tsob_c,
                      solo_CL_con,
                      solo_CL_ide,
                      analise)

        V_to,angulo_de_subida,MT,CL_g,CLa_g = MTOW(poten,
                       V,
                       rho,
                       atrito,
                       cmac,
                       CLalpha,
                       CL0,
                       lista_b,
                       lista_Cr,
                       lista_Ct,
                       eq_Clalpha,
                       eq_alpha_0,
                       eq_alpha_s,
                       diedro,
                       CD,
                       m,
                       vis,
                       N_g,
                       i_w,
                       incremento_MTOW,
                       CD0end,
                       fator,
                       solo_CL_con,
                       solo_CL_ide,
                       analise,
                       C1,)

        print('MTOW =',round(MT,3),'Kg')
        L_D = round(L/D,3)
        
        MT = round(MT,3)
        
        lista_LsoD.append(L_D)
        lista_MTOW.append(MT)
            

    graf1=plt.figure(num=None, figsize=(10.5, 7.5), dpi=200, facecolor='w', edgecolor='k')
    plt.plot(lista_T,lista_MTOW,color='b')
    plt.xlabel ('T [°C]')
    plt.ylabel ('MTOW [Kg]')    
    plt.title ('MTOW em função da temperatura')
    
    graf1.savefig(local_graf+'Sustentação em função da temperatura'+' V'+str(V)+'.png')
    
    graf2=plt.figure(num=None, figsize=(10.5, 7.5), dpi=200, facecolor='w', edgecolor='k')
    plt.plot(lista_T,lista_LsoD,color='b')
    plt.xlabel ('T [°C]')
    plt.ylabel ('L/D')    
    plt.title ('Eficiência em função da temperatura')
    
    graf2.savefig(local_graf+'Eficiência em função da temperatura'+' V'+str(V)+'.png')
    
    
    print('Tudo terminado! Verifique a pasta de Resultados')


    local_das_listas='Resultados/'+nome_da_pasta+'/graf'+'.txt'
    
    lista_T = list(lista_T)
    tamanho_das_listas = len(lista_T)
    
    f = open(local_das_listas,'w')
    f.write('________________________________________________________________________________________________________________________________________________________________________________')

    f.write('\n\nPerfil '+nome_do_perfil)
    f.write('\n\nTemp = [')

    for i in range(tamanho_das_listas):
        f.write(' , '+str((round(lista_T[i],1))))
        
    f.write(' ]\n')

    f.write('\n\nMTOW    = [')

    for i in range(tamanho_das_listas):
        f.write(' , '+str(lista_MTOW[i]))
        
    f.write(' ]\n')

    f.write('\n\nL/D  = [')

    for i in range(tamanho_das_listas):
        f.write(' , '+str(lista_LsoD[i]))
        
    f.write(' ]\n')

    f.write('________________________________________________________________________________________________________________________________________________________________________________')
    f.close()
    
fim = time.time()

print('\nTempo de processamento: %s segundos'%round(fim-com,1))


    
    