class Question:
    def __init__(self, userUUID, formUUID, selfUUID, questionTitle, isRequired):
        self.userUUID = userUUID
        self.formUUID = formUUID
        self.selfUUID = selfUUID
        self.questionTitle = questionTitle
        self.isRequired = isRequired
        
        
class LongFormQuestion(Question):
    def __init__(self, userUUID, formUUID, selfUUID, questionTitle, isRequired, placeholderText):
        super().__init__(userUUID, formUUID, selfUUID, questionTitle, isRequired)
        self.placeholderText = placeholderText

class MultiChoiceQuestion(Question):
    def __init__(self, userUUID, formUUID, selfUUID, questionTitle, isRequired, optionsList):
        super().__init__(userUUID, formUUID, selfUUID, questionTitle, isRequired)
        self.optionsList = optionsList