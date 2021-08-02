#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


# In[2]:


"""i work with Santam Machine and the results are in .xls format
    you can use other formats but remember to change the code,
    important things are measurements and units
    after loading your data, we should have two numpy array
    x for elongation and y for Force"""

file_name = 'Fe.xls'
data = pd.read_excel(file_name)


#measurments
thickness = 3e-3
width = 5.96e-3
gage_length_s = 25e-3

#preparing loaded pandas dataframe to extract x and y
force = data['Unnamed: 1'][24:].reset_index().drop(['index'], axis=1)
extension = data['Santam Machine Controller - Excel Report'][24:].reset_index().drop(['index'], axis=1)

data = pd.concat([force, extension], axis=1).convert_dtypes()
data.columns = ['force', 'extension']

x = data.values[:,1]
y = data.values[:,0]


# In[3]:


def find_linear_point(x, y, threshold=0.00001):
    """this function will find 3 points with the highest distance on a single line
        to find elastic region.
        return shape is (mid point),(point1),(point2),mid_point_index, distance of two other points from mid point"""
    max_range = 0
    max_index = 0
    is_break = False
    for i in range(1, len(x)//2):
        for j in range(1, i):
            if x[i+j] == x[i] or x[i-j]==x[i]:
                continue
            tangent1 = (y[i+j] - y[i]) / (x[i+j] - x[i])
            tangent2 = (y[i] - y[i-j]) / (x[i] - x[i-j])
            phi1 = math.atan(tangent1)
            phi2 = math.atan(tangent2)
            if abs(phi1 - phi2) < threshold:
                if j >= max_range:
                    max_range = j
                    max_index = i
            else:
                break
    return (x[max_index], y[max_index]),            (x[max_index-(max_range//2)], y[max_index-(max_range//2)]),            (x[max_index+(max_range//2)], y[max_index+(max_range//2)]),            max_index, max_range//2

#to check that find_linear_point works correctly
point, point2, point3, mid_id, mid_range= find_linear_point(data.values[:,1], data.values[:,0])
plt.plot(x, y)
plt.plot(point[0], point[1], "s")
plt.plot(point2[0], point2[1], "s")
plt.plot(point3[0], point3[1], "s")
plt.title('points that will use for detecting module and yield point')
plt.ylabel('Force (N)')
plt.xlabel('Elongation with error (mm)')
plt.grid(True)
plt.axis([0, None, 0, None])
plt.savefig('Fe_Elastic', dpi=200, transparent=False)

plt.show()


# In[4]:


def frac_point(x, y):
    """in this function we want to find the fracture point or the point that test is finished
        i used quick change of tangent at fracture point and linear line after that
        so i reversed data and used find linear points and after that finding a line
        parallel to straight line after frac. with a little bit space like finding 
        yield point; but in reversed data
        return is index of frac point in data"""
    reversed_x = x[::-1]
    reversed_y = y[::-1]
    
    point, point2, point3, mid_id, mid_range= find_linear_point(reversed_x, reversed_y)

    module = (reversed_y[mid_id + mid_range] - reversed_y[mid_id - mid_range])    /(reversed_x[mid_id + mid_range] - reversed_x[mid_id - mid_range])

    b = point[1] - module*(point[0]-0.001)

    for i in range(len(reversed_x)):
        x1 = reversed_x[i]
        x2 = reversed_x[i+1]
        y1 = reversed_y[i]
        y2 = reversed_y[i+1]
        if (y2-(module*x2 +b))*(y1-(module*x1+b)) < 0:
            frac_index = i+1
            break

    return len(x)-frac_index


# In[5]:


def unsteady(x, y):
    """there is a little non-linearity in bigenning that comes from error of machine
        we have to remove it from our data, so in this func. we find how much error we have and return it"""
    midpoint, point1, point2, max_id, mid_range = find_linear_point(x, y)
    tangent = (point2[1] - point1[1])/(point2[0] - point1[0])
    #y = ax + b
    b = midpoint[1] - tangent*midpoint[0]
    
    #at y = 0, x must be 0, so defference is unsteadity
    # dx = -b/a
    return -b/tangent

#moving all the data te remove unsteadity:
x = x-unsteady(x, y)

plt.plot(x, y)
plt.title('Force-Elongation curve for Fe sample')
plt.ylabel('Force (N)')
plt.xlabel('Elongation (mm)')
plt.grid(True)
plt.axis([0, None, 0, None])
plt.savefig('Fe_removed_error', dpi=200, transparent=False)
plt.show()


# In[6]:


#calculatin engeeniring strain and stress
eng_strain = (x*1e-3) / gage_length_s
eng_stress = (y / (thickness * width))*1e-6

frac_index = frac_point(x, y)
print(f'fracture stress : {eng_stress[frac_index]:.2f} MPa and strain: {eng_strain[frac_index]:4f}')

plt.plot(eng_strain, eng_stress)
plt.plot(eng_strain[frac_index], eng_stress[frac_index], "s")
plt.title('Engeeniring Stress-Strain curve for Fe sample')
plt.ylabel('eng-Stress (MPa)')
plt.xlabel('Strain')
plt.grid(True)
plt.axis([0, None, 0, None])
plt.savefig('Fe_eng_stress_strain', dpi=200, transparent=False)
plt.show()


# In[7]:


#calculating True stress and strain data
true_stress = []
true_strain = []

for i in eng_strain:
    true_strain.append(math.log(1+i))

for i in range(eng_stress.shape[0]):
    true_stress.append(eng_stress[i] * (1 + eng_strain[i]))

true_strain = true_strain[:np.argmax(true_stress)]
true_stress = true_stress[:np.argmax(true_stress)]
    
plt.plot(true_strain, true_stress)
plt.title('True Stress-Strain curve for Fe sample')
plt.ylabel('true-Stress (MPa)')
plt.xlabel('true-Strain')
plt.grid(True)
plt.axis([0, None, 0, None])

plt.savefig('Fe_True_Stress_Strain', dpi=200, transparent=False)
plt.show()


# In[8]:


#calculating Module
module = (true_stress[mid_id + mid_range] - true_stress[mid_id - mid_range])/(true_strain[mid_id + mid_range] - true_strain[mid_id - mid_range])

print(f'Module: {module:.2f} MPa')

#to find yield point
#y = ax + b, for parallel line we need : if y=0 ==> x=0.002, so module*0.002 = -b
b = -0.002*module
bys = []
bxs = []
for i in range(100):
    xs = (i/100)*0.015
    bxs.append(xs)
    bys.append(module*xs + b)

for i in range(len(true_stress)):
    x1 = true_strain[i]
    x2 = true_strain[i+1]
    y1 = true_stress[i]
    y2 = true_stress[i+1]
    if (y2-(module*x2 +b))*(y1-(module*x1+b)) < 0:
        yp_stress = y1
        yp_strain = x1
        break
        

#drawing data and yield point to check it works correctly
plt.plot(true_strain, true_stress)
plt.plot(bxs, bys)
plt.plot(yp_strain, yp_stress, "s")
plt.title('True Stress-Strain curve for Fe sample')
plt.ylabel('true-Stress (MPa)')
plt.xlabel('true-Strain')
plt.grid(True)
plt.axis([0, None, 0, None])
plt.savefig('Fe_Yield_point', dpi=200, transparent=False)
plt.show()


# In[9]:


#calculating maximum of stress in True stress-strain data
true_utstress = true_stress[-1]
true_utstrain = true_strain[-1]

# print(utstress, utstrain)


# In[10]:


#calculating maximum of stress and strain in engeeniring data to report as UTS
eng_stress_maxarg = np.argmax(eng_stress)
eng_utstress = eng_stress[eng_stress_maxarg]
eng_utstrain = eng_strain[eng_stress_maxarg]

print(f'Ultimate tensile stress : {eng_utstress:.2f} MPa and strain: {eng_utstrain:.2f}')
