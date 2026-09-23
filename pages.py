from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class UrbanRoutesPage:

        # Seção De e Para

        from_field = (By.ID, 'from')
        to_field = (By.ID, 'to')

        # Fluxo de chamada de taxi
        taxi_option = (By.XPATH, '//button[contains(text(),"Chamar")]')
        comfort_icon = (By.XPATH, '//img[contains(@src,"kids")]')
        comfort_active = (By.XPATH, '//div[contains(@class,"tcard") and contains(@class,"active")]')

        # Telefone
        phone_trigger = (By.CLASS_NAME, 'np-text')
        phone_input = (By.ID, 'phone')
        phone_next_button = (By.XPATH, '//button[text()="Próximo"]')
        phone_code_input = (By.ID, 'code')
        phone_confirm_button = (By.XPATH, '//button[text()="Confirmar"]')

        # Pagamento / cartão
        payment_trigger = (By.CLASS_NAME, 'pp-text')
        payment_value = (By.CLASS_NAME, 'pp-value-text')
        add_card_option = (By.XPATH, '//div[contains(@class,"pp-title") and contains(text(),"Adicionar cart")]')
        card_number_input = (By.XPATH, '//input[@id="number"]')
        card_code_input = (By.XPATH, '//input[contains(@class,"card-input") and @id="code"]')
        add_card_button = (By.XPATH, '//button[text()="Adicionar"]')
        payment_modal_close_button = (
            By.XPATH,
            '//div[@class="head" and contains(text(),"pagamento")]/parent::*//button[contains(@class,"close-button")]'
        )

        # Comentário para o motorista
        driver_comment_input = (By.ID, 'comment')

        # Requisitos do pedido
        blanket_container = (
            By.XPATH,
            '//div[contains(@class,"r-sw-container") and .//div[contains(@class,"r-sw-label") and contains(text(),"Cobertor")]]'
        )
        ice_cream_row = (
            By.XPATH,
            '//div[contains(@class,"r-counter-label") and text()="Sorvete"]/parent::div'
        )

        # Pedir / busca do carro
        order_button = (By.XPATH, '//button[contains(@class,"smart-button")]')
        car_search_indicator = (By.XPATH, '//div[contains(@class,"order-header-title") or contains(text(),"Buscar")]')

        def __init__(self, driver):
             self.driver = driver
             self.wait = WebDriverWait(driver, 10)

        # Métodos COR PON

        def _find(self, locator):
                return self.wait.until (EC.visibility_of_element_located(locator))

        def _click(self, locator):
                self.wait.until (EC.element_to_be_clickable(locator)).click()

        def _type(self, locator, text):
                element = self._find(locator)
                element.clear()
                element.send_keys(text)

        # Endereço

        def _get_text(self, locator):
                return self._find(locator).text

        def _get_value(self, locator):
                return self._find(locator).get_attribute('value')

        def enter_location(self, from_text, to_text):
                self._type(self.from_field, from_text)
                self._type(self.to_field, to_text)

        def get_from_location(self):
                return self._get_value(self.from_field)

        def get_to_location(self):
                return self._get_value(self.to_field)

        # Chamar Táxi

        def click_taxi_option(self):
                self._click(self.taxi_option)

        def click_comfort_icon(self):
                self._click(self.comfort_icon)

        def click_comfort_active(self):
                try:
                        active_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.comfort_active))
                        return "active" in active_button.get_attribute("class")
                except:
                        return False

        # Telefone
        # OBS: o campo não aceita o número formatado com espaços (ex.:
        # "+1 123 123 12 12") — a validação do app só passa sem espaços.
        # Por isso removemos os espaços antes de digitar.

        def set_phone_number(self, phone_number):
                self._click(self.phone_trigger)
                self._type(self.phone_input, phone_number.replace(' ', ''))
                self._click(self.phone_next_button)
                # espera o modal do código aparecer antes de seguir
                self._find(self.phone_code_input)

        def set_phone_code(self, code):
                self._type(self.phone_code_input, code)
                self._click(self.phone_confirm_button)

        def get_phone_number(self):
                # depois de confirmado, o número é exibido no gatilho lateral
                return self._get_text(self.phone_trigger)

        # Cartão

        def set_card(self, card_number, card_code):
                self._click(self.payment_trigger)
                self._click(self.add_card_option)
                self._type(self.card_number_input, card_number)
                code_field = self._find(self.card_code_input)
                code_field.send_keys(card_code)
                code_field.send_keys(Keys.TAB)
                self._click(self.add_card_button)
                self._click(self.payment_modal_close_button)

        def is_card_active(self):
                return self._get_text(self.payment_value) == 'Cartão'

        # Comentário para o motorista

        def set_driver_comment(self, message):
                self._type(self.driver_comment_input, message)

        def get_driver_comment(self):
                return self._get_value(self.driver_comment_input)

        # Requisitos do pedido

        def open_order_requirements(self):
                # os campos de requisitos já ficam visíveis assim que a tarifa
                # é selecionada, então não é preciso expandir nada — o método
                # existe só para deixar o passo explícito no teste.
                self._find(self.blanket_container)

        def is_blanket_and_handkerchiefs_selected(self):
                container = self._find(self.blanket_container)
                checkbox = container.find_element(By.XPATH, './/input[contains(@class,"switch-input")]')
                return checkbox.is_selected()

        def toggle_blanket_and_handkerchiefs(self):
                container = self._find(self.blanket_container)
                slider = container.find_element(By.XPATH, './/span[contains(@class,"slider")]')
                slider.click()

        def click_ice_cream_plus(self):
                row = self._find(self.ice_cream_row)
                row.find_element(By.XPATH, './/div[contains(@class,"counter-plus")]').click()

        def get_ice_cream_count(self):
                row = self._find(self.ice_cream_row)
                value = row.find_element(By.XPATH, './/div[contains(@class,"counter-value")]').text
                return int(value)

        # Pedir / busca do carro

        def click_order_button(self):
                self._click(self.order_button)

        def is_car_search_visible(self):
                # OBS: depende de POST /api/v1/order responder com sucesso no
                # backend do container. Se o container estiver instável (500
                # Internal Server Error nesse endpoint, já visto em outras
                # sessões), este método sempre vai dar timeout — não é bug
                # do teste.
                try:
                        self._find(self.car_search_indicator)
                        return True
                except Exception:
                        return False
