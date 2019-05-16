import os
import csv

'''
    CSV Structure

    MesDelParto, AñoDelParto, LugarDelParto, PartoAsistido,
    PartoNormalOConComplicaciones, PartoConOSinCesárea,
    ATérminoOPrematuro, NúmeroDeSemanasDelEmbarazo,
    EdadDeLaMadreEnAñosCumplidos, SexoDelNacido, PesoDelNacido,
    NúmeroDeHijosNacidosVivosTotalesALoLargoDeSuVida
    
    Each file contains data of an entire year

'''

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIRTHS_DATA = [BASE_DIR, 'data', 'births', 'datos_nacimientos{}.txt']
BIRTHS_PROCESSED = [BASE_DIR, 'data', 'births', 'processed', 'births_processed.csv']

'''
    Obtains a path using current SO path separator
    using a the specified path represented as a list.
'''
def get_file_path(path_list):
    res = ''

    for p in path_list:
        res = os.path.join(res, p)

    return res

'''
    A line is valid if and only if:
        
        - Provincia de Inscripción es Sevilla
        - Municipio de Inscripción es Sevilla
        - Provincia del Parto es Sevilla
        - Municipio del Parto es Sevilla
        - Indicador Nacionalidad Española de la Madre es Positivo
        - País Nacionalidad Madre es España
        - Cuándo Adquiere la Nacionalidad la Madre es De Nacimientos
        - Provincia de Nacimiento de la Madre es Sevilla
        - Municipio de Nacimiento de la Madre es Sevilla
        - Provincia de Residencia de la Madre es Sevilla
        - Municipio de Residencia de la Madre es Sevilla
        - Peso del Nacido no está Vacío
        - Clasificación del Nacido es Nacido con Vida y Vivió Más de 24 Horas
'''
def line_is_valid(proi, muni, propar, munpar, nacioem, paisnacm, cuannacm,
                  proma, munma, prorem, munrem, peson, clasif):

    res = False

    if(proi == '41' and muni == '091' and propar == '41' 
       and munpar == '091' and nacioem == '1' and paisnacm == '108'
       and cuannacm == '1' and proma == '41' and munma == '091'
       and prorem == '41' and munrem == '091' and peson != '    '
       and clasif == '3'):
        res = True

    return res

def prettify_lugarpa(int_lugarpa):

    res = int_lugarpa
    
    if int_lugarpa == '1':
        res = 'Centro Sanitario'
        
    elif int_lugarpa == '2':
        res = 'Domicilio Particular'
        
    elif int_lugarpa == '3':
        res = 'Otro lugar'

    return res

def prettify_asistido(int_asistido):

    res = int_asistido
    
    if int_asistido == '1':
        res = 'Sí'
        
    elif int_asistido == '2':
        res = 'No'

    return res

def prettify_norma(int_norma):

    res = int_norma
    
    if int_norma == '1':
        res = 'Normal'
        
    elif int_norma == '2':
        res = 'Con complicaciones'

    return res

def prettify_cesarea(int_cesarea):

    res = int_cesarea
    
    if int_cesarea == '1':
        res = 'Con cesárea'
        
    elif int_cesarea == '2':
        res = 'Sin cesárea'

    return res

def prettify_intersem(int_intersem):

    res = int_intersem
    
    if int_intersem == '1':
        res = 'A término'
        
    elif int_intersem == '2':
        res = 'Prematuro'
        
    elif int_intersem == '3':
        res = 'No consta'

    return res

def prettify_sexo(int_sexo):

    res = int_sexo
    
    if int_sexo == '1':
        res = 'Varón'
        
    elif int_sexo == '6':
        res = 'Mujer'

    return res

def prettify_peson(int_peson):

    res = int_peson
    
    if int_peson != '    ':
        res = int_peson[0:1] + '.' + int_peson[1:4]

    return res

