import pyfiglet
from pyfiglet import Figlet


class StartUp:
    '''
    On Start up this will display an options page of the CLI tool  
    with a nice ASCII terminal banner

    '''

    def __init__(self):
        self.font = 'big'

    def on_start_up(self):
        custom_fig = Figlet(font=self.font)
        application_name = custom_fig.renderText("Tweeting Mill")
        iteration = "v.0.1.0 - A Twitter CLI Tool"
        introductions = [application_name + '\n' + iteration]
        for introduction in introductions:
            print(introduction)

    def options(self):
        first_option = "0 - Return to the options page."
        second_option = "1 - Search up a twitter user and user's recent post."
        third_option = "2 - Create a data log to form a word cloud of recent tweets of a user."
        fourth_option = "3 - Exit program"
        option_lists = [first_option + "\n" + second_option +
                        "\n" + third_option + "\n" + fourth_option]
        for option in option_lists:
            print(option)
