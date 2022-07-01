import sys

class Housing_Exception(Exception):

    def __init__(self,error_message:Exception,error_details:sys):
        super().__init__(error_message)
        self.error_message= Housing_Exception.get_detail_error_message(error_message=error_message,
                                                                       error_details=error_details)
    
    @staticmethod
    def get_detail_error_message(error_message:Exception,error_details:sys)->str:
        _,_ ,exec_tb= error_details.exc_info()
        file_name=exec_tb.tb_frame.f_code.co_filename
        exception_block_line_no=exec_tb.tb_frame.f_lineno
        try_block_no=exec_tb.tb_lineno

        error_message = f"""Error occured in script:
                        [ {file_name} ] at
                        try block number is {[try_block_no]} and
                        exception block number is {[exception_block_line_no]} and 
                        error message is {[error_message]}"""
        return error_message
    
    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return Housing_Exception.__name__.str()
        