if __name__ == '__main__':
    import sys
    sys.path.insert(0, "Testing")
    sys.path.insert(0, ".")
    sys.path.insert(0, "..")

import json, os
from Engine.Settings import Settings as SETT
from Simulations import Simulation1

SETT.VISUAL_ON = False # ??????

class TestBoxLeak:
    def __init__(self):
        file = open('Testing/lastSaved.json', 'r')
        try:
            dataLoaded = json.load( file )
            lastSaved = dataLoaded['lastSaved_fileName']
            time = dataLoaded['time']
            state_name = dataLoaded['state_name']
        except BaseException:
            lastSaved = 'InitialStates/initState-electricTest1.json'
            time = 0.0
            state_name = 'electricTest1'
            print("Json file is probably empty.")
        if not os.path.exists(lastSaved):
            print(f"{lastSaved} is a name of a file that doesn't exist.")
            print("Running default initial state.")
            lastSaved = 'InitialStates/initState-electricTest1.json'
            time = 0.0
            state_name = 'electricTest1'

        state_fileName = lastSaved.split('/')[-1]
        path_name = lastSaved.replace(f'/{state_fileName}', '')

        self.simulations = [
            Simulation1(
                state_fileName=state_fileName,
                path_name=path_name,
                state_name=state_name,
                init_time=time
            )
            ]

    def runFromLastSave(self):
        self.simulations[0].run()

        time = self.simulations[0].time
        state_name = self.simulations[0].state_name
        lastSaved_fileName = self.simulations[0].lastSaved_fileName
        saved_data = {
            "time": time,
            "state_name": state_name,
            "lastSaved_fileName": lastSaved_fileName
        }

        if lastSaved_fileName is not None:
            json.dump(saved_data, open('Testing/lastSaved.json', 'w'), indent=4)
        else:
            print('lastSaved_fileName is None')

	
if __name__ == '__main__':
	test = TestBoxLeak()
	test.runFromLastSave()