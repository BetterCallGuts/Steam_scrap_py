from tools import screab


outputs_type = ["csv", 'database', "both"]
outputs = input("Output file should be save in('csv', 'database', 'both'):")

if outputs in outputs_type:
  screab(outputs)
else:
  print("Plz choose one filetype, and type it as it is. ")


