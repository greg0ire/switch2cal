import switch2Cal
import unittest
from datetime import datetime

class TestSwitch2CalFunctions(unittest.TestCase):
    def testCleanAlreadyCleanPeriod(self):
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
        # assert there was no splitting
        self.assertEquals(len(cleanedEvents), 1)

        cleanedPeriod = cleanedEvents.pop()
        # assert this function is idempotent (the event is already clean)
        self.assertEquals(cleanedPeriod['start_date'], period['start_date'])
        self.assertEquals(cleanedPeriod['end_date'], period['end_date'])

    def testRoundEarlyStartDate(self):
        period = {
            'name': 'testProject',
            'start_date': datetime(
                year   = 2000,
                month  = 1,
                day    = 1,
                hour   = 8,
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
        # assert there was no splitting
        self.assertEquals(len(cleanedEvents), 1)

        cleanedPeriod = cleanedEvents.pop()
        self.assertEquals(
            cleanedPeriod['start_date'],
            datetime(
                year   = 2000,
                month  = 1,
                day    = 1,
                hour   = 9,
                minute = 30,
                second = 00
            ))
        self.assertEquals(cleanedPeriod['end_date'], period['end_date'])

    def testRoundLateEndDate(self):
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
                hour   = 20,
                minute = 10,
                second = 30
            )
        }
        cleanedEvents = switch2Cal.cleanPeriod(period)
        # assert there was no splitting
        self.assertEquals(len(cleanedEvents), 1)

        cleanedPeriod = cleanedEvents.pop()
        self.assertEquals(cleanedPeriod['start_date'], period['start_date'])
        self.assertEquals(
            cleanedPeriod['end_date'],
            datetime(
                year   = 2000,
                month  = 1,
                day    = 1,
                hour   = 19,
                minute = 00,
                second = 00
            ))

    def testsplit(self):
        period = {
            'name': 'testproject',
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
                day    = 3,
                hour   = 20,
                minute = 10,
                second = 30
            )
        }
        cleanedEvents = switch2Cal.cleanPeriod(period)
        # assert there was no splitting
        self.assertEquals(len(cleanedEvents), 2)

        firstPeriod = cleanedEvents.popleft()
        self.assertEquals(
            firstPeriod,
            {
                'name': 'testproject',
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
                    hour   = 19,
                    minute = 00,
                    second = 00
                )
            }
        )
        secondPeriod = cleanedEvents.pop()
        self.assertEquals(
            secondPeriod,
            {
                'name': 'testproject',
                'start_date': datetime(
                    year   = 2000,
                    month  = 1,
                    day    = 3,
                    hour   = 9,
                    minute = 30,
                    second = 00
                ),
                'end_date': datetime(
                    year   = 2000,
                    month  = 1,
                    day    = 3,
                    hour   = 20,
                    minute = 10,
                    second = 30
                )
            })

if __name__ == '__main__':
    unittest.main()
