import unittest

class CustomTestResult(unittest.TextTestResult):  
    def __init__(self, stream, descriptions, verbosity):  
        super().__init__(stream, descriptions, verbosity)  
        self.successes = []  

    def addSuccess(self, test):  
        super().addSuccess(test)  
        self.successes.append(test) 
       
class CustomTestRunner(unittest.TextTestRunner):  
    def _makeResult(self):  
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)  
    
    def run(self, test):  
        result = super().run(test)  

        failures = []  
        errors = []  
        successes = []  

        for test_case, reason in result.failures:  
            failures.append(test_case)  
        
        for test_case, reason in result.errors:  
            errors.append(test_case)  

        successes = result.successes  
        success_count = len(successes)  

        print(f'SUCCESS: {success_count} - TEST CASES:')
        print("\n".join(str(tc) for tc in successes))
        print(f'FAILURES: {len(result.failures)} - TEST CASES:')  
        print("\n".join(str(tc) for tc in failures))
        print(f'ERRORS: {len(result.errors)} - TEST CASES:')  
        print("\n".join(str(tc) for tc in errors))

        for error in errors:
            failures.append(error)
        
        res = {
            'succ': successes,
            'fail': failures
        }
        
        return res 