from model_loader import Model_Loader
import time

llm = Model_Loader()

# avg time:  186 sec
pp="""
IDENTIFICATION DIVISION.
PROGRAM-ID. HELLO-WORLD.
DATA DIVISION.
WORKING-STORAGE SECTION.
    01 WS-LIMIT     PIC 9(2).
    01 WS-NUMA      PIC 9(3).
    01 WS-NUMB      PIC 9(3).
    01 WS-NUMC      PIC 9(3).
PROCEDURE DIVISION.
ACCEPT WS-LIMIT
MOVE 1 TO WS-NUMA
MOVE 1 TO WS-NUMB
MOVE 1 TO WS-NUMC
DISPLAY WS-NUMA
DISPLAY WS-NUMB
PERFORM UNTIL WS-LIMIT<1

    COMPUTE WS-NUMC=WS-NUMA + WS-NUMB
    END-COMPUTE
    MOVE WS-NUMB TO WS-NUMA
    MOVE WS-NUMC TO WS-NUMB
    DISPLAY WS-NUMC
    COMPUTE WS-LIMIT= WS-LIMIT - 1 
    END-COMPUTE
    
END-PERFORM
STOP RUN.
"""
# avg time: 37sec 32ram 8cr
qq = """
IDENTIFICATION DIVISION.
PROGRAM-ID. IDSAMPLE.
ENVIRONMENT DIVISION.
PROCEDURE DIVISION.
    DISPLAY 'HELLO WORLD'.
    STOP RUN.
"""
s1 = time.time()
data = llm.convert_code(lang_from="cobol", lang_to="python",text=pp)
print("Time:", time.time()-s1)
print(data)

data.save_code(file_ext=".py")