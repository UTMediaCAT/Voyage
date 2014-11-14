__author__ = 'ryan'

import os,sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import unittest
import executer as ex
EXP="article"

class ExecuterTest (unittest.TestCase):
    def test_run(self):
        ex.comm_write(EXP,"RR")
        self.assertEqual(format('Run: %s - Already Running' % ex.name_format(EXP)),ex.run(EXP))
        ex.comm_write(EXP,"WR")
        self.assertEqual(format('%s - Last Command Not Processed Yet'% ex.name_format(EXP)),ex.run(EXP))
        ex.comm_write(EXP,"PR")
        self.assertEqual(format('Run: %s - Resuming' % ex.name_format(EXP)),ex.run(EXP))
        ex.comm_write(EXP,"SR")
        self.assertEqual(format('Run: %s - Started Running' % ex.name_format(EXP)),ex.run(EXP))

    def test_pause(self):
        ex.comm_write(EXP,"RP")
        self.assertEqual(format('Pause: %s - Pausing' % ex.name_format(EXP)),ex.pause(EXP))
        ex.comm_write(EXP,"WR")
        self.assertEqual(format('%s - Last Command Not Processed Yet'% ex.name_format(EXP)),ex.pause(EXP))
        ex.comm_write(EXP,"PP")
        self.assertEqual(format('Pause: %s - Already in Pause' % ex.name_format(EXP)),ex.pause(EXP))
        ex.comm_write(EXP,"SR")
        self.assertEqual(format('Pause: %s - Cannot pause non-Started Instance' % ex.name_format(EXP)),ex.pause(EXP))

    def test_stop(self):
        ex.comm_write(EXP,"RR")
        self.assertEqual(format('Stop: %s - Stopping' % ex.name_format(EXP)),ex.stop(EXP))
        ex.comm_write(EXP,"WR")
        self.assertEqual(format('%s - Last Command Not Processed Yet'% ex.name_format(EXP)),ex.stop(EXP))
        ex.comm_write(EXP,"PR")
        self.assertEqual(format('Stop: %s - Stopping Paused Explorer' % ex.name_format(EXP)),ex.stop(EXP))
        ex.comm_write(EXP,"SR")
        self.assertEqual(format('Stop: %s - Cannot Stop non-Started Explorer' % ex.name_format(EXP)),ex.stop(EXP))

