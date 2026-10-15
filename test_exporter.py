import unittest
import asyncio
import os
import json
from exporter import AsyncLogProcessor

class TestAsyncLogProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = AsyncLogProcessor()
        self.test_json = "test_out.json"

    def tearDown(self):
        if os.path.exists(self.test_json):
            os.remove(self.test_json)

    def test_ingestion_and_filtering(self):
        asyncio.run(self.processor.ingest_log("ERROR", "Test error message", "test-service"))
        asyncio.run(self.processor.ingest_log("INFO", "Test info message", "test-service"))
        
        errors = self.processor.filter_by_level("ERROR")
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, "Test error message")

    def test_json_export(self):
        asyncio.run(self.processor.ingest_log("INFO", "Export test", "system"))
        asyncio.run(self.processor.export_to_json(self.test_json))
        
        self.assertTrue(os.path.exists(self.test_json))
        with open(self.test_json, "r") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["message"], "Export test")

if __name__ == "__main__":
    unittest.main()
