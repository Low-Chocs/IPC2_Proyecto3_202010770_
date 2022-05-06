from flask import jsonify


class company:
    def __init__(self, name: str, positive_words: list, negative_words: list, services:list):
        self.name = name
        self.positive_words = positive_words
        self.negative_words = negative_words
        self.services = services
        self.messages = []
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.message = []
        self.alias = []

    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

    def get_positive_words(self):
        return self.positive_words
    
    def set_positive_words(self, positive_words):
        self.positive_words = positive_words

    def get_negative_words(self):
        return self.negative_words
    
    def set_negative_words(self, negative_words):
        self.negative_words = negative_words

    def get_services(self):
        return self.services
    
    def set_services(self, services):
        self.services = services

    def get_messages(self):
        return self.messages
    
    def set_messages(self, messages):
        self.messages = messages

    def get_message(self):
        return self.message
    
    def set_message(self, message):
        self.message = message

    def get_positive(self):
        return self.positive
    
    def get_negative(self):
        return self.negative

    def set_positive(self):
        self.positive += 1

    def set_negative(self):
        self.negative += 1
    
    def get_neutral(self):
        return self.neutral

    def set_neutral(self):
        self.neutral += 1

class date:

    def __init__(self, date):
        self.date = date
        self.quantity = 1
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.message = []
        self.positive_words = []
        self.negative_words = []

    def set_quantity(self):
        self.quantity += 1
    
    def get_quantity(self):
        return self.quantity 
    
    def get_date(self):
        return self.date

    def get_positive(self):
        return self.positive
    
    def get_negative(self):
        return self.negative

    def set_positive(self):
        self.positive += 1

    def set_negative(self):
        self.negative += 1

    def get_message(self):
        return self.message 

    def set_message(self, element):
        self.message.append(element)

    def get_positive_words(self):
        return self.positive_words
    
    def get_negative_words(self):
        return self.negative_words

    def set_positive_words(self, list):
        if len(self.positive_words) == 0:
            for i in list:
                self.positive_words.append(i)
        else:
            for i in list:
                counter = 0
                for j in self.positive_words:
                    if i == j:
                        counter += 1
                if counter >= 1:
                    self.positive_words.append(i)

    def set_negative_words(self, list):
        if len(self.negative_words) == 0:
            for i in list:
                self.negative_words.append(i)
        else:
            for i in list:
                counter = 0
                for j in self.negative_words:
                    if i == j:
                        counter += 1
                if counter > 0:
                    self.negative_words.append(i)

    def get_neutral(self):
        return self.neutral

    def set_neutral(self):
        self.neutral += 1

class services:
    
    def __init__(self, service):
        self.service = service
        self.quantity = 0
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.message = []
        self.positive_words = []
        self.negative_words = []

    def set_quantity(self):
        self.quantity += 1
    
    def get_quantity(self):
        return self.quantity 
    
    def get_services(self):
        return self.service

    def get_positive(self):
        return self.positive
    
    def get_negative(self):
        return self.negative

    def set_positive(self):
        self.positive += 1

    def set_negative(self):
        self.negative += 1

    def get_message(self):
        return self.message 

    def set_message(self, element):
        self.message.append(element)

    def get_positive_words(self):
        return self.positive_words
    
    def get_negative_words(self):
        return self.negative_words

    def set_positive_words(self, list):
        if len(self.positive_words) == 0:
            for i in list:
                self.positive_words.append(i)
        else:
            for i in list:
                counter = 0
                for j in self.positive_words:
                    if i == j:
                        counter += 1
                if counter >= 1:
                    self.positive_words.append(i)

    def set_negative_words(self, list):
        if len(self.negative_words) == 0:
            for i in list:
                self.negative_words.append(i)
        else:
            for i in list:
                counter = 0
                for j in self.negative_words:
                    if i == j:
                        counter += 1
                if counter > 0:
                    self.negative_words.append(i)

    def get_neutral(self):
        return self.neutral

    def set_neutral(self):
        self.neutral += 1

class getters:
    def __init__(self, object: list):
        self.object = object

    def json_generator_messages(self):
        json = []

        for i in self.object:
            for j in i.get_messages():
                mes = {
                    'Lugar': j[0],
                    'Fecha': j[1],
                    'Hora': j[2],
                    'Usuario': j[3],
                    'Red social': j[4],
                    'Mensaje': j[5]
                }
                json.append(mes)
        return jsonify(json)

    def json_generator_status_positive(self):
        json = []

        for i in self.object:
            for j in i.get_positive_words():
        
                mes = {
                    'Palabra Positiva': j
                }
                json.append(mes)
        return jsonify(json)

    def json_generator_status_negative(self):
        json = []

        for i in self.object:
            for j in i.get_negative_words():
        
                mes = {
                    'Palabra Negativa': j
                }
                json.append(mes)
        return jsonify(json)

    def json_generator_status_negative(self):
        json = []

        for i in self.object:
            for j in i.get_negative_words():
        
                mes = {
                    'Palabra Negativa': j
                }
                json.append(mes)
        return jsonify(json)
    
    def get_messages_company(self):
        json = []

        for i in self.object:
                mes = {
                    'Compañia': i.get_name(),
                    'Servicios': i.get_services()
                }
                json.append(mes)
        return jsonify(json)

