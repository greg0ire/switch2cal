import switch2Cal
import unittest
from datetime import datetime

class TestSwitch2CalFunctions(unittest.TestCase):
    def testCleanPeriod(self):
        period = {
            'name': 'testProject',
            'start_date': datetime(
                year   = 2000,
                month  = 1,
                day    = 1,
                hour   = 10,
                minute = 00,
                second = 00
            ),
            'end_date': datetime(
                year   = 2000,
                month  = 1,
                day    = 1,
                hour   = 11,
                minute = 10,
                second = 30
            )
        }
        cleanedEvents = switch2Cal.cleanPeriod(period)
        self.assertEquals(len(cleanedEvents), 1)

        cleanedPeriod = cleanedEvents.pop()
        self.assertEquals(cleanedPeriod['start_date'], period['start_date'])
        self.assertEquals(cleanedPeriod['end_date'], period['end_date'])



if __name__ == '__main__':
    unittest.main()
