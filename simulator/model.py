import time


class ButtonSimulator:
    def __init__(self):
        self.buttons = {}
        self.long_press_threshold = 1.0
        self.double_click_window = 0.5

    def _init_button(self, button):
        self.buttons[button] = {
            "state": "IDLE",
            "press_time": None,
            "last_release_time": None,
        }

    def handle_event(self, button, action):
        now = time.time()

        if button not in self.buttons:
            self._init_button(button)

        btn = self.buttons[button]

        # ------------------------
        # PRESS
        # ------------------------
        if action == "press":
            btn["state"] = "PRESSED"
            btn["press_time"] = now

            return {
                "button": button,
                "event": "PRESS"
            }

        # ------------------------
        # RELEASE
        # ------------------------
        elif action == "release":
            if btn["state"] != "PRESSED":
                return {"error": "invalid state"}

            duration = now - btn["press_time"]

            btn["state"] = "IDLE"
            btn["press_time"] = None

            # LONG CLICK
            if duration >= self.long_press_threshold:
                btn["last_release_time"] = None
                return {
                    "button": button,
                    "event": "LONG_CLICK",
                    "duration": round(duration, 2),
                }
import time
import logging

# настройка логирования
logging.basicConfig(level=logging.INFO)


class ButtonSimulator:
    def __init__(self):
        self.buttons = {}
        self.long_press_threshold = 1.0
        self.double_click_window = 0.5

    def _init_button(self, button):
        self.buttons[button] = {
            "state": "IDLE",
            "press_time": None,
            "last_release_time": None,
        }

    def handle_event(self, button, action):
        now = time.time()

        if button not in self.buttons:
            self._init_button(button)

        btn = self.buttons[button]

        logging.info(f"Button {button} action: {action}")

        # ------------------------
        # PRESS
        # ------------------------
        if action == "press":
            btn["state"] = "PRESSED"
            btn["press_time"] = now

            result = {
                "button": button,
                "event": "PRESS"
            }

            logging.info(f"Result: {result}")
            return result

        # ------------------------
        # RELEASE
        # ------------------------
        elif action == "release":
            if btn["state"] != "PRESSED":
                result = {"error": "invalid state"}
                logging.info(f"Result: {result}")
                return result

            duration = now - btn["press_time"]

            btn["state"] = "IDLE"
            btn["press_time"] = None

            # LONG CLICK
            if duration >= self.long_press_threshold:
                btn["last_release_time"] = None

                result = {
                    "button": button,
                    "event": "LONG_CLICK",
                    "duration": round(duration, 2),
                }

                logging.info(f"Result: {result}")
                return result

            # DOUBLE CLICK
            if (
                btn["last_release_time"] is not None
                and (now - btn["last_release_time"] <= self.double_click_window)
            ):
                btn["last_release_time"] = None

                result = {
                    "button": button,
                    "event": "DOUBLE_CLICK"
                }

                logging.info(f"Result: {result}")
                return result

            # SHORT CLICK
            btn["last_release_time"] = now

            result = {
                "button": button,
                "event": "SHORT_CLICK",
                "duration": round(duration, 2),
            }

            logging.info(f"Result: {result}")
            return result

        # ------------------------
        result = {"error": "unknown action"}
        logging.info(f"Result: {result}")
        return result
            
               