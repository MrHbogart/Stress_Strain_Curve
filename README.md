# Stress_Strain_Curve
An small python code that derive some values and stress-strain curves out of tensile test excel records.

this simple code will extract Stress-strain curve and UTS, Module, yield point and fracture point from Force-elongation data made from tensile test.

to use it, you have to have excel file with two columns Force(N) and elongation (mm) like my example file, or change the code to work for your own data.

results are look like this:

this is force-elongation curve, points are made for elastic region so those points should be seperated and located on linear elastic region, if it is'nt, it wont work correctly.
![alt text](https://github.com/MrHbogart/Stress_Strain_Curve/blob/main/example/Fe_Elastic.png)
