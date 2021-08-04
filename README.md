# Stress_Strain_Curve
An small python code that derive some values and stress-strain curves out of tensile test excel records.

this simple code will extract Stress-strain curve and UTS, Module, yield point and fracture point from Force-elongation data made from tensile test.

to use it, you have to have excel file with two columns Force(N) and elongation (mm) like my example file, or change the code to work for your own data.

results are look like this:

this is force-elongation curve, points are made for elastic region so those points should be seperated and located on linear elastic region, if it is'nt, it wont work correctly.
![alt text](https://github.com/MrHbogart/Stress_Strain_Curve/blob/main/example/Fe_Elastic.png)



at the bigenning of tensile test, there is an small error that makes the bigenning of the curve, unlinear, we have to correct it in the bigenning of work.
(this are automatically, dont worry)
![alt text](https://github.com/MrHbogart/Stress_Strain_Curve/blob/main/example/Fe_removed_error.png)

next curve is engeeniring Stress-Strain curve, and the point that automattically found, is fracture point.
if the point is not exactly on fracture point, only fracture result is wrong, not anythin else.

![alt text](https://github.com/MrHbogart/Stress_Strain_Curve/blob/main/example/Fe_eng_stress_strain.png)

the next curve is True Stress-Strain curve


![alt text](https://github.com/MrHbogart/Stress_Strain_Curve/blob/main/example/Fe_True_Stress_Strain.png)

and the next photo is previous photo with a line that use to find yield point.
so if the line is located incorrectly, yield point strss and strain in results are wrong


![alt text](https://github.com/MrHbogart/Stress_Strain_Curve/blob/main/example/Fe_Yield_point.png)

and at the end, on the console you will recive results:


![alt text](https://github.com/MrHbogart/Stress_Strain_Curve/blob/main/example/results.png)




Hope it helps you ENGEENIERS :))
