import re
from xml.etree import ElementTree as et

from flask import jsonify
from dictionary import company
from dictionary import date as new_dates
from dictionary import services  as object_service
from xml.dom import minidom

class load_XML:

    def __init__(self):
        self.correct_text = spelling()
        pass
    
    def element_tree(self, text, object_list: list):
        positive_words = []
        negative_words = []
        company_name = []
        services = []
        messages = []
        lexic = lexical()
        dictionary_services = {}

        

        root = et.XML(text)

        for element in root:
            if self.correct_text.correct_case(element.tag) == 'diccionario':
                for subelement in element:
                    for subelement2 in subelement:
                        if self.correct_text.correct_case(subelement.tag) =='sentimientos_positivos':
                            positive_words.append(subelement2.text)
                        if self.correct_text.correct_case(subelement.tag) =='sentimientos_negativos':
                            negative_words.append(subelement2.text)
                        if self.correct_text.correct_case(subelement.tag) =='empresas_analizar':
                            for subelement3 in subelement2:
                                if self.correct_text.correct_case(subelement3.tag) == 'nombre':
                                    company_name.append(subelement3.text)
                                if self.correct_text.correct_case(subelement3.tag) == 'servicio':
                                    for subelement_attrib in subelement3.attrib:
                                        if self.correct_text.correct_case(subelement_attrib) == 'nombre':
                                            services = []
                                            services.append(subelement3.attrib[subelement_attrib]) 
                                        for subelement4 in subelement3:
                                            if self.correct_text.correct_case(subelement4.tag) == 'alias':
                                                print(subelement3.attrib[subelement_attrib])
                                                print(subelement4.text)
                                                services.append(subelement4.text)
                                        dictionary_services[subelement3.attrib[subelement_attrib]] = services
                
                if len(company_name) != 0:
                    for list_element in company_name:
                        object_list.append(company(list_element, positive_words, negative_words, dictionary_services))
                else:
                    object_list.append(company('No name', positive_words, negative_words, dictionary_services))

            elif self.correct_text.correct_case(element.tag)  == 'lista_mensajes':
                for subelement in element:
                    messages.append(lexic.lexical(subelement.text))
        
        for element in object_list:
            new_list = []

            for message_element in messages:
                match = re.search(self.correct_text.correct_case(element.get_name().replace(' ','')),self.correct_text.correct_case(message_element[5]), re.IGNORECASE)

                if match != None:
                    new_list.append(message_element)
            element.set_messages(new_list)
            
        for element in object_list:
            for message_element in element.get_messages():   
                lexic.positive_counter(element, message_element[5])
        
        var = lexic.xml_generator(object_list)
        print(str(lexic.prettify(var)))
        
        return jsonify(str(lexic.prettify(var)))
    
   



class spelling:
    def __init__(self):
        pass

    def correct_case(self, text: str):
        text = text.lower()

        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            text = text.replace(a, b).replace(a.upper(), b.upper())
        return text