if __name__ == '__main__':

    births_data_path = get_file_path(BIRTHS_DATA)
    births_processed = get_file_path(BIRTHS_PROCESSED)

    if os.path.exists(births_processed):
        os.remove(births_processed)
    
    births_data_file = births_data_path.format(2017)

    with open(births_data_file, mode='r', encoding='utf-8') as datafile, \
            open(births_processed, mode='a+', encoding='utf-8') as processed:

        # Both reader & writer
        csv_reader = csv.reader(datafile, delimiter=',')
        csv_writer_users = csv.writer(processed, delimiter=',')
        
        titles_list = []
        
        #titles_list.append('Provincia de Inscripción')
        #titles_list.append('Municipio de Inscripción')
        titles_list.append('Mes del Parto')
        titles_list.append('Año del Parto')
        #titles_list.append('Provincia del Parto')
        #titles_list.append('Municipio del Parto')
        titles_list.append('Lugar del Parto')
        titles_list.append('Parto Asistido')
        #titles_list.append('Número de Nacidos con o sin vida')
        titles_list.append('Parto Normal o con Complicaciones')
        titles_list.append('Parto con o sin Cesárea')
        titles_list.append('A Término o Prematuro')
        titles_list.append('Número de Semanas del Embarazo')
        #titles_list.append('Mes de Nacimiento de la Madre')
        #titles_list.append('Año de Nacimiento de la Madre')
        #titles_list.append('Indicador Nacionalidad Española de la Madre')
        #titles_list.append('Indicador Nacionalidad Extranjera de la Madre')
        #titles_list.append('País Nacionalidad Madre')
        #titles_list.append('Cuándo Adquiere la Nacionalidad la Madre')
        #titles_list.append('Provincia de Nacimiento de la Madre')
        #titles_list.append('Municipio de Nacimiento de la Madre')
        #titles_list.append('País de Nacimiento en el Extranjero de la Madre')
        #titles_list.append('Provincia de Residencia de la Madre')
        #titles_list.append('Municipio de Residencia de la Madre')
        #titles_list.append('País de Residencia en el Extranjero de la Madre')
        #titles_list.append('Nivel de Estudios de la Madre')
        #titles_list.append('Profesión Madre de la Madre')
        #titles_list.append('Estado Civil de la Madre')
        #titles_list.append('Indicador de si es Primer Matrimonio de la Madre')
        #titles_list.append('Mes del Actual Matrimonio')
        #titles_list.append('Año del Actual Matrimonio')
        #titles_list.append('Indicador de si la Madre Tiene Pareja de Hecho')
        #titles_list.append('Indicador de si es la Primera Unión Estable de la Madre')
        #titles_list.append('Mes de Inicio de la Actual Unión Estable de la Madre')
        #titles_list.append('Año de Inicio de la Actual Unión Estable de la Madre')
        #titles_list.append('Número de Hijos Contando este Parto (Vivos y Muertos)')
        #titles_list.append('Número de Hijos Nacidos Vivos en Partos Anteriores')
        #titles_list.append('Mes de Nacimiento del Hijo Anterior')
        #titles_list.append('Año de Nacimiento del Hijo Anterior')
        #titles_list.append('Provincia de Nacimiento del Hijo Anterior')
        #titles_list.append('Municipio de Nacimiento del Hijo Anterior')
        #titles_list.append('País de Nacimiento en el Extranjero del Hijo Anterior')
        #titles_list.append('Indicador Nacionalidad Española del Hijo Anterior')
        #titles_list.append('Indicador Nacionalidad Extranjera del Hijo Anterior')
        #titles_list.append('País Nacionalidad del Hijo Anterior')
        #titles_list.append('Mes de Nacimiento del Padre')
        #titles_list.append('Año de Nacimiento del Padre')
        #titles_list.append('Indicador Nacionalidad Española del Padre')
        #titles_list.append('Indicador Nacionalidad Extranjera del Padre')
        #titles_list.append('País de Nacionalidad del Padre')
        #titles_list.append('Cuándo Adquiere la Nacionalidad el Padre')
        #titles_list.append('Provincia de Nacimiento del Padre')
        #titles_list.append('Municipio de Nacimiento del Padre')
        #titles_list.append('País de Nacimiento en el Extranjero del Padre')
        #titles_list.append('Dónde Reside el Padre')
        #titles_list.append('Provincia de Residencia del Padre')
        #titles_list.append('Municipio de Residencia del Padre')
        #titles_list.append('País de Residencia en el Extranjero del Padre')
        #titles_list.append('Nivel de Estudios del Padre')
        #titles_list.append('Profesión del Padre')
        #titles_list.append('Tamaño Municipio de Inscripción')
        #titles_list.append('Tamaño Municipio de Nacimiento de la Madre')
        #titles_list.append('Tamaño Municipio de Nacimiento del Padre')
        #titles_list.append('Tamaño Municipio de Nacimiento del Hijo Anterior')
        #titles_list.append('Tamaño Municipio de Residencia de la Madre')
        #titles_list.append('Tamaño Municipio de Residencia del Padre')
        #titles_list.append('Tamaño País de Nacimiento de la Madre')
        #titles_list.append('Tamaño País de Nacimiento del Padre')
        #titles_list.append('Tamaño País de Nacimiento del Hijo Anterior')
        #titles_list.append('Tamaño País de Residencia de la Madre')
        #titles_list.append('Tamaño País de Residencia del Padre')
        #titles_list.append('Tamaño País de Nacionalidad de la Madre')
        #titles_list.append('Tamaño País de Nacionalidad del Padre')
        #titles_list.append('Tamaño País de Nacionalidad del Hijo Anterior')
        #titles_list.append('Tamaño País de Nacionalidad del Nacido')
        titles_list.append('Edad de la Madre en Años Cumplidos')
        #titles_list.append('Edad de la Madre al Contraer Matrimonio en Años Cumplidos')
        #titles_list.append('Edad de la Madre al Inicio de la Relación Estable en Años Cumplidos')
        #titles_list.append('Años de Casada')
        #titles_list.append('Años de Relación Estable')
        #titles_list.append('Intervalo Intergenésico en Meses')
        #titles_list.append('Edad del Padre en Años Cumplidos')
        #titles_list.append('Indicador Nacionalidad Española del Nacido')
        #titles_list.append('Indicador Nacionalidad Extranjera del Nacido')
        #titles_list.append('País de Nacionalidad del Nacido')
        titles_list.append('Sexo del Nacido')
        titles_list.append('Peso del Nacido')
        #titles_list.append('Indicador de si el Nacido Vivió Más de 24 Horas')
        #titles_list.append('Indicador de si el Nacido Nació Vivo o Muerto')
        #titles_list.append('Indicador de si se Practicó Autopsia al Nacido')
        #titles_list.append('Indicador de si el Nacido Murió Antes o Durante el Trabajo del Parto')
        #titles_list.append('Primer Dígito del Código de Causa de Muerte del Nacido')
        #titles_list.append('Segundo + Tercer Dígito del Código de Causa de Muerte del Nacido')
        #titles_list.append('Cuarto Dígito del Código de Causa de Muerte del Nacido')
        #titles_list.append('Clasificación del Nacido')
        #titles_list.append('Orden del Nacimiento del Nacido Vivo')
        titles_list.append('Número de Hijos Nacidos Vivos Totales a lo Largo de su Vida')
        #titles_list.append('Tamaño Municipio Parto')

        # DELETE
        csv_writer_users.writerow(titles_list)
        
        line_counter = 0
        
        for line in csv_reader:
            line_counter += 1
            
            # First line only contains header descriptor
            if line_counter == 1:
                continue
            
            csv_line = []
            
            # Extract fields' values
            proi = line[0][0:2]
            #csv_line.append(proi)
            #print('Provincia de Inscripción: ' + proi)
            muni = line[0][2:5]
            #csv_line.append(muni)
            #print('Municipio de Inscripción: ' + muni)
            mespar = line[0][5:7]
            csv_line.append(mespar)
            #print('Mes del Parto: ' + mespar)
            anopar = line[0][7:11]
            csv_line.append(anopar)
            #print('Año del Parto: ' + anopar)
            propar = line[0][11:13]
            #csv_line.append(propar)
            #print('Provincia del Parto: ' + propar)
            munpar = line[0][13:16]
            #csv_line.append(munpar)
            #print('Municipio del Parto: ' + munpar)
            lugarpa = line[0][16:17]
            csv_line.append(prettify_lugarpa(lugarpa))
            #print('Lugar del Parto: ' + lugarpa)
            asistido = line[0][17:18]
            csv_line.append(prettify_asistido(asistido))
            #print('Parto Asistido: ' + asistido)
            multipli = line[0][18:19]
            #csv_line.append(multipli)
            #print('Número de Nacidos con o sin vida: ' + multipli)
            norma = line[0][19:20]
            csv_line.append(prettify_norma(norma))
            #print('Parto Normal o con Complicaciones: ' + norma)            
            cesarea = line[0][20:21]
            csv_line.append(prettify_cesarea(cesarea))
            #print('Parto con o sin Cesárea: ' + cesarea)
            intersem = line[0][21:22]
            csv_line.append(prettify_intersem(intersem))
            #print('A Término o Prematuro: ' + intersem)
            semanas = line[0][22:24]
            csv_line.append(semanas)
            #print('Número de Semanas del Embarazo: ' + semanas)
            mesnacm = line[0][24:26]
            #csv_line.append(mesnacm)
            #print('Mes de Nacimiento de la Madre: ' + mesnacm)
            anonacm = line[0][26:30]
            #csv_line.append(anonacm)
            #print('Año de Nacimiento de la Madre: ' + anonacm)
            nacioem = line[0][30:31]
            #csv_line.append(nacioem)
            #print('Indicador Nacionalidad Española de la Madre: ' + nacioem)
            nacioxm = line[0][31:32]
            #csv_line.append(nacioxm)
            #print('Indicador Nacionalidad Extranjera de la Madre: ' + nacioxm)
            paisnacm = line[0][32:35]
            #csv_line.append(paisnacm)
            #print('País Nacionalidad Madre: ' + paisnacm)
            cuannacm = line[0][35:36]
            #csv_line.append(cuannacm)
            #print('Cuándo Adquiere la Nacionalidad la Madre: ' + cuannacm)
            proma = line[0][36:38]
            #csv_line.append(proma)
            #print('Provincia de Nacimiento de la Madre: ' + proma)
            munma = line[0][38:41]
            #csv_line.append(munma)
            #print('Municipio de Nacimiento de la Madre: ' + munma)
            paisnxm = line[0][41:44]
            #csv_line.append(paisnxm)
            #print('País de Nacimiento en el Extranjero de la Madre: ' + paisnxm)
            prorem = line[0][44:46]
            #csv_line.append(prorem)
            #print('Provincia de Residencia de la Madre: ' + prorem)
            munrem = line[0][46:49]
            #csv_line.append(munrem)
            #print('Municipio de Residencia de la Madre: ' + munrem)
            paisrxm = line[0][49:52]
            #csv_line.append(paisrxm)
            #print('País de Residencia en el Extranjero de la Madre: ' + paisrxm)
            estudiom = line[0][52:54]
            #csv_line.append(estudiom)
            #print('Nivel de Estudios de la Madre: ' + estudiom)
            cautom = line[0][54:56]
            #csv_line.append(cautom)
            #print('Profesión Madre de la Madre: ' + cautom)
            ecivm = line[0][56:57]
            #csv_line.append(ecivm)
            #print('Estado Civil de la Madre: ' + ecivm)
            caspnm = line[0][57:58]
            #csv_line.append(caspnm)
            #print('Indicador de si es Primer Matrimonio de la Madre: ' + caspnm)
            mesmat = line[0][58:60]
            #csv_line.append(mesmat)
            #print('Mes del Actual Matrimonio: ' + mesmat)
            anomat = line[0][60:64]
            #csv_line.append(anomat)
            #print('Año del Actual Matrimonio: ' + anomat)
            phecho = line[0][64:65]
            #csv_line.append(phecho)
            #print('Indicador de si la Madre Tiene Pareja de Hecho: ' + phecho)
            estable1 = line[0][65:66]
            #csv_line.append(estable1)
            #print('Indicador de si es la Primera Unión Estable de la Madre: ' + estable1)
            mesest1 = line[0][66:68]
            #csv_line.append(mesest1)
            #print('Mes de Inicio de la Actual Unión Estable de la Madre: ' + mesest1)
            anoest1 = line[0][68:72]
            #csv_line.append(anoest1)
            #print('Año de Inicio de la Actual Unión Estable de la Madre: ' + anoest1)
            numh = line[0][72:74]
            #csv_line.append(numh)
            #print('Número de Hijos Contando este Parto (Vivos y Muertos): ' + numh)
            numhv = line[0][74:76]
            #csv_line.append(numhv)
            #print('Número de Hijos Nacidos Vivos en Partos Anteriores: ' + numhv)
            meshan = line[0][76:78]
            #csv_line.append(meshan)
            #print('Mes de Nacimiento del Hijo Anterior: ' + meshan)
            anohan = line[0][78:82]
            #csv_line.append(anohan)
            #print('Año de Nacimiento del Hijo Anterior: ' + anohan)
            prohante = line[0][82:84]
            #csv_line.append(prohante)
            #print('Provincia de Nacimiento del Hijo Anterior: ' + prohante)
            munhante = line[0][84:87]
            #csv_line.append(munhante)
            #print('Municipio de Nacimiento del Hijo Anterior: ' + munhante)
            paishantx = line[0][87:90]
            #csv_line.append(paishantx)
            #print('País de Nacimiento en el Extranjero del Hijo Anterior: ' + paishantx)
            nacioeha = line[0][90:91]
            #csv_line.append(nacioeha)
            #print('Indicador Nacionalidad Española del Hijo Anterior: ' + nacioeha)
            nacioxha = line[0][91:92]
            #csv_line.append(nacioxha)
            #print('Indicador Nacionalidad Extranjera del Hijo Anterior: ' + nacioxha)
            paisnaha = line[0][92:95]
            #csv_line.append(paisnaha)
            #print('País Nacionalidad del Hijo Anterior: ' + paisnaha)
            mesnacp = line[0][95:97]
            #csv_line.append(mesnacp)
            #print('Mes de Nacimiento del Padre: ' + mesnacp)
            anonacp = line[0][97:101]
            #csv_line.append(anonacp)
            #print('Año de Nacimiento del Padre: ' + anonacp)
            nacioep = line[0][101:102]
            #csv_line.append(nacioep)
            #print('Indicador Nacionalidad Española del Padre: ' + nacioep)
            nacioxp = line[0][102:103]
            #csv_line.append(nacioxp)
            #print('Indicador Nacionalidad Extranjera del Padre: ' + nacioxp)
            paisnacp = line[0][103:106]
            #csv_line.append(paisnacp)
            #print('País de Nacionalidad del Padre: ' + paisnacp)
            cuannacp = line[0][106:107]
            #csv_line.append(cuannacp)
            #print('Cuándo Adquiere la Nacionalidad el Padre: ' + cuannacp)
            propa = line[0][107:109]
            #csv_line.append(propa)
            #print('Provincia de Nacimiento del Padre: ' + propa)
            munpa = line[0][109:112]
            #csv_line.append(munpa)
            #print('Municipio de Nacimiento del Padre: ' + munpa)
            paisnxp = line[0][112:115]
            #csv_line.append(paisnxp)
            #print('País de Nacimiento en el Extranjero del Padre: ' + paisnxp)
            dondep = line[0][115:116]
            #csv_line.append(dondep)
            #print('Dónde Reside el Padre: ' + dondep)
            prorep = line[0][116:118]
            #csv_line.append(prorep)
            #print('Provincia de Residencia del Padre: ' + prorep)
            munrep = line[0][118:121]
            #csv_line.append(munrep)
            #print('Municipio de Residencia del Padre: ' + munrep)
            paisrxp = line[0][121:124]
            #csv_line.append(paisrxp)
            #print('País de Residencia en el Extranjero del Padre: ' + paisrxp)
            estudiop = line[0][124:126]
            #csv_line.append(estudiop)
            #print('Nivel de Estudios del Padre: ' + estudiop)
            cautop = line[0][126:128]
            #csv_line.append(cautop)
            #print('Profesión del Padre: ' + cautop)
            tmunin = line[0][128:129]
            #csv_line.append(tmunin)
            #print('Tamaño Municipio de Inscripción: ' + tmunin)
            tmunnm = line[0][129:130]
            #csv_line.append(tmunnm)
            #print('Tamaño Municipio de Nacimiento de la Madre: ' + tmunnm)
            tmunnp = line[0][130:131]
            #csv_line.append(tmunnp)
            #print('Tamaño Municipio de Nacimiento del Padre: ' + tmunnp)
            tmunnha = line[0][131:132]
            #csv_line.append(tmunnha)
            #print('Tamaño Municipio de Nacimiento del Hijo Anterior: ' + tmunnha)
            tmunrm = line[0][132:133]
            #csv_line.append(tmunrm)
            #print('Tamaño Municipio de Residencia de la Madre: ' + tmunrm)
            tmunrp = line[0][133:134]
            #csv_line.append(tmunrp)
            #print('Tamaño Municipio de Residencia del Padre: ' + tmunrp)
            tpaisnacimientomadre = line[0][134:135]
            #csv_line.append(tpaisnacimientomadre)
            #print('Tamaño País de Nacimiento de la Madre: ' + tpaisnacimientomadre)
            tpaisnacimientopadre = line[0][135:136]
            #csv_line.append(tpaisnacimientopadre)
            #print('Tamaño País de Nacimiento del Padre: ' + tpaisnacimientopadre)
            tpaisnacimientohijoante = line[0][136:137]
            #csv_line.append(tpaisnacimientohijoante)
            #print('Tamaño País de Nacimiento del Hijo Anterior: ' + tpaisnacimientohijoante)
            tpaisrmadre = line[0][137:138]
            #csv_line.append(tpaisrmadre)
            #print('Tamaño País de Residencia de la Madre: ' + tpaisrmadre)
            tpaisrpadre = line[0][138:139]
            #csv_line.append(tpaisrpadre)
            #print('Tamaño País de Residencia del Padre: ' + tpaisrpadre)
            tpaisnacionalidadmadre = line[0][139:140]
            #csv_line.append(tpaisnacionalidadmadre)
            #print('Tamaño País de Nacionalidad de la Madre: ' + tpaisnacionalidadmadre)
            tpaisnacionalidadpadre = line[0][140:141]
            #csv_line.append(tpaisnacionalidadpadre)
            #print('Tamaño País de Nacionalidad del Padre: ' + tpaisnacionalidadpadre)
            tpaisnacionalidadhijoant = line[0][141:142]
            #csv_line.append(tpaisnacionalidadhijoant)
            #print('Tamaño País de Nacionalidad del Hijo Anterior: ' + tpaisnacionalidadhijoant)
            tpaisnacionalidadnacido = line[0][142:143]
            #csv_line.append(tpaisnacionalidadnacido)
            #print('Tamaño País de Nacionalidad del Nacido: ' + tpaisnacionalidadnacido)
            edadm = line[0][143:145]
            csv_line.append(edadm)
            #print('Edad de la Madre en Años Cumplidos: ' + edadm)
            edadmm = line[0][145:147]
            #csv_line.append(edadmm)
            #print('Edad de la Madre al Contraer Matrimonio en Años Cumplidos: ' + edadmm)
            edadmrel = line[0][147:149]
            #csv_line.append(edadmrel)
            #print('Edad de la Madre al Inicio de la Relación Estable en Años Cumplidos: ' + edadmrel)
            anoca = line[0][149:151]
            #csv_line.append(anoca)
            #print('Años de Casada: ' + anoca)
            anorel = line[0][151:153]
            #csv_line.append(anorel)
            #print('Años de Relación Estable: ' + anorel)
            iniha = line[0][153:156]
            #csv_line.append(iniha)
            #print('Intervalo Intergenésico en Meses: ' + iniha)
            # Campo a blanco: line[0][156:159]
            edadp = line[0][159:161]
            #csv_line.append(edadp)
            #print('Edad del Padre en Años Cumplidos: ' + edadp)
            nacioen = line[0][161:162]
            #csv_line.append(nacioen)
            #print('Indicador Nacionalidad Española del Nacido: ' + nacioen)
            nacioxn = line[0][162:163]
            #csv_line.append(nacioxn)
            #print('Indicador Nacionalidad Extranjera del Nacido: ' + nacioxn)
            paisnacn = line[0][163:166]
            #csv_line.append(paisnacn)
            #print('País de Nacionalidad del Nacido: ' + paisnacn)
            sexo = line[0][166:167]
            csv_line.append(prettify_sexo(sexo))
            #print('Sexo del Nacido: ' + sexo)
            peson = line[0][167:171]
            csv_line.append(prettify_peson(peson))
            #print('Peso del Nacido: ' + peson)
            v24hn = line[0][171:172]
            #csv_line.append(v24hn)
            #print('Indicador de si el Nacido Vivió Más de 24 Horas: ' + v24hn)
            nacvn = line[0][172:173]
            #csv_line.append(nacvn)
            #print('Indicador de si el Nacido Nació Vivo o Muerto: ' + nacvn)
            autopsn = line[0][173:174]
            #csv_line.append(autopsn)
            #print('Indicador de si se Practicó Autopsia al Nacido: ' + autopsn)
            muern = line[0][174:175]
            #csv_line.append(muern)
            #print('Indicador de si el Nacido Murió Antes o Durante el Trabajo del Parto: ' + muern)
            codca1n = line[0][175:176]
            #csv_line.append(codca1n)
            #print('Primer Dígito del Código de Causa de Muerte del Nacido: ' + codca1n)
            codca2n = line[0][176:178]
            #csv_line.append(codca2n)
            #print('Segundo + Tercer Dígito del Código de Causa de Muerte del Nacido: ' + codca2n)
            codca4n = line[0][178:179]
            #csv_line.append(codca4n)
            #print('Cuarto Dígito del Código de Causa de Muerte del Nacido: ' + codca4n)
            clasif = line[0][179:180]
            #csv_line.append(clasif)
            #print('Clasificación del Nacido: ' + clasif)
            sordenv = line[0][180:182]
            #csv_line.append(sordenv)
            #print('Orden del Nacimiento del Nacido Vivo: ' + sordenv)
            numhvt = line[0][182:184]
            csv_line.append(numhvt)
            #print('Número de Hijos Nacidos Vivos Totales a lo Largo de su Vida: ' + numhvt)
            tmunpar = line[0][184:185]
            #csv_line.append(tmunpar)
            #print('Tamaño Municipio Parto: ' + tmunpar)
            # Campo a blanco: line[0][185:202]
            
            line_valid = line_is_valid(proi, muni, propar, munpar, nacioem, paisnacm, cuannacm,
                  proma, munma, prorem, munrem, peson, clasif)
            
            if not line_valid:
                print('Line {} is invalid... Skipping to next line'.format(line_counter))
                continue
            
            
            csv_writer_users.writerow(csv_line)
        
        # Write and Persist the line to the file
        processed.flush()