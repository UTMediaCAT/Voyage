__author__ = 'ryan'

import os
import sys
sys.path.append("..")
import unittest
import executer as ex
EXP = "article"
COMM_FILE = "_comm.stream"


class TestExecuter (unittest.TestCase):

    def test_comm_read_write(self):
        ex.comm_write(EXP, "RR")
        comm = open(EXP + COMM_FILE, 'r')
        msg = comm.read()
        comm.close()
        self.assertEqual(msg, "RR", "write explorer stream fail")
        comm = open(EXP + COMM_FILE, 'w')
        comm.write("WS")
        comm.close()
        self.assertEqual(ex.comm_read(EXP), "WS", "read explorer stream fail")

    def test_get_status(self):
        ex.comm_write(EXP, "WS")
        self.assertEqual(ex.get_status(EXP), "W", "get status should get the first of the stream file")

    def test_explorer_format(self):
        self.assertEqual(ex.explorer_format("ArTiClE"), "article", "'article' should be all lower case")
        self.assertEqual(ex.explorer_format("article"), "article", "'article' should be all lower case")
        self.assertEqual(ex.explorer_format("TwItTeR"), "twitter", "'twitter' should be all lower case")
        self.assertEqual(ex.explorer_format("twitter"), "twitter", "'twitter' should be all lower case")
        self.assertEqual(ex.explorer_format("asdas"), None, "other than 'article' and 'twitter' should return none")
        self.assertEqual(ex.explorer_format("articles"), None, "other than 'article' and 'twitter' should return none")
        self.assertEqual(ex.explorer_format("twitters"), None, "other than 'article' and 'twitter' should return none")

    def test_command_format(self):
        self.assertEqual(ex.command_format("StAtuS"), "status", "'status' should be all lower case")
        self.assertEqual(ex.command_format("status"), "status", "'status' should be all lower case")
        self.assertEqual(ex.command_format("RuN"), "run", "'run' should be all lower case")
        self.assertEqual(ex.command_format("run"), "run", "'run' should be all lower case")
        self.assertEqual(ex.command_format("PaUsE"), "pause", "'pause' should be all lower case")
        self.assertEqual(ex.command_format("pause"), "pause", "'pause' should be all lower case")
        self.assertEqual(ex.command_format("StOp"), "stop", "'stop' should be all lower case")
        self.assertEqual(ex.command_format("stop"), "stop", "'stop' should be all lower case")
        self.assertEqual(ex.explorer_format("asdas"), None,
                         "other than 'status','run','pause','stop' should return none")
        self.assertEqual(ex.explorer_format("StoPs"), None,
                         "other than 'status','run','pause','stop' should return none")

    def test_status_format(self):
        self.assertEqual(ex.status_format("R"), "Running", "'R' should be return 'Running'")
        self.assertEqual(ex.status_format("P"), "Paused", "'P' should be return 'Paused'")
        self.assertEqual(ex.status_format("S"), "Stopped", "'S' should be return 'Stopped'")
        self.assertEqual(ex.status_format("W"), "Waiting", "'W' should be return 'Waiting'")
        self.assertEqual(ex.status_format("w"), None, "case of status is sensitive")
        self.assertEqual(ex.status_format("G"), None, "other than 'W', 'S', 'P', 'R' should return none")

    def test_input_format(self):
        self.assertEqual(ex.input_format("Twitter", "Run"), ("twitter", "run"), "it should return tupple")
        self.assertEqual(ex.input_format("Article", "Stop"), ("article", "stop"), "it should return tupple")

    def test_name_format(self):
        self.assertEqual(ex.name_format("asgg"), "Asgg Explorer", "format fail")

    def test_run(self):
        ex.comm_write(EXP, "RR 22321")
        self.assertEqual(format('Run: %s - Already Running' % ex.name_format(EXP)), ex.run(EXP),
                         "use run function in run should show msg and no other change")
        ex.comm_write(EXP, "WR 23412")
        self.assertEqual(format('%s - Last Command Not Processed Yet' % ex.name_format(EXP)), ex.run(EXP),
                         "use run function in wait should show msg and no other change")
        ex.comm_write(EXP, "PR 32412")
        self.assertEqual(format('Run: %s - Resuming' % ex.name_format(EXP)), ex.run(EXP),
                         "use run function in pause should show msg and change status to wait")
        self.assertEqual(ex.get_status(EXP), "W", "status chould change to wait when is paused")
        ex.comm_write(EXP, "SR 12345")
        self.assertEqual(format('Run: %s - Started Running' % ex.name_format(EXP)), ex.run(EXP),
                         "use run function in stop should show msg and no other change")

    def test_pause(self):
        ex.comm_write(EXP, "RP 12323")
        self.assertEqual(format('Pause: %s - Pausing' % ex.name_format(EXP)), ex.pause(EXP),
                         "use pause function in run should show msg and change status to wait")
        self.assertEqual(ex.get_status(EXP), "W", "status should change to wait when on run")
        ex.comm_write(EXP, "WR 23332")
        self.assertEqual(format('%s - Last Command Not Processed Yet' % ex.name_format(EXP)), ex.pause(EXP),
                         "use pause function in wait should show msg and no other change")
        ex.comm_write(EXP, "PP 12342")
        self.assertEqual(format('Pause: %s - Already in Pause' % ex.name_format(EXP)), ex.pause(EXP),
                         "use pause function in pause should show msg and no other change")
        ex.comm_write(EXP, "SR 23122")
        self.assertEqual(format('Pause: %s - Cannot pause non-Started Instance' % ex.name_format(EXP)), ex.pause(EXP),
                         "use pause function in wait should show msg and no other change")

    def test_stop(self):
        ex.comm_write(EXP, "RR 12332")
        self.assertEqual(format('Stop: %s - Stopping' % ex.name_format(EXP)), ex.stop(EXP),
                         "use stop function in wait should show msg and change status")
        self.assertEqual(ex.get_status(EXP), "W", "when stop in run should change status to wait")
        ex.comm_write(EXP, "WR 23123")
        self.assertEqual(format('%s - Last Command Not Processed Yet' % ex.name_format(EXP)), ex.stop(EXP),
                         "use stop function in wait should show msg and no other change")
        ex.comm_write(EXP, "PR 33241")
        self.assertEqual(format('Stop: %s - Stopping Paused Explorer' % ex.name_format(EXP)), ex.stop(EXP),
                         "use stop function in pause should show msg and change status")
        self.assertEqual(ex.get_status(EXP), "W", "when stop in pause should change status to wait")
        ex.comm_write(EXP, "SR 23123")
        self.assertEqual(format('Stop: %s - Cannot Stop non-Started Explorer' % ex.name_format(EXP)), ex.stop(EXP),
                         "use stop function in stop should show msg and no other change")
        
if __name__ == "__main__":
    unittest.main()