class lexical:

    def __init__(self):
        pass

    def lexical(self, normal_text):
        
        text_message = normal_text
        return_list = []

        #Part 1: Place, date, time
        try:
            match = re.search(r'\s*lugar\s*y\s*fecha\s*:\s*([A-Za-z]|\s*)*,\s*(\d{2}\/\d{2}\/\d{4})\s*(\d{2}:\d{2})', text_message, re.IGNORECASE)
        except TypeError:
            print('No match was found')

        search_place = ''
        for i in range(match.start(), match.end()):
            search_place += text_message[i]

        try:
            match_place = re.search(r':\s*([A-Za-z]|\s)*\s*,',  search_place, re.IGNORECASE)
        except TypeError:
            print('No match was found')

        print(match_place.start(), match_place.end())
        search_place2 = ''
        for index in range(match_place.start(), match_place.end()):
            if search_place[index] != ':':
                if search_place[index] != ',':
                    search_place2 += search_place[index]
                else: break 

        return_list.append(search_place2)

        try:
            match = re.search(r'\d{2}/\d{2}/\d{4}', text_message, re.IGNORECASE)
        except TypeError:
            print('No match was found')

        search_date = ''
        for i in range(match.start(), match.end()):
                search_date += text_message[i]

        return_list.append(search_date)

        try:
            match = re.search(r'(\d{2}:\d{2})', text_message)
        except TypeError:
            print('No match was found')

        search_hour = ''
        for i in range(match.start(), match.end()):
                search_hour += text_message[i]

        return_list.append(search_hour)

        #Part 1 END: Place, date, time

        #Part 2: User
        try:
            match = re.search(r'usuario\s*:\s*\S*', text_message, re.IGNORECASE)
        except TypeError:
            print('No match was found')

        search_user = ''
        for i in range(match.start(), match.end()):
            search_user += text_message[i]

        search_user2 = ''

        try:
            match = re.search(r':', search_user, re.IGNORECASE)
        except TypeError:
            print('No match was found')

        print(match.start())

        for i in range(match.start(), len(search_user)):
            if search_user[i] != ' ' and search_user[i] != ':':
                search_user2 += search_user[i]

        return_list.append(search_user2)
        #Part 2 END: User 

        #Part 3: Social Media
        try:
            match = re.search(r'red social\s*:\s*\S*', text_message, re.IGNORECASE)
        except TypeError:
            print('No match was found')

        search_social_media = ''
        for i in range(match.start(), match.end()):
            search_social_media += text_message[i]

        search_social_media2 = ''

        try:
            match = re.search(r':', search_social_media, re.IGNORECASE)
        except TypeError:
            print('No match was found')


        for i in range(match.start(), len(search_social_media)):
            if search_social_media[i] != ' ' and search_social_media[i] != ':':
                search_social_media2 += search_social_media[i]

        return_list.append(search_social_media2)
        #Part 3 END: Social Media
        
        #Part 4: Message
        message = ''
        try:
            match = re.search(r'red social\s*:\s*\S*', text_message, re.IGNORECASE)
        except TypeError:
            print('No match was found')

        for i in range(match.end(), len(text_message)):
            message += text_message[i]
        
        return_list.append(message)
        #Part 4 END: Message

        return return_list
    
    def positive_counter(self, element, message):
        correct_text = spelling()

        positive = 0
        for positive_words in element.get_positive_words():
            print(message)
            match = re.search(correct_text.correct_case(str(positive_words).replace(' ','')),correct_text.correct_case(message), re.IGNORECASE)
            if match != None:
                positive += 1

        negative = 0
        for negative_words in element.get_negative_words():
            match = re.search(correct_text.correct_case(str(negative_words).replace(' ','')),correct_text.correct_case(message), re.IGNORECASE)

            if match != None:
                negative += 1

        if positive > negative:
            print('Is a positive message')
            element.set_positive()
        elif positive < negative:
            print('Is a negative message')
            element.set_negative()
        else:
            print('Is a neutral message')
            element.set_neutral()

    def dict_counter(self, element, message):
        correct_text = spelling()
        list = []
        message_counter = 0

        for dict_element in element:
            print(dict_element)
            var = dict_element
            match = re.search(correct_text.correct_case(str(var).replace(' ','')),correct_text.correct_case(str(message)), re.IGNORECASE)
            if match != None:
                print('no encontre')
            else:
                message_counter += 1

        if message_counter == 0:
            return False
        else:
            return True
    
    def dict_finder(self, element, lista):
        correct_text = spelling()
        message_counter = 0
        for dict_element in lista:
            for  element2 in dict_element.get_services():
                if element in element2:
                    return False
        return True



    def xml_generator(self, list):

        #Date
        date_list = []
        date_quan = 0
         
        for list_element in list:
            for date in list_element.get_messages():
                if len(date_list) == 0:
                    
                    date_list.append(new_dates(date[1]))
                    date_list[0].set_message(date[5])
                    date_list[0].set_positive_words(list_element.get_positive_words())
                    date_list[0].set_negative_words(list_element.get_negative_words())
                else:
                    counter = 0
                    for i in date_list:
                        if i.get_date() == date[1]:
                            i.set_quantity()
                            i.set_message(date[5])
                            i.set_positive_words(list_element.get_positive_words())
                            i.set_negative_words(list_element.get_negative_words())
                            counter += 1

                    if counter == 0:
                        date_list.append(new_dates(date[1]))
                        for i in date_list:
                            i.set_message(date[5])
                            i.set_positive_words(list_element.get_positive_words())
                            i.set_negative_words(list_element.get_negative_words())
                    

        for i in date_list:
            print(i.get_date())
            for j in i.get_message():
                self.positive_counter(i, j)
        
        #Date END

        
        #Services list
        '''
        service_list = []
        service_quan = 0
        message_list = []
        
        for service_element in list:
            for services in service_element.get_services():
                if len(service_list) == 0:
                    service_list.append(object_service(list_element.get_services()[services]))
                    service_list[0].set_positive_words(list_element.get_positive_words())
                    service_list[0].set_negative_words(list_element.get_negative_words())
                    for word in list:
                        for word2 in word.get_messages():
                            if self.dict_counter(service_list[len(service_list)-1].get_services(), word2[5]):
                                print('pase', word2[5])
                                service_list[0].set_message(word2[5])

                elif len(service_list) > 0:
                    counter = 0
                    for i in list_element.get_services()[services]:
                        if self.dict_finder(i, service_list):
                            counter += 1
                        else:
                            continue
                    if counter != 0:
                        service_list.append(object_service(list_element.get_services()[services]))
                        service_list[len(service_list)-1].set_positive_words(list_element.get_positive_words())
                        service_list[len(service_list)-1].set_negative_words(list_element.get_negative_words())
                        print(len(service_list))
                        for word in list:
                            for word2 in word.get_messages():
                                if self.dict_counter(service_list[len(service_list)-1].get_services(), word2[5]):
                                    print('pase', word2[5])
                                    service_list[len(service_list)-1].set_message(word2[5])
            
        for i in service_list:
            print(i.get_message())




        #Services list end
        
        '''

        service_list = []
        service_quan = 0
        message_list = []
        
        for servicio in list:
            print(servicio)
            for servicio2 in servicio.get_services():
                service_list.append(object_service(servicio.get_services()[servicio2]))
                message_list = []
                for messages2 in servicio.get_messages():
                    if self.dict_counter(servicio.get_services()[servicio2], messages2):
                        print('si existe esa palabra')
                        service_list[len(service_list)-1].set_message(messages2[5])
                for prueba in service_list[len(service_list)-1].get_message():
                    self.positive_counter(servicio, prueba)
                        
        root = et.Element('root')
        response_list = et.SubElement(root, 'lista_respuestas')
        response = et.SubElement(response_list, 'respuesta')
        for date in date_list:
            et.SubElement(response, 'fecha').text = date.get_date()
            messages = et.SubElement(response, 'mensajes')
            et.SubElement(messages, 'total').text = str(len(date.get_message()))
            et.SubElement(messages, 'positivos').text = str(date.get_positive())
            et.SubElement(messages, 'negativos').text = str(date.get_negative())
            et.SubElement(messages, 'neutros').text = str(date.get_neutral())

        for empresa in list:
            empresas = et.SubElement(response, 'empresa', nombre = empresa.get_name())
            messages = et.SubElement(empresas, 'mensajes')
            et.SubElement(messages, 'total').text = str(len(empresa.get_messages()))
            et.SubElement(messages, 'positivos').text = str(empresa.get_positive())
            et.SubElement(messages, 'negativos').text = str(empresa.get_negative())
            et.SubElement(messages, 'neutros').text = str(empresa.get_neutral())

    
            servicios = et.SubElement(empresas, 'servicios')
            for service in empresa.get_services():
                et.SubElement(servicios, 'servicio', nombre = str(service))
        

    

        archivo = et.ElementTree(root)
        archivo.write('Ejemplo.xml')
        print (self.prettify(root))
        
        f = open("Ejemplo.xml", "r")
        hola = f.read()
        f.close()

        return root


    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
    """
        rough_string = et.tostring(elem, 'utf-8').decode('utf8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")



            
        
            


    
    