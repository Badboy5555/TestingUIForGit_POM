from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from locators.Locators import TextBoxPageLocators, RadioButtonPageLocators, WebrTablesLocators
from generator.generator import generate_data


class TextBoxPage(BasePage):
    locators = TextBoxPageLocators()

    def fill_input_form(self):
        person_data = next(generate_data())

        input_full_name = person_data.FULL_NAME
        input_email = person_data.EMAIL
        input_current_address = person_data.CURRENT_ADDRESS.replace('\n', ' ')
        input_permanent_address = person_data.PERMANENT_ADDRESS.replace('\n', ' ')

        self.element_is_visible(self.locators.INPUT_FULL_NAME).send_keys(input_full_name)
        self.element_is_visible(self.locators.INPUT_EMAIL).send_keys(input_email)
        self.element_is_visible(self.locators.INPUT_CURRENT_ADDRESS).send_keys(input_current_address)
        self.element_is_visible(self.locators.INPUT_PERMANENT_ADDRESS).send_keys(input_permanent_address)

        submit = self.element_is_clicable(self.locators.SUBMIT_BUTT)
        self.go_to_element(submit)
        submit.click()
        return input_full_name, input_email, input_current_address, input_permanent_address

    def get_output_form(self):
        output_full_name = self.element_is_present(self.locators.OUTPUT_FULL_NAME).text.split(':')[-1]
        output_email = self.element_is_present(self.locators.OUTPUT_EMAIL).text.split(':')[-1]
        output_current_address = self.element_is_present(self.locators.OUTPUT_CURRENT_ADDRESS).text.split(':')[-1]
        output_current_address.replace('\n', ' ')
        output_permanent_address = self.element_is_present(self.locators.OUTPUT_PERMANENT_ADDRESS).text.split(':')[-1]
        output_permanent_address.replace('\n', ' ')
        return output_full_name, output_email, output_current_address, output_permanent_address


class RadioButtonPage(BasePage):
    locators = RadioButtonPageLocators()

    def yes_button_click(self):
        self.element_is_present(self.locators.YES).click()

    def no_button_click(self):
        self.element_is_clicable(self.locators.NO).click()

    def impressinve_button_click(self):
        self.element_is_clicable(self.locators.IMPRESSIVE).click()

    def get_result_text(self):
        result_text = self.element_is_present(self.locators.TEXT_SUCCESS).text
        return result_text


class WebrTablesPage(BasePage):
    locators = WebrTablesLocators()

    def create_random_persons(self, how_much=2):
        """ Creates 'how_much' number of persons,
            returns [[...], [...]] of created persons"""
        persons_list = []
        while how_much != 0:
            self.element_is_clicable(self.locators.ADD_BUTT).click()

            person_data = next(generate_data())

            input_first_name = person_data.FIRST_NAME
            input_last_name = person_data.LAST_NAME
            input_email = person_data.EMAIL
            input_age = person_data.AGE
            input_salary = person_data.SALARY
            input_department = person_data.DEPARTMENT

            self.element_is_visible(self.locators.FIRST_NAME).send_keys(input_first_name)
            self.element_is_visible(self.locators.LAST_NAME).send_keys(input_last_name)
            self.element_is_visible(self.locators.EMAIL).send_keys(input_email)
            self.element_is_visible(self.locators.AGE).send_keys(input_age)
            self.element_is_visible(self.locators.SALARY).send_keys(input_salary)
            self.element_is_visible(self.locators.DEPARTMENT).send_keys(input_department)

            submit = self.element_is_clicable(self.locators.SUBMIT_BUTT)
            self.go_to_element(submit)
            submit.click()
            persons_list.append(
                [input_first_name, input_last_name, str(input_age), input_email, str(input_salary), input_department])
            how_much -= 1
        return persons_list

    def create_specified_persons(self, input_list: list[list[str]]):
        """ Creates 'how_much' numbenr of persons,
            returns [[...], [...]] of created persons
            first_name, last_name, email, age, salary, department
            """
        persons_list = []

        for i in input_list:
            self.element_is_clicable(self.locators.ADD_BUTT).click()

            input_first_name, input_last_name, input_email, input_age, input_salary, input_department = i

            self.element_is_visible(self.locators.FIRST_NAME).send_keys(input_first_name)
            self.element_is_visible(self.locators.LAST_NAME).send_keys(input_last_name)
            self.element_is_visible(self.locators.EMAIL).send_keys(input_email)
            self.element_is_visible(self.locators.AGE).send_keys(input_age)
            self.element_is_visible(self.locators.SALARY).send_keys(input_salary)
            self.element_is_visible(self.locators.DEPARTMENT).send_keys(input_department)
            submit = self.element_is_clicable(self.locators.SUBMIT_BUTT)
            self.go_to_element(submit)
            submit.click()
            persons_list.append(
                [input_first_name, input_last_name, str(input_age), input_email, str(input_salary), input_department])
        return persons_list

    def get_last_person(self):
        """ Returns [...] """
        last_person_row = self.elements_are_present(self.locators.PERSONS)[-1]
        all_data_of_current_person = last_person_row.find_elements(*self.locators.ALL_DATA_OF_CURRENT_PERSON)[:-1]
        output_first_name, output_last_name, output_age, output_email, output_salary, output_department = \
            [i.text for i in all_data_of_current_person]
        return [output_first_name, output_last_name, output_age, output_email, output_salary, output_department]

    def get_all_persons(self):
        """returns [[...], [...]]"""
        all_persons = self.elements_are_present(self.locators.PERSONS)
        output_persons = [[i.text for i in person.find_elements(*self.locators.ALL_DATA_OF_CURRENT_PERSON)[:-1]]
                for person in all_persons]
        return output_persons

    def search_by_any_key(self, query=2):
        self.element_is_clicable(self.locators.SEARCH_INPUT).send_keys(query)

    def edit_last_person_first_name(self, query):
        last_person_row = self.elements_are_present(self.locators.PERSONS)[-1]
        last_person_row.find_element(*self.locators.EDIT_BUTT).click()
        first_name_field = self.element_is_visible(self.locators.FIRST_NAME)

        first_name_field.clear()
        first_name_field.send_keys(str(query))
        self.element_is_clicable(self.locators.SUBMIT_BUTT).click()

    def delete_last_person(self):
        last_person_row = self.elements_are_present(self.locators.PERSONS)[-1]
        last_person_row.find_element(*self.locators.DELETE_BUTT).click()

    def switch_rows(self, rows_amount):
        elem = self.element_is_clicable(self.locators.ROWS_SELECTOR)
        self.go_to_element(elem)
        select_rows = Select(elem)
        select_rows.select_by_value(rows_amount)
        number_of_rows = len(self.elements_are_present(self.locators.ROWS_ON_PAGE))
        return number_of_rows
