Private Sub CommandButton1_Click()
' THINCARB VBA Macro'

' (C) Colin Neal, CEH Wallingford'
'     Translated from Lotus 1-2-3 to Excel Visual Basic by Steve King, STFC RAL'

' This macro uses the Goal Seek algorithm which uses a fixed default for the'
' tolerance of the solution. If you require an adjustable tolerance, rewrite'
' this macro to use the Solver.'

Static already_called As Boolean

Dim Sheet1 As Excel.Worksheet
    Set Sheet1 = ActiveSheet
    Dim i As Integer
    Dim startrow As Integer, lastrow As Integer
    Dim targetval As Double, setval As Double, changeval As Double
    
' Disable attempts to run the macro again when it is already running'
    If Not already_called Then
        already_called = True

' Pick up the target value to set and range of data rows'
        targetval = Sheet1.Cells(4, "E")
        startrow = Sheet1.Cells(5, "E")
        lastrow = Sheet1.Cells(6, "E")
    
' Loop over lines of values'
        For i = startrow To lastrow
            setval = Sheet1.Cells(i, "M")
            changeval = Sheet1.Cells(i, "K")
' Make {EpCO2 less rough inc CO3} a rough guess for a start value for {EpCO2 Accurate}'
            Sheet1.Cells(i, "K").Value = Sheet1.Cells(i, "J").Value
        
' Now call the solver'
            Sheet1.Cells(i, "M").GoalSeek Goal:=targetval, ChangingCell:=Sheet1.Cells(i, "K")
       
        Next i

        already_called = False

    End If
    Message

End Sub

Sub Message()
     
     MsgBox "Finished!"

End Sub
