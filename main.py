import time

import data
import helpers

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pages
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = Chrome(options=options)
        cls.driver.implicitly_wait(5)
        # Necessário para helpers.retrieve_phone_code conseguir ler as
        # respostas de rede via performance log (CDP).
        cls.driver.execute_cdp_cmd("Network.enable", {})
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print('Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.')

    def  setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        self.page = UrbanRoutesPage(self.driver)

        self.page.enter_location(data.ADDRESS_FROM, data.ADDRESS_TO)

    def _start_confort_flow(self):
        # Endereço já foi preenchido em setup_method; chamar enter_location
        # de novo aqui duplicava o texto (o .clear() não é confiável nesse
        # campo controlado por React, então o texto se acumulava).
        self.page.click_taxi_option()
        self.page.click_comfort_icon()

    def test_set_route(self):
       assert UrbanRoutesPage.get_from_location(self.page) == data.ADDRESS_FROM
       assert UrbanRoutesPage.get_to_location (self.page) == data.ADDRESS_TO

       #time.sleep(10)

    def test_select_plan(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()
        assert self.page.click_comfort_active()

    def test_fill_phone_number(self):
        self._start_confort_flow()
        self.page.set_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        self.page.set_phone_code(code)
        # O app não aceita o número com espaços, então ele é digitado sem
        # espaços — por isso a comparação também remove os espaços.
        assert self.page.get_phone_number() == data.PHONE_NUMBER.replace(' ', '')

    def test_fill_card(self):
        self._start_confort_flow()
        self.page.set_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.page.is_card_active()

    def test_comment_for_driver(self):
        self._start_confort_flow()
        self.page.set_driver_comment(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_driver_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self._start_confort_flow()
        self.page.open_order_requirements()
        assert not self.page.is_blanket_and_handkerchiefs_selected()
        self.page.toggle_blanket_and_handkerchiefs()
        assert self.page.is_blanket_and_handkerchiefs_selected()

    def test_order_2_ice_creams(self):
        self._start_confort_flow()
        self.page.open_order_requirements()
        number_of_ice_creams = 2
        for count in range(number_of_ice_creams):
            self.page.click_ice_cream_plus()
        assert self.page.get_ice_cream_count() == number_of_ice_creams

    def test_car_search_model_appears(self):
        self._start_confort_flow()
        self.page.set_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        self.page.set_phone_code(code)
        self.page.set_card(data.CARD_NUMBER, data.CARD_CODE)
        self.page.click_order_button()
        assert self.page.is_car_search_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